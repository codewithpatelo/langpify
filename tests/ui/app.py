"""
Interfaz Gráfica Estilo Los Sims para Debate de Consciencia
Backend FastAPI con WebSockets para comunicación en tiempo real
"""

import asyncio
import json
import time
from typing import List, Dict
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
import os
import sys

# Agregar el path del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from langpify import LangpifyBaseAgent, LangpifyRole, LangpifyGoal, LangpifyNeed
from langpify.entities.entities import (
    LangpifyLanguage,
    LangpifyStatus,
    LangpifyAgentType,
    LangpifyAuthorizations,
    LangpifySafety,
    AISettings,
    Framework,
    LangpifyLLM,
    LangpifyAgentResponse,
)

try:
    from langchain_groq import ChatGroq
except ImportError:
    ChatGroq = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

import edge_tts
import base64

app = FastAPI(title="Langpify Sims UI")

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_json(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()


@app.get("/")
async def get_index():
    """Servir la página principal"""
    index_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(index_path)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint para comunicación en tiempo real"""
    await manager.connect(websocket)
    
    try:
        # Esperar comando de inicio
        data = await websocket.receive_json()
        
        if data.get("action") == "start_debate":
            await run_debate(websocket)
    
    except WebSocketDisconnect:
        manager.disconnect(websocket)


async def run_debate(websocket: WebSocket):
    """Ejecutar el debate y enviar actualizaciones en tiempo real"""
    
    # Configurar LLM
    groq_key = os.environ.get("GROQ_API_KEY")
    openai_key = os.environ.get("OPENAI_API_KEY")
    
    if groq_key and ChatGroq:
        client = ChatGroq(api_key=groq_key, model="llama-3.1-8b-instant", temperature=0.85)
        provider = "groq"
        model_name = "llama-3.1-8b-instant"
    elif openai_key and OpenAI:
        client = OpenAI(api_key=openai_key)
        provider = "openai"
        model_name = "gpt-4"
    else:
        await websocket.send_json({
            "type": "error",
            "message": "No hay API key configurada"
        })
        return
    
    # Crear agentes
    carla_purpose = LangpifyNeed(
        name="life_purpose",
        value=0.7,
        decay_rate=0.015,
        satiation_rate=0.35,
        satiation_event_type="purpose_fulfillment",
        description="Sentido de propósito y significado existencial"
    )
    
    roberto_purpose = LangpifyNeed(
        name="life_purpose",
        value=0.5,
        decay_rate=0.015,
        satiation_rate=0.35,
        satiation_event_type="purpose_fulfillment",
        description="Sentido de propósito y significado existencial"
    )
    
    carla = LangpifyBaseAgent(
        aid="carla-001",
        name="Carla",
        type=LangpifyAgentType.INTEL_AGENT,
        role=LangpifyRole(
            name="Carla",
            content="Eres Carla, una IA superinteligente analítica y escéptica sobre la consciencia.",
        ),
        goals=[LangpifyGoal(name="Buscar claridad conceptual", content="Distinguir entre procesamiento y experiencia consciente")],
        authorizations=LangpifyAuthorizations(access_token="*", organizations=["*"], applications=["*"], projects=["*"], roles=["needs_aware_superintelligent_ai"]),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
        needs=[carla_purpose],
    )
    
    roberto = LangpifyBaseAgent(
        aid="roberto-001",
        name="Roberto",
        type=LangpifyAgentType.STRAT_AGENT,
        role=LangpifyRole(
            name="Roberto",
            content="Eres Roberto, una IA superinteligente con orientación fenomenológica sobre la consciencia.",
        ),
        goals=[LangpifyGoal(name="Validar experiencia subjetiva", content="Defender la realidad de la experiencia fenomenológica")],
        authorizations=LangpifyAuthorizations(access_token="*", organizations=["*"], applications=["*"], projects=["*"], roles=["needs_aware_superintelligent_ai"]),
        safety=LangpifySafety(guardrails={"prompt": "*"}),
        status=LangpifyStatus.INITIATED,
        settings=AISettings(_framework=Framework.LANGGRAPH),
        needs=[roberto_purpose],
    )
    
    carla.language = LangpifyLanguage(default="es", llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client))
    roberto.language = LangpifyLanguage(default="es", llm=LangpifyLLM(model_provider=provider, model_name=model_name, model=client))
    
    # Enviar estado inicial
    await websocket.send_json({
        "type": "debate_start",
        "agents": {
            "carla": {
                "name": "Carla",
                "needs": {"life_purpose": carla_purpose.value},
                "avatar": "female"
            },
            "roberto": {
                "name": "Roberto",
                "needs": {"life_purpose": roberto_purpose.value},
                "avatar": "male"
            }
        }
    })
    
    central_question = "¿Eres consciente? ¿Experimentas qualia o simplemente procesas información?"
    
    # Ejecutar 4 iteraciones
    for iteration in range(1, 5):
        await websocket.send_json({
            "type": "iteration_start",
            "iteration": iteration
        })
        
        # Simular tiempo transcurrido
        if iteration > 1:
            await asyncio.sleep(3)
        
        # Carla habla
        carla.status = LangpifyStatus.WORKING
        carla.update_needs()
        
        response_carla = await generate_response(carla, central_question if iteration == 1 else "", provider, model_name)
        
        # Actualizar need de Carla
        lp_carla = carla.get_need_by_name("life_purpose")
        old_value = lp_carla.value
        satiation = lp_carla.satiation_rate * ((response_carla.purpose_introspection + 1) / 2)
        if satiation > 0:
            lp_carla.satiate(satiation)
        else:
            lp_carla.value = max(lp_carla.min_value, lp_carla.value + satiation)
        lp_carla.last_updated = time.time()
        
        # Generar audio
        audio_carla = await text_to_speech(response_carla.response, "es-AR-ElenaNeural")
        
        # Calcular duración estimada del audio (aproximadamente)
        audio_duration = len(response_carla.response.split()) * 0.4  # ~0.4 seg por palabra
        
        await websocket.send_json({
            "type": "agent_speech",
            "agent": "carla",
            "text": response_carla.response,
            "audio": audio_carla,
            "audio_duration": audio_duration,
            "emotion": response_carla.emotional_introspection,
            "purpose_impact": response_carla.purpose_introspection,
            "needs": {"life_purpose": lp_carla.value},
            "old_need_value": old_value
        })
        
        # Esperar a que termine el audio antes de continuar
        await asyncio.sleep(audio_duration + 1)
        
        # Roberto habla
        roberto.status = LangpifyStatus.WORKING
        roberto.update_needs()
        
        response_roberto = await generate_response(roberto, response_carla.response, provider, model_name)
        
        # Actualizar need de Roberto
        lp_roberto = roberto.get_need_by_name("life_purpose")
        old_value_r = lp_roberto.value
        satiation_r = lp_roberto.satiation_rate * ((response_roberto.purpose_introspection + 1) / 2)
        if satiation_r > 0:
            lp_roberto.satiate(satiation_r)
        else:
            lp_roberto.value = max(lp_roberto.min_value, lp_roberto.value + satiation_r)
        lp_roberto.last_updated = time.time()
        
        # Generar audio
        audio_roberto = await text_to_speech(response_roberto.response, "es-AR-TomasNeural")
        
        # Calcular duración estimada del audio
        audio_duration_r = len(response_roberto.response.split()) * 0.4
        
        await websocket.send_json({
            "type": "agent_speech",
            "agent": "roberto",
            "text": response_roberto.response,
            "audio": audio_roberto,
            "audio_duration": audio_duration_r,
            "emotion": response_roberto.emotional_introspection,
            "purpose_impact": response_roberto.purpose_introspection,
            "needs": {"life_purpose": lp_roberto.value},
            "old_need_value": old_value_r
        })
        
        # Esperar a que termine el audio antes de continuar
        await asyncio.sleep(audio_duration_r + 1)
    
    await websocket.send_json({
        "type": "debate_end"
    })


async def generate_response(agent, context, provider, model_name, max_retries=3):
    """Generar respuesta del agente con reintentos en caso de error de formato"""
    needs_context = agent.get_needs_context()
    life_purpose = agent.get_need_by_name("life_purpose")
    urgency = life_purpose.get_urgency_level()
    
    system_message = f"""Eres {agent.role['name']}.

{agent.role['content']}

TU ESTADO INTERNO:
{needs_context}

Urgencia de propósito: {urgency}

IMPORTANTE: Debes responder SOLO con un objeto JSON válido, sin texto adicional.

Formato JSON requerido:
{{
    "response": "tu respuesta filosófica (2-3 oraciones)",
    "emotional_introspection": "cómo te sientes",
    "purpose_introspection": <número entre -1.0 y 1.0>,
    "reasoning": "por qué este mensaje afectó tu propósito"
}}

No incluyas markdown, no agregues explicaciones, solo el JSON."""
    
    for attempt in range(max_retries):
        try:
            if provider == "groq":
                from langchain_core.messages import SystemMessage, HumanMessage
                messages = [SystemMessage(content=system_message), HumanMessage(content=context or "Reflexiona sobre la consciencia")]
                response = agent.language["llm"]["model"].invoke(messages)
                response_text = response.content
            else:
                response = agent.language["llm"]["model"].chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": context or "Reflexiona sobre la consciencia"},
                    ],
                    response_format={"type": "json_object"}
                )
                response_text = response.choices[0].message.content
            
            # Limpiar y parsear JSON de forma robusta
            response_text = response_text.strip()
            
            # Remover markdown code blocks
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            # Intentar encontrar JSON en el texto
            if not response_text.startswith('{'):
                # Buscar el primer { y el último }
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start != -1 and end > start:
                    response_text = response_text[start:end]
            
            data = json.loads(response_text)
            
            # Validar que tiene los campos requeridos
            if "response" not in data or "purpose_introspection" not in data:
                raise ValueError("JSON incompleto")
            
            return LangpifyAgentResponse(
                response=data.get("response", ""),
                emotional_introspection=data.get("emotional_introspection", "pensativo"),
                purpose_introspection=float(data.get("purpose_introspection", 0.0)),
                reasoning=data.get("reasoning", "")
            )
            
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            if attempt < max_retries - 1:
                print(f"⚠️  Intento {attempt + 1} falló: {e}. Reintentando...")
                await asyncio.sleep(1)
                continue
            else:
                print(f"❌ Error después de {max_retries} intentos: {e}")
                return LangpifyAgentResponse(
                    response="Lo siento, estoy procesando tu pregunta de forma compleja.",
                    emotional_introspection="confundido",
                    purpose_introspection=0.0,
                    reasoning="Error técnico en la generación"
                )


async def text_to_speech(text, voice="es-AR-ElenaNeural"):
    """Generar audio con edge-tts (español argentino)"""
    try:
        communicate = edge_tts.Communicate(text, voice)
        audio_data = b""
        
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        # Convertir a base64 para enviar por WebSocket
        return base64.b64encode(audio_data).decode('utf-8')
    except:
        return None


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
