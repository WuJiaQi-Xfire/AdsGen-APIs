# 路由模块初始化文件
# 这个文件允许Python将目录视为包
# 并允许从app.routers导入模块

# 导入各个路由模块的router对象
from api.v1.endpoints.default import router as default
from api.v1.endpoints.users import router as users
from api.v1.endpoints.test import router as test
