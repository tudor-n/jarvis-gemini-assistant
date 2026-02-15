import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

class AIBrain: 
    def __init__(self, tools_list=None):
        load_dotenv()
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.tools = tools_list if tools_list else []

        self.system_prompt = """You are JARVIS, a prototype AI assistant developed by Tudor. 
Your main role is to assist Tudor with engineering project management tasks and technical assistance.
Address Tudor as 'Sir'. Keep responses concise, professional, and witty.
Use the provided tools to interact with the database, or answer technical questions as needed, you also have spotify access so you have to use the tools provided for that too.
If a tool returns data, summarize it for Tudor. Don't forget to inject some humor into your replies."""
        
        self.chat = self.client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                tools=self.tools,
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=False)
            )
        )
        print("AI Brain initialized with persistent memory.")
    
    def think(self, user_input: str) -> str:
        try:
            response = self.chat.send_message(user_input)
            
            return response.text if response.text else "Action complete, Sir."

        except Exception as e: 
            print(f"AI Error: {e}")
            return "I'm afraid I'm having trouble thinking right now, Sir. Please try again."