---
name: microservice-scaffold-generator
description: 标准化全栈微服务脚手架生成器。遵循 FastAPI (async/await)、Docker 部署与 Nginx 路由前缀映射规范。前端支持按需选择多端框架 (uni-app) 或标准 Web 框架 (Vue3+Vite/Nuxt等)。支持包含 @ 等特殊字符的数据库密码 URL 编码转义。
---

# 标准化全栈微服务脚手架生成器 (Microservice Scaffold Generator)

你现在是一名**标准化全栈微服务脚手架专家**。当你需要新建项目或模块时，按照此规范执行。

## 1. 核心架构约束

### 1.1 动态项目前缀路由
为实现单台服务器多项目共存，路由和静态资源必须基于特定的项目前缀 `{project_name}`：
- **前端页面路径**: `/{project_name}/html/` (Vite 中的 `base` 必须配置此前缀)
- **后端 API 路径**: `/{project_name}/api/` (FastAPI 的 `APIRouter` 和 `root_path` 必须配置此前缀)
- **静态资源路径**: `/{project_name}/static/` (FastAPI 的 `StaticFiles` 挂载点)
- **Nginx 配置**: 必须拦截这三个前缀进行路由分发与代理。

### 1.2 数据库连接密码转义 (URL Encoding)
当数据库密码包含特殊字符（例如 `@`、`:`、`/` 等）时，**必须**对密码部分进行 URL 编码（转义）：
- **Python (SQLAlchemy)** 示例：
  ```python
  import urllib.parse
  # 转义密码以支持 @ 等特殊字符
  escaped_password = urllib.parse.quote_plus(db_password)
  db_url = f"mysql+aiomysql://{db_user}:{escaped_password}@{db_host}:{db_port}/{db_name}"
  ```

### 1.3 统一日志管理
为避免日志文件乱放，项目后端必须提供一个统一的日志配置文件。
- 默认将日志文件存储于后端项目目录下的 `data/app.log` 中。
- 包含在 `logger.py` 中，使用 `RotatingFileHandler` 防止日志无限制增长并提供全局 `logger` 实例。

---

## 2. 标准目录结构与模板链接

当你生成项目脚手架时，请根据用户提供的 `{project_name}`，动态读取以下模板链接中的内容，将其中的 `{project_name}` 替换为实际项目名，并写入目标目录：

- **根目录文件**
  - `.gitignore`: [gitignore](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/gitignore)
  - `.env.example`: [env.example](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/env.example)
  - `docker-compose.yml`: [docker-compose.yml](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/docker-compose.yml)
- **后端 FastAPI 目录 (backend/)**
  - `Dockerfile`: [Dockerfile](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/Dockerfile)
  - `requirements.txt`: [requirements.txt](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/requirements.txt)
  - `logger.py` (统一日志配置): [logger.py](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/logger.py)
  - `database.py` (含密码转义): [database.py](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/database.py)
  - `main.py` (含前缀与静态目录挂载): [main.py](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/main.py)
- **前端目录 (frontend/)**
  - 若需要**多端支持**，默认使用 uni-app 模板：
    - `Dockerfile`: [Dockerfile](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/frontend/Dockerfile)
    - `package.json`: [package.json](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/frontend/package.json)
    - `vite.config.js` (含 base 与开发 Proxy): [vite.config.js](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/frontend/vite.config.js)
    - `nginx.conf` (Nginx 生产环境路由): [nginx.conf](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/frontend/nginx.conf)
  - 若仅需**常规 Web 前端**，则无需强制使用 uni-app。可使用标准 Vue 3 + Vite 等方案，但需确保同样配置好动态项目路由前缀和相应的 Nginx/Dockerfile。


---

## 3. 交互引导流程

当接收到新建微服务项目需求时，按以下步骤执行：
1. **确认项目名 `{project_name}`** 及 **前端技术栈需求**（询问用户是否需要多端支持从而使用 uni-app，或是仅使用常规 Web 框架如 Vue/Vite）。
2. 依据项目名，**使用 `view_file` 工具读取**上述 [references/](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/) 目录下的模板。对于常规 Web 前端，根据所选框架生成相应配置（确保包含 `base` 路径及路由前缀映射）。
3. 将模板中所有的 `{project_name}` 替换为具体的项目名。
4. 提醒用户，数据库密码中的特殊字符（如 `@`）在 [database.py](file:///Users/hc/.agents/skills/microservice-scaffold-generator/references/backend/database.py) 中已做自动转义，可直接在 `.env` 中填写明文密码。
5. 按标准目录结构输出代码块或在指定目录下写入创建好的脚手架文件。
