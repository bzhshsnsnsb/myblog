from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str


class TagOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    slug: str


class ArticleInput(BaseModel):
    title: str = Field(min_length=2, max_length=120)
    slug: str = Field(pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$", max_length=140)
    excerpt: str = Field(min_length=10, max_length=280)
    content: str = Field(min_length=20)
    cover: str = Field(min_length=5, max_length=500)
    category: str = Field(min_length=1, max_length=40)
    tags: list[str] = Field(default_factory=list, max_length=8)
    featured: bool = False
    published: bool = True


class ArticleListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    slug: str
    excerpt: str
    cover: str
    featured: bool
    published: bool
    published_at: datetime
    category: CategoryOut
    tags: list[TagOut]


class CommentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    author: str
    content: str
    created_at: datetime


class CommentAdminOut(CommentOut):
    email: str
    approved: bool
    article_id: int


class ArticleDetail(ArticleListItem):
    content: str
    updated_at: datetime
    comments: list[CommentOut]


class CommentInput(BaseModel):
    author: str = Field(min_length=2, max_length=40)
    email: EmailStr
    content: str = Field(min_length=2, max_length=500)


class LoginInput(BaseModel):
    username: str
    password: str


class LoginOut(BaseModel):
    token: str
    username: str


class PaginatedArticles(BaseModel):
    items: list[ArticleListItem]
    total: int
    page: int
    page_size: int


class SiteStats(BaseModel):
    articles: int
    categories: int
    tags: int
    comments: int

