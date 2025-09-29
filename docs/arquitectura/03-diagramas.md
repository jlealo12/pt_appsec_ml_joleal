# Documentación del proceso de autenticación

~~~mermaid

sequenceDiagram
    participant Dev as Desarrollador
    participant Script as Script de Auth
    participant Server as Servidor Local
    participant Browser as Navegador
    participant Auth0 as Auth0
    participant API as API Protegida

    Note over Dev,API: Flujo inicial de autenticación (una vez por desarrollador)
    
    Dev->>Script: Ejecuta comando de login
    
    Note over Script: Paso 1: Generar PKCE
    Script->>Script: Genera code_verifier (random)
    Script->>Script: Genera code_challenge (SHA256)
    
    Note over Script: Paso 2: Preparar servidor local
    Script->>Server: Inicializa servidor HTTP en puerto libre
    Server-->>Script: Puerto asignado (ej: 8080)
    
    Note over Script: Paso 3: Construir URL de autorización
    Script->>Script: Construye URL con parámetros:<br/>- response_type=code<br/>- client_id<br/>- redirect_uri=localhost:8080<br/>- code_challenge<br/>- scope=openid offline_access<br/>- state (random)
    
    Note over Script: Paso 4: Abrir navegador
    Script->>Browser: Abre URL de Auth0
    Script->>Dev: "Navegador abierto, complete la autenticación..."
    
    Note over Browser,Auth0: Paso 5: Autenticación del usuario
    Browser->>Auth0: GET /authorize (con parámetros)
    Auth0-->>Browser: Pantalla de login
    Dev->>Browser: Ingresa credenciales
    Browser->>Auth0: POST credenciales
    Auth0-->>Browser: Validación exitosa
    
    Note over Auth0,Server: Paso 6: Callback con código
    Auth0->>Server: GET /callback?code=ABC123&state=XYZ
    Server->>Script: Notifica código recibido
    Server-->>Auth0: HTTP 200 (página de éxito)
    
    Note over Script: Paso 7: Validar state
    Script->>Script: Verifica state parameter
    
    Note over Script,Auth0: Paso 8: Intercambio código por tokens
    Script->>Auth0: POST /oauth/token<br/>- grant_type=authorization_code<br/>- client_id<br/>- code=ABC123<br/>- code_verifier<br/>- redirect_uri
    Auth0-->>Script: access_token, refresh_token, expires_in
    
    Note over Script: Paso 9: Almacenar tokens
    Script->>Script: Guarda refresh_token en ~/.config/app/
    Script->>Script: Calcula timestamp de expiración
    
    Note over Script: Paso 10: Cleanup
    Script->>Server: Detiene servidor local
    Script->>Browser: Cierra pestaña (opcional)
    Script->>Dev: "✓ Autenticación exitosa"
    
    Note over Script,API: Paso 11: Prueba inicial
    Script->>API: GET /endpoint (Authorization: Bearer access_token)
    API-->>Script: HTTP 200 (conexión exitosa)
    Script->>Dev: "✓ Conexión con API confirmada"
~~~