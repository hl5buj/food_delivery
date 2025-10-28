"""
Authentication and Authorization Example with Dependency Chains

This module demonstrates FastAPI's dependency injection system for implementing
authentication and role-based access control (RBAC).

Key Concepts:
- Dependency chains: get_token → get_current_user → get_admin_user
- Role-based authorization with admin/user roles
- HTTPException handling for authentication failures

Usage:
    uvicorn main:app --reload

Test with:
    - Public: GET http://localhost:8000/
    - User: GET http://localhost:8000/profile?token=alice_token
    - Admin: GET http://localhost:8000/admin?token=alice_token
"""
# main.py
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI(
    title="Dependency Chain Example",
    description="Authentication and authorization with cascading dependencies",
    version="1.0.0"
)

# 가짜 사용자 데이터베이스
fake_users_db = {
    "alice_token": {
        "username": "alice",
        "email": "alice@example.com",
        "role": "admin"  # 관리자
    },
    "bob_token": {
        "username": "bob",
        "email": "bob@example.com",
        "role": "user"   # 일반 사용자
    },
}

# 의존성 1: 토큰 가져오기
def get_token(token: str):
    """
    Extract authentication token from query parameters.

    This is the first dependency in the authentication chain. It validates
    that a token is provided in the request.

    Args:
        token (str): Authentication token from query parameter

    Returns:
        str: The validated token string

    Raises:
        HTTPException: 401 Unauthorized if token is missing

    Example:
        GET /profile?token=alice_token
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 없습니다"
        )
    return token

# 의존성 2: 토큰으로 사용자 찾기 (의존성 1을 사용)
def get_current_user(token: str = Depends(get_token)):
    """
    Validate token and retrieve user information.

    This dependency depends on get_token(), demonstrating dependency chaining.
    It looks up the user in the database using the provided token.

    Args:
        token (str): Validated token from get_token() dependency

    Returns:
        dict: User information containing username, email, and role

    Raises:
        HTTPException: 401 Unauthorized if token is invalid

    Dependency Chain:
        get_token() → get_current_user()
    """
    user = fake_users_db.get(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다"
        )
    
    return user

# 의존성 3: 관리자 권한 확인 (의존성 2를 사용)
def get_admin_user(current_user: dict = Depends(get_current_user)):
    """
    Verify that the current user has administrator privileges.

    This is the final dependency in the chain, implementing role-based
    access control by checking the user's role attribute.

    Args:
        current_user (dict): User object from get_current_user() dependency

    Returns:
        dict: Admin user information if role check passes

    Raises:
        HTTPException: 403 Forbidden if user is not an admin

    Dependency Chain:
        get_token() → get_current_user() → get_admin_user()
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    return current_user

# 엔드포인트 1: 누구나 접근 가능
@app.get("/", tags=["public"])
def home():
    """
    Public endpoint accessible without authentication.

    Returns:
        dict: Welcome message

    Example:
        GET http://localhost:8000/
    """
    return {"message": "환영합니다! 로그인 없이도 볼 수 있습니다"}

# 엔드포인트 2: 로그인한 사용자만
@app.get("/profile", tags=["authenticated"])
def get_profile(user: dict = Depends(get_current_user)):
    """
    Retrieve the authenticated user's profile.

    Requires valid authentication token. Uses dependency chain to validate
    and retrieve user information.

    Args:
        user (dict): Authenticated user from get_current_user() dependency

    Returns:
        dict: Welcome message and user profile information

    Raises:
        HTTPException: 401 if token is missing or invalid

    Dependency Chain:
        get_token() → get_current_user() → get_profile()

    Example:
        GET http://localhost:8000/profile?token=alice_token
        GET http://localhost:8000/profile?token=bob_token
    """
    return {
        "message": f"{user['username']}님 환영합니다!",
        "profile": user
    }

# 엔드포인트 3: 관리자만
@app.get("/admin", tags=["admin"])
def admin_only(admin: dict = Depends(get_admin_user)):
    """
    Admin-only endpoint demonstrating role-based access control.

    Uses complete dependency chain to validate authentication and verify
    admin privileges before granting access.

    Args:
        admin (dict): Admin user from get_admin_user() dependency

    Returns:
        dict: Admin welcome message and panel access

    Raises:
        HTTPException: 401 if token is missing/invalid, 403 if not admin

    Dependency Chain:
        get_token() → get_current_user() → get_admin_user() → admin_only()

    Example:
        GET http://localhost:8000/admin?token=alice_token (success)
        GET http://localhost:8000/admin?token=bob_token (403 Forbidden)
    """
    return {
        "message": f"관리자 {admin['username']}님 환영합니다!",
        "admin_panel": "모든 권한이 있습니다"
    }

# 엔드포인트 4: 사용자 삭제 (관리자만)
@app.delete("/users/{username}", tags=["admin"])
def delete_user(
    username: str,
    admin: dict = Depends(get_admin_user)
):
    """
    Delete a user (admin privileges required).

    Demonstrates combining path parameters with dependency injection
    for administrative operations.

    Args:
        username (str): Username to delete (from path)
        admin (dict): Admin user from get_admin_user() dependency

    Returns:
        dict: Confirmation message with admin and target username

    Raises:
        HTTPException: 401 if token missing/invalid, 403 if not admin

    Example:
        DELETE http://localhost:8000/users/bob?token=alice_token
    """
    return {
        "message": f"관리자 {admin['username']}이(가) {username}을(를) 삭제했습니다"
    }