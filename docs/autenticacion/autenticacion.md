# Documentación del proceso de autenticación

## Flujo inicial de autenticación (OAuth2.0 + PKCE)

### **Paso 1: Generar Code Verifier y Code Challenge**
- Crear un string aleatorio de 43-128 caracteres (code verifier)
- Generar el code challenge aplicando SHA256 al verifier y codificándolo en base64url
- Guardar temporalmente el code verifier para usarlo después

### **Paso 2: Construir la URL de autorización**
Crear una URL hacia Auth0 con estos parámetros:
- `response_type=code`
- `client_id=tu_client_id`
- `redirect_uri=http://localhost:puerto` (puerto libre en la máquina local)
- `scope=openid profile offline_access` (incluyendo offline_access para obtener refresh token)
- `code_challenge=el_code_challenge_generado`
- `code_challenge_method=S256`
- `state=valor_aleatorio_para_seguridad`

### **Paso 3: Iniciar servidor local temporal**
- Crear un servidor HTTP simple en localhost (puerto dinámico)
- Este servidor escuchará el callback de Auth0
- Debe manejar la ruta configurada como redirect_uri

### **Paso 4: Abrir navegador**
- Abrir automáticamente el navegador del usuario con la URL de autorización
- El usuario verá la pantalla de login de Auth0
- Tras autenticarse, Auth0 redirigirá a tu servidor local

### **Paso 5: Recibir el código de autorización**
Tu servidor local recibirá una petición GET con:
- `code=codigo_de_autorizacion` (lo que necesitas)
- `state=valor_que_enviaste` (verificar que coincida)
- Si hay error: `error=descripcion_del_error`

### **Paso 6: Intercambiar código por tokens**
Hacer una petición POST al endpoint `/oauth/token` de Auth0:
- `grant_type=authorization_code`
- `client_id=tu_client_id`
- `code=codigo_recibido_en_callback`
- `redirect_uri=misma_uri_del_paso_2`
- `code_verifier=el_verifier_original_del_paso_1`

### **Paso 7: Procesar respuesta de tokens**
Auth0 responderá con:
- `access_token`: para usar inmediatamente con tu API
- `refresh_token`: para renovar tokens cuando expiren (¡esto es clave!)
- `expires_in`: tiempo de vida del access token en segundos
- `token_type`: normalmente "Bearer"

### **Paso 8: Almacenar tokens de forma segura**
- Guardar el refresh token en ubicación segura local
- Opcionalmente guardar también el access token inicial
- Almacenar timestamp de expiración calculado
- **¡Nunca guardar en el repositorio git!**

### **Paso 9: Cleanup y confirmación**
- Cerrar el servidor local temporal
- Cerrar la pestaña del navegador (mostrar página de éxito)
- Confirmar al usuario que la autenticación fue exitosa
- Realizar una prueba rápida con el token obtenido

## Consideraciones técnicas importantes

**Puerto del servidor local:**
- Usar un puerto dinámico libre (no hardcodeado)
- Configurar ese puerto en Auth0 como redirect_uri válida, o usar comodines si Auth0 lo permite

**Timeout y manejo de errores:**
- El servidor local debe tener timeout (ej: 5 minutos)
- Si el usuario no completa la auth, limpiar y mostrar error claro
- Manejar casos donde el usuario cierra el navegador

**Seguridad del state parameter:**
- Generar valor aleatorio único por cada flujo
- Verificar que el state recibido coincida con el enviado
- Esto previene ataques CSRF

**Experiencia del usuario:**
- Mostrar mensaje claro de qué está pasando
- "Abriendo navegador para autenticación..."
- "Esperando autorización... (puedes cerrar esta ventana después del login)"

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