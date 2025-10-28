# routers/restaurants.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/restaurants",
    tags=["restaurants"]
)

# 가짜 음식점 데이터
fake_restaurants_db = [
    {"id": 1, "name": "맛있는 치킨", "category": "치킨", "rating": 4.5},
    {"id": 2, "name": "행복한 피자", "category": "피자", "rating": 4.8},
]

@router.get("/")
def get_all_restaurants():
    """모든 음식점 조회"""
    return {"restaurants": fake_restaurants_db}

# 카테고리별 검색 (예: GET /restaurants/search?category=치킨)
# 아래에 있는 '카테고리로 음식점 검색'하는 Method가 '특정 음식점 조회' 다음에 오면 에러가 난다
# 현재의 순서처럼 '카테고리로 음식점 검색'하는 Method가 먼저 와야 한다.
# 이유는 FastAPI가 경로를 매칭할 때 더 구체적인 경로를 먼저 찾기 때문입니다. 
@router.get("/search")
def search_restaurants(category: str):
    """카테고리로 음식점 검색"""
    results = [r for r in fake_restaurants_db if r["category"] == category]
    return {"results": results}

@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int):
    """특정 음식점 조회"""
    for restaurant in fake_restaurants_db:
        if restaurant["id"] == restaurant_id:
            return restaurant
    
    return {"error": "음식점을 찾을 수 없습니다"}

# 엔드포인트: POST /restaurants/
@router.post("/")
def create_restaurant(name: str, category: str, rating: float):
    """새 음식점 생성"""
    # 새 ID 생성 (기존 최대 ID + 1)
    new_id = max(restaurant["id"] for restaurant in fake_restaurants_db) + 1

    # 새 음식점 추가
    new_restaurant = {"id": new_id, "name": name, "category": category, "rating": rating}
    fake_restaurants_db.append(new_restaurant)

    return {"message": "음식점 생성 완료", "restaurant": new_restaurant}
