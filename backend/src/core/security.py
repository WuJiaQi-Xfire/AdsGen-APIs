from datetime import datetime, timedelta
from typing import Any, Union, Optional

from passlib.context import CryptContext
from jose import jwt

# 密码上下文，用于哈希和验证密码
# 使用pbkdf2_sha256替代bcrypt，避免bcrypt版本兼容性问题
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# JWT相关配置
SECRET_KEY = "your-secret-key-here"  # 在生产环境中应该从环境变量中获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希处理
    
    参数:
        password: 原始密码
        
    返回:
        哈希后的密码
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证密码是否正确
    
    参数:
        plain_password: 原始密码
        hashed_password: 哈希后的密码
        
    返回:
        密码是否正确
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    创建JWT访问令牌
    
    参数:
        subject: 令牌主题，通常是用户ID
        expires_delta: 令牌过期时间
        
    返回:
        JWT令牌
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
