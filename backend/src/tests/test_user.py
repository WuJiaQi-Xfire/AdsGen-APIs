'''
Test user CRUD operations
'''

import sys
from pathlib import Path
import asyncio

from db.session import AsyncSessionLocal
from crud.user import user
from sqlalchemy import select

# add project root directory to Python import path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.append(str(ROOT_DIR))

# 获取异步数据库会话
async def get_test_db():
    """
    获取测试数据库会话
    """
    async with AsyncSessionLocal() as db:
        yield db

# 测试获取多个用户
async def test_get_multi_users():
    """
    测试CRUDBase中的get_multi方法
    
    这个测试直接使用从CRUDBase继承的get_multi方法，
    不创建新用户，而是直接获取数据库中已有的用户
    """
    # 获取数据库会话
    db = await anext(get_test_db())
    
    # 使用CRUDBase中的get_multi方法获取用户列表
    users = await user.get_multi(db=db, skip=0, limit=100)
    
    # 打印获取到的用户数量
    print(f"成功获取到 {len(users)} 个用户")
    
    # 验证结果
    assert users is not None
    
    # 打印用户列表
    if users:
        print("用户列表:")
        for i, db_user in enumerate(users):
            print(f"{i+1}. {db_user.username} ({db_user.email})")
    else:
        print("数据库中没有用户")

# 测试CRUDBase中的get_multi方法的实现
async def test_crud_base_get_multi_implementation():
    """
    测试CRUDBase中get_multi方法的具体实现
    
    这个测试检查CRUDBase中get_multi方法的实现是否正确
    """
    # 获取数据库会话
    db = await anext(get_test_db())
    
    # 直接使用CRUDBase中的get_multi方法
    # 这里我们使用user实例，它是CRUDUser的实例，继承自CRUDBase
    print("测试CRUDBase.get_multi方法的实现:")
    print(f"user.model: {user.model.__name__}")
    
    # 检查get_multi方法的实现
    result = await db.execute(select(user.model).offset(0).limit(5))
    query_result = result.scalars().all()
    base_result = await user.get_multi(db=db, skip=0, limit=5)
    
    # 验证两种方式获取的结果数量一致
    assert len(query_result) == len(base_result)
    print(f"直接查询获取到 {len(query_result)} 个用户")
    print(f"通过get_multi获取到 {len(base_result)} 个用户")
    
    # 验证两种方式获取的结果内容一致
    if query_result and base_result:
        # 检查第一个用户的ID是否一致
        assert query_result[0].id == base_result[0].id
        print(f"验证通过: 两种方式获取的第一个用户ID一致 ({query_result[0].id})")

# 如果直接运行此文件，则执行测试
if __name__ == "__main__":
    print("\n" + "="*50)
    print("开始测试: test_get_multi_users")
    print("="*50)
    asyncio.run(test_get_multi_users())
    
    print("\n" + "="*50)
    print("开始测试: test_crud_base_get_multi_implementation")
    print("="*50)
    asyncio.run(test_crud_base_get_multi_implementation())
    
    print("\n" + "="*50)
    print("所有测试完成")
    print("="*50)
