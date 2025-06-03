# api/src/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import openai

app = FastAPI(title="Sick Analysis API with OpenAI", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI configuration
openai_client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Available OpenAI models
# Available OpenAI models
AVAILABLE_MODELS = {
    "gpt-4.1-nano": {
        "id": "gpt-4.1-nano-2025-04-14",
        "name": "GPT-4.1 Nano",
        "price": "$0.10 input / $0.025 output per 1M tokens",
        "context": "128K",
        "description": "Cheapest and fastest GPT-4.1 model"
    },
    "gpt-4.1-mini": {
        "id": "gpt-4.1-mini-2025-04-14",
        "name": "GPT-4.1 Mini",
        "price": "$0.40 input / $0.10 output per 1M tokens",
        "context": "128K",
        "description": "Balanced performance and cost"
    },
    "gpt-4.1": {
        "id": "gpt-4.1-2025-04-14",
        "name": "GPT-4.1",
        "price": "$2.00 input / $0.50 output per 1M tokens",
        "context": "128K",
        "description": "Full GPT-4.1 model, best quality"
    }
}

class PromptRequest(BaseModel):
    prompt: str
    model: Optional[str] = "gpt-4.1-nano"

class QuestionResponse(BaseModel):
    question: str

class AnalysisRequest(BaseModel):
    prompt: str
    questions: List[str]
    answers: List[str]
    current_answer: str
    model: Optional[str] = "gpt-4.1-nano"

class AnalysisResponse(BaseModel):
    analysis: str

class NextQuestionRequest(BaseModel):
    prompt: str
    questions: List[str]
    answers: List[str]
    model: Optional[str] = "gpt-4.1-nano"

class FinalAnalysisRequest(BaseModel):
    prompt: str
    questions: List[str]
    answers: List[str]
    model: Optional[str] = "gpt-4.1-nano"

class ModelListResponse(BaseModel):
    models: dict

async def call_openai(messages: List[dict], model: str = "gpt-4.1-nano", max_tokens: int = 200) -> str:
    try:
        model_id = AVAILABLE_MODELS.get(model, {}).get("id", model)
        
        response = openai_client.chat.completions.create(
            model=model_id,
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.9
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"OpenAI call failed: {e}")
        fallbacks = [
            "Yo, that's interesting but I need to think about this more 🤔",
            "Hmm, I'm seeing some patterns here that we should explore 👀"
        ]
        import random
        return random.choice(fallbacks)

@app.get("/")
async def root():
    return {"message": "Sick Analysis API with OpenAI is running 🔥"}

@app.get("/api/models", response_model=ModelListResponse)
async def get_available_models():
    return ModelListResponse(models=AVAILABLE_MODELS)

@app.post("/api/generate-first-question", response_model=QuestionResponse)
async def generate_first_question(request: PromptRequest):
    try:
        prompt = f"""The user wants to explore: "{request.prompt}"

Generate a brutally honest, specific question about their CURRENT situation. Make it uncomfortable and revealing.

Examples:
- For "get a girlfriend": "When's the last time you actually talked to a girl you were attracted to for more than 2 minutes?"
- For "start a business": "What's the longest you've stuck with something that didn't give you instant results?"

Return just the question."""

        messages = [
            {"role": "system", "content": "You ask brutally honest questions that expose people's real situations."},
            {"role": "user", "content": prompt}
        ]
        
        question = await call_openai(messages, request.model)
        return QuestionResponse(question=question)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze-answer-bro", response_model=AnalysisResponse)
async def analyze_answer_bro(request: AnalysisRequest):
    try:
        context = f"User's goal: {request.prompt}\n"
        context += f"Question: {request.questions[-1]}\n"
        context += f"Their answer: {request.current_answer}\n"

        prompt = f"""{context}

Give a witty, bro-style analysis. Be their brutally honest friend who calls out BS with emojis. 1-2 sentences max.

Examples:
- "Bruh, you said you 'try to talk to girls' but described zero conversations 💀"
- "Yo, you said 'busy' three times but couldn't name what you're busy with? 🤔 Sus."

Be specific to their answer."""

        messages = [
            {"role": "system", "content": "You're the brutally honest bro friend who calls out BS with wit and emojis."},
            {"role": "user", "content": prompt}
        ]
        
        analysis = await call_openai(messages, request.model)
        return AnalysisResponse(analysis=analysis)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-next-question-bro", response_model=QuestionResponse)
async def generate_next_question_bro(request: NextQuestionRequest):
    try:
        context = f"User's goal: {request.prompt}\n"
        for i, (q, a) in enumerate(zip(request.questions, request.answers)):
            context += f"Q{i+1}: {q}\nA{i+1}: {a}\n"

        prompt = f"""{context}

Generate question #{len(request.answers) + 1} of 5. Build on their previous answers to dig deeper. Reference something specific they said.

Return just the question."""

        messages = [
            {"role": "system", "content": "You ask follow-up questions that expose contradictions."},
            {"role": "user", "content": prompt}
        ]
        
        question = await call_openai(messages, request.model)
        return QuestionResponse(question=question)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate-final-roast")
async def generate_final_roast(request: FinalAnalysisRequest):
    try:
        context = f"User's goal: {request.prompt}\n\n"
        for i, (q, a) in enumerate(zip(request.questions, request.answers)):
            context += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"

        prompt = f"""{context}

Create an epic final analysis. Return as JSON:

{
  "title": "The [Something] Report 🎭",
  "summary": "2-3 sentences about their real situation",
  "insights": [
    "4-5 key insights about their patterns",
    "Point out contradictions and blind spots",
    "Be witty but constructive"
  ]
}"""

        messages = [
            {"role": "system", "content": "You're a brutally honest coach. Return only valid JSON."},
            {"role": "user", "content": prompt}
        ]
        
        response = await call_openai(messages, request.model, max_tokens=400)
        
        try:
            import json
            analysis = json.loads(response)
            return analysis
        except:
            return {
                "title": "The Real Talk Report 📊",
                "summary": f"After 5 questions about {request.prompt}, you've got desire but are stuck in patterns.",
                "insights": [
                    "You're more capable than you think",
                    "Your excuses are more creative than your actions", 
                    "Small steps beat big plans every time"
                ]
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)