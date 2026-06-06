"""
Simple FastAPI application example
Requires: fastapi, uvicorn
Run: uvicorn api_app:app --reload
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from logger import get_logger

logger = get_logger('api_app')

# Create FastAPI app
app = FastAPI(
    title='Test-01 API',
    description='Practical FastAPI application example',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)


# Data models
class User(BaseModel):
    """User model"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100, description='User name')
    email: str = Field(..., pattern=r'^[^@]+@[^@]+\.[^@]+$', description='User email')
    age: Optional[int] = Field(None, ge=0, le=150, description='User age')


class UserResponse(BaseModel):
    """User response model"""
    message: str
    user: Optional[User] = None
    users: Optional[List[User]] = None


# In-memory database (for demo)
users_db = []
next_id = 1


# Event handlers
@app.on_event('startup')
async def startup_event():
    """Run on application startup"""
    logger.info('API application starting up...')
    # Add sample data
    global next_id
    users_db.append(User(id=1, name='Alice', email='alice@example.com', age=30))
    users_db.append(User(id=2, name='Bob', email='bob@example.com', age=25))
    next_id = 3
    logger.info(f'Loaded {len(users_db)} sample users')


@app.on_event('shutdown')
async def shutdown_event():
    """Run on application shutdown"""
    logger.info('API application shutting down...')


# Health check
@app.get('/', tags=['Health'])
async def root():
    """Root endpoint - health check"""
    return {
        'status': 'ok',
        'app_name': 'Test-01 API',
        'version': '1.0.0',
        'timestamp': datetime.datetime.now().isoformat()
    }


@app.get('/health', tags=['Health'])
async def health_check():
    """Health check endpoint"""
    return {'status': 'healthy'}


# User endpoints
@app.get('/users', response_model=UserResponse, tags=['Users'])
async def get_users(skip: int = 0, limit: int = 10):
    """
    Get all users with pagination
    
    - **skip**: Number of users to skip
    - **limit**: Maximum number of users to return (max 100)
    """
    limit = min(limit, 100)  # Cap at 100
    users = users_db[skip:skip + limit]
    return UserResponse(message=f'Found {len(users)} users', users=users)


@app.get('/users/{user_id}', response_model=UserResponse, tags=['Users'])
async def get_user(user_id: int):
    """
    Get user by ID
    
    - **user_id**: User ID
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return UserResponse(message='User found', user=user)


@app.post('/users', response_model=UserResponse, status_code=201, tags=['Users'])
async def create_user(user: User):
    """
    Create new user
    
    - **user**: User data
    """
    global next_id
    user.id = next_id
    next_id += 1
    users_db.append(user)
    logger.info(f'Created user: {user.name} (ID: {user.id})')
    return UserResponse(message='User created successfully', user=user)


@app.put('/users/{user_id}', response_model=UserResponse, tags=['Users'])
async def update_user(user_id: int, user_update: User):
    """
    Update user by ID
    
    - **user_id**: User ID
    - **user_update**: Updated user data
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    
    user.name = user_update.name
    user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age
    
    logger.info(f'Updated user: {user.name} (ID: {user.id})')
    return UserResponse(message='User updated successfully', user=user)


@app.delete('/users/{user_id}', response_model=UserResponse, tags=['Users'])
async def delete_user(user_id: int):
    """
    Delete user by ID
    
    - **user_id**: User ID
    """
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    
    users_db = [u for u in users_db if u.id != user_id]
    logger.info(f'Deleted user: {user.name} (ID: {user.id})')
    return UserResponse(message='User deleted successfully', user=user)


# Stats endpoint
@app.get('/stats', tags=['Statistics'])
async def get_stats():
    """Get user statistics"""
    if not users_db:
        return {'total_users': 0, 'avg_age': 0}
    
    total = len(users_db)
    avg_age = sum(u.age for u in users_db if u.age) / total
    
    return {
        'total_users': total,
        'avg_age': round(avg_age, 2),
        'min_age': min(u.age for u in users_db if u.age) if any(u.age for u in users_db) else None,
        'max_age': max(u.age for u in users_db if u.age) if any(u.age for u in users_db) else None
    }


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f'Unhandled exception: {exc}')
    return JSONResponse(
        status_code=500,
        content={'message': 'Internal server error'}
    )


# Run instruction
if __name__ == '__main__':
    import uvicorn
    print('=' * 60)
    print('Starting FastAPI application...')
    print('=' * 60)
    print('\nAPI Documentation:')
    print('  - Swagger UI: http://localhost:8000/docs')
    print('  - ReDoc: http://localhost:8000/redoc')
    print('\nAPI Endpoints:')
    print('  - GET  /           - Health check')
    print('  - GET  /users      - Get all users')
    print('  - GET  /users/{id} - Get user by ID')
    print('  - POST /users      - Create user')
    print('  - PUT  /users/{id} - Update user')
    print('  - DEL  /users/{id} - Delete user')
    print('  - GET  /stats      - Get statistics')
    print('\n' + '=' * 60)
    
    uvicorn.run(app, host='0.0.0.0', port=8000)
