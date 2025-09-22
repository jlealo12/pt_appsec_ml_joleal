# Brief de Arquitectura

## Contexto
### Descripción del problema
Se requiere una herramienta que permita analizar código contra el top 10 de vulnerabilidades de la OWASP, diagnosticar posibles vulnerabilidades y sugerir correcciones, todo esto de manera automática al momento de hacer un commit en un repositorio git.

### Usuarios principales
- Desarrolladores de software: tendrán una herramienta integrada a su flujo de trabajo para asegurar la calidad y seguridad de su código.
- Equipo AppSec: podrá estandarizar y automatizar la revisión de seguridad de código, reduciendo la exposición a riesgo del negocio. El equipo también podrá monitorear y auditar las prácticas de desarrollo para identificar áreas de mejora, proponer nuevas soluciones, y capacitar a los desarrolladores en la áreas de mejora.

### Motivación de negocio
- Mejorar la seguridad del código fuente
- Reducir riesgos de vulnerabilidades en producción 
- Facilitar la detección temprana de problemas de seguridad durante el ciclo de desarrollo

## Objetivos
- Configurar un sistema de IA para analizar código en busca de vulnerabilidades OWASP Top 10.
- Integrar el análisis en el flujo de trabajo de Git mediante pre-commit hooks.

## Fuera de Alcance
- Se va a diseñar el sistema para que pueda ser escalable, pero no se va a implementar la escalabilidad en esta etapa.
- No se va a implementar un sistema de CI/CD completo, pero se va a diseñar la solución para que pueda integrarse con CI/CD en el futuro.
- No se va a implementar un sistema de monitoreo completo, pero se espera generar un tablero de muestra.
- No se va a implementar el sistema de alertamiento completo.
- Se va a diseñar la arquitectura de nube, pero se va apriorizar la implementación en local.

## Métricas de Éxito
- Precisión en la detección de vulnerabilidades (mínimo 80% en la identificación)
- Precisión en la sugerencia de correcciones (mínimo 70% en la utilidad de las sugerencias, pendiente validar cómo se medirá)
- Tiempo de respuesta (análisis en menos de 30 segundos por commit)