"""
Modular Router Architecture Example

This module demonstrates FastAPI's router-based architecture for organizing
large applications into maintainable, modular components.

Key Concepts:
- Separation of concerns with APIRouter
- Modular code organization by feature/domain
- Automatic API documentation grouping with tags
- Prefix-based URL namespacing

Usage:
    uvicorn main_ROUTER:app --reload --port 8002

Test with:
    - GET http://localhost:8002/ (root)
    - GET http://localhost:8002/users/
    - GET http://localhost:8002/restaurants/
    - Visit http://localhost:8002/docs for interactive API docs
"""
# main.py
from fastapi import FastAPI
from routers import users, restaurants

# FastAPI 앱 생성
app = FastAPI(
    title="음식 배달 API",
    description="사용자와 음식점을 관리하는 API입니다",
    version="1.0.0"
)

# 라우터 등록하기
app.include_router(users.router)
app.include_router(restaurants.router)

# 메인 페이지 (선택사항)
@app.get("/", tags=["root"])
def root():
    """
    Root endpoint providing API information.

    Returns:
        dict: Welcome message and documentation link

    Example:
        GET http://localhost:8002/
    """
    return {
        "message": "음식 배달 API에 오신 것을 환영합니다!",
        "docs": "/docs에서 API 문서를 확인하세요"
    }