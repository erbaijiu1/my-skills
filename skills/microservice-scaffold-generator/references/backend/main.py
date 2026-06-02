import os
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

PROJECT_NAME = os.getenv("PROJECT_NAME", "myproject")

app = FastAPI(
    title=f"{PROJECT_NAME} API",
    # 容器化 Nginx 代理后，FastAPI 内部生成 docs 链接需要正确识别 root_path
    root_path=f"/{PROJECT_NAME}/api"
)

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态资源挂载路径必须为 /{project_name}/static
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount(f"/{PROJECT_NAME}/static", StaticFiles(directory=static_dir), name="static")

# 主路由，路径带前缀 /{project_name}/api
router = APIRouter(prefix=f"/{PROJECT_NAME}/api")

@router.get("/health")
async def health_check():
    return {"status": "ok", "project": PROJECT_NAME}

app.include_router(router)
