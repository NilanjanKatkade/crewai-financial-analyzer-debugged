from crewai import Task
from agents import financial_analyst
#, verifier,risk_assessor , investment_advisor
from tools import FinancialDocumentTool

#1. DOCUMENT VERIFICATION
# verification = Task(
#     description="""
# Read the uploaded file located at {file_path} using the provided tool.

# Determine whether the file is a genuine financial document.
# A financial document typically contains:
# - revenue
# - expenses
# - balance sheet items
# - income statement
# - financial disclosures
# - quarterly or annual reports

# If the document does NOT contain financial data, clearly state:
# "INVALID_DOCUMENT"

# Do NOT guess. Base your answer strictly on the document contents.
# """,
#     expected_output="""
# Return a short structured response:

# VALID_DOCUMENT or INVALID_DOCUMENT

# Also include 2-3 lines explaining why.
# """,
#     agent=verifier,
#     tools=[FinancialDocumentTool()],
#     async_execution=False,
# )

analyze_financial_document = Task(
    description="""
You must:

1) Use the financial_document_reader tool.
2) Pass {file_path} into the tool.
3) Read the returned document text.
4) Then generate the financial analysis.

If the document cannot be read, clearly say so.

Do not skip tool usage.
""",
    expected_output="""
Return EXACTLY in this format:

Executive Summary:
<text>

Financial Performance:
<text>

Risks:
<text>

Investment Recommendation:
<Buy / Hold / Avoid with justification>
""",
    agent=financial_analyst,
    tools=[FinancialDocumentTool()],
)

# #3. RISK ASSESSMENT
# risk_assessment = Task(
#     description="""
# Using the extracted financial information from the document, identify real financial risks.

# Examples of risks:
# - declining revenue
# - high debt
# - negative cash flow
# - operational losses
# - dependence on few customers
# - regulatory issues

# Base conclusions strictly on the document content.
# If insufficient data exists, say so clearly.
# """,
#     expected_output="""
# Return JSON:

# {
#   "risks_identified": [],
#   "risk_level": "Low | Medium | High",
#   "reasoning": ""
# }
# """,
#     agent=risk_assessor,
#     tools=[FinancialDocumentTool()] ,
#     async_execution=False,
# )

# #4. INVESTMENT RECOMMENDATION
# investment_analysis = Task(
#     description="""
# Based ONLY on:
# 1) financial analysis
# 2) risk assessment

# Provide an investment recommendation.

# You must NOT speculate.
# You must NOT recommend random stocks.
# If information is insufficient, say so.
# """,
#     expected_output="""
# Return JSON:

# {
#   "recommendation": "Buy | Hold | Avoid | Insufficient Data",
#   "justification": "",
#   "confidence_level": "Low | Medium | High"
# }
# """,
#     agent=investment_advisor,
#     async_execution=False,
# )