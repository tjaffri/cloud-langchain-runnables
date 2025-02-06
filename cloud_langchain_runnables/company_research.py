from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.tools import Tool
from langgraph.graph import StateGraph
from langchain.output_parsers import PydanticOutputParser
import requests

from cloud_langchain_runnables.common import LLM, SimpleGraphState

# Define the output schema
class CompanyOfficer(BaseModel):
    name: str = Field(description="Name of the company officer")
    title: str = Field(description="Title/position of the officer")

class CompanyInfo(BaseModel):
    officers: List[CompanyOfficer] = Field(description="List of key company officers")
    current_stock_price: float = Field(description="Current stock price of the company")
    year_founded: int = Field(description="Year the company was founded")
    headquartered_at: str = Field(description="Company headquarters location")

# Initialize tools
search = GoogleSerperAPIWrapper()

def get_stock_price(symbol: str) -> float:
    """Get the current stock price for a given symbol."""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=C1F4FXPLSY0IHWUK"
    response = requests.get(url)
    data = response.json()
    latest_time = next(iter(data["Time Series (5min)"]))
    return float(data["Time Series (5min)"][latest_time]["4. close"])

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
    company_info = parser.parse(result["output"])
    return {
        "output": company_info.dict()
    }

workflow = StateGraph(SimpleGraphState)
workflow.add_node("company_research", company_research_node)
workflow.set_entry_point("company_research")
workflow.set_finish_point("company_research")
company_research_graph = workflow.compile() 