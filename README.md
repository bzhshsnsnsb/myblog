# Bamboo AI Operations Blog

一套面向 AI 运维工程师的个人博客，包含公开技术站点与内容管理后台。

## 技术栈

- 前端：Vue 3、Vite、Element Plus、Vue Router、Pinia、Axios、Markdown-it
- 后端：Python、FastAPI、SQLAlchemy、SQLite、Pydantic

## 本地启动

### 后端

```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API 文档：http://127.0.0.1:8000/docs

### 前端

```powershell
cd frontend
npm install
npm run dev
```

站点：http://127.0.0.1:5173

默认管理员：`admin` / `admin123`

> 生产环境请在后端设置 `BLOG_SECRET`、`ADMIN_USERNAME` 和 `ADMIN_PASSWORD`，并在前端设置 `VITE_API_BASE_URL`。

## 测试

```powershell
cd backend
pytest

cd ..\frontend
npm run build
```
