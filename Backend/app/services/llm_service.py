import os
import json
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate


def get_llm():
    """Initialize the Groq LLM via LangChain."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=api_key,
        temperature=0.3,
    )


RESUME_VALIDATION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a document classifier. Determine if the given text is a valid resume/CV.

A valid resume typically contains:
- Personal/contact information
- Work experience or employment history
- Education background
- Skills section
- Professional summary or objective

Your response MUST be in the following JSON format:
{{
    "is_valid_resume": <true or false>,
    "confidence": <number from 0-100>,
    "reason": "<brief explanation of why this is or isn't a resume>"
}}

Be strict in your validation.""",
    ),
    (
        "human",
        "Is this a valid resume?\n\n{text}",
    ),
])


RESUME_ANALYSIS_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an expert resume reviewer and career coach. 
Analyze the given resume text thoroughly and provide a detailed, actionable review.

Your response MUST be in the following JSON format:
{{
    "overall_score": <number from 1-10>,
    "summary": "<brief 2-3 sentence overview of the resume>",
    "strengths": ["<strength 1>", "<strength 2>", ...],
    "weaknesses": ["<weakness 1>", "<weakness 2>", ...],
    "suggestions": [
        {{
            "category": "<category name like 'Formatting', 'Content', 'Skills', 'Experience', 'Education', 'ATS Optimization'>",
            "suggestion": "<specific actionable suggestion>"
        }}
    ],
    "missing_sections": ["<any important sections that are missing>"],
    "ats_compatibility": {{
        "score": <number from 1-10>,
        "issues": ["<ATS issue 1>", "<ATS issue 2>", ...]
    }},
    "keywords_found": ["<relevant keyword 1>", "<relevant keyword 2>", ...],
   

Be specific, professional, and constructive in your feedback.""",
    ),
    (
        "human",
        "Please analyze the following resume:\n\n{resume_text}",
    ),
])


async def validate_resume(text: str) -> dict:
    """Validate if the uploaded document is actually a resume."""
    llm = get_llm()
    chain = RESUME_VALIDATION_PROMPT | llm

    response = await chain.ainvoke({"text": text[:3000]})  # Use first 3000 chars for validation

    content = response.content.strip()
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "is_valid_resume": False,
            "confidence": 0,
            "reason": "Failed to validate document format."
        }


async def analyze_resume(resume_text: str) -> dict:
    """Send resume text to Groq LLM for analysis and suggestions."""
    llm = get_llm()
    chain = RESUME_ANALYSIS_PROMPT | llm

    response = await chain.ainvoke({"resume_text": resume_text})

    content = response.content.strip()
    # Clean markdown formatting if the model wraps it in blockquotes
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse LLM response into JSON format.",
            "raw_response": content
        }
