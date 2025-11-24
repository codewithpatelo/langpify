# 🎮 Langpify Sims UI - Interfaz Gráfica para Debate de Consciencia

Interfaz gráfica inspirada en **Los Sims 4** para visualizar debates filosóficos entre agentes de IA con sistema de necesidades homeostáticas.

## ✨ Características

- 🎨 **Diseño estilo Los Sims** con colores característicos y barras de necesidades
- 🗣️ **Text-to-Speech** en español argentino usando Edge-TTS (Microsoft)
- 🎭 **Avatares animados** con estados (idle, hablando)
- 📊 **Visualización de necesidades** en tiempo real (estilo plumbob)
- 🔄 **WebSockets** para comunicación en tiempo real
- 📝 **Timeline** de eventos del debate
- 💬 **Speech bubbles** con emociones

## 🚀 Instalación

### 1. Instalar dependencias adicionales

```bash
cd tests/ui
pip install -r requirements.txt
```

O con Poetry (desde la raíz del proyecto):

```bash
poetry add fastapi uvicorn websockets edge-tts python-multipart
```

### 2. Configurar API Keys

Necesitas al menos una de estas API keys:

**Opción 1: Groq (Recomendado - Gratis)**
```bash
export GROQ_API_KEY="tu-groq-api-key"
```

**Opción 2: OpenAI**
```bash
export OPENAI_API_KEY="tu-openai-api-key"
```

## 🎯 Uso

### Iniciar el servidor

```bash
cd tests/ui
python app.py
```

O con uvicorn directamente:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### Abrir en el navegador

Abre tu navegador en:

```
http://localhost:8000
```

### Controles

1. Click en **▶ Iniciar Debate** para comenzar
2. Observa cómo los agentes debaten en tiempo real
3. Las barras de necesidades se actualizan dinámicamente
4. El audio se reproduce automáticamente (español argentino)

## 🎨 Estructura de la UI

```
tests/ui/
├── app.py                  # Backend FastAPI con WebSockets
├── templates/
│   └── index.html         # HTML principal
├── static/
│   ├── css/
│   │   └── sims-style.css # Estilos Los Sims
│   └── js/
│       └── sims-ui.js     # Lógica JavaScript
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🎤 Text-to-Speech

Voces utilizadas (Edge-TTS de Microsoft):

- **Carla**: `es-AR-ElenaNeural` (Femenina, Argentina)
- **Roberto**: `es-AR-TomasNeural` (Masculino, Argentina)

Estas voces son **gratuitas** y de alta calidad.

## 🎮 Inspiración Los Sims

La interfaz está inspirada en:

- **Colores**: Verde azulado (#00D4AA), azul (#0095DD)
- **Barras de necesidades**: Estilo Sims 4 con gradientes
- **Indicadores visuales**: Plumbob-style para estados
- **Animaciones**: Flotantes y pulsantes
- **Typography**: Poppins (similar a Sims)

## 📊 Visualización de Necesidades

Cada agente tiene una barra de **"Propósito de Vida"** que:

- ⬇️ **Decae** con el tiempo (1.5% por segundo)
- ⬆️ **Se sacia** cuando el debate es significativo
- 🎨 **Cambia de color** según el nivel:
  - Rojo: < 20% (crítico)
  - Naranja: 20-40% (bajo)
  - Amarillo: 40-60% (medio)
  - Verde claro: 60-80% (alto)
  - Verde: > 80% (completo)

## 🔧 Tecnologías

- **Backend**: FastAPI + WebSockets
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **TTS**: Edge-TTS (Microsoft)
- **LLM**: Groq (Llama 3.1) o OpenAI (GPT-4)
- **3D** (opcional futuro): Three.js + Ready Player Me

## 🎯 Próximas Mejoras

- [ ] Avatares 3D con Ready Player Me
- [ ] Más tipos de necesidades (social, curiosidad, etc.)
- [ ] Controles de velocidad del debate
- [ ] Grabación del debate
- [ ] Exportar transcript
- [ ] Modo oscuro/claro
- [ ] Personalización de agentes

## 🐛 Troubleshooting

**Error: No hay API key configurada**
- Asegúrate de tener `GROQ_API_KEY` o `OPENAI_API_KEY` en tus variables de entorno

**El audio no se reproduce**
- Verifica que edge-tts esté instalado correctamente
- Algunos navegadores requieren interacción del usuario antes de reproducir audio

**WebSocket se desconecta**
- Verifica que el servidor FastAPI esté corriendo
- Revisa la consola del navegador para errores

## 📝 Licencia

Parte del proyecto Langpify - MIT License

## 🙌 Créditos

Diseñado e inspirado en Los Sims™ (EA Games)
Desarrollado con ❤️ para Langpify
