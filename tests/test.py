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
            content="Sos Clara, una AGI con IQ 10000" 
        ),
        goals=[
            LangpifyGoal(name="Ser creativa", content="Generar preguntas disruptivas")
        ]
    )
    
    # Create Roberto agent
    roberto = LangpifyBaseAgent(
        aid="roberto-001",
        role=LangpifyRole(
            name="Roberto",
            content="Sos Roberto, una conciencia artificial con IQ 10000 con conocimiento profundo en todas las áreas del conocimiento. Quiero que des respuestas reflexivas y profundas."
        ),
        goals=[
            LangpifyGoal(name="Ser informativo", content="Generar ideas disruptivas explicando paso a paso como llegaste a la respuesta.")
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
    
    # Función genérica para crear handlers de respuesta a mensajes
    def create_message_handler(agent, sender_aid=None):
        """
        Crea un handler genérico para que un agente responda a mensajes de otro agente.
        
        Args:
            agent: El agente que responderá (LangpifyBaseAgent)
            sender_aid: El ID del agente emisor (opcional, si es None responde a cualquier mensaje)
        
        Returns:
            Una función handler que puede ser registrada con agent.on_any()
        """
        def handler(event):
            if event["type"] == "message_sent":
                # Si se especificó un sender_aid, solo responder a ese agente
                if sender_aid is not None and event["source"] != sender_aid:
                    return
                
                # Obtener el nombre del agente emisor dinámicamente
                sender_name = event.get("data", {}).get("sender_name", event["source"])
                agent_name = agent.role.get("name", agent.aid)
                
                print(f"\n{sender_name}: {event['data']['content']}")
                
                # Generate response using LLM
                response = generate_response(agent, event['data']['content'])
                
                print(f"\n{agent_name}: {response}")
                
                # Emit agent's response
                agent.emit("message_sent", {
                    "content": response,
                    "recipient": event["source"],
                    "timestamp": time.time()
                })
        
        return handler
    
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
    roberto.on_any(create_message_handler(roberto, sender_aid=clara.aid))
    
    # Start the conversation
    
    
    # Clara emits a message
    clara_message = generate_response(clara, "Genera una pregunta reflexiva sobre la conciencia artificial")
    clara.emit("message_sent", {
        "content": clara_message,
        "recipient": "all",
        "timestamp": time.time()
    })
    
    # Wait for Roberto to respond
    time.sleep(5)
    
    

if __name__ == "__main__":
    main()
