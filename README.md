# Langpify

## Entidades Clave
- **Agentes**: Son entidades autónomas que procesan mensajes, toman decisiones y pueden interactuar entre sí y con herramientas. Cada agente sigue abstracciones de alto nivel inspiradas en FIPA y puede ser registrado en protocolos modernos como MCP, ACP y A2A.
- **Herramientas (Tools)**: Funcionalidades externas que los agentes pueden invocar (por ejemplo, búsqueda médica). Gestionadas por el Tool Management Service (TMS).
- **Servicios**: Incluyen el Agent Management Service (AMS), inspirado en FIPA, para gestión de ciclo de vida de agentes, y el TMS para herramientas. Ambos exponen métodos de alto nivel y están inspirados en especificaciones FIPA.
- **Eventos**: Representan cambios de estado en los agentes o en el sistema. Los eventos permiten que los agentes se adapten y reaccionen ante nuevas condiciones internas o externas, facilitando la comunicación y coordinación basada en eventos entre agentes y otros componentes del sistema.

## Abstracción y Reusabilidad
El sistema implementa un meta-framework agnóstico a frameworks y modelos, agregando protocolos antiguos y modernos bajo un mismo esquema. Esto permite interoperabilidad y reusabilidad: identificamos las características comunes entre tecnologías y las abstraemos en interfaces y contratos de dominio. Así, cada componente puede ser reemplazado o extendido sin afectar el núcleo de negocio.

## Clase Base de Agentes
La clase base de agentes está inspirada en el trabajo científico [AopifyJs](https://link.springer.com/chapter/10.1007/978-3-030-20454-9_52), que buscaba estandarizar el desarrollo de agentes inteligentes a través del protocolo FIPA, métodos altamente declarativos y explicativos inspirados en las ciencias cognitivas y abstracciones de alto nivel para la toma de decisiones. En este proyecto, la clase fue renombrada a **LangpifyBaseAgent** para reflejar su actualización al ecosistema moderno de LLMs y nuevos protocolos (MCP, A2A, ACP). Esta clase define atributos y métodos clave para la identidad, ciclo de vida, comunicación y descubrimiento de agentes.

El desarrollo agencial moderno enfrenta una fragmentación acelerada: múltiples frameworks, modelos y proveedores, cada uno con sus propias abstracciones y dependencias. Esto genera alta curva de aprendizaje, baja interoperabilidad y riesgo de obsolescencia tecnológica. Langpify surge como respuesta a este contexto, proponiendo un meta-framework que actúa como agregador de protocolos, frameworks, modelos y proveedores, permitiendo el desarrollo de agentes verdaderamente adaptativos y reutilizables.

### ¿Por qué Langpify?

- **Interoperabilidad por diseño**  
  Langpify abstrae las capacidades clave de los agentes (comunicación, adaptación, percepción) en métodos de alto nivel y funciones agnosticas de cualquier framework o modelo de lenguaje. Así, es posible cambiar de stack tecnológico (por ejemplo, de LangChain a LlamaIndex) sin reescribir la lógica agencial.

- **Diseño modular y extensible**  
  Separa explícitamente necesidades, deseos, objetivos y roles de la ingeniería de prompts, permitiendo modularizar y refinar cada parte de manera independiente. Esto facilita la escalabilidad y la adaptación ante nuevos requerimientos cambiantes, además de habilitar la generación y gestión de prompts dinámicos. Langpify incorpora el concepto de Prompt Dinámico del protocolo MCP, permitiendo que los agentes construyan y ajusten sus prompts en tiempo real según el contexto y las necesidades de la conversación o tarea.

- **Compatibilidad con estándares legacy y emergentes**  
  Langpify integra protocolos clásicos como FIPA y modernos como MCP, A2A y ACP, sirviendo de puente entre la IA simbólica tradicional y los agentes impulsados por LLMs. Esto permite migraciones graduales y protege la inversión en soluciones existentes.

- **Transparencia y explicabilidad**  
  Los métodos y atributos de los agentes usan nombres inspirados en procesos mentales básicos (communicate, sense, adapt), facilitando la comprensión y el mantenimiento por equipos multidisciplinarios. La intención del agente es clara y explícita, promoviendo el desarrollo agencial como pseudo-código.

  **Principales métodos y atributos de LangpifyBaseAgent agrupados por procesos mentales:**

  - **Identidad**
    - `aid`: Identificador único del agente
    - `role`: Rol del agente
    - `agent_card`: Tarjeta de agente para descubrimiento (A2A)
    - `config`: Configuración general del agente -> si no se especifica toma ai_settings globales

  - **Ciclo de vida**
    - `status`: Estado del ciclo de vida (INITIATED, ACTIVE, SUSPENDED, etc -> Basado en FIPA Y ACP)
    - `suspend()`: Suspende temporalmente el agente
    - `resume()`: Reactiva el agente suspendido
    - `register()`: Expone el agente como servicio A2A

  - **Percepción**
    - `sense(key: str)`: Consulta el estado interno del agente

  - **Atención y Memoria**
    - Uso de `MemorySaver` para persistencia de memoria conversacional
    - Variables internas relacionadas con el estado y memoria

  - **Motivación**
    - `goals`: Lista de metas u objetivos del agente

  - **Lenguaje**
    - `language`: Contiene LLM independientemente del modelo y proveedor elegido

  - **Planificación**
    - `workflow`: Workflows y grafos

  - **Comunicación**
    // Soporte para comunicación asincronica, streaming y eventos:
    - `emit(event_type: str, data: Dict[str, Any] = None)`: Emite eventos
    - `on(event_type: str, callback: Callable)`: Registra listeners para eventos
    - `off(event_type: str, callback: Callable)`: Elimina listeners
    - `on_any(callback: Callable)`: Listener para cualquier evento
    - `off_any(callback: Callable)`: Elimina listeners globales
    - `subscribe_to(agent)`: Suscribirse a eventos de otro agente
    - `unsubscribe_from(agent)`: Cancelar suscripción
    - `_handle_external_event(event)`: Manejar eventos externos
    // Soporte para comunicación sincronica:
    - `communicate(prompt: str)`: Procesa mensajes y genera respuestas


Langpify no es solo un framework, sino una plataforma conceptual y técnica que promueve la interoperabilidad, la adaptabilidad y la sostenibilidad en el desarrollo de agentes inteligentes. Permite construir sistemas robustos y evolutivos, preparados para integrar nuevas tecnologías y protocolos sin sacrificar claridad ni control.




## Instalación

```bash
pip install langpify
```

O usando Poetry:

```bash
poetry add langpify
```

## Uso

```python
from langpify import example

# Ejemplo básico
result = example.hello_world()
print(result)  # Imprime: "Hello, World!"
```

## Desarrollo

### Configuración del entorno de desarrollo

1. Clona el repositorio:
```bash
git clone https://github.com/yourusername/langpify.git
cd langpify
```

2. Instala Poetry (si aún no lo tienes):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. Instala las dependencias:
```bash
poetry install
```

### Ejecutar tests

```bash
poetry run pytest
```

### Verificar estilo de código

```bash
poetry run black .
poetry run isort .
poetry run flake8 .
poetry run mypy .
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.
