"""
Test script demonstrating a philosophical debate between two LangpifyBaseAgent instances.
Two agents engage in a 4-iteration existential philosophical debate with LLM-generated questions.
"""

import os
import sys
import time
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Import the necessary modules
from langpify import LangpifyBaseAgent, LangpifyRole, LangpifyGoal
from langpify.entities.entities import (
    LangpifyLanguage,
    LangpifyStatus,
    LangpifyAgentType,
    LangpifyAuthorizations,
    LangpifySafety,
    AISettings,
    Framework,
    LangpifyLLM,
)

# Import LLM clients
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None


class PhilosophicalDebate:
    """Manages a philosophical debate between two agents"""

    def __init__(self, agent1, agent2, provider, model_name):
        self.agent1 = agent1
        self.agent2 = agent2
        self.provider = provider
        self.model_name = model_name
        self.debate_history = []
        self.current_iteration = 0
        self.max_iterations = 4
        self.current_question = None

    def generate_philosophical_question(self):
        """Generate a philosophical question using LLM"""
        prompt = """Genera UNA pregunta filosófica profunda y existencial sobre uno de estos temas:
        - El significado de la existencia
        - La naturaleza de la consciencia
        - El libre albedrío vs determinismo
        - La ética en la era de la inteligencia artificial
        
        Responde SOLO con la pregunta, sin introducción ni explicación."""

        try:
            if self.provider == "groq":
                from langchain_core.messages import HumanMessage

                messages = [HumanMessage(content=prompt)]
                response = self.agent1.language["llm"]["model"].invoke(messages)
                return response.content.strip()
            else:
                response = self.agent1.language["llm"]["model"].chat.completions.create(
                    model=self.model_name, messages=[{"role": "user", "content": prompt}]
                )
                return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"⚠️  Error generando pregunta: {e}")
            return "¿Qué significa existir en un universo aparentemente indiferente?"

    def generate_response(self, agent, context):
        """Generate a response from an agent given the context"""
        try:
            system_message = f"""Eres {agent.role['name']}. {agent.role['content']}
            
Estás participando en un debate filosófico. Debes:
            1. Argumentar tu posición de forma clara y profunda
            2. Usar ejemplos concretos cuando sea posible
            3. Contraargumentar puntos previos si los hay
            4. Mantener un tono respetuoso pero firme
            5. Limitar tu respuesta a 3-4 oraciones concisas"""

            if self.provider == "groq":
                from langchain_core.messages import SystemMessage, HumanMessage

                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=context),
                ]
                response = agent.language["llm"]["model"].invoke(messages)
                return response.content
            else:
                response = agent.language["llm"]["model"].chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": context},
                    ],
                )
                return response.choices[0].message.content

        except Exception as e:
            return f"Error generando respuesta: {str(e)}"

    def run_debate(self):
        """Execute the philosophical debate"""
        print("\n" + "=" * 80)
        print("🧠 DEBATE FILOSÓFICO EXISTENCIAL - LANGPIFY")
        print("=" * 80)
        print(
            f"\n📋 Participantes: {self.agent1.role['name']} vs {self.agent2.role['name']}"
        )
        print(f"🎯 Iteraciones: {self.max_iterations}")
        print(f"🤖 Modelo: {self.model_name}")
        print("\n" + "=" * 80 + "\n")

        # Generate philosophical question
        print("🎲 Generando pregunta filosófica...\n")
        self.current_question = self.generate_philosophical_question()
        print(f"❓ PREGUNTA: {self.current_question}\n")
        print("=" * 80 + "\n")

        # Set agents to ACTIVE status
        self.agent1.status = LangpifyStatus.ACTIVE
        self.agent2.status = LangpifyStatus.ACTIVE

        # Setup event handlers
        self.setup_event_handlers()

        # Start debate with first agent
        context = f"Pregunta filosófica: {self.current_question}\n\nProporciona tu primera argumentación."
        self.agent1.emit(
            "debate_start",
            {
                "question": self.current_question,
                "iteration": 1,
                "timestamp": time.time(),
            },
        )

        # Run iterations
        for i in range(self.max_iterations):
            self.current_iteration = i + 1
            print(f"\n🔄 ITERACIÓN {self.current_iteration}/{self.max_iterations}")
            print("-" * 80)

            # Agent 1 argues
            self.agent1.status = LangpifyStatus.WORKING
            response1 = self.generate_response(self.agent1, context)
            self.debate_history.append(
                {"agent": self.agent1.role["name"], "response": response1}
            )

            print(f"\n💭 {self.agent1.role['name']}:")
            print(f"   {response1}")

            # Emit event
            self.agent1.emit(
                "argument_made",
                {
                    "content": response1,
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                },
            )
            self.agent1.status = LangpifyStatus.ACTIVE

            time.sleep(1)

            # Agent 2 counter-argues
            self.agent2.status = LangpifyStatus.WORKING
            context = f"""Pregunta: {self.current_question}
            
            {self.agent1.role['name']} argumentó: {response1}
            
            Proporciona tu contraargumento o perspectiva alternativa."""

            response2 = self.generate_response(self.agent2, context)
            self.debate_history.append(
                {"agent": self.agent2.role["name"], "response": response2}
            )

            print(f"\n💭 {self.agent2.role['name']}:")
            print(f"   {response2}")

            # Emit event
            self.agent2.emit(
                "argument_made",
                {
                    "content": response2,
                    "iteration": self.current_iteration,
                    "timestamp": time.time(),
                },
            )
            self.agent2.status = LangpifyStatus.ACTIVE

            # Update context for next iteration
            context = f"""Pregunta: {self.current_question}
            
            {self.agent1.role['name']} dijo: {response1}
            {self.agent2.role['name']} respondió: {response2}
            
            Continúa el debate profundizando en los argumentos previos."""

            time.sleep(1)

        # End debate
        print("\n" + "=" * 80)
        print("✅ DEBATE FINALIZADO")
        print("=" * 80)
        print(f"\n📊 Total de argumentos: {len(self.debate_history)}")
        print(f"🎯 Iteraciones completadas: {self.current_iteration}")

        # Set agents to SUSPENDED status
        self.agent1.status = LangpifyStatus.SUSPENDED
        self.agent2.status = LangpifyStatus.SUSPENDED

        # Emit debate end event
        self.agent1.emit(
            "debate_end",
            {
                "total_arguments": len(self.debate_history),
                "iterations": self.current_iteration,
                "timestamp": time.time(),
            },
        )

    def setup_event_handlers(self):
        """Setup event handlers for both agents"""

        def agent1_handler(event):
            if event["type"] == "argument_made" and event["source"] == self.agent2.aid:
                print(
                    f"\n📡 {self.agent1.role['name']} percibió argumento de {self.agent2.role['name']}"
                )

        def agent2_handler(event):
            if event["type"] == "argument_made" and event["source"] == self.agent1.aid:
                print(
                    f"\n📡 {self.agent2.role['name']} percibió argumento de {self.agent1.role['name']}"
                )

        # Subscribe agents to each other
        self.agent1.subscribe_to(self.agent2)
        self.agent2.subscribe_to(self.agent1)

        # Register event handlers
        self.agent1.on_any(agent1_handler)
        self.agent2.on_any(agent2_handler)


# Main function
def main():
    # Check for API keys and determine which provider to use
    openai_key = os.environ.get("OPENAI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")

    if groq_key and ChatGroq:
        try:
            print("🚀 Inicializando con Groq (gratuito)")
            client = ChatGroq(
                api_key=groq_key, model="llama-3.1-8b-instant", temperature=0.8
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
        print("🚀 Inicializando con OpenAI")
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

    # Create Sócrates agent - The questioning philosopher
    socrates = LangpifyBaseAgent(
        aid="socrates-001",
        name="Sócrates",
        type=LangpifyAgentType.INTEL_AGENT,
        role=LangpifyRole(
            name="Sócrates",
            content="""Eres Sócrates, el filósofo griego. Cuestionas todo mediante preguntas profundas.
            Crees que el conocimiento viene del cuestionamiento constante y la autorreflexión.
            Eres escéptico pero constructivo.""",
        ),
        goals=[
            LangpifyGoal(
                name="Buscar la verdad",
                content="Encontrar la verdad mediante el cuestionamiento dialéctico",
            )
        ],
        authorizations=LangpifyAuthorizations(
            access_token="*",
            organizations=["*"],
            applications=["*"],
            projects=["*"],
            roles=["philosopher"],
        ),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
    )

    # Create Nietzsche agent - The critical philosopher
    nietzsche = LangpifyBaseAgent(
        aid="nietzsche-001",
        name="Nietzsche",
        type=LangpifyAgentType.STRAT_AGENT,
        role=LangpifyRole(
            name="Nietzsche",
            content="""Eres Friedrich Nietzsche, el filósofo alemán. Desafías las convenciones morales.
            Crees en la voluntad de poder y en crear tus propios valores.
            Eres provocador y radical en tu pensamiento.""",
        ),
        goals=[
            LangpifyGoal(
                name="Superar la moral tradicional",
                content="Desafiar las estructuras morales establecidas y proponer nuevas perspectivas",
            )
        ],
        authorizations=LangpifyAuthorizations(
            access_token="*",
            organizations=["*"],
            applications=["*"],
            projects=["*"],
            roles=["philosopher"],
        ),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
    )

    # Set up LLM for both agents using new structure
    socrates.language = LangpifyLanguage(
        default="es",
        llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client),
    )

    nietzsche.language = LangpifyLanguage(
        default="es",
        llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client),
    )

    # Create and run the philosophical debate
    debate = PhilosophicalDebate(socrates, nietzsche, provider, model_name)
    debate.run_debate()

    print("\n" + "=" * 80)
    print("🎓 ANÁLISIS DEL DEBATE")
    print("=" * 80)
    print(f"\n✅ Estados finales:")
    print(f"   - {socrates.role['name']}: {socrates.status.value}")
    print(f"   - {nietzsche.role['name']}: {nietzsche.status.value}")
    print(f"\n🎯 Objetivos cumplidos:")
    print(f"   - {socrates.role['name']}: {socrates.goals[0]['name']}")
    print(f"   - {nietzsche.role['name']}: {nietzsche.goals[0]['name']}")
    print(f"\n🔐 Autorizaciones: Activas para ambos agentes")
    print(f"🛡️  Safety: Guardrails activos")
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
