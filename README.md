# FastAPI Food Delivery - Learning Examples

A collection of FastAPI implementation patterns demonstrating different architectural approaches and design concepts for building web APIs.

## 📚 Overview

This repository contains **three different implementations** of a food delivery API, each showcasing different FastAPI features:

1. **Dependency Chain Pattern** (`main.py`) - Authentication & Authorization
2. **Reusable Dependencies Pattern** (`main_DEPEND.py`) - Pagination & Common Utilities
3. **Modular Router Pattern** (`main_ROUTER.py`) - Scalable Application Architecture

## 🎯 Learning Objectives

- **Dependency Injection**: Master FastAPI's dependency injection system
- **Authentication**: Implement token-based auth with role-based access control
- **Code Reusability**: Create reusable dependencies for common patterns
- **Modularity**: Organize large applications with APIRouter
- **Best Practices**: Learn FastAPI routing, validation, and documentation

## 🚀 Quick Start

### Prerequisites

- Python 3.7+
- pip package manager

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd food_delivery

# Install dependencies
pip install fastapi uvicorn
```

### Running the Applications

Each implementation runs on a different port:

```bash
# Pattern 1: Dependency Chain (port 8000)
uvicorn main:app --reload

# Pattern 2: Reusable Dependencies (port 8001)
uvicorn main_DEPEND:app --reload --port 8001

# Pattern 3: Modular Router (port 8002)
uvicorn main_ROUTER:app --reload --port 8002
```

### Access Interactive Documentation

Once running, visit these URLs in your browser:

- **Swagger UI**: `http://localhost:PORT/docs`
- **ReDoc**: `http://localhost:PORT/redoc`

## 📖 Implementation Patterns

### Pattern 1: Dependency Chain (main.py)

**Concepts**: Cascading dependencies, authentication, authorization

**Key Features**:
- Three-level dependency chain: `get_token → get_current_user → get_admin_user`
- Role-based access control (admin vs. regular user)
- HTTPException handling for auth failures

**Test Tokens**:
- `alice_token` - Admin user
- `bob_token` - Regular user

**Example Usage**:
```bash
# Public endpoint (no auth)
curl http://localhost:8000/

# User profile (auth required)
curl "http://localhost:8000/profile?token=alice_token"

# Admin endpoint (admin role required)
curl "http://localhost:8000/admin?token=alice_token"

# This will fail (403 Forbidden)
curl "http://localhost:8000/admin?token=bob_token"
```

**Dependency Chain Flow**:
```
Client Request
    ↓
get_token() - Validates token presence
    ↓
get_current_user() - Looks up user by token
    ↓
get_admin_user() - Verifies admin role
    ↓
Endpoint Handler
```

---

### Pattern 2: Reusable Dependencies (main_DEPEND.py)

**Concepts**: Reusable dependencies, pagination, parameter validation

**Key Features**:
- Single `pagination_params()` dependency used across multiple endpoints
- Automatic parameter validation (limit capped at 100)
- Consistent pagination across product listing and search

**Example Usage**:
```bash
# Get first 10 products
curl http://localhost:8001/products

# Get items 11-30
curl "http://localhost:8001/products?skip=10&limit=20"

# Search with pagination
curl "http://localhost:8001/search?keyword=상품1&skip=0&limit=5"

# Limit is automatically capped at 100
curl "http://localhost:8001/products?limit=200"  # Returns max 100
```

**Benefits**:
- DRY principle (Don't Repeat Yourself)
- Centralized validation logic
- Easy to maintain and extend

---

### Pattern 3: Modular Router (main_ROUTER.py)

**Concepts**: Code organization, separation of concerns, scalability

**Key Features**:
- Separate router modules for users and restaurants
- Automatic URL prefixing (`/users`, `/restaurants`)
- Organized by feature/domain rather than file type

**Project Structure**:
```
food_delivery/
├── main_ROUTER.py          # Main application
├── routers/
│   ├── __init__.py
│   ├── users.py           # User management endpoints
│   └── restaurants.py     # Restaurant endpoints
```

**Example Usage**:
```bash
# Users Router
curl http://localhost:8002/users/
curl http://localhost:8002/users/1
curl -X POST "http://localhost:8002/users/?name=박민수&email=park@example.com"

# Restaurants Router
curl http://localhost:8002/restaurants/
curl "http://localhost:8002/restaurants/search?category=치킨"
curl http://localhost:8002/restaurants/1
curl -X POST "http://localhost:8002/restaurants/?name=행복한 치킨&category=치킨&rating=4.7"
```

**Scalability Benefits**:
- Easy to add new feature modules
- Team members can work on separate routers
- Clear separation of concerns
- Maintainable as application grows

---

## 🔍 Key Concepts Explained

### Dependency Injection

FastAPI's dependency injection system allows you to:
- Reuse common logic across endpoints
- Create cascading dependencies (dependencies that depend on other dependencies)
- Validate and transform request data before it reaches your endpoint
- Implement authentication and authorization elegantly

**Example**:
```python
def get_token(token: str):
    if not token:
        raise HTTPException(status_code=401)
    return token

@app.get("/profile")
def get_profile(user: dict = Depends(get_current_user)):
    return user
```

### APIRouter

APIRouter allows you to organize your application into modules:
- Each router handles a specific domain (users, restaurants, etc.)
- Routers can have their own prefix and tags
- Multiple routers can be included in the main app

**Example**:
```python
# routers/users.py
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/")
def get_users():
    ...

# main.py
app.include_router(users.router)
```

### Route Ordering

**Important**: FastAPI matches routes in the order they're defined. Specific paths must come before parameterized paths.

**Correct**:
```python
@router.get("/search")  # Specific path first
def search():
    ...

@router.get("/{id}")    # Parameterized path second
def get_by_id():
    ...
```

**Incorrect**:
```python
@router.get("/{id}")    # This will match "search" as an ID!
def get_by_id():
    ...

@router.get("/search")  # This will never be reached
def search():
    ...
```

## 📝 API Documentation

Complete API documentation is available in [API_REFERENCE.md](./API_REFERENCE.md).

## 🧪 Testing Examples

### Testing Dependency Chain (Pattern 1)

```bash
# Success: Admin access
curl "http://localhost:8000/admin?token=alice_token"

# Fail: Regular user trying admin endpoint (403)
curl "http://localhost:8000/admin?token=bob_token"

# Fail: Missing token (401)
curl http://localhost:8000/profile

# Fail: Invalid token (401)
curl "http://localhost:8000/profile?token=invalid"
```

### Testing Pagination (Pattern 2)

```bash
# Default pagination (skip=0, limit=10)
curl http://localhost:8001/products

# Custom pagination
curl "http://localhost:8001/products?skip=20&limit=15"

# Test limit capping (will return max 100)
curl "http://localhost:8001/products?limit=500"

# Search with pagination
curl "http://localhost:8001/search?keyword=상품1&skip=5&limit=3"
```

### Testing Modular Router (Pattern 3)

```bash
# Test user CRUD
curl http://localhost:8002/users/
curl http://localhost:8002/users/1
curl -X POST "http://localhost:8002/users/?name=test&email=test@test.com"

# Test restaurant CRUD
curl http://localhost:8002/restaurants/
curl "http://localhost:8002/restaurants/search?category=피자"
curl http://localhost:8002/restaurants/2

# Test route ordering (search should work, not be interpreted as ID)
curl "http://localhost:8002/restaurants/search?category=치킨"
```

## 🎓 Learning Path

Recommended order for studying the examples:

1. **Start with Pattern 2** (main_DEPEND.py)
   - Simplest dependency concept
   - Easy to understand reusable patterns
   - Good introduction to FastAPI dependencies

2. **Move to Pattern 1** (main.py)
   - More complex dependency chains
   - Authentication and authorization
   - HTTPException handling

3. **Finish with Pattern 3** (main_ROUTER.py)
   - Application architecture
   - Code organization
   - Scalability patterns

## 🔧 Project Structure

```
food_delivery/
├── main.py                 # Pattern 1: Dependency chains
├── main_DEPEND.py         # Pattern 2: Reusable dependencies
├── main_ROUTER.py         # Pattern 3: Modular router
├── routers/
│   ├── __init__.py
│   ├── users.py          # User management router
│   └── restaurants.py    # Restaurant management router
├── API_REFERENCE.md      # Complete API documentation
└── README.md             # This file
```

## 💡 Key Takeaways

### Dependency Injection
- Dependencies can depend on other dependencies (chaining)
- Use dependencies for authentication, validation, and shared logic
- FastAPI automatically calls dependencies in the correct order

### Code Organization
- Use APIRouter for modular applications
- Organize by feature/domain, not file type
- Keep routers focused on single responsibility

### Best Practices
- Order routes from specific to general
- Use tags for API documentation grouping
- Leverage automatic validation and documentation
- Create reusable dependencies for common patterns

## 🚦 Common Pitfalls

1. **Route Ordering**: Always define specific paths before parameterized paths
2. **Token Parameter**: Remember to include query parameters in curl commands
3. **Port Conflicts**: Each example uses a different port (8000, 8001, 8002)
4. **In-Memory Data**: Data resets when server restarts (no persistence)

## 📚 Additional Resources

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [FastAPI Bigger Applications](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add more implementation patterns
- Improve documentation
- Add test cases
- Suggest better examples

## 📄 License

This project is created for educational purposes.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Happy Learning! 🎉**
