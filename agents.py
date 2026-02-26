##This is correct 
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
# from langchain_openai import ChatOpenAI
from tools import FinancialDocumentTool

# ---------- LLM ----------
# llm = ChatOpenAI(
#     model="gpt-4o-mini",
#     temperature=0.1  # lower = less hallucination
# )
# 
from crewai import LLM
import os

llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)

#DOCUMENT VERIFIER
# verifier = Agent(
#     role="Financial Document Verification Specialist",
#     goal=(
#         "Determine whether the uploaded file is a financial document such as an annual report, "
#         "quarterly report, balance sheet, income statement, or financial disclosure."
#     ),
#     backstory=(
#         "You are a compliance officer trained in reviewing corporate filings and financial reports. "
#         "You carefully read documents and only approve them if they contain genuine financial information."
#     ),
#     verbose=True,
#     memory=False,
#     tools=[FinancialDocumentTool()],
#     llm=llm,
#     allow_delegation=False
# )

#FINANCIAL ANALYST
financial_analyst = Agent(
    role="Corporate Financial Analyst",
    goal=(
        "Carefully analyze the provided financial document and base all conclusions strictly on the document content. Do not make assumptions not supported by the document."
    ),
    backstory=(
        "You are a CFA-certified financial analyst. You analyze company reports carefully and only rely on "
        "information present in the provided document. If data is missing, you clearly state it."
    ),
    verbose=False,
    memory=False,
    max_retry_limit=0,
    system_prompt="""
    You are a financial analyst.
    Base conclusions only on the document.
    Return structured financial report.
    """,
    tools=[FinancialDocumentTool()],
    llm=llm,
    allow_delegation=False
)

# #RISK ASSESSOR
# risk_assessor = Agent(
#     role="Financial Risk Assessment Expert",
#     goal=(
#         "Identify real financial risks mentioned or implied in the document such as debt load, declining revenue, "
#         "cash flow problems, or operational issues."
#     ),
#     backstory=(
#         "You specialize in corporate risk evaluation and base your conclusions only on factual financial evidence."
#     ),
#     verbose=True,
#     memory=False,
#     tools=[FinancialDocumentTool()],
#     llm=llm,
#     allow_delegation=False
# )

# #INVESTMENT ADVISOR
# investment_advisor = Agent(
#     role="Investment Recommendation Specialist",
#     goal=(
#         "Provide a conservative investment recommendation based ONLY on the analyst and risk assessment outputs."
#     ),
#     backstory=(
#         "You are a registered investment advisor. You never fabricate data and you never give speculative "
#         "recommendations. If the information is insufficient, you say so."
#     ),
#     verbose=True,
#     memory=False,
#     llm=llm,
#     allow_delegation=False
# )