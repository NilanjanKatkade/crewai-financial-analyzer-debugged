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
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv
load_dotenv()

# from crewai_tools import SerperDevTool
from langchain_community.document_loaders import PyPDFLoader

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

        loader = PyPDFLoader(path)
        docs = loader.load()

        full_report = ""

        # ----------- Read the PDF -----------
        for doc in docs:
            page_text = doc.page_content

            page_text = page_text.replace("\r", " ")
            page_text = page_text.replace("\t", " ")

            while "\n\n" in page_text:
                page_text = page_text.replace("\n\n", "\n")

            while "  " in page_text:
                page_text = page_text.replace("  ", " ")

            full_report += page_text.strip() + "\n"


        # ----------- IMPORTANT: Chunking (Fixes token overflow) -----------

        from langchain.text_splitter import RecursiveCharacterTextSplitter

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200
        )

        chunks = splitter.split_text(full_report)
        # only most important financial pages
        selected_chunks = []

        keywords = [
            "revenue",
            "net income",
            "cash flow",
            "balance sheet",
            "total assets",
            "total liabilities",
            "operating income",
            "risk factors",
            "liquidity",
            "guidance"
        ]

        for chunk in chunks:
            if any(k.lower() in chunk.lower() for k in keywords):
                selected_chunks.append(chunk)

        # HARD LIMIT (VERY IMPORTANT)
        selected_chunks = selected_chunks[:5]

        compressed_report = "\n\n".join(selected_chunks)

        return compressed_report

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