from typing import Any, Dict, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.security import get_password_hash, verify_password
from crud.base import CRUDBase
from models.user import User as UserModel
from schemas.user import UserCreate, UserUpdate

class CRUDUser(CRUDBase[UserModel, UserCreate, UserUpdate]):
    async def get_by_attribute(self, db: AsyncSession, *, attribute: str, value: Any) -> Optional[UserModel]:
        """
        通过属性获取用户
        
        参数:
            db: 数据库会话
            attribute: 属性名称
            value: 属性值
            
        返回:
            用户对象，如果不存在则返回None
        """
        result = await db.execute(select(UserModel).filter(getattr(UserModel, attribute) == value))
        db_obj = result.scalars().first()
        if db_obj:
            return db_obj
        return None

    async def create(self, db: AsyncSession, obj_in: UserCreate) -> UserModel:
        """
        创建新用户，处理密码加密
        
        参数:
            db: 数据库会话
            obj_in: 用户数据，Pydantic模型
            
        返回:
            创建的用户对象
        """
        try:
            # 转换为字典并处理密码
            obj_in_data = obj_in.model_dump()
            obj_in_data["hashed_password"] = get_password_hash(obj_in.password)
            if "password" in obj_in_data:
                del obj_in_data["password"]
            
            # 创建用户对象
            db_obj = UserModel(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise Exception(f"创建用户时出错: {str(e)}")

    async def update(self, db: AsyncSession, db_obj: UserModel, obj_in: UserUpdate) -> UserModel:
        """
        更新用户信息，处理密码加密
        
        参数:
            db: 数据库会话
            db_obj: 要更新的用户对象
            obj_in: 更新数据，Pydantic模型
            
        返回:
            更新后的用户对象
        """
        try:
            # 获取更新数据
            update_data = obj_in.model_dump(exclude_unset=True)
            
            # 处理密码加密
            if "password" in update_data and update_data["password"]:
                update_data["hashed_password"] = get_password_hash(update_data["password"])
                del update_data["password"]
            
            # 更新对象属性
            for field in update_data:
                setattr(db_obj, field, update_data[field])
                
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise Exception(f"更新用户时出错: {str(e)}")

    async def authenticate(self, db: AsyncSession, *, email: str, password: str) -> Optional[UserModel]:
        """
        验证用户
        
        参数:
            db: 数据库会话
            email: 用户邮箱
            password: 用户密码
            
        返回:
            验证成功返回用户对象，失败返回None
        """
        user = await self.get_by_attribute(db, attribute="email", value=email)
        if user and verify_password(password, user.hashed_password):
            return user
        return None

    def is_active(self, user: UserModel) -> bool:
        """
        检查用户是否激活
        
        参数:
            user: 用户对象
            
        返回:
            用户是否激活
        """
        return user.is_active

    def is_superuser(self, user: UserModel) -> bool:
        """
        检查用户是否是超级用户
        
        参数:
            user: 用户对象
            
        返回:
            用户是否是超级用户
        """
        return user.is_superuser
user = CRUDUser(UserModel)
