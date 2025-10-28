# main.py
from fastapi import FastAPI, Depends

app = FastAPI()

# 가짜 상품 데이터 (100개)
fake_products = [
    {"id": i, "name": f"상품{i}", "price": i * 1000}
    for i in range(1, 101)
]

# 의존성 함수: 페이지네이션 파라미터
def pagination_params(
    skip: int = 0,      # 건너뛸 개수 (기본값 0)
    limit: int = 10     # 가져올 개수 (기본값 10)
):
    """
    페이지네이션을 위한 공통 파라미터
    
    skip: 몇 개를 건너뛸지
    limit: 몇 개를 가져올지
    
    예시:
    - skip=0, limit=10 → 1~10번째
    - skip=10, limit=10 → 11~20번째
    - skip=20, limit=10 → 21~30번째
    """
    # 검증: limit은 최대 100까지만
    if limit > 100:
        limit = 100
    
    # 결과를 딕셔너리로 반환
    return {"skip": skip, "limit": limit}

# 엔드포인트 1: 상품 목록
@app.get("/products")
def get_products(pagination: dict = Depends(pagination_params)):
    """
    상품 목록 조회 (페이지네이션 적용)
    
    예시 요청:
    - GET /products → 1~10번 상품
    - GET /products?skip=10&limit=20 → 11~30번 상품
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    
    # 슬라이싱으로 일부만 가져오기
    products = fake_products[skip : skip + limit]
    
    return {
        "total": len(fake_products),
        "skip": skip,
        "limit": limit,
        "products": products
    }

# 엔드포인트 2: 검색 결과 (같은 페이지네이션 사용)
@app.get("/search")
def search_products(
    keyword: str,
    pagination: dict = Depends(pagination_params)  # 재사용!
):
    """
    상품 검색 (페이지네이션 적용)
    
    예시:
    GET /search?keyword=상품1&skip=0&limit=5
    """
    skip = pagination["skip"]
    limit = pagination["limit"]
    
    # 키워드가 포함된 상품 필터링
    filtered = [
        p for p in fake_products 
        if keyword in p["name"]
    ]
    
    # 페이지네이션 적용
    results = filtered[skip : skip + limit]
    
    return {
        "keyword": keyword,
        "total_results": len(filtered),
        "skip": skip,
        "limit": limit,
        "results": results
    }