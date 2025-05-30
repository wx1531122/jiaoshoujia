**通用原则 (贯穿所有阶段):**

*   **版本控制 (Git):** 从一开始就使用 Git，为每个阶段或重要功能里程碑打上标签。
*   **文档:** 简单记录下你做的决策、模块功能和如何使用。即使是给自己看的。
*   **测试:** 尽早引入测试，至少是关键路径的测试。
*   **代码风格:** 使用 Black、Flake8 (Python) 和 Prettier、ESLint (React) 保持代码一致性。

---

**阶段一: 核心认证与项目骨架**

**目标:** 实现最基础的用户注册、登录、登出功能，并搭建好前后端项目的基本结构。新项目基于此能快速跑起来一个带认证的空壳应用。

**后端模块 (Python - 推荐 FastAPI)**

1.  **`core/` 目录:**
    *   **`config.py`:**
        *   模块: `Settings` (Pydantic-Settings)
        *   功能: 从 `.env` 加载应用配置 (数据库URL, JWT密钥, Token有效期等)。
    *   **`security.py`:**
        *   模块: `PasswordManager` (封装 `passlib`)
        *   功能: 密码哈希、密码验证。
        *   模块: `TokenManager` (封装 `python-jose` 或 `PyJWT`)
        *   功能: 创建访问令牌 (access token)、刷新令牌 (refresh token)、解码并验证令牌。
2.  **`db/` 目录:**
    *   **`database.py`:**
        *   模块: `DatabaseSessionManager` 或直接定义 engine, SessionLocal
        *   功能: SQLAlchemy 引擎、数据库会话 (SessionLocal)、声明式基类 (Base)。
    *   **`base_model.py` (可选):**
        *   模块: `TimestampedModel` (继承 `Base`)
        *   功能: 包含 `id`, `created_at`, `updated_at` 字段的基类模型。
3.  **`users/` (或 `auth/`) 模块/目录:**
    *   **`models.py`:**
        *   模块: `User` (SQLAlchemy, 继承 `TimestampedModel`)
        *   功能: 用户表模型 (id, username, email, hashed_password, is_active, created_at, updated_at)。
    *   **`schemas.py`:**
        *   模块: `UserCreate` (Pydantic) - 用于注册
        *   模块: `UserRead` (Pydantic) - 用于读取用户信息
        *   模块: `Token` (Pydantic) - 用于返回JWT
        *   模块: `LoginCredentials` (Pydantic) - 用于登录
    *   **`crud.py`:**
        *   模块: `UserCRUD`
        *   功能: 创建用户 (`create_user`)、按用户名/邮箱获取用户 (`get_user_by_username`, `get_user_by_email`)。
    *   **`router.py`:** (FastAPI APIRouter)
        *   模块: `AuthRouter`
        *   功能:
            *   `/register` (POST): 用户注册。
            *   `/login` (POST): 用户登录，返回JWT。
            *   `/me` (GET): 获取当前登录用户信息 (需要认证)。
4.  **`main.py` (或 `app.py`):**
    *   模块: FastAPI 应用实例
    *   功能: 初始化应用，挂载 `AuthRouter`，配置CORS (基本配置)。

**前端模块 (React - 推荐 Vite + TypeScript)**

1.  **`src/services/` 目录:**
    *   **`apiClient.ts`:**
        *   模块: Axios 实例或 `fetch` 封装
        *   功能: 基础URL配置，请求/响应拦截器 (用于自动附加Token, 处理通用错误)。
    *   **`authService.ts`:**
        *   模块: `AuthAPI`
        *   功能: 调用后端 `/login`, `/register`, `/me` 接口的函数。
2.  **`src/contexts/` (或 `src/store/` 使用Zustand/Redux Toolkit) 目录:**
    *   **`AuthContext.tsx`:**
        *   模块: `AuthProvider`, `useAuth` hook
        *   功能: 管理认证状态 ( `isAuthenticated`, `user`, `token` )，提供 `login`, `logout` 方法。Token存储在localStorage。
3.  **`src/components/auth/` 目录:**
    *   **`LoginForm.tsx`:** 登录表单组件。
    *   **`RegisterForm.tsx`:** 注册表单组件。
4.  **`src/components/common/` (非常基础的，如果需要的话):**
    *   **`LoadingSpinner.tsx`:** 简单的加载指示器。
5.  **`src/router/` 目录:**
    *   **`index.tsx` (或 `AppRouter.tsx`):**
        *   模块: `AppRoutes` (使用 `react-router-dom`)
        *   功能: 定义公共路由和受保护路由。
    *   **`ProtectedRoute.tsx`:**
        *   模块: `ProtectedRoute` 组件
        *   功能: 如果未认证，重定向到登录页。
6.  **`src/pages/` 目录:**
    *   **`LoginPage.tsx`:** 登录页面。
    *   **`RegisterPage.tsx`:** 注册页面。
    *   **`HomePage.tsx` (受保护):** 简单的主页，显示 "Welcome {username}"。
    *   **`ProfilePage.tsx` (受保护):** 显示从 `/me` 获取的用户信息。
7.  **`src/App.tsx`:**
    *   模块: 应用根组件
    *   功能: 包裹 `AuthProvider` 和 `AppRoutes`。
8.  **`.env.development` / `.env.production`:** 存放 `VITE_API_BASE_URL`。

**阶段一成果:** Status: COMPLETED
一个可以运行的前后端应用，支持用户注册、登录，受保护的页面，JWT认证。项目结构基本成型。

---

**阶段二: 增强用户体验与功能**

**目标:** 完善认证流程 (密码重置、邮箱验证)，添加基础的数据库迁移，提供更好的错误处理和通知，构建基本应用布局。
**Status: COMPLETED**

**后端模块 (Python)**

1.  **数据库迁移 (集成 Alembic): Status: COMPLETED**
    *   **`alembic/` 目录:** Alembic 环境配置和版本脚本。**Status: COMPLETED**
    *   `User` 模型中增加 `is_verified_email` (Boolean, default False), `email_verification_token`, `password_reset_token`, `password_reset_token_expiry` 字段。**Status: COMPLETED** (Manual migration script created)
2.  **`core/` 目录: Status: COMPLETED**
    *   **`dependencies.py`:**
        *   模块: `get_current_active_user` (FastAPI依赖项) **Status: COMPLETED**
        *   功能: 从Token中获取用户，并检查是否 active。改进 `/me` 路由使用此依赖。**Status: COMPLETED**
    *   **`exceptions.py`:**
        *   模块: 自定义异常类 (如 `CredentialsException`, `UserNotFoundException`) **Status: COMPLETED**
        *   功能: 更清晰的错误类型。**Status: COMPLETED**
    *   **`error_handlers.py` (或在 `main.py` 中):**
        *   模块: 全局异常处理器 **Status: COMPLETED**
        *   功能: 捕获自定义异常和HTTPException，返回统一JSON格式错误。**Status: COMPLETED**
    *   **`email_service.py`:**
        *   模块: `EmailService` (使用 `fastapi-mail`) **Status: COMPLETED**
        *   功能: 发送邮件的通用方法 (用于邮箱验证、密码重置)。配置从 `config.py` 读取SMTP设置。**Status: COMPLETED**
3.  **`users/` (或 `auth/`) 模块/目录 (增强): Status: COMPLETED**
    *   **`schemas.py` (新增):** `RequestPasswordResetSchema`, `ResetPasswordSchema`, `RequestEmailVerificationSchema`, `MessageSchema`. **Status: COMPLETED**
    *   **`crud.py` (新增):**
        *   设置/清除邮箱验证token (`set_email_verification_token`, `verify_user_by_email_token`)。**Status: COMPLETED**
        *   设置/清除密码重置token (`set_password_reset_token`, `reset_password_by_token`, `get_user_by_password_reset_token`)。**Status: COMPLETED**
    *   **`router.py` (新增端点):**
        *   `/request-password-reset` (POST): 请求密码重置邮件。**Status: COMPLETED**
        *   `/reset-password` (POST): 使用token重置密码。**Status: COMPLETED** (Path is `/reset-password`, token in body)
        *   `/verify-email/{token}` (GET): 验证邮箱。**Status: COMPLETED** (Path is `/verify-email/{token}`)
        *   `/request-email-verification` (POST): 请求新的验证邮件。**Status: COMPLETED**
    *   `/logout` (POST, 可选): 如果JWT需要服务器端失效 (通常不需要，前端清除即可)。**Status: NOT IMPLEMENTED (Optional)**

**前端模块 (React)**

1.  **`src/components/layout/` 目录: Status: COMPLETED**
    *   **`AuthLayout.tsx`:** 用于登录、注册等页面的简单居中布局。**Status: COMPLETED**
    *   **`DashboardLayout.tsx`:**
        *   模块: `DashboardLayout` **Status: COMPLETED**
        *   功能: 包含顶部导航栏 (Navbar) 和主要内容区域。退出按钮在Navbar。**Status: COMPLETED**
    *   **`Navbar.tsx`:**
        *   模块: `Navbar` **Status: COMPLETED**
        *   功能: 显示应用Logo/名称，用户头像/名称，登出按钮。**Status: COMPLETED**
2.  **`src/components/auth/` 目录 (新增): Status: COMPLETED**
    *   **`RequestPasswordResetForm.tsx`** **Status: COMPLETED**
    *   **`ResetPasswordForm.tsx`** **Status: COMPLETED**
3.  **`src/components/common/` (新增/增强): Status: COMPLETED**
    *   **`Notification.tsx` (或集成 `react-toastify` / `notistack`):**
        *   模块: Toast/Notification 系统 **Status: COMPLETED** (Component created)
        *   功能: 显示成功、错误、信息提示。**Status: COMPLETED**
    *   **`Modal.tsx` (可选，如果需要弹出确认框等):** 简单的模态框组件。**Status: NOT IMPLEMENTED (Optional)**
4.  **`src/pages/` 目录 (新增/修改): Status: COMPLETED**
    *   **`RequestPasswordResetPage.tsx`** **Status: COMPLETED**
    *   **`ResetPasswordPage.tsx`** **Status: COMPLETED**
    *   **`EmailVerificationPage.tsx`:** 显示验证状态或提示检查邮箱。**Status: COMPLETED**
    *   修改登录/注册页面使用 `AuthLayout`。**Status: COMPLETED**
    *   修改 `HomePage`, `ProfilePage` 等使用 `DashboardLayout`。**Status: COMPLETED**
5.  **`src/services/authService.ts` (增强): Status: COMPLETED**
    *   添加调用新后端端点的函数。**Status: COMPLETED**
6.  **`src/contexts/AuthContext.tsx` (或 store) (增强): Status: COMPLETED**
    *   在 `login` 成功后，可以将用户信息存储起来，如 `user` 对象。**Status: COMPLETED** (Already part of Phase 1, verified `is_verified_email` field is accessible)
    *   `logout` 方法清除 localStorage 中的 token 和用户状态。**Status: COMPLETED** (Already part of Phase 1)
7.  **`src/utils/` 目录 (可选):**
    *   **`formValidators.ts`:** 常用的表单验证规则。**Status: NOT IMPLEMENTED (Optional)**

**阶段二成果:** Status: COMPLETED
用户认证流程更完整 (邮箱验证、密码重置)，有数据库迁移支持 (手动脚本创建)，错误处理和用户反馈更好 (自定义异常、错误处理中间件、通知组件概念)，应用有了基本的导航和布局。

---

**阶段三: 项目模板化与高级功能**

**目标:** 将现有成果打包成可复用的项目模板 (Cookiecutter)，引入更高级的功能如角色权限管理 (RBAC) 和可选的后台任务，完善文档和开发体验。

**后端模块 (Python)**

1.  **角色与权限管理 (RBAC) - 可选但推荐:**
    *   **`rbac/` 目录:**
        *   **`models.py`:** `Role`, `Permission`, `UserRole` (多对多), `RolePermission` (多对多) 模型。
        *   **`schemas.py`:** 相应的 Pydantic schema。
        *   **`crud.py`:** CRUD 操作 для ролей, разрешений и их связей.
        *   **`dependencies.py`:**
            *   模块: `require_role(role_name: str)`
            *   模块: `require_permission(permission_name: str)`
            *   功能: FastAPI 依赖项，用于保护需要特定角色/权限的端点。
        *   **`router.py` (可选):** 提供管理角色和权限的API (通常给超级管理员用)。
    *   **`users/models.py` (修改):** 将用户的角色关系添加到 `User` 模型 (通过 `UserRole` 中间表)。
    *   **`users/schemas.py` (修改):** `UserRead` 中可能包含用户角色信息。
2.  **`core/` 目录:**
    *   **`logging_config.py`:**
        *   模块: 日志配置
        *   功能: 配置结构化日志 (如 JSON)，方便后续集成日志系统。
3.  **`crud/` (通用CRUD基类 - 可选):**
    *   **`base.py`:**
        *   模块: `CRUDBase<ModelType, CreateSchemaType, UpdateSchemaType>`
        *   功能: 提供通用的 `get`, `get_multi`, `create`, `update`, `remove` 方法。具体业务CRUD可继承它。
4.  **后台任务 (Celery / ARQ - 可选，如果常用):**
    *   **`tasks/` 目录:**
        *   模块: 任务定义 (如 `send_verification_email_task`)
        *   配置: Celery/ARQ worker 配置。
    *   修改邮件发送逻辑，使其通过后台任务异步执行。
5.  **项目模板化 (Cookiecutter):**
    *   将整个后端项目结构调整为 Cookiecutter 模板。
    *   `cookiecutter.json`: 定义模板变量 (项目名, 作者, 数据库名等)。
    *   使用 `{{ cookiecutter.project_slug }}` 等模板语法。
    *   `.env.example` 预配置。
    *   `README.md` 模板，包含安装、运行说明。
6.  **Docker 化 (可选，但非常推荐):**
    *   `Dockerfile` 用于构建后端镜像。
    *   `docker-compose.yml` 用于开发环境一键启动后端服务和SQLite (或Postgres/MySQL)。

**前端模块 (React)**

1.  **UI组件库集成/扩展 (可选):**
    *   如果决定使用如 Material UI, Ant Design, Chakra UI，在此阶段深度集成。
    *   或者完善自己的小型通用组件库 `src/components/ui/` (Table, Advanced Form Controls, etc.)。
2.  **角色权限控制 (如果后端实现RBAC):**
    *   **`src/contexts/AuthContext.tsx` (增强):** `user` 对象中包含角色/权限信息。
    *   **`src/router/RoleProtectedRoute.tsx` (或增强 `ProtectedRoute`):**
        *   模块: `RoleProtectedRoute`
        *   功能: 检查用户是否拥有特定角色/权限才能访问路由。
    *   **`src/hooks/usePermissions.ts`:**
        *   模块: `usePermissions` hook
        *   功能: 方便在组件中检查用户是否有特定权限，用于条件渲染UI元素。
3.  **状态管理优化 (如果需要):**
    *   如果 Context API 变得复杂，考虑迁移到 Zustand 或 Redux Toolkit。
4.  **项目模板化 (与后端一起):**
    *   前端部分也纳入 Cookiecutter 模板。
    *   `package.json` 中的项目名等使用模板变量。
5.  **Docker 化 (可选):**
    *   `Dockerfile` 用于构建前端静态资源或Node服务。
    *   `docker-compose.yml` 中包含前端服务。

**阶段三成果:**
一个功能完善、可配置、可扩展的Python + React项目脚手架。通过Cookiecutter可以快速生成新项目。可选的RBAC和后台任务满足更复杂的需求。通过Docker可以轻松部署和开发。

---
