#!/usr/bin/env python3
"""
OAuth2.0 + PKCE Authentication Script
Etapa 1: Preparación PKCE y estructura base
"""

import base64
import hashlib
import secrets
import os
from pathlib import Path
from typing import Optional, Dict, Any
from dataclasses import dataclass
from urllib.parse import urlencode, urlparse, parse_qs
import json

import requests
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()


class PKCEParams(BaseModel):
    """Parámetros para el flujo PKCE"""

    code_verifier: str = Field(..., min_length=43, max_length=128)
    code_challenge: str = Field(..., min_length=1)
    code_challenge_method: str = Field(default="S256")
    state: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """Respuesta de tokens de Auth0"""

    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str = Field(default="Bearer")
    scope: Optional[str] = None


@dataclass
class Auth0Config:
    """Configuración de Auth0"""

    domain: str
    client_id: str
    audience: str  # Tu API identifier
    scopes: list[str]
    redirect_port: int = 8080


class PKCEGenerator:
    """Generador de parámetros PKCE según RFC 7636"""

    @staticmethod
    def generate_code_verifier() -> str:
        """
        Genera un code_verifier aleatorio.
        Debe ser un string de 43-128 caracteres usando [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
        """
        # Generamos 32 bytes aleatorios y los codificamos en base64url (sin padding)
        # Esto produce exactamente 43 caracteres
        random_bytes = secrets.token_bytes(32)
        code_verifier = (
            base64.urlsafe_b64encode(random_bytes).decode("utf-8").rstrip("=")
        )
        return code_verifier

    @staticmethod
    def generate_code_challenge(code_verifier: str) -> str:
        """
        Genera el code_challenge a partir del code_verifier.
        code_challenge = BASE64URL(SHA256(code_verifier))
        """
        # Calculamos SHA256 del code_verifier
        digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        # Codificamos en base64url sin padding
        code_challenge = base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")
        return code_challenge

    @staticmethod
    def generate_state() -> str:
        """Genera un parámetro state aleatorio para prevenir CSRF"""
        return secrets.token_urlsafe(32)

    @classmethod
    def generate_pkce_params(cls) -> PKCEParams:
        """Genera todos los parámetros PKCE necesarios"""
        code_verifier = cls.generate_code_verifier()
        code_challenge = cls.generate_code_challenge(code_verifier)
        state = cls.generate_state()

        return PKCEParams(
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            code_challenge_method="S256",
            state=state,
        )


class TokenStorage:
    """Manejo seguro del almacenamiento de tokens"""

    def __init__(self, app_name: str = "oauth-precommit"):
        self.app_name = app_name
        self.config_dir = Path.home() / ".config" / app_name
        self.token_file = self.config_dir / "tokens.json"

        # Crear directorio si no existe
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Establecer permisos restrictivos (solo el usuario puede leer/escribir)
        os.chmod(self.config_dir, 0o700)

    def save_tokens(self, tokens: TokenResponse) -> None:
        """Guarda los tokens de forma segura"""
        token_data = {
            "access_token": tokens.access_token,
            "refresh_token": tokens.refresh_token,
            "expires_in": tokens.expires_in,
            "token_type": tokens.token_type,
            "scope": tokens.scope,
            "saved_at": secrets.token_hex(16),  # timestamp ofuscado para validación
        }

        with open(self.token_file, "w") as f:
            json.dump(token_data, f, indent=2)

        # Establecer permisos restrictivos en el archivo
        os.chmod(self.token_file, 0o600)
        print(f"✓ Tokens guardados en: {self.token_file}")

    def load_tokens(self) -> Optional[Dict[str, Any]]:
        """Carga los tokens guardados"""
        if not self.token_file.exists():
            return None

        try:
            with open(self.token_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠ Error cargando tokens: {e}")
            return None

    def clear_tokens(self) -> None:
        """Elimina los tokens guardados"""
        if self.token_file.exists():
            self.token_file.unlink()
            print("✓ Tokens eliminados")


class OAuth2PKCEFlow:
    """Flujo principal de OAuth2.0 con PKCE"""

    def __init__(self, config: Auth0Config):
        self.config = config
        self.storage = TokenStorage()
        self.pkce_params: Optional[PKCEParams] = None

    def build_authorization_url(self) -> str:
        """Construye la URL de autorización con parámetros PKCE"""
        # Generar parámetros PKCE
        self.pkce_params = PKCEGenerator.generate_pkce_params()

        # Construir redirect_uri
        redirect_uri = f"http://localhost:{self.config.redirect_port}/callback"

        # Parámetros de la URL de autorización
        auth_params = {
            "response_type": "code",
            "client_id": self.config.client_id,
            "redirect_uri": redirect_uri,
            "scope": " ".join(self.config.scopes),
            "code_challenge": self.pkce_params.code_challenge,
            "code_challenge_method": self.pkce_params.code_challenge_method,
            "state": self.pkce_params.state,
            "audience": self.config.audience,
        }

        # Construir URL completa
        base_url = f"https://{self.config.domain}/authorize"
        auth_url = f"{base_url}?{urlencode(auth_params)}"

        return auth_url

    def validate_callback_params(self, callback_url: str) -> tuple[str, bool]:
        """
        Valida los parámetros recibidos en el callback
        Retorna: (authorization_code, is_valid)
        """
        parsed_url = urlparse(callback_url)
        params = parse_qs(parsed_url.query)

        # Verificar si hay error
        if "error" in params:
            error = params["error"][0]
            error_desc = params.get("error_description", [""])[0]
            print(f"❌ Error en autorización: {error}")
            if error_desc:
                print(f"   Descripción: {error_desc}")
            return "", False

        # Verificar que tenemos los parámetros necesarios
        if "code" not in params or "state" not in params:
            print("❌ Parámetros faltantes en callback")
            return "", False

        # Verificar state parameter (prevención CSRF)
        received_state = params["state"][0]
        if not self.pkce_params or received_state != self.pkce_params.state:
            print("❌ State parameter inválido - posible ataque CSRF")
            return "", False

        code = params["code"][0]
        print("✓ Callback válido - código de autorización recibido")
        return code, True


def main():
    """Función principal para testing"""

    # Demostración de generación PKCE
    print("=== Demostración Generación PKCE ===")
    pkce = PKCEGenerator.generate_pkce_params()
    print(f"Code Verifier: {pkce.code_verifier}")
    print(f"Code Challenge: {pkce.code_challenge}")
    print(f"State: {pkce.state}")
    print(f"Length verifier: {len(pkce.code_verifier)} caracteres")

    # # Configuración de ejemplo (reemplazar con valores reales)
    # config = Auth0Config(
    #     domain="tu-dominio.auth0.com",
    #     client_id="tu_client_id",
    #     audience="https://tu-api.com",
    #     scopes=["openid", "profile", "offline_access"],
    # )

    # # Crear instancia del flujo OAuth
    # oauth_flow = OAuth2PKCEFlow(config)

    # # Demostración de construcción de URL
    # print("\n=== URL de Autorización ===")
    # auth_url = oauth_flow.build_authorization_url()
    # print(f"URL: {auth_url[:100]}...")

    # # Demostración de almacenamiento
    # print("\n=== Sistema de Almacenamiento ===")
    # print(f"Directorio config: {oauth_flow.storage.config_dir}")
    # print(f"Archivo tokens: {oauth_flow.storage.token_file}")


if __name__ == "__main__":
    main()
