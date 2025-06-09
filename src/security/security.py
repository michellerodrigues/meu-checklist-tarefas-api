"""
Módulo se Segurança, responsável pela camada de segurança da aplicação

"""
from __future__ import annotations

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def criar_hash_senha(senha: str) -> str:
    """Cria o Hash da Senha em texto plano

    Args:
        senha (string): Senha com texto plano

    Returns:
        str: Hash da senha criada
    """

    return pwd_context.hash(senha)


def verificar_senha(senha: str, hash_senha: str) -> bool:
    """Compara a senha de texto plano e o hash da senha

    Args:
        senha (str): Senha com texto plano
        hash_senha (str): Hash da senha

    Returns:
        bool: true se o hash da senha informada e
        o hash da senha gravada são iguais

    """
    return pwd_context.verify(senha, hash_senha)
