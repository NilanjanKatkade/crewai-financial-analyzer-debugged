# ## Importing libraries and files
# import os
# from dotenv import load_dotenv
# load_dotenv()

# from crewai_tools import tools
# from crewai_tools.tools.serper_dev_tool import SerperDevTool

# ## Creating search tool
# search_tool = SerperDevTool()

# ## Creating custom pdf reader tool
# class FinancialDocumentTool():
#     async def read_data_tool(path='data/sample.pdf'):
#         """Tool to read data from a pdf file from a path

#         Args:
#             path (str, optional): Path of the pdf file. Defaults to 'data/sample.pdf'.

#         Returns:
#             str: Full Financial Document file
#         """
        
#         docs = Pdf(file_path=path).load()

#         full_report = ""
#         for data in docs:
#             # Clean and format the financial document data
#             content = data.page_content
            
#             # Remove extra whitespaces and format properly
#             while "\n\n" in content:
#                 content = content.replace("\n\n", "\n")
                
#             full_report += content + "\n"
            
#         return full_report

# ## Creating Investment Analysis Tool
# class InvestmentTool:
#     async def analyze_investment_tool(financial_document_data):
#         # Process and analyze the financial document data
#         processed_data = financial_document_data
        
#         # Clean up the data format
#         i = 0
#         while i < len(processed_data):
#             if processed_data[i:i+2] == "  ":  # Remove double spaces
#                 processed_data = processed_data[:i] + processed_data[i+1:]
#             else:
#                 i += 1
                
#         # TODO: Implement investment analysis logic here
#         return "Investment analysis functionality to be implemented"

# ## Creating Risk Assessment Tool
# class RiskTool:
#     async def create_risk_assessment_tool(financial_document_data):        
#         # TODO: Implement risk assessment logic here
#         return "Risk assessment functionality to be implemented"



from crewai.tools import BaseTool
from pydantic import BaseModel, Field
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
from pypdf import PdfReader
load_dotenv()

# from crewai_tools import SerperDevTool
# from langchain_community.document_loaders import PyPDFLoader

#SEARCH TOOL
# search_tool = SerperDevTool()


from typing import Type
# from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class FinancialDocumentInput(BaseModel):
    path: str = Field(..., description="Path to the financial PDF document")


class FinancialDocumentTool(BaseTool):
    name: str = "financial_document_reader"
    description: str = (
        "Reads a financial PDF document and returns the extracted text content."
    )
    args_schema: Type[BaseModel] = FinancialDocumentInput



    def _run(self, path: str) -> str:

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found at path: {path}")

        if not path.lower().endswith(".pdf"):
            raise ValueError("Only PDF files are supported")

        reader = PdfReader(path)

        full_report = ""

        for page in reader.pages:
            text = page.extract_text()
            if text:
                text = text.replace("\r", " ")
                text = text.replace("\t", " ")
                text = " ".join(text.split())
                full_report += text + "\n"

        # Safety guard for LLM context
        MAX_CHARS = 6000
        return full_report[:MAX_CHARS]
#OPTIONAL: Investment Tool (Structured Stub)
class InvestmentTool:

    @staticmethod
    def analyze_investment_tool(financial_document_data: str) -> str:
        """
        Placeholder investment analysis tool.
        Can be expanded later with quantitative logic.
        """
        if not financial_document_data:
            return "No financial data provided."

        return "Investment analysis module ready for extension."


#OPTIONAL: Risk Tool (Structured Stub)
class RiskTool:

    @staticmethod
    def create_risk_assessment_tool(financial_document_data: str) -> str:
        """
        Placeholder risk assessment tool.
        """
        if not financial_document_data:
            return "No financial data provided."

        return "Risk assessment module ready for extension."