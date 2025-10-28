"""
User Management Router

This module provides user-related endpoints using FastAPI's APIRouter.
Demonstrates modular organization with automatic URL prefixing and
documentation grouping.

Endpoints:
    GET /users/ - List all users
    GET /users/{user_id} - Get specific user
    POST /users/ - Create new user
"""
# routers/users.py
from fastapi import APIRouter

# APIRouter 생성
# prefix: 모든 경로 앞에 자동으로 붙는 접두사
# tags: Swagger 문서에서 그룹으로 묶어서 보여줌
router = APIRouter(
    prefix="/users",  # 이 라우터의 모든 경로는 /users로 시작
    tags=["users"]    # Swagger UI에서 "users" 그룹으로 표시
)

# 가짜 데이터베이스 (나중에 실제 DB로 교체할 예정)
fake_users_db = [
    {"id": 1, "name": "김철수", "email": "kim@example.com"},
    {"id": 2, "name": "이영희", "email": "lee@example.com"},
]

# 엔드포인트: GET /users/
# prefix가 /users니까 실제 경로는 /users/ 입니다
@router.get("/")
def get_all_users():
    """
    Retrieve all users.

    Returns:
        dict: Dictionary containing list of all users

    Example:
        GET /users/
        Response: {"users": [{"id": 1, "name": "김철수", ...}, ...]}
    """
    return {"users": fake_users_db}

# 엔드포인트: GET /users/1
# 실제 경로는 /users/{user_id} 입니다
@router.get("/{user_id}")
def get_user(user_id: int):
    """
    Retrieve a specific user by ID.

    Args:
        user_id (int): User ID from path parameter

    Returns:
        dict: User object if found, error message otherwise

    Example:
        GET /users/1
        Response: {"id": 1, "name": "김철수", "email": "kim@example.com"}
    """
    # user_id와 일치하는 사용자 찾기
    for user in fake_users_db:
        if user["id"] == user_id:
            return user

    # 못 찾으면 404 에러
    return {"error": "사용자를 찾을 수 없습니다"}

# 엔드포인트: POST /users/
@router.post("/")
def create_user(name: str, email: str):
    """
    Create a new user.

    Args:
        name (str): User's name
        email (str): User's email address

    Returns:
        dict: Success message and created user object with auto-generated ID

    Example:
        POST /users/?name=박민수&email=park@example.com
        Response: {
            "message": "사용자 생성 완료",
            "user": {"id": 3, "name": "박민수", "email": "park@example.com"}
        }
    """
    # 새 ID 생성 (기존 최대 ID + 1)
    new_id = max(user["id"] for user in fake_users_db) + 1

    # 새 사용자 추가
    new_user = {"id": new_id, "name": name, "email": email}
    fake_users_db.append(new_user)

    return {"message": "사용자 생성 완료", "user": new_user}