# main.py
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI()

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
    쿼리 파라미터에서 토큰을 가져옵니다
    
    예시: GET /profile?token=alice_token
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
    토큰을 검증하고 사용자 정보를 반환합니다
    
    get_token 의존성을 먼저 실행해서 토큰을 받아옵니다
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
    현재 사용자가 관리자인지 확인합니다
    
    get_current_user 의존성을 먼저 실행해서 사용자를 받아옵니다
    """
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="관리자 권한이 필요합니다"
        )
    
    return current_user

# 엔드포인트 1: 누구나 접근 가능
@app.get("/")
def home():
    return {"message": "환영합니다! 로그인 없이도 볼 수 있습니다"}

# 엔드포인트 2: 로그인한 사용자만
@app.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    """
    로그인한 사용자의 프로필 조회
    
    의존성 체인:
    get_token → get_current_user → 이 함수
    """
    return {
        "message": f"{user['username']}님 환영합니다!",
        "profile": user
    }

# 엔드포인트 3: 관리자만
@app.get("/admin")
def admin_only(admin: dict = Depends(get_admin_user)):
    """
    관리자 페이지 (관리자만 접근 가능)
    
    의존성 체인:
    get_token → get_current_user → get_admin_user → 이 함수
    """
    return {
        "message": f"관리자 {admin['username']}님 환영합니다!",
        "admin_panel": "모든 권한이 있습니다"
    }

# 엔드포인트 4: 사용자 삭제 (관리자만)
@app.delete("/users/{username}")
def delete_user(
    username: str,
    admin: dict = Depends(get_admin_user)
):
    """
    사용자 삭제 (관리자 전용)
    """
    return {
        "message": f"관리자 {admin['username']}이(가) {username}을(를) 삭제했습니다"
    }