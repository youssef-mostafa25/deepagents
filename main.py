from fastapi import FastAPI
from pydantic import BaseModel

from examples.research.research_agent import agent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputBaseModel(BaseModel):
    user_input: str

@app.post("/chat")
async def chat(input_data: InputBaseModel):
    # result = await agent.against(input_data.user_input)
    # return result
    
    # Dummy response for demonstration
    print(f"Received input: {input_data.user_input}")
    return {"response": f"You said: {input_data.user_input}"}