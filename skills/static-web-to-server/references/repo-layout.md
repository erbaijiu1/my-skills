# Repo Layout Reference

建议目标仓库采用单仓多应用布局，并将应用统一收纳到 web_transfer 目录下：

```text
repo-root/
  .github/
    skills/
      static-web-to-server/
        SKILL.md
        references/
  web_transfer/
    backend_dev/
    frontend_nuxt/
    admin_dashboard/
  <cloned static pages and assets>/
```

这样做的好处：

- 所有迁移工作在一个 Git 仓库里统一管理。
- web_transfer 作为应用容器目录，更容易与原始静态克隆内容做物理隔离。
- 前台、后台、接口可以共享提交历史和 issue 上下文。
- 便于按目录分工，不需要拆成多个仓库再做额外同步。

推荐的落盘原则：

- 后端接口、数据模型、静态服务逻辑优先进入 web_transfer/backend_dev。
- 面向站点访客的页面重构优先进入 web_transfer/frontend_nuxt。
- 面向内部维护人员的数据录入、编辑、配置页面进入 web_transfer/admin_dashboard。
- 如果本次任务不需要后台维护功能，不要强行改动 web_transfer/admin_dashboard。

兼容现有模式的建议：

- 若 web_transfer/backend_dev 已有 app/api 和扁平化 schema/model 文件，新增内容优先贴合现状，再决定是否逐步细分目录。
- 若 web_transfer/frontend_nuxt 已经存在页面，新的迁移页面优先复用现有 layouts 和页面组织方式。
- 若 web_transfer/admin_dashboard 已有依赖栈，优先延续它的组件库和状态管理方案，不再引入第二套后台 UI 体系。