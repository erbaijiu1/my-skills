---
name: static-web-to-server
description: 'Migrate HTTrack or other cloned static HTML sites into web_transfer/backend_dev (FastAPI), web_transfer/frontend_nuxt (Nuxt 3 / Vue 3), and optional web_transfer/admin_dashboard (Vite Vue 3 admin). Use for static-to-dynamic page migration, asset extraction, link rewriting, schema extraction, mock JSON generation, API-first refactors, and componentized page rebuilds.'
argument-hint: '页面或目录，例如 index.html、products/、about-us/'
---

# Static Web To Server

将静态克隆站点逐步迁移为可维护的全栈项目，并优先复用目标仓库已有模式，而不是为了“标准化”重建一套新骨架。

## 何时使用

- 需要把 HTTrack 克隆的静态 HTML 页面迁移到 FastAPI + Nuxt 3 架构。
- 需要把重复 HTML 内容抽取为结构化数据、接口和可复用组件。
- 需要整理原始站点资源，修复链接，并移除明显无用的克隆产物。
- 需要在保留原页面结构和交互的前提下做组件化改造。
- 需要在已有 web_transfer 项目中补充前台页面、后端接口，或按需扩展 admin_dashboard。

## 输入

必需输入：

- 待迁移的页面、目录或模板类型，例如首页、产品列表页、详情页。
- 目标仓库根目录，或至少说明 web_transfer 是否已经存在。

可选但强烈建议补充：

- 是否存在 web_transfer/backend_dev、web_transfer/frontend_nuxt、web_transfer/admin_dashboard。
- 是否需要后台维护功能。
- 是否是单站点部署还是多站点部署。
- 是否已有 Nginx、Docker、docker-compose 或其他网关约束。
- 是否已有可复用接口、数据表、种子数据或 mock 数据。

## 预检

在生成代码前，先检查：

1. 目标仓库当前目录结构、依赖和已有约定。
2. 原始静态页面的 HTML、CSS、JS、图片、字体、内联脚本和第三方追踪脚本。
3. 页面类型是否可以归并为少量模板，而不是逐页硬迁移。
4. 资源路径、接口路径、站点前缀和部署约束是否已经存在既有模式。

如果目标仓库已有明确的目录布局、API 风格、组件体系或部署方案，优先贴合现状，不做无关重构。

## 目标布局约定

建议目标仓库采用 web_transfer 作为应用容器目录，迁移时保持这个结构，便于统一 Git 管理和分端开发：

- web_transfer/backend_dev: 后端服务目录，优先复用现有 FastAPI 结构。
- web_transfer/frontend_nuxt: 前台站点目录，优先复用现有 Nuxt 3 结构。
- web_transfer/admin_dashboard: 后台管理端目录，仅在确实存在管理需求时使用。

详细约定见 [repo layout reference](./references/repo-layout.md)。

## 决策门

- 如果目标仓库已经有既定目录、状态管理、接口分层或组件体系，优先沿用，不创建第二套前后端骨架。
- 如果当前任务只涉及前台页面迁移，不要默认扩展 admin_dashboard。
- 如果当前仓库不是多站点部署，不要强行引入业务前缀或子路径策略。
- 如果静态资源规模很大，优先提纯在用资源，不要把整包克隆产物直接塞进前端 public。

多站点路径前缀策略见 [multi-project path prefixing](./references/multi-project-path-prefixing.md)。
静态资源抽取与托管策略见 [static asset migration](./references/static-asset-migration.md)。

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

### Step 2: Asset Sanitization & Centralized Extraction

- 修复 HTML 内的 href、src、srcset、背景图、字体路径和脚本引用。
- 对重要内联样式和内联脚本做显式提取，避免迁移中丢失。
- 当资源量过大时，只保留实际被页面、组件、种子数据或模板引用的文件。

### Step 3: Schema Extraction

- 分析重复内容块，例如产品卡片、新闻列表、导航项、轮播项、联系方式。
- 提取字段并建立明确的数据结构。
- 生成可供联调的 mock 数据，例如 test_data.json。

### Step 4: Backend First

- 先在 web_transfer/backend_dev 中为核心页面或核心数据域提供接口。
- 优先使用 async def 路由、清晰的 schema、基础错误处理、CORS 和 Depends。
- 若目标仓库已采用扁平结构或现有 API 分层，则延续该模式；只在确有必要时再引入更细的版本化目录。

### Step 5: Frontend Inject

- 在 web_transfer/frontend_nuxt 中把页面拆为 Nuxt / Vue 3 组件，例如 Header、Footer、Hero、ProductCard、ArticleList。
- 优先使用 Nuxt 的 pages、components、layouts、composables 组织代码。
- 使用 useFetch、$fetch 或现有项目约定的数据获取方式替换写死内容。
- 仅在确实存在共享状态或复杂交互时引入 Pinia，不要为简单页面过度建模。

### Step 6: Admin Dashboard

- 当迁移任务涉及产品维护、新闻维护、分类维护、文件上传、站点配置等后台功能时，再扩展 web_transfer/admin_dashboard。
- 若目标仓库中的 admin_dashboard 已有既定技术栈和组件体系，应沿用这一模式。
- 后台管理接口应与 backend_dev 保持字段命名和校验规则一致。

### Step 7: Cleanup

- 删除 HTTrack 生成的无用 txt、log、追踪脚本、重复副本和明显无效页面。
- 保留对迁移结果仍有价值的原始参考页面，直到对应动态页面验证完成。

## 输出格式

输出中应明确给出：

- 本次迁移针对的页面、目录或模板类型。
- 资源迁移结果和路径映射。
- 提取出的数据模型、字段表或 mock 数据。
- web_transfer/backend_dev 中新增或修改的接口与文件。
- web_transfer/frontend_nuxt 中新增或修改的页面、组件、数据请求逻辑。
- 如涉及后台管理，说明 web_transfer/admin_dashboard 中新增的页面、表单、列表或路由。
- 本次删除的冗余文件类别，以及保留原因。

## 避坑指南

- 不要忽略原站中的 jQuery 或原生事件绑定，迁移时要显式改写为 Vue 事件和生命周期逻辑。
- 不要把所有页面一次性硬迁移，优先抽取可复用模板后再推广。
- 不要为了追求所谓标准结构而无视目标仓库已有模式，先兼容现状，再做渐进式优化。
- 不要把所有数据都直接写死回组件里，优先抽离为接口或 mock 数据。
- 不要在信息不全时脑补部署拓扑、路径前缀或后台需求；先检查仓库，再决定是否扩展。

## 工作建议

1. 先选一个核心页面作为样板，例如首页或产品列表页。
2. 完成一条闭环：资源整理、接口输出、前端改造、页面验证。
3. 样板稳定后，再按页面类型批量迁移。

## 代码分组：亲密性原则

编写或修改迁移后的 API、组件、数据加载及转换逻辑时：

- 将服务于同一业务目的的语句放在一起，在不同步骤或子步骤之间空一行，循环内部也要体现边界。例如资源校验、数据转换、结果输出可形成各自的逻辑组。
- 步骤注释紧贴对应代码，空行放在注释之前；索引、Map、集合等局部准备工作归入使用它们的步骤。
- 不机械地逐句加空行，不强制给简单逻辑加编号注释；遵循语言和项目格式化规范，保留会影响 HTML 渲染或字符串内容的空白。
- 验证迁移结果时同时检查分组可读性；仅整理本次触及的代码，不为统一间距批量重排原始克隆文件或无关代码。
