from typing import Type, TypeVar, Generic, List
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from src.crud.base import CRUDBase
from src.db.session import get_db
from src.schemas.user import User as UserSchema

# 泛型参数定义：
ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)  # 用于创建的 Pydantic 模型
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)  # 用于更新的 Pydantic 模型

class CRUDRouter(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    通用异步 CRUD 路由类
    """
    def __init__(
        self, 
        crud: CRUDBase[ModelType, CreateSchemaType, UpdateSchemaType],
    ):
        self.crud = crud
        self.router = APIRouter()

    async def create_item(self, item_in: CreateSchemaType, db: AsyncSession = Depends(get_db)):
        """
        创建新项目
        """
        try:
            db_item = await self.crud.create(db=db, obj_in=item_in)
            return db_item
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"创建项目失败: {str(e)}"
            )

    async def read_item(self, item_id: int, db: AsyncSession = Depends(get_db)):
        """
        根据 ID 获取单个项目
        """
        db_item = await self.crud.get(db=db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="项目未找到")
        return db_item

    async def update_item(
        self, 
        item_id: int, 
        item_in: UpdateSchemaType, 
        db: AsyncSession = Depends(get_db)
    ):
        """
        根据 ID 更新项目
        """
        db_item = await self.crud.get(db=db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="项目未找到")
        updated_item = await self.crud.update(db=db, db_obj=db_item, obj_in=item_in)
        return updated_item

    async def delete_item(self, item_id: int, db: AsyncSession = Depends(get_db)):
        """
        根据 ID 删除项目，返回删除前的数据
        """
        db_item = await self.crud.get(db=db, id=item_id)
        if not db_item:
            raise HTTPException(status_code=404, detail="项目未找到")
        
        return await self.crud.remove(db=db, id=item_id)

    async def read_items(self, skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
        """
        获取项目列表
        """
        items = await self.crud.get_multi(db=db, skip=skip, limit=limit)
        return items
