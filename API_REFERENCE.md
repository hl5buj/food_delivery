# FastAPI Food Delivery - API Reference

This document provides comprehensive API documentation for three different implementation patterns of the Food Delivery application.

## Table of Contents
- [Implementation Patterns](#implementation-patterns)
- [Pattern 1: Dependency Chain (main.py)](#pattern-1-dependency-chain)
- [Pattern 2: Reusable Dependencies (main_DEPEND.py)](#pattern-2-reusable-dependencies)
- [Pattern 3: Modular Router (main_ROUTER.py)](#pattern-3-modular-router)

---

## Implementation Patterns

### Pattern 1: Dependency Chain (main.py)
**Port**: 8000 (default)
**Focus**: Authentication and authorization with cascading dependencies
**Use Case**: Learning dependency injection chains and role-based access control

### Pattern 2: Reusable Dependencies (main_DEPEND.py)
**Port**: 8001
**Focus**: Reusable pagination dependency across endpoints
**Use Case**: Learning to create common utility dependencies

### Pattern 3: Modular Router (main_ROUTER.py)
**Port**: 8002
**Focus**: Organizing large applications with APIRouter
**Use Case**: Learning modular application architecture

---

## Pattern 1: Dependency Chain

### Base URL
```
http://localhost:8000
```

### Authentication
This API uses simple token-based authentication via query parameters.

**Test Tokens**:
- `alice_token` - Admin user
- `bob_token` - Regular user

### Endpoints

#### GET /
**Description**: Public endpoint, no authentication required
**Tags**: public

**Response**:
```json
{
  "message": "환영합니다! 로그인 없이도 볼 수 있습니다"
}
```

---

#### GET /profile
**Description**: Get authenticated user's profile
**Tags**: authenticated
**Authentication**: Required

**Query Parameters**:
- `token` (string, required): Authentication token

**Request Example**:
```bash
curl "http://localhost:8000/profile?token=alice_token"
```

**Response**:
```json
{
  "message": "alice님 환영합니다!",
  "profile": {
    "username": "alice",
    "email": "alice@example.com",
    "role": "admin"
  }
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token

---

#### GET /admin
**Description**: Admin-only endpoint
**Tags**: admin
**Authentication**: Required (Admin role)

**Query Parameters**:
- `token` (string, required): Admin authentication token

**Request Example**:
```bash
curl "http://localhost:8000/admin?token=alice_token"
```

**Response**:
```json
{
  "message": "관리자 alice님 환영합니다!",
  "admin_panel": "모든 권한이 있습니다"
}
```

**Error Responses**:
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: User is not an admin

---

#### DELETE /users/{username}
**Description**: Delete a user (admin only)
**Tags**: admin
**Authentication**: Required (Admin role)

**Path Parameters**:
- `username` (string, required): Username to delete

**Query Parameters**:
- `token` (string, required): Admin authentication token

**Request Example**:
```bash
curl -X DELETE "http://localhost:8000/users/bob?token=alice_token"
```

**Response**:
```json
{
  "message": "관리자 alice이(가) bob을(를) 삭제했습니다"
}
```

---

## Pattern 2: Reusable Dependencies

### Base URL
```
http://localhost:8001
```

### Endpoints

#### GET /products
**Description**: Get paginated product list
**Tags**: products

**Query Parameters**:
- `skip` (integer, optional, default: 0): Number of items to skip
- `limit` (integer, optional, default: 10): Maximum items to return (max: 100)

**Request Examples**:
```bash
# First page (items 1-10)
curl "http://localhost:8001/products"

# Second page (items 11-30)
curl "http://localhost:8001/products?skip=10&limit=20"

# Items 91-100
curl "http://localhost:8001/products?skip=90&limit=20"
```

**Response**:
```json
{
  "total": 100,
  "skip": 0,
  "limit": 10,
  "products": [
    {"id": 1, "name": "상품1", "price": 1000},
    {"id": 2, "name": "상품2", "price": 2000}
  ]
}
```

---

#### GET /search
**Description**: Search products with pagination
**Tags**: products

**Query Parameters**:
- `keyword` (string, required): Search keyword
- `skip` (integer, optional, default: 0): Number of items to skip
- `limit` (integer, optional, default: 10): Maximum items to return (max: 100)

**Request Example**:
```bash
curl "http://localhost:8001/search?keyword=상품1&skip=0&limit=5"
```

**Response**:
```json
{
  "keyword": "상품1",
  "total_results": 11,
  "skip": 0,
  "limit": 5,
  "results": [
    {"id": 1, "name": "상품1", "price": 1000},
    {"id": 10, "name": "상품10", "price": 10000},
    {"id": 11, "name": "상품11", "price": 11000},
    {"id": 12, "name": "상품12", "price": 12000},
    {"id": 13, "name": "상품13", "price": 13000}
  ]
}
```

---

## Pattern 3: Modular Router

### Base URL
```
http://localhost:8002
```

### Endpoints

#### GET /
**Description**: Root endpoint with API information
**Tags**: root

**Response**:
```json
{
  "message": "음식 배달 API에 오신 것을 환영합니다!",
  "docs": "/docs에서 API 문서를 확인하세요"
}
```

---

### Users Router (`/users`)

#### GET /users/
**Description**: Get all users
**Tags**: users

**Request Example**:
```bash
curl "http://localhost:8002/users/"
```

**Response**:
```json
{
  "users": [
    {"id": 1, "name": "김철수", "email": "kim@example.com"},
    {"id": 2, "name": "이영희", "email": "lee@example.com"}
  ]
}
```

---

#### GET /users/{user_id}
**Description**: Get specific user by ID
**Tags**: users

**Path Parameters**:
- `user_id` (integer, required): User ID

**Request Example**:
```bash
curl "http://localhost:8002/users/1"
```

**Response**:
```json
{
  "id": 1,
  "name": "김철수",
  "email": "kim@example.com"
}
```

**Error Response**:
```json
{
  "error": "사용자를 찾을 수 없습니다"
}
```

---

#### POST /users/
**Description**: Create a new user
**Tags**: users

**Query Parameters**:
- `name` (string, required): User's name
- `email` (string, required): User's email

**Request Example**:
```bash
curl -X POST "http://localhost:8002/users/?name=박민수&email=park@example.com"
```

**Response**:
```json
{
  "message": "사용자 생성 완료",
  "user": {
    "id": 3,
    "name": "박민수",
    "email": "park@example.com"
  }
}
```

---

### Restaurants Router (`/restaurants`)

#### GET /restaurants/
**Description**: Get all restaurants
**Tags**: restaurants

**Request Example**:
```bash
curl "http://localhost:8002/restaurants/"
```

**Response**:
```json
{
  "restaurants": [
    {"id": 1, "name": "맛있는 치킨", "category": "치킨", "rating": 4.5},
    {"id": 2, "name": "행복한 피자", "category": "피자", "rating": 4.8}
  ]
}
```

---

#### GET /restaurants/search
**Description**: Search restaurants by category
**Tags**: restaurants

**Important**: This endpoint must be defined before `/{restaurant_id}` to prevent routing conflicts.

**Query Parameters**:
- `category` (string, required): Category to filter by

**Request Example**:
```bash
curl "http://localhost:8002/restaurants/search?category=치킨"
```

**Response**:
```json
{
  "results": [
    {"id": 1, "name": "맛있는 치킨", "category": "치킨", "rating": 4.5}
  ]
}
```

---

#### GET /restaurants/{restaurant_id}
**Description**: Get specific restaurant by ID
**Tags**: restaurants

**Path Parameters**:
- `restaurant_id` (integer, required): Restaurant ID

**Request Example**:
```bash
curl "http://localhost:8002/restaurants/1"
```

**Response**:
```json
{
  "id": 1,
  "name": "맛있는 치킨",
  "category": "치킨",
  "rating": 4.5
}
```

**Error Response**:
```json
{
  "error": "음식점을 찾을 수 없습니다"
}
```

---

#### POST /restaurants/
**Description**: Create a new restaurant
**Tags**: restaurants

**Query Parameters**:
- `name` (string, required): Restaurant name
- `category` (string, required): Food category
- `rating` (float, required): Rating score

**Request Example**:
```bash
curl -X POST "http://localhost:8002/restaurants/?name=행복한 치킨&category=치킨&rating=4.7"
```

**Response**:
```json
{
  "message": "음식점 생성 완료",
  "restaurant": {
    "id": 3,
    "name": "행복한 치킨",
    "category": "치킨",
    "rating": 4.7
  }
}
```

---

## Interactive API Documentation

All three implementations include automatic interactive API documentation:

- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

Simply navigate to these URLs in your browser after starting the server.

## Common Response Codes

- `200 OK`: Successful request
- `401 Unauthorized`: Missing or invalid authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error

## Notes

- All implementations use in-memory storage (data resets on restart)
- IDs are auto-generated incrementally
- No actual database connections are used (educational purposes)
