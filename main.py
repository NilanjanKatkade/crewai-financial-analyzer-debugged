from fastapi import BackgroundTasks
from database import init_db, create_job, update_job, get_job
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import json

from crewai import Crew, Process
from agents import (
#    verifier,
    financial_analyst,
#    risk_assessor,
#    investment_advisor
)
from task import (
#    verification,
    analyze_financial_document,
#    risk_assessment,
#    investment_analysis
)

from crewai import LLM
import os

repair_llm = LLM(
    model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0,
    max_tokens=700
)

import time

def safe_llm_call(func, *args, **kwargs):
    """Retries LLM calls on rate limit"""
    for attempt in range(5):
        try:
            return func(*args, **kwargs)

        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = 6 + (attempt * 4)
                print(f"Rate limited. Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise e

    raise Exception("LLM failed after multiple retries")

def repair_structure(text: str):
    prompt = f"""
You will receive a financial analysis.

Reformat it into EXACTLY four labeled sections:

Executive Summary:
Financial Performance:
Risks:
Investment Recommendation:

Do not add new information.
Only reorganize and summarize the provided text.

Text:
{text}
"""

    response = repair_llm.call(prompt)
    return response


app = FastAPI(title="Financial Document Analyzer")
@app.on_event("startup")
def startup_event():
    init_db()
import time
from litellm import RateLimitError
def process_analysis(job_id: str, file_path: str, query: str):
    try:
        response = safe_llm_call(run_crew, query, file_path)

        # --------- EMPTY CHECK ----------
        if not response:
            update_job(job_id, "Analysis failed: empty LLM response")
            return

        raw_text = str(response)

        # --------- CLEAN OUTPUT ----------
        cleaned = clean_output(raw_text)

        # remove this annoying model line
        cleaned = cleaned.replace("I now know the final answer", "").strip()

        # --------- STRUCTURE VALIDATION ----------
        # if structure missing → repair
        if not ensure_sections(cleaned):
            repaired = safe_llm_call(repair_structure, cleaned)
            cleaned = clean_output(str(repaired))
        # final check
        if not ensure_sections(cleaned):
            update_job(job_id, "Analysis failed after repair")
            return
        # --------- SAVE CLEAN RESULT ----------
        update_job(job_id, cleaned)

    except Exception as e:
        update_job(job_id, f"Processing failed: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
def run_crew(query: str, file_path: str):
    for attempt in range(5):
        try:
            financial_crew = Crew(
                agents=[financial_analyst],
                tasks=[analyze_financial_document],
                process=Process.sequential,
                verbose=True
            )

            result = financial_crew.kickoff({
                "query": query,
                "file_path": file_path
            })

            print("RAW CREW RESULT:", result)

            return result

        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait = 5 * (attempt + 1)
                print(f"Rate limited. Waiting {wait}s...")
                time.sleep(wait)
            else:
                raise e



# -------------------- HEALTH CHECK --------------------
@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}
def clean_output(text: str):
    bad_tokens = [
        "Thought:",
        "Action:",
        "Observation:",
        "Final Answer:",
        "I now know the final answer",
        "<analysis>",
        "</analysis>",
        "<thinking>",
    ]

    for token in bad_tokens:
        if token in text:
            text = text.replace(token, "")

    return text.strip()

def ensure_sections(text: str):
    text_lower = text.lower()

    checks = {
        "summary": ["executive summary", "summary"],
        "performance": ["financial performance", "financial analysis", "performance"],
        "risks": ["risks", "risk factors"],
        "recommendation": ["investment recommendation", "recommendation", "final recommendation"]
    }

    for category in checks:
        if not any(keyword in text_lower for keyword in checks[category]):
            return False

    return True


@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document"),
    background_tasks: BackgroundTasks = None
):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "Only PDF files allowed")

    file_id = str(uuid.uuid4())
    file_path = f"data/{file_id}.pdf"

    os.makedirs("data", exist_ok=True)

    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    # Create DB Job
    job_id = str(uuid.uuid4())
    create_job(job_id, file.filename)

    # Send to background worker
    background_tasks.add_task(process_analysis, job_id, file_path, query)

    return {
        "status": "processing",
        "job_id": job_id,
        "message": "Your document is being analyzed. Use /result/{job_id} to fetch result."
    }

@app.get("/result/{job_id}")
def fetch_result(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(404, "Job not found")

    return job

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)