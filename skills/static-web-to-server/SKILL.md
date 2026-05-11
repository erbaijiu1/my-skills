---
name: static-web-to-server
description: 'Migrate HTTrack or other cloned static HTML sites into web_transfer/backend_dev (FastAPI), web_transfer/frontend_nuxt (Nuxt 3 / Vue 3), and optional web_transfer/admin_dashboard (Vite Vue 3 admin). Use for asset extraction, link rewriting, schema extraction, mock JSON generation, API-first refactors, and static-to-dynamic page migration.'
argument-hint: '页面或目录，例如 index.html、products/、about-us/'
---

# Static Web To Server

将静态克隆站点逐步迁移为可维护的全栈项目，并尽量复用目标仓库已有模式。

## 何时使用

- 需要把 HTTrack 克隆的静态 HTML 页面迁移到 FastAPI + Nuxt 3 架构。
- 需要把重复的 HTML 内容提取为结构化数据和接口。
- 需要把原始站点资源整理到统一静态目录，并修复链接。
- 需要在保留原页面结构和交互的前提下做组件化改造。
- 需要为后台管理功能补充 admin_dashboard 页面或接口对接。

## 目标布局约定

建议目标仓库采用 web_transfer 作为应用容器目录，迁移时保持这个结构，便于统一 Git 管理和分端开发：

- web_transfer/backend_dev: 后端服务目录，优先复用现有 FastAPI 结构。
- web_transfer/frontend_nuxt: 前台站点目录，优先复用现有 Nuxt 3 结构。
- web_transfer/admin_dashboard: 后台管理端目录，仅在确实存在管理需求时使用。

详细约定见 [repo layout reference](./references/repo-layout.md)。

## 多项目部署与路径前缀约定 (Multi-Project Path Prefixing)

为了支持多个克隆站点在同一台服务器或同一套网关下部署且互不冲突，我们统一采用“业务隔离前缀(Site Code)”机制。在迁移或初始化新克隆站点时，所有的前端页面路径、后台系统路径以及后端 API，都要带有业务前缀：

1. **Frontend Nuxt (`web_transfer/frontend_nuxt`)**:
   - `nuxt.config.ts` 中的 `app.baseURL` 应配置为 `/${siteCode}/` (如 `/shindary/`)，以便前台页面统一挂载到子目录。
   - 所有的 API 请求（如 `useFetch`）前缀也必须包含对应前缀：`${config.public.apiBase}/${config.public.siteCode}/api/v1/public/...`。

2. **Admin Dashboard (`web_transfer/admin_dashboard`)**:
   - `vite.config.ts` 中的 `base` 应配置为 `/${siteCode}_admin/` (如 `/shindary_admin/`)，从而与前台页面彻底分离。
   - 项目内部 Axios 实例的 `baseURL` 必须指向后端带前缀的真实地址（例如 `/${siteCode}/api/v1/admin/`）。

3. **Backend FastAPI (`web_transfer/backend_dev`)**:
   - 所有的 Public 或 Admin 的接口 API Router 必须加上 `/{siteCode}/` (如 `/shindary/api/v1/...`)。

## 硬性规则

1. 在生成任何代码前，先检查 web_transfer/backend_dev、web_transfer/frontend_nuxt、web_transfer/admin_dashboard 的现有结构和依赖，优先沿用当前项目模式，不做无关重构。
2. 所有迁移产物都应落在 web_transfer 目录下的既有应用目录中，不要再创建第二套平行前后端骨架。
3. 保留页面视觉层级、核心交互和 SEO 关键内容，不要只保留文本而丢失结构。
4. 先做单页或单类页面打样，再批量推广到同类页面。
5. 清理冗余克隆产物时，只删除确认无用的临时文件、追踪脚本和重复资源，不要误删业务素材。

## 迁移流程

### Step 1: Inventory

- 扫描目标 HTML、CSS、JS、图片、字体和内联脚本。
- 产出资源清单，识别可复用资源、重复资源、第三方追踪脚本和失效路径。
- 识别页面模板类型，例如首页、列表页、详情页、资讯页、联系页。

### Step 2: Asset Sanitization

- 将静态资源按类型归档，统一迁移到后续应用使用的公开静态目录。
- 修复 HTML 内的 href、src、srcset、背景图、字体路径和脚本引用。
- 对重要内联样式和内联脚本做显式提取，避免迁移中丢失。

### Step 3: Schema Extraction

- 分析重复内容块，例如产品卡片、新闻列表、导航项、轮播项、联系方式。
- 提取字段并建立明确的数据结构。
- 生成可供联调的 mock 数据，例如 test_data.json。

### Step 4: Backend First

- 先在 web_transfer/backend_dev 中为核心页面或核心数据域提供接口。
- 优先使用 async def 路由、清晰的 schema、基础错误处理、CORS 和 Depends。
- 若目标仓库中的 web_transfer/backend_dev 已采用 app/main.py、models.py、schemas.py、api/ 的轻量结构，则优先延续该模式。
- 只有在新增模块明显需要版本化时，才逐步引入 app/api/v1 这类更细分的目录，而不是强制一次性改造整个后端。

### Step 5: Frontend Inject

- 在 web_transfer/frontend_nuxt 中把页面拆为 Nuxt / Vue 3 组件，例如 Header、Footer、Hero、ProductCard、ArticleList。
- 优先使用 Nuxt 的 pages、components、layouts、composables 组织代码。
- 使用 useFetch、$fetch 或现有项目约定的数据获取方式替换写死内容。
- 仅在确实存在共享状态或复杂交互时引入 Pinia，不要为简单页面过度建模。

### Step 6: Admin Dashboard

- 当迁移任务涉及产品维护、新闻维护、分类维护、文件上传、站点配置等后台功能时，再扩展 web_transfer/admin_dashboard。
- 若目标仓库中的 web_transfer/admin_dashboard 已有既定技术栈和组件体系，应沿用这一模式。
- 后台管理接口应与 web_transfer/backend_dev 保持字段命名和校验规则一致。

### Step 7: Cleanup

- 删除 HTTrack 生成的无用 txt、log、追踪脚本、重复副本和明显无效页面。
- 保留对迁移结果仍有价值的原始参考页面，直到对应动态页面验证完成。

## 输出要求

- 明确说明本次迁移针对的页面或目录。
- 给出资源迁移结果和路径映射。
- 给出数据模型或字段表。
- 给出 web_transfer/backend_dev 中新增或修改的接口与文件。
- 给出 web_transfer/frontend_nuxt 中新增或修改的页面、组件、数据请求逻辑。
- 如涉及后台管理，说明 web_transfer/admin_dashboard 中新增的页面、表单、列表或路由。
- 给出本次删除的冗余文件类别。

## 避坑指南

- 不要忽略原站中的 jQuery 或原生事件绑定，迁移时要显式改写为 Vue 事件和生命周期逻辑。
- 不要把所有页面一次性硬迁移，优先抽取可复用模板后再推广。
- 不要为了追求所谓标准结构而无视目标仓库已有模式，先兼容现状，再做渐进式优化。
- 不要把所有数据都直接写死回组件里，优先抽离为接口或 mock 数据。

## 工作建议

1. 先选一个核心页面作为样板，例如首页或产品列表页。
2. 完成一条闭环：资源整理、接口输出、前端改造、页面验证。
3. 样板稳定后，再按页面类型批量迁移。