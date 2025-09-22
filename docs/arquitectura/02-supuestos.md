# Supuestos y Restricciones

## Supuestos

### Arquitectura
- **S1**: La arquitectura server-side es más escalable y controlable que ejecutar análisis directamente en las máquinas de los desarrolladores.
- **S2**: Separar la lógica de análisis del pre-commit hook permite mejor control, auditoría y evolución del sistema.
- **S3**: Un orquestador centralizado es necesario para manejar eficientemente el análisis paralelo de múltiples vulnerabilidades OWASP.
- **S4**: La base de conocimiento con documentación OWASP/CWE mejora significativamente la precisión del análisis.

### Modelos
- **S5**: Los modelos locales (Gemma via Ollama) son suficientes para probar el flujo de trabajo del MVP, pero la migración a modelos más potentes (Claude 4 Sonnet/GPT-5) es necesaria para producción.
- **S6**: El análisis paralelo de cada vulnerabilidad OWASP seguido de integración de resultados puede ser más preciso que un análisis monolítico.
- **S7**: Los prompts especializados por tipo de vulnerabilidad pueden dar mejores resultados que prompts genéricos.

### Rendimiento
- **S8**: Implementar caché podría evitar re-análisis innecesarios y mejorar significativamente los tiempos de respuesta.
- **S9**: Un servicio de colas puede permitir manejar picos de commits sin degradar la experiencia del desarrollador.
- **S10**: El tiempo de inferencia es el principal cuello de botella del sistema.

### Integración
- **S11**: Mantener un registro de commits evaluados permite integración futura con CI/CD sin mayor complejidad.
- **S12**: La validación de integridad (commit evaluado vs commit pusheado) es crítica para la confianza del sistema.

## Restricciones

### Retos Técnicos
- **R1**: Commits grandes: El sistema debe manejar commits que excedan los límites de contexto del modelo, posiblemente requiriendo segmentación inteligente.
- **R2**: Commits pequeños: Cambios mínimos pueden carecer de contexto suficiente para análisis efectivo de vulnerabilidades.
- **R3**: Lenguajes no soportados: El modelo puede no reconocer o analizar adecuadamente ciertos lenguajes de programación.
- **R4**: Fricción en desarrollo: El tiempo de análisis no puede ser tan largo que afecte negativamente la velocidad de desarrollo.

### Arquitectura
- **R5**: Se necesitan dos endpoints: uno para análisis en tiempo real y otro para validación en CI.
- **R6**: La autenticación OAuth (Auth0) es mandatoria para identificar usuarios y proteger APIs.
- **R7**: Base de datos relacional es requerida para tracking de estados, hashes y metadatos de commits.

### Stack Tecnológico
- **R8**: Python + FastAPI + LangGraph como stack principal.
- **R9**: SQLite para MVP local, con migración planificada a PostgreSQL/DynamoDB en nube.
- **R10**: Pre-commit hook debe usar la librería oficial de Python para máxima compatibilidad.
- **R11**: Arquitectura hexagonal/limpia para facilitar mantenimiento y evolución.

### Seguridad y Privacidad
- **R12**: Almacenar información del usuario en la base de datos requiere evaluación cuidadosa de privacidad y seguridad.
- **R13**: Notificaciones por violaciones de integridad deben implementarse como alertas de seguridad críticas.

### Evolución del Sistema
- **R14**: El diseño debe permitir evolución de Ollama local a servicios cloud sin refactoring mayor.
- **R15**: La integración con CI debe ser contemplada desde el diseño inicial, aunque no se implemente en MVP.
- **R16**: El sistema debe diseñarse para ser agnóstico al proveedor de nube (AWS/otros).

### Limitaciones del MVP
- **R17**: Enfoque inicial en 3 vulnerabilidades OWASP específicas para validar el concepto.
- **R18**: Sin implementación de escalabilidad real, pero diseño debe contemplarla.
- **R19**: Monitoreo básico únicamente, sin dashboards completos de analytics.