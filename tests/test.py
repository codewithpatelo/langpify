"""
Simple test script demonstrating a basic flow between two LangpifyBaseAgent instances.
Clara emits a message, Roberto responds to it using OpenAI.
"""

import os
import sys
import time
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Import the necessary modules
from langpify import LangpifyBaseAgent, LangpifyRole, LangpifyGoal
from langpify.entities.entities import LangpifyLanguage, LangpifyStatus

# Import OpenAI
from openai import OpenAI

# Main function
def main():
    # Check for OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY environment variable not set. Please set it before running this script.")
        return
    
    # Create OpenAI client
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    # Create Clara agent
    clara = LangpifyBaseAgent(
        aid="clara-001",
        role=LangpifyRole(
            name="Clara",
            content="Sos Clara, una asistente de IA creativa y entusiasta."
        ),
        goals=[
            LangpifyGoal(name="Ser creativa", content="Generar ideas interesantes")
        ]
    )
    
    # Create Roberto agent
    roberto = LangpifyBaseAgent(
        aid="roberto-001",
        role=LangpifyRole(
            name="Roberto",
            content="Sos Roberto, un asistente de IA conocedor y analítico."
        ),
        goals=[
            LangpifyGoal(name="Ser informativo", content="Proporcionar información detallada")
        ]
    )
    
    # Set up OpenAI for both agents
    clara.language = LangpifyLanguage(
        model_provider="openai",
        model_name="gpt-3.5-turbo",
        model=openai_client
    )
    
    roberto.language = LangpifyLanguage(
        model_provider="openai",
        model_name="gpt-3.5-turbo",
        model=openai_client
    )
    
    # Define Roberto's event handler to respond to Clara's messages
    def roberto_handler(event):
        if event["type"] == "message_sent" and event["source"] == clara.aid:
            print(f"\nClara: {event['data']['content']}")
            
            # Generate response using OpenAI
            response = generate_response(roberto, event['data']['content'])
            
            print(f"\nRoberto: {response}")
            
            # Emit Roberto's response
            roberto.emit("message_sent", {
                "content": response,
                "recipient": clara.aid,
                "timestamp": time.time()
            })
    
    # Function to generate responses using OpenAI
    def generate_response(agent, prompt):
        try:
            # Prepare system message with agent role
            system_message = f"You are {agent.role['name']}. {agent.role['content']}"
            
            # Call OpenAI API
            response = agent.language["model"].chat.completions.create(
                model=agent.language["model_name"],
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Extract and return response text
            return response.choices[0].message.content
            
        except Exception as e:
            error_message = f"Error communicating with OpenAI: {str(e)}"
            return error_message
    
    # Subscribe Roberto to Clara's events
    roberto.subscribe_to(clara)
    roberto.on_any(roberto_handler)
    
    # Start the conversation
    print("\n=== Inicio de la simulación del flujo del agente ===\n")
    
    # Clara emits a message
    clara_message = generate_response(clara, "Genera una pregunta reflexiva sobre la inteligencia artificial.")
    clara.emit("message_sent", {
        "content": clara_message,
        "recipient": "all",
        "timestamp": time.time()
    })
    
    # Wait for Roberto to respond
    time.sleep(5)
    
    print("\n=== Fin de la simulación del flujo del agente ===\n")

if __name__ == "__main__":
    main()
