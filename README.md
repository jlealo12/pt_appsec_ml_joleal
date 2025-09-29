# AppSec GenAI - Evaluador de Vulnerabilidades OWASP

## Resumen del Reto

El desafío consiste en desarrollar una herramienta que permita evaluar código fuente contra el Top 10 de vulnerabilidades de OWASP utilizando modelos de lenguaje e inteligencia artificial. La herramienta debe ser capaz de:

- Diagnosticar vulnerabilidades de forma autónoma
- Sugerir correcciones automáticas
- Integrarse en el flujo de desarrollo mediante pre-commit hooks
- Proporcionar capacidades de auditoría para el equipo de AppSec

### Usuarios Objetivo

- **Desarrolladores**: Usuarios principales que consumen la herramienta en su ciclo de desarrollo
- **Equipo de AppSec**: Administradores que monitorean y auditan las evaluaciones, identificando patrones de vulnerabilidades y métricas de corrección

### Objetivos de Negocio

- Mejorar la seguridad del código fuente
- Reducir vulnerabilidades que lleguen a producción
- Facilitar la detección temprana de problemas de seguridad

## Solución Propuesta

### Arquitectura del Sistema

La solución implementa un flujo cliente-servidor con los siguientes componentes:

1. **Cliente (Pre-commit Hook)**
   - Intercepta los commits en el repositorio local
   - Valida la autenticación del usuario
   - Envía los cambios (diff) a la API de evaluación
   - Procesa la respuesta y bloquea/permite el commit

2. **Servidor de Autenticación (Auth0)**
   - Implementa OAuth 2.0 con flujo PKCE
   - Genera y valida tokens JWT
   - Gestiona credenciales de usuario

3. **API de Evaluación**
   - Valida tokens JWT
   - Orquesta la evaluación en paralelo contra múltiples vulnerabilidades OWASP
   - Implementa un agente por cada tipo de vulnerabilidad
   - Agrega resultados y responde al cliente

### Flujo de Trabajo

```
Usuario → Cambios en Git → Pre-commit Hook → Validación de Auth
                                ↓
                         API de Evaluación → Modelos de IA (paralelo)
                                ↓
                    Resultados agregados → Decisión (aprobar/rechazar)
```

## Stack Tecnológico

- **Lenguaje**: Python
- **Framework Web**: FastAPI con Pydantic para validaciones
- **Framework de Agentes**: Strands Agents (AWS)
- **Proveedor LLM**: OpenAI
- **Autenticación**: JWT con Auth0 (OAuth 2.0 + PKCE)
- **Pre-commit**: Framework pre-commit

### Estructura del Proyecto

El desarrollo se organizó en 3 repositorios:

1. **API**: Servidor de evaluación con agentes [pt_appsec_ml_joleal](https://github.com/jlealo12/pt_appsec_ml_joleal)
2. **Hook**: Librería de pre-commit para clientes [pt_appsec_ml_hook](https://github.com/jlealo12/pt_appsec_ml_hook)
3. **Test Repo**: Repositorio de validación de la implementación [pt_appsec_ml_joleal_validation](https://github.com/jlealo12/pt_appsec_ml_joleal_validation)

#### Estructura de respositorios
~~~bash
.
├── pt_appsec_ml_joleal
│   ├── docs
│   │   ├── arquitectura
│   │   │   ├── 00-brief.md
│   │   │   ├── 01-requisitos.md
│   │   │   ├── 02-supuestos.md
│   │   │   └── 03-diagramas.md
│   │   └── diagramas
│   │       └── diagramas_pt_appsec.drawio
│   ├── main.py
│   ├── Makefile
│   ├── pyproject.toml
│   ├── README.md
│   ├── scripts
│   │   ├── agent_prompts
│   │   │   ├── A01_BAC.md
│   │   │   ├── A02_CF.md
│   │   │   └── A03_Injection.md
│   │   ├── connect_to_auth0.py
│   │   ├── oauth_login.py
│   │   ├── ollama_agent_base.py
│   │   ├── openai_base_agent.py
│   │   ├── openai_owasp_agent.py
│   │   ├── openai_owasp_single_agent.py
│   │   └── openai_structured_output_agent.py
│   ├── src
│   │   ├── agent.py
│   │   ├── app.py
│   │   ├── auth_utils.py
│   │   ├── config.py
│   │   ├── configs
│   │   │   └── configs.json
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── prompts
│   │   │   ├── A01_BAC.md
│   │   │   ├── A02_CF.md
│   │   │   └── A03_Injection.md
│   │   ├── utils.py
│   │   └── workflow.py
│   ├── tests
│   └── uv.lock
├── pt_appsec_ml_hook
│   ├── hooks
│   │   ├── auth_manager.py
│   │   ├── hook.py
│   │   ├── __init__.py
│   │   └── oauth_login.py
│   ├── Makefile
│   ├── pyproject.toml
│   ├── README.md
│   └── uv.lock
└── pt_appsec_ml_joleal_validation
    ├── main.py
    ├── Makefile
    ├── pyproject.toml
    ├── README.md
    ├── test-pre-commit.py
    └── uv.lock
~~~

## Documentación técnica de la prueba

[Documentación](docs/)

## Estado de Implementación

### Funcionalidades Completadas

✅ API funcional que evalúa código contra las 3 primeras vulnerabilidades OWASP  
✅ Endpoint `/evaluate` para análisis de fragmentos de código  
✅ Ruta `/validate` preparada (sin implementación completa)  
✅ Pre-commit hook configurado con ciclo de autenticación  
✅ Flujo completo de autenticación OAuth 2.0 con PKCE  
✅ Almacenamiento de credenciales en archivo JSON local  
✅ Validaciones funcionales básicas del sistema

### Pendientes

❌ Implementación completa del endpoint `/validate` para commits  
❌ Tabla de auditoría para registro de validaciones  
❌ Integración con guardrails para protección contra prompt injection  
❌ Sistema de caché basado en hash de commits  
❌ Pruebas de performance y estrés  
❌ Evaluación de los 10 riesgos completos de OWASP  
❌ Despliegue en nube y análisis de costos

## Observaciones Críticas

### 1. Latencia y Experiencia de Usuario

⚠️ **Desafío Principal**: Los modelos de lenguaje tienen latencias naturalmente altas (varios segundos), lo que puede afectar negativamente la experiencia de desarrollo si se implementa como bloqueante en pre-commit.

**Recomendación**: Considerar mover la validación bloqueante al pipeline de CI/CD en lugar del pre-commit, permitiendo que los desarrolladores validen opcionalmente en local.

### 2. Vulnerabilidades de Seguridad

#### Prompt Injection

🔴 **Crítico**: El sistema es susceptible a ataques de prompt injection. Ejemplos detectados:

- Uso de secuencias de cierre para engañar al modelo
- Instrucciones que hacen pasar código malicioso como ejemplos
- Ejemplo: `print("Hello World")` puede ser inyectado como código válido

**Necesidades**:
- Implementación de guardrails
- Sanitización de inputs
- Validación de tags y caracteres especiales (con cuidado de no afectar código legítimo como XML/Markdown)

#### Gestión de Prompts

Los prompts deben:
- Almacenarse fuera del código (S3 con KMS, Secrets Manager, Parameter Store)
- No ser accesibles por el cliente
- Estar protegidos contra extracción mediante prompt hacking

### 3. Escalabilidad

**Desafíos identificados**:
- 10 peticiones paralelas por commit (una por vulnerabilidad OWASP)
- Multiplicado por el número de desarrolladores activos
- Sin sistema de caché implementado

**Soluciones propuestas**:
- Sistema de caché basado en hash de commits
- Evaluación incremental (solo código modificado)
- Optimización de modelos y proveedores

### 4. Limitaciones de los Modelos

- **Alucinaciones**: Los modelos pueden generar falsos positivos/negativos
- **Calidad variable**: Dependiendo del tipo de código y vulnerabilidad
- **Costo**: El uso intensivo de APIs de OpenAI puede ser costoso a escala

## Trabajo Futuro Recomendado

### Prioridad Alta

1. **Implementar guardrails** para protección contra prompt injection
2. **Sistema de caché** para optimizar performance
3. **Tabla de auditoría** con registro de todas las validaciones
4. **Definir llave de integridad** (hash de commit recomendado)

### Prioridad Media

5. Completar evaluación de las 10 vulnerabilidades OWASP
6. Pruebas de performance y benchmarking
7. Comparación de modelos y proveedores
8. Refinamiento de prompts basado en evaluaciones

### Prioridad Baja

9. Fine-tuning de modelos para casos específicos
10. Integración con herramientas empresariales existentes
11. Dashboard de analítica para AppSec
12. Despliegue en nube con análisis de costos

## Notas Importantes

- El Top 10 de OWASP son recomendaciones mínimas, no un programa completo de seguridad
- Se recomienda alinear las evaluaciones con el programa de AppSec específico de la organización
- La validación opcional en local + bloqueante en CI/CD ofrece mejor balance entre seguridad y experiencia de desarrollo
