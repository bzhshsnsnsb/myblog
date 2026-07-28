import re
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from .auth import create_token, require_admin, verify_credentials
from .database import Base, SessionLocal, engine, get_db
from .models import Article, Category, Comment, Tag
from .schemas import (
    ArticleDetail, ArticleInput, ArticleListItem, CommentAdminOut, CommentInput, CommentOut,
    LoginInput, LoginOut, PaginatedArticles, SiteStats,
)
from .seed import seed_database


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        seed_database(db)
    yield


app = FastAPI(title="AIOps Lab API", version="1.0.0", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def article_query():
    return select(Article).options(selectinload(Article.category), selectinload(Article.tags))


def resolve_category(db: Session, name: str) -> Category:
    category = db.scalar(select(Category).where(Category.name == name))
    if not category:
        base = slugify(name)
        slug = base
        index = 2
        while db.scalar(select(Category.id).where(Category.slug == slug)):
            slug = f"{base}-{index}"
            index += 1
        category = Category(name=name, slug=slug)
        db.add(category)
    return category


def resolve_tags(db: Session, names: list[str]) -> list[Tag]:
    tags = []
    for name in dict.fromkeys(value.strip() for value in names if value.strip()):
        tag = db.scalar(select(Tag).where(Tag.name == name))
        if not tag:
            tag = Tag(name=name, slug=f"{slugify(name)}-{abs(hash(name)) % 10000}")
            db.add(tag)
        tags.append(tag)
    return tags


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/auth/login", response_model=LoginOut)
def login(payload: LoginInput):
    if not verify_credentials(payload.username, payload.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    return LoginOut(token=create_token(payload.username), username=payload.username)


@app.get("/api/articles", response_model=PaginatedArticles)
def list_articles(
    page: int = Query(1, ge=1), page_size: int = Query(8, ge=1, le=50), category: str | None = None,
    tag: str | None = None, search: str | None = None,
    db: Session = Depends(get_db),
):
    query = article_query()
    count_query = select(func.count(Article.id))
    filters = []
    filters.append(Article.published.is_(True))
    if category:
        filters.append(Article.category.has(Category.slug == category))
    if tag:
        filters.append(Article.tags.any(Tag.slug == tag))
    if search:
        filters.append(or_(Article.title.ilike(f"%{search}%"), Article.excerpt.ilike(f"%{search}%")))
    query = query.where(*filters).order_by(Article.published_at.desc())
    count_query = count_query.where(*filters)
    items = db.scalars(query.offset((page - 1) * page_size).limit(page_size)).all()
    return PaginatedArticles(items=items, total=db.scalar(count_query) or 0, page=page, page_size=page_size)


@app.get("/api/articles/{slug}", response_model=ArticleDetail)
def article_detail(slug: str, db: Session = Depends(get_db)):
    query = article_query().options(selectinload(Article.comments)).where(Article.slug == slug, Article.published.is_(True))
    article = db.scalar(query)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    article.comments = [comment for comment in article.comments if comment.approved]
    return article


@app.post("/api/articles/{slug}/comments", response_model=CommentOut, status_code=201)
def create_comment(slug: str, payload: CommentInput, db: Session = Depends(get_db)):
    article = db.scalar(select(Article).where(Article.slug == slug, Article.published.is_(True)))
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    comment = Comment(**payload.model_dump(), article=article)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Category.id, Category.name, Category.slug, func.count(Article.id).label("count"))
        .outerjoin(Article).where(or_(Article.published.is_(True), Article.id.is_(None))).group_by(Category.id).order_by(Category.name)
    ).all()
    return [dict(row._mapping) for row in rows]


@app.get("/api/tags")
def list_tags(db: Session = Depends(get_db)):
    rows = db.execute(select(Tag.id, Tag.name, Tag.slug, func.count(Article.id).label("count")).outerjoin(Tag.articles).group_by(Tag.id)).all()
    return [dict(row._mapping) for row in rows]


@app.get("/api/stats", response_model=SiteStats)
def public_stats(db: Session = Depends(get_db)):
    return SiteStats(
        articles=db.scalar(select(func.count(Article.id)).where(Article.published.is_(True))) or 0,
        categories=db.scalar(select(func.count(Category.id))) or 0,
        tags=db.scalar(select(func.count(Tag.id))) or 0,
        comments=db.scalar(select(func.count(Comment.id)).where(Comment.approved.is_(True))) or 0,
    )


@app.get("/api/admin/articles", response_model=list[ArticleListItem], dependencies=[Depends(require_admin)])
def admin_articles(db: Session = Depends(get_db)):
    return db.scalars(article_query().order_by(Article.updated_at.desc())).all()


@app.get("/api/admin/articles/{article_id}", response_model=ArticleDetail, dependencies=[Depends(require_admin)])
def admin_article_detail(article_id: int, db: Session = Depends(get_db)):
    article = db.scalar(article_query().options(selectinload(Article.comments)).where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    return article


@app.post("/api/admin/articles", response_model=ArticleDetail, status_code=201, dependencies=[Depends(require_admin)])
def admin_create_article(payload: ArticleInput, db: Session = Depends(get_db)):
    if db.scalar(select(Article.id).where(Article.slug == payload.slug)):
        raise HTTPException(status_code=409, detail="文章别名已存在")
    values = payload.model_dump(exclude={"category", "tags"})
    article = Article(**values, category=resolve_category(db, payload.category), tags=resolve_tags(db, payload.tags))
    db.add(article)
    db.commit()
    return db.scalar(article_query().options(selectinload(Article.comments)).where(Article.id == article.id))


@app.put("/api/admin/articles/{article_id}", response_model=ArticleDetail, dependencies=[Depends(require_admin)])
def admin_update_article(article_id: int, payload: ArticleInput, db: Session = Depends(get_db)):
    article = db.scalar(article_query().where(Article.id == article_id))
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    duplicate = db.scalar(select(Article.id).where(Article.slug == payload.slug, Article.id != article_id))
    if duplicate:
        raise HTTPException(status_code=409, detail="文章别名已存在")
    for key, value in payload.model_dump(exclude={"category", "tags"}).items():
        setattr(article, key, value)
    article.category = resolve_category(db, payload.category)
    article.tags = resolve_tags(db, payload.tags)
    db.commit()
    return db.scalar(article_query().options(selectinload(Article.comments)).where(Article.id == article.id))


@app.delete("/api/admin/articles/{article_id}", status_code=204, dependencies=[Depends(require_admin)])
def admin_delete_article(article_id: int, db: Session = Depends(get_db)):
    article = db.get(Article, article_id)
    if not article:
        raise HTTPException(status_code=404, detail="文章不存在")
    db.delete(article)
    db.commit()


@app.get("/api/admin/comments", response_model=list[CommentAdminOut], dependencies=[Depends(require_admin)])
def admin_comments(db: Session = Depends(get_db)):
    return db.scalars(select(Comment).order_by(Comment.created_at.desc())).all()


@app.patch("/api/admin/comments/{comment_id}", response_model=CommentAdminOut, dependencies=[Depends(require_admin)])
def admin_toggle_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="留言不存在")
    comment.approved = not comment.approved
    db.commit()
    db.refresh(comment)
    return comment


@app.delete("/api/admin/comments/{comment_id}", status_code=204, dependencies=[Depends(require_admin)])
def admin_delete_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = db.get(Comment, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="留言不存在")
    db.delete(comment)
    db.commit()
