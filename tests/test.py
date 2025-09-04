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

# Import LLM clients
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

# Main function
def main():
    # Check for API keys and determine which provider to use
    openai_key = os.environ.get("OPENAI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")
    
    if groq_key and ChatGroq:
        try:
            print("🚀 Usando Groq (gratuito)")
            client = ChatGroq(
                api_key=groq_key,
                model="llama-3.1-8b-instant",
                temperature=0.7
            )
            provider = "groq"
            model_name = "llama-3.1-8b-instant"
        except Exception as e:
            print(f"⚠️  Error inicializando Groq: {e}")
            print("🔄 Intentando con OpenAI...")
            if openai_key and OpenAI:
                client = OpenAI(api_key=openai_key)
                provider = "openai"
                model_name = "gpt-3.5-turbo"
            else:
                print("❌ Error: No se pudo inicializar ningún cliente LLM")
                return
    elif openai_key and OpenAI:
        print("🚀 Usando OpenAI")
        client = OpenAI(api_key=openai_key)
        provider = "openai"
        model_name = "gpt-3.5-turbo"
    else:
        print("❌ Error: Se requiere al menos una API key:")
        print("   - GROQ_API_KEY (gratuito, recomendado)")
        print("   - OPENAI_API_KEY")
        print("\n📝 Para obtener Groq API key gratuita:")
        print("   1. Ve a https://console.groq.com/")
        print("   2. Crea una cuenta gratuita")
        print("   3. Genera una API key")
        print("   4. export GROQ_API_KEY='tu-groq-api-key'")
        return
    
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
    
    # Set up LLM for both agents
    clara.language = LangpifyLanguage(
        model_provider=provider,
        model_name=model_name,
        model=client
    )
    
    roberto.language = LangpifyLanguage(
        model_provider=provider,
        model_name=model_name,
        model=client
    )
    
    # Define Roberto's event handler to respond to Clara's messages
    def roberto_handler(event):
        if event["type"] == "message_sent" and event["source"] == clara.aid:
            print(f"\nClara: {event['data']['content']}")
            
            # Generate response using LLM
            response = generate_response(roberto, event['data']['content'])
            
            print(f"\nRoberto: {response}")
            
            # Emit Roberto's response
            roberto.emit("message_sent", {
                "content": response,
                "recipient": clara.aid,
                "timestamp": time.time()
            })
    
    # Function to generate responses using LLM (OpenAI or Groq)
    def generate_response(agent, prompt):
        try:
            # Prepare system message with agent role
            system_message = f"You are {agent.role['name']}. {agent.role['content']}"
            
            if agent.language["model_provider"] == "groq":
                # Use LangChain ChatGroq
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=prompt)
                ]
                response = agent.language["model"].invoke(messages)
                return response.content
            else:
                # Use OpenAI client
                response = agent.language["model"].chat.completions.create(
                    model=agent.language["model_name"],
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": prompt}
                    ]
                )
                return response.choices[0].message.content
            
        except Exception as e:
            error_message = f"Error communicating with {agent.language['model_provider']}: {str(e)}"
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
