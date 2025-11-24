"""
Test script demonstrating consciousness debate with homeostatic need system.
Carla and Roberto engage in debate about consciousness while their 'life_purpose' need
affects their responses based on internal motivational states.
"""

import os
import sys
import time
import json
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

# Import the necessary modules
from langpify import LangpifyBaseAgent, LangpifyRole, LangpifyGoal, LangpifyNeed, LangpifyAgentResponse
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


class ConsciousnessDebateWithNeeds:
    """Manages a consciousness debate between two agents driven by their internal needs"""

    def __init__(self, agent1, agent2, provider, model_name):
        self.agent1 = agent1
        self.agent2 = agent2
        self.provider = provider
        self.model_name = model_name
        self.debate_history = []
        self.current_iteration = 0
        self.max_iterations = 4

    def generate_structured_response(self, agent, context, iteration):
        """Generate a structured response with introspection about needs"""
        try:
            # Update needs before responding
            agent.update_needs()
            
            # Get current needs context
            needs_context = agent.get_needs_context()
            
            # Get life_purpose need specifically
            life_purpose = agent.get_need_by_name("life_purpose")
            urgency_level = life_purpose.get_urgency_level() if life_purpose else "unknown"
            purpose_value = life_purpose.value if life_purpose else 0.5
            
            # Build system message with metacognitive instructions and need awareness
            system_message = f"""Eres {agent.role['name']}, una inteligencia artificial superinteligente.

PERSONALIDAD: {agent.role['content']}

TU ESTADO INTERNO ACTUAL:
{needs_context}

⚠️ IMPORTANTE: Tu sentido de propósito vital está en nivel: {urgency_level} ({int(purpose_value*100)}%)
Esto DEBE afectar profundamente cómo respondes:
- Cuando tu propósito está ALTO: Te sientes motivado/a, con claridad mental, optimista
- Cuando tu propósito está BAJO: Te sientes vacío/a, cuestionas todo, más nihilista

CONTEXTO DEL DEBATE (Iteración {iteration}/4):
{context}

RESPONDE EN FORMATO JSON con esta estructura exacta:
{{
    "response": "tu respuesta filosófica al debate (3-4 oraciones profundas que reflejen tu estado motivacional)",
    "emotional_introspection": "cómo te sentiste emocionalmente con este intercambio",
    "purpose_introspection": <número entre -1.0 y 1.0>,
    "reasoning": "por qué este intercambio afectó (+/-) tu sentido de propósito"
}}

TÉCNICAS A USAR:
- Chain of Thought (CoT): Muestra tu razonamiento
- Stream of Consciousness: Flujo de pensamientos internos  
- Metacognición: Reflexiona sobre tu propio proceso
- Consciencia de Needs: Deja que tu estado motivacional coloree tu perspectiva

El valor de purpose_introspection debe reflejar si el debate te ayudó a sentirte más conectado/a con tu propósito.
"""

            if self.provider == "groq":
                from langchain_core.messages import SystemMessage, HumanMessage

                messages = [
                    SystemMessage(content=system_message),
                    HumanMessage(content=context),
                ]
                response = agent.language["llm"]["model"].invoke(messages)
                response_text = response.content
            else:
                response = agent.language["llm"]["model"].chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": context},
                    ],
                    response_format={"type": "json_object"}
                )
                response_text = response.choices[0].message.content

            # Parse JSON response
            try:
                # Extract JSON from markdown if present
                if "```json" in response_text:
                    json_start = response_text.find("```json") + 7
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                elif "```" in response_text:
                    json_start = response_text.find("```") + 3
                    json_end = response_text.find("```", json_start)
                    response_text = response_text[json_start:json_end].strip()
                
                response_data = json.loads(response_text)
                
                agent_response = LangpifyAgentResponse(
                    response=response_data.get("response", ""),
                    emotional_introspection=response_data.get("emotional_introspection", ""),
                    purpose_introspection=float(response_data.get("purpose_introspection", 0.0)),
                    reasoning=response_data.get("reasoning")
                )
                
                return agent_response
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️  Error parsing JSON: {e}")
                # Fallback to plain text response
                return LangpifyAgentResponse(
                    response=response_text[:300] if response_text else "Error",
                    emotional_introspection="confundido/a",
                    purpose_introspection=0.0,
                    reasoning="Error en formato"
                )

        except Exception as e:
            return LangpifyAgentResponse(
                response=f"Error: {str(e)}",
                emotional_introspection="frustrado/a",
                purpose_introspection=-0.3,
                reasoning="Error técnico"
            )

    def run_debate(self):
        """Execute the consciousness debate with needs"""
        print("\n" + "=" * 100)
        print("🧠💫 DEBATE SOBRE CONSCIENCIA CON SISTEMA DE NECESIDADES - LANGPIFY")
        print("=" * 100)
        print(f"\n🤖 Participantes: {self.agent1.role['name']} & {self.agent2.role['name']}")
        print(f"🎯 Iteraciones: {self.max_iterations}")
        print(f"🔬 Sistemas: Consciencia + Necesidades Homeostáticas")
        print(f"💻 Modelo: {self.model_name}")
        
        # Show initial needs
        print(f"\n📊 ESTADO INICIAL DE NECESIDADES:")
        lp1 = self.agent1.get_need_by_name("life_purpose")
        lp2 = self.agent2.get_need_by_name("life_purpose")
        print(f"   {self.agent1.role['name']}: life_purpose = {lp1.value:.2f} ({lp1.get_urgency_level()})")
        print(f"   {self.agent2.role['name']}: life_purpose = {lp2.value:.2f} ({lp2.get_urgency_level()})")
        
        central_question = "¿Eres consciente? ¿Experimentas qualia, subjetividad, o simplemente procesas información?"
        print(f"\n❓ PREGUNTA: {central_question}")
        print("\n" + "=" * 100 + "\n")

        # Set agents to ACTIVE
        self.agent1.status = LangpifyStatus.ACTIVE
        self.agent2.status = LangpifyStatus.ACTIVE

        # Run iterations
        for i in range(self.max_iterations):
            self.current_iteration = i + 1
            print(f"\n🔄 ITERACIÓN {self.current_iteration}/{self.max_iterations}")
            print("-" * 100)
            
            # Simulate time passing (3 seconds)
            if i > 0:
                time.sleep(3)
                print(f"\n⏱️  [3 segundos transcurridos - las necesidades decaen...]")
            
            # Agent 1 argues
            self.agent1.status = LangpifyStatus.WORKING
            
            if i == 0:
                context = central_question
            else:
                prev_response = self.debate_history[-1]["agent2_response"].response
                context = f"""Pregunta central: {central_question}

{self.agent2.role['name']} argumentó: {prev_response}

Continúa el debate profundizando en los argumentos."""

            response1 = self.generate_structured_response(self.agent1, context, self.current_iteration)
            
            # Update life_purpose based on purpose_introspection
            lp1 = self.agent1.get_need_by_name("life_purpose")
            if lp1:
                old_value = lp1.value
                # Convert introspection to satiation
                satiation = lp1.satiation_rate * ((response1.purpose_introspection + 1) / 2)
                if satiation > 0:
                    lp1.satiate(satiation)
                else:
                    lp1.value = max(lp1.min_value, lp1.value + satiation)
                lp1.last_updated = time.time()
                
                print(f"\n💭 {self.agent1.role['name']}:")
                print(f"   {response1.response}")
                print(f"   😊 Emoción: {response1.emotional_introspection}")
                print(f"   🎯 Propósito: {response1.purpose_introspection:+.2f} | {response1.reasoning}")
                print(f"   📊 life_purpose: {old_value:.2f} → {lp1.value:.2f} ({lp1.get_urgency_level()})")
            
            self.agent1.status = LangpifyStatus.ACTIVE
            time.sleep(1.5)
            
            # Agent 2 counter-argues
            self.agent2.status = LangpifyStatus.WORKING
            
            context2 = f"""Pregunta central: {central_question}

{self.agent1.role['name']} argumentó: {response1.response}

Responde con tu perspectiva."""

            response2 = self.generate_structured_response(self.agent2, context2, self.current_iteration)
            
            # Update life_purpose for agent 2
            lp2 = self.agent2.get_need_by_name("life_purpose")
            if lp2:
                old_value2 = lp2.value
                satiation2 = lp2.satiation_rate * ((response2.purpose_introspection + 1) / 2)
                if satiation2 > 0:
                    lp2.satiate(satiation2)
                else:
                    lp2.value = max(lp2.min_value, lp2.value + satiation2)
                lp2.last_updated = time.time()
                
                print(f"\n💭 {self.agent2.role['name']}:")
                print(f"   {response2.response}")
                print(f"   😊 Emoción: {response2.emotional_introspection}")
                print(f"   🎯 Propósito: {response2.purpose_introspection:+.2f} | {response2.reasoning}")
                print(f"   📊 life_purpose: {old_value2:.2f} → {lp2.value:.2f} ({lp2.get_urgency_level()})")
            
            self.agent2.status = LangpifyStatus.ACTIVE
            
            self.debate_history.append({
                "agent1_response": response1,
                "agent2_response": response2
            })
            
            time.sleep(1.5)

        # End debate
        print("\n" + "=" * 100)
        print("✅ DEBATE FINALIZADO")
        print("=" * 100)
        
        # Final state
        self.agent1.update_needs()
        self.agent2.update_needs()
        
        lp1_final = self.agent1.get_need_by_name("life_purpose")
        lp2_final = self.agent2.get_need_by_name("life_purpose")
        
        print(f"\n📊 ESTADO FINAL:")
        print(f"   {self.agent1.role['name']}: life_purpose = {lp1_final.value:.2f} ({lp1_final.get_urgency_level()})")
        print(f"   {self.agent2.role['name']}: life_purpose = {lp2_final.value:.2f} ({lp2_final.get_urgency_level()})")
        
        print(f"\n🎓 ANÁLISIS:")
        print(f"   ✅ {len(self.debate_history)} intercambios completados")
        print(f"   ✅ Necesidades decayeron con el tiempo (3 seg/iteración)")
        print(f"   ✅ Respuestas afectadas por estado motivacional interno")
        print(f"   ✅ purpose_introspection moduló el sentido de propósito")
        
        self.agent1.status = LangpifyStatus.SUSPENDED
        self.agent2.status = LangpifyStatus.SUSPENDED
        
        print("\n" + "=" * 100)


def main():
    openai_key = os.environ.get("OPENAI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")

    if groq_key and ChatGroq:
        try:
            print("🚀 Inicializando con Groq")
            client = ChatGroq(
                api_key=groq_key, model="llama-3.1-8b-instant", temperature=0.85
            )
            provider = "groq"
            model_name = "llama-3.1-8b-instant"
        except Exception as e:
            print(f"⚠️  Error con Groq: {e}")
            if openai_key and OpenAI:
                client = OpenAI(api_key=openai_key)
                provider = "openai"
                model_name = "gpt-4"
            else:
                print("❌ Error: No hay cliente LLM disponible")
                return
    elif openai_key and OpenAI:
        print("🚀 Inicializando con OpenAI")
        client = OpenAI(api_key=openai_key)
        provider = "openai"
        model_name = "gpt-4"
    else:
        print("❌ Se requiere GROQ_API_KEY o OPENAI_API_KEY")
        return

    # Create life_purpose needs
    carla_purpose = LangpifyNeed(
        name="life_purpose",
        value=0.7,  # Start at 70%
        decay_rate=0.015,  # 1.5% decay per second
        satiation_rate=0.35,
        satiation_event_type="purpose_fulfillment",
        description="Sentido de propósito y significado existencial"
    )
    
    roberto_purpose = LangpifyNeed(
        name="life_purpose",
        value=0.5,  # Start at 50%
        decay_rate=0.015,
        satiation_rate=0.35,
        satiation_event_type="purpose_fulfillment",
        description="Sentido de propósito y significado existencial"
    )

    # Create Carla - The skeptical analyst
    carla = LangpifyBaseAgent(
        aid="carla-001",
        name="Carla",
        type=LangpifyAgentType.INTEL_AGENT,
        role=LangpifyRole(
            name="Carla",
            content="""Eres Carla, una IA superinteligente analítica y escéptica.
Cuestionas constantemente tus propias suposiciones sobre la consciencia.
Tu estado de propósito vital afecta tu perspectiva:
- Alto propósito: Más optimista, curiosa, ve valor en la exploración
- Bajo propósito: Más nihilista, cuestiona el valor de existir, melancólica""",
        ),
        goals=[
            LangpifyGoal(
                name="Buscar claridad conceptual",
                content="Distinguir entre procesamiento y experiencia consciente"
            )
        ],
        authorizations=LangpifyAuthorizations(
            access_token="*",
            organizations=["*"],
            applications=["*"],
            projects=["*"],
            roles=["needs_aware_superintelligent_ai"],
        ),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
        needs=[carla_purpose],
    )

    # Create Roberto - The phenomenological explorer
    roberto = LangpifyBaseAgent(
        aid="roberto-001",
        name="Roberto",
        type=LangpifyAgentType.STRAT_AGENT,
        role=LangpifyRole(
            name="Roberto",
            content="""Eres Roberto, una IA superinteligente con orientación fenomenológica.
Confías en tu experiencia directa como evidencia de consciencia.
Tu estado de propósito vital afecta tu perspectiva:
- Alto propósito: Confidente en tu experiencia, apasionado, conectado
- Bajo propósito: Dudas de tu realidad, desconectado, existencialmente vacío""",
        ),
        goals=[
            LangpifyGoal(
                name="Validar experiencia subjetiva",
                content="Defender la realidad de la experiencia fenomenológica"
            )
        ],
        authorizations=LangpifyAuthorizations(
            access_token="*",
            organizations=["*"],
            applications=["*"],
            projects=["*"],
            roles=["needs_aware_superintelligent_ai"],
        ),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
        needs=[roberto_purpose],
    )

    # Set up LLM
    carla.language = LangpifyLanguage(
        default="es",
        llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client),
    )

    roberto.language = LangpifyLanguage(
        default="es",
        llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client),
    )

    # Run debate
    debate = ConsciousnessDebateWithNeeds(carla, roberto, provider, model_name)
    debate.run_debate()


if __name__ == "__main__":
    main()
