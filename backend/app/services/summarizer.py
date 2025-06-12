import os
import json
from typing import List, Dict
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv
import openai
import instructor

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

client = openai.OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=os.getenv("GROQ_API_KEY")
)
client = instructor.patch(client)

MODEL = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
You are a research assistant.
Given the following answers extracted from documents, identify key themes across the content.
Group related answers under the same theme and cite the source of each answer.

Output must strictly follow the following JSON schema:
- theme: one-line summary for the theme.
- summary: a detailed explanation as elaborate as you can be in context of question and response.
- citations: list of citation strings (e.g., 'doc.pdf – Page 2 – Para 4 – Sentence 1').

Don't create hallucinated citations.
"""

class ThemeGroup(BaseModel):
    theme: str
    summary: str
    citations: List[str]

def generate_themes(answer_chunks: List[Dict]) -> List[ThemeGroup]:
    text_blocks = []
    for item in answer_chunks:
        citation = item.get("citation", "Unknown")
        text = item.get("text", "")
        text_blocks.append(f"- {text} ({citation})")

    full_input = "\n".join(text_blocks)

    try:
        response = client.chat.completions.create(
            model=MODEL,
            response_model=List[ThemeGroup],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": full_input}
            ],
            temperature=0.3,
            max_retries=2
        )
        return response
    except Exception as e:
        return [ThemeGroup(theme="Error", summary=f"Failed to parse response: {str(e)}", citations=[])]
