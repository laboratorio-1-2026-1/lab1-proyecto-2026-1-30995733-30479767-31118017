from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pasar luego a un archivo .env
SECRET_KEY = "super_secreto_smartgym_cambiar_luego"  # Llave secreta para firmar los tokens
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token expira en media hora

def get_password_hash(password: str) -> str:
    """Recibe una contraseña en texto plano y devuelve el hash encriptado"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña ingresada con el hash de la base de datos"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Genera el Token JWT cuando el login es exitoso"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt