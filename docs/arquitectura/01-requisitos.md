# Requisitos

## Funcionales

### Análisis de Código
- **RF1**: El sistema debe analizar automáticamente el código fuente modificado en cada commit para detectar vulnerabilidades del OWASP Top 10 2021.
- **RF2**: El sistema debe detectar mínimo 3 tipos de vulnerabilidades del OWASP Top 10 (ej: SQLi, XSS, SSRF).
- **RF3**: El sistema debe rechazar commits que contengan vulnerabilidades identificadas y proporcionar explicación clara del problema junto con sugerencias de corrección.
- **RF4**: El sistema debe aprobar commits sin vulnerabilidades detectadas.

### Autenticación e Integridad
- **RF5**: El sistema debe autenticar al usuario que realiza el commit utilizando OAuth 2.0 (Auth0 como servicio de autenticación).
- **RF6**: El sistema debe identificar exactamente qué usuario está realizando cada commit.
- **RF7**: El sistema debe verificar la integridad de los commits, validando que los fragmentos de código analizados corresponden exactamente a los commits incluidos en el push al servidor remoto.
- **RF8**: El sistema debe mantener un registro de commits evaluados con sus hashes/IDs para posterior verificación en CI.

### Integración y Workflow
- **RF9**: El sistema debe integrarse con Git mediante pre-commit hooks que se ejecuten automáticamente.
- **RF10**: El sistema debe ejecutar el análisis server-side mediante APIs protegidas.
- **RF11**: El sistema debe proporcionar un endpoint para que CI pueda validar que un commit fue previamente evaluado.

### Procesamiento y Orquestación
- **RF12**: El sistema debe manejar commits de diferentes tamaños (grandes y pequeños).
- **RF13**: El sistema debe soportar múltiples lenguajes de programación.
- **RF14**: El sistema debe ejecutar análisis en paralelo para evaluar cada vulnerabilidad del OWASP Top 10.
- **RF15**: El sistema debe integrar los resultados de análisis paralelos en una respuesta unificada.

## No Funcionales

### Rendimiento
- **RNF1**: El tiempo de análisis por commit debe ser menor a 30 segundos.
- **RNF2**: El sistema debe manejar múltiples commits concurrentes utilizando un servicio de colas.
- **RNF3**: El sistema debe implementar caché para evitar re-análisis de commits idénticos.

### Seguridad
- **RNF4**: El sistema debe implementar medidas anti prompt-injection en la comunicación con el LLM.
- **RNF5**: Todas las APIs deben estar protegidas con autenticación OAuth 2.0.
- **RNF6**: El sistema debe generar alertas de seguridad cuando se detecten intentos de evasión del control de pre-commit.
- **RNF7**: El sistema debe manejar de forma segura los tokens de autenticación y datos sensibles.

### Disponibilidad y Confiabilidad
- **RNF8**: El sistema debe ser escalable para manejar múltiples repositorios y desarrolladores.
- **RNF9**: El sistema debe mantener logs de auditoría de todos los análisis realizados.

### Precisión
- **RNF10**: El sistema debe alcanzar mínimo 80% de precisión en la detección de vulnerabilidades.
- **RNF11**: Las sugerencias de corrección deben tener mínimo 70% de utilidad práctica.

### Integración
- **RNF12**: El sistema debe estar diseñado para integrarse con sistemas de CI/CD existentes.
- **RNF13**: El sistema debe proporcionar capacidades de monitoreo y métricas para el equipo AppSec.

### Almacenamiento
- **RNF14**: El sistema debe persistir información de commits analizados, estados (aprobado/rechazado), análisis realizados y metadatos relevantes en base de datos relacional.
- **RNF15**: El sistema debe implementar estrategias de retención de datos apropiadas para compliance y auditoría.

# Alcance MVP

## Requisitos funcionales

Todos menos RF7 (en servidor remoto) y RF11 (No se construye el pipeline de CI).

## Requisitos no funcionales
Todos menos RNF6, RNF8 (No se implementa escalabilidad en esta etapa), RNF12 (No se integra con CI/CD en esta etapa), RNF13 (solo se da una muestra de monitoreo), RNF15.