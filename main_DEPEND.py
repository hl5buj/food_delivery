"""
Pagination with Reusable Dependencies Example

This module demonstrates how to create reusable dependency functions for
common API patterns like pagination. The same pagination dependency is
used across multiple endpoints.

Key Concepts:
- Reusable dependency functions for common parameters
- Parameter validation within dependencies
- Using same dependency across multiple endpoints

Usage:
    uvicorn main_DEPEND:app --reload --port 8001

Test with:
    - GET http://localhost:8001/products
    - GET http://localhost:8001/products?skip=10&limit=20
    - GET http://localhost:8001/search?keyword=상품1&skip=0&limit=5
"""
# main.py
from fastapi import FastAPI, Depends

app = FastAPI(
    title="Pagination Dependency Example",
    description="Reusable pagination pattern with dependency injection",
    version="1.0.0"
)

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
    Reusable dependency function for pagination parameters.

    This dependency can be injected into any endpoint that needs pagination,
    providing consistent parameter validation and default values across the API.

    Args:
        skip (int): Number of items to skip (default: 0)
        limit (int): Maximum number of items to return (default: 10)

    Returns:
        dict: Dictionary with validated skip and limit values

    Validation:
        - limit is capped at maximum 100 to prevent excessive data retrieval

    Examples:
        - skip=0, limit=10 → items 1-10
        - skip=10, limit=10 → items 11-20
        - skip=20, limit=10 → items 21-30
        - skip=0, limit=200 → items 1-100 (capped at 100)
    """
    # 검증: limit은 최대 100까지만
    if limit > 100:
        limit = 100

    # 결과를 딕셔너리로 반환
    return {"skip": skip, "limit": limit}

# 엔드포인트 1: 상품 목록
@app.get("/products", tags=["products"])
def get_products(pagination: dict = Depends(pagination_params)):
    """
    Retrieve paginated product list.

    Demonstrates reusable pagination dependency across endpoints.

    Args:
        pagination (dict): Pagination parameters from pagination_params() dependency

    Returns:
        dict: Response containing:
            - total: Total number of products
            - skip: Number of items skipped
            - limit: Maximum items returned
            - products: List of product objects

    Examples:
        GET /products → items 1-10
        GET /products?skip=10&limit=20 → items 11-30
        GET /products?skip=90&limit=20 → items 91-100
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
@app.get("/search", tags=["products"])
def search_products(
    keyword: str,
    pagination: dict = Depends(pagination_params)  # 재사용!
):
    """
    Search products with pagination.

    Demonstrates reusing the same pagination dependency across different
    endpoints. The pagination parameters work consistently with search results.

    Args:
        keyword (str): Search keyword to filter products
        pagination (dict): Pagination parameters from pagination_params() dependency

    Returns:
        dict: Response containing:
            - keyword: The search keyword used
            - total_results: Total matching products
            - skip: Number of items skipped
            - limit: Maximum items returned
            - results: List of matching product objects

    Examples:
        GET /search?keyword=상품1&skip=0&limit=5
        GET /search?keyword=상품2&skip=5&limit=10
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