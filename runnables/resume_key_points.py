from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_messages(
    [
        HumanMessagePromptTemplate.from_template(
            """Your task is to review candidate resumes and extract key data points.
You are to find the First Name, Surname, Email Address, Current Company Name and Current Position in that order. 
The response should be in CSV format without headers.
Please note that First Name and Surname are to be distinct columns.
Here is the resume to extract from: 

{resume_text}"""
        )
    ]
)

llm = ChatOpenAI(
    model="gpt-4o", temperature=0, max_tokens=1024, timeout=60 * 2, max_retries=2
)

resume_key_points_runnable = prompt | llm
