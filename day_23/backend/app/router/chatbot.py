import os
from fastapi import HTTPException, APIRouter, Depends
from google import genai
from dotenv import load_dotenv
from app.schemas.chat import ChatRequest, ChatResponse
from app.model.user import User
from app.utils.dependency import get_current_user


load_dotenv()

router = APIRouter()

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")
client = genai.Client(api_key=api_key)
chat_session = client.chats.create(model="gemini-2.5-flash")



@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest, 
                        current_user: User = Depends(get_current_user),
                        ):
    """
    Stateful endpoint that posts user text to Gemini, 
    maintaining context history across consecutive requests.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
        
    try:
        # Send the user query to the continuing session
        response = chat_session.send_message(request.message)
        return ChatResponse(response=response.text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")


