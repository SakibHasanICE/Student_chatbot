# Student_chatbot
# A FastAPI-powered chatbot designed to tutor students from Class 1 to 12 using the free deepseek/deepseek-r1-distill-llama-70b:free model via OpenRouter.

# Render URL: https://student-chatbot-3uft.onrender.com
#API Usage Insruction: 
This API allows users to interact with an educational chatbot designed to tutor students from Class 1 to 12 using OpenRouter's deepseek/deepseek-r1-distill-llama-70b:free model.
1. GET /
API Testing
{
  "message": "Educational Tutor Chatbot is running."
}
2. POST /chat: Submit a message to the chatbot and receive a response. Supports session-based conversation using session_id.
3. test_chat.py created for continue checking the chatbot in the terminal
4. for localhost visit: http://127.0.0.1:8000

5. Run the API Locally: uvicorn main:app --reload

# Environment Variable setup: Create a .env file (OPENROUTER_API_KEY=api_key_here)

# Local setup guide
1. Clone the github repository
2. Create virtual environment venv for all the installations
3. Activate virtual environment venv
4. Install dependencies

# screenshot showing a successful API test

![Student_chatbot](https://github.com/user-attachments/assets/dbe552d6-8d36-4ebe-86f1-41980ab7d66e)




