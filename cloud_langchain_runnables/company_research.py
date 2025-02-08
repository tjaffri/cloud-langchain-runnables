from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langgraph.graph import StateGraph
from langchain.output_parsers import PydanticOutputParser
import requests
import os
import json

from cloud_langchain_runnables.common import LLM, SimpleGraphState

# Define the output schema
class CompanyOfficer(BaseModel):
    name: str = Field(description="Name of the company officer")
    title: str = Field(description="Title/position of the officer")

class CompanyInfo(BaseModel):
    officers: List[CompanyOfficer] = Field(description="List of key company officers")
    current_stock_price: Optional[float] = Field(description="Current stock price of the company if publicly traded", default=None)
    year_founded: int = Field(description="Year the company was founded")
    headquartered_at: str = Field(description="Company headquarters location")

# Initialize tools
search = GoogleSerperAPIWrapper()

def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol using Finnhub."""
    finnhub_token = os.getenv("FINNHUB_API_KEY")
    if not finnhub_token:
        raise ValueError("FINNHUB_API_KEY environment variable is not set")
        
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={finnhub_token}"
    response = requests.get(url)
    data = response.json()
    
    if "c" not in data:
        raise ValueError(f"Could not get stock price for {symbol}. Response: {data}")
        
    return float(data["c"])  # 'c' is current price in Finnhub API

# Create output parser
parser = PydanticOutputParser(pydantic_object=CompanyInfo)

# Create the agent prompt
prompt = ChatPromptTemplate.from_messages([
    HumanMessagePromptTemplate.from_template(
        """You are a company research agent. Your task is to gather comprehensive information about a company.
        
Research Steps:
1. Use the search tool to find general information about the company including:
   - Key officers (CEO, Founder, etc.)
   - Year founded
   - Headquarters location
2. Find the stock ticker symbol if the company is public
3. Get the current stock price using the provided function

Company to research: {company_name}

Important: Make multiple searches if needed to find all required information. Be thorough and accurate.

{format_instructions}

{agent_scratchpad}"""
    )
])

# Create tools list
tools = [
    Tool(
        name="web_search",
        description="Search the web for information about companies, including officers, founding date, and headquarters location.",
        func=GoogleSerperAPIWrapper().run
    ),
    Tool(
        name="get_stock_price",
        description="Get the current stock price for a company using its ticker symbol (e.g., AAPL for Apple)",
        func=get_stock_price
    )
]

# Create the agent
agent = create_openai_tools_agent(
    llm=LLM,
    tools=tools, 
    prompt=prompt.partial(format_instructions=parser.get_format_instructions())
)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Create runnable
company_research_runnable = agent_executor

# Create graph
def company_research_node(state: SimpleGraphState) -> SimpleGraphState:
    company_name = str(state.get("input"))
    result = company_research_runnable.invoke({"company_name": company_name})
    
    # Parse the output into our Pydantic model
    try:
        company_info = parser.parse(result["output"])
        
        # Additional validation for non-existent companies
        if not company_info.officers:  # If no officers found, likely not a real company
            raise ValueError(f"Could not find valid information for company: {company_name}")
            
        # Basic validation of the data
        if company_info.year_founded < 1800 or company_info.year_founded > 2024:
            raise ValueError(f"Invalid founding year for company: {company_name}")
            
        if not company_info.headquartered_at or company_info.headquartered_at.strip() == "":
            raise ValueError(f"No headquarters location found for company: {company_name}")
            
        return {
            "output": json.dumps(company_info.model_dump())
        }
    except Exception as e:
        raise Exception(f"Failed to process company {company_name}: {str(e)}")

workflow = StateGraph(SimpleGraphState)
workflow.add_node("company_research", company_research_node)
workflow.set_entry_point("company_research")
workflow.set_finish_point("company_research")
company_research_graph = workflow.compile() 