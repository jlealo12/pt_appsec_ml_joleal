# OWASP workflow

En el hook (cliente) se hace la petición del bearer, luego se hace la petición al servidor con el bearer y el payload, el servidor valida el bearer y si es correcto procesa el payload y devuelve la respuesta al cliente.

En el hook:
- Generar random string
- Calcular hash del random string con sha256
- Hacer petición al servidor con el hash y el code challenge
~~~
https://dev-ww24ezrm404scmeb.us.auth0.com/authorize?
  response_type=code&
  client_id={YOUR_CLIENT_ID}&
  state={RANDOM_STRING}&
  redirect_uri=https://example-app.com/redirect&
  code_challenge={YOUR_CODE_CHALLENGE}&
  code_challenge_method=S256
~~~
- Recibir codigo temporal del servidor
- Hacer petición al servidor con el codigo temporal y el payload
~~~
curl -X POST https://dev-ww24ezrm404scmeb.us.auth0.com/oauth/token \
  -d grant_type=authorization_code \
  -d redirect_uri=https://example-app.com/redirect \
  -d client_id={YOUR_CLIENT_ID} \
  -d client_secret={YOUR_CLIENT_SECRET} \
  -d code_verifier={YOUR_CODE_VERIFIER} \
  -d code={YOUR_AUTHORIZATION_CODE}
~~~
- Recibir respuesta del servidor con el token

En las variables de ambiente deberían estar:
- YOUR_CLIENT_ID
- YOUR_CLIENT_SECRET

Desde el hook se genera:
- RANDOM_STRING
- YOUR_CODE_CHALLENGE

El servidor entrega en el primer llamado:
- YOUR_AUTHORIZATION_CODE
El valor de YOUR_CODE_VERIFIER es el mismo que RANDOM_STRING

El servidor entrega en el segundo llamado:
~~~
{
    "access_token": "AQUI_VA_EL_TOKEN",
    "expires_in": 86400,
    "token_type": "Bearer",
}
~~~