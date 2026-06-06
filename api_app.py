"""
用户管理系统 API - 全面中文化版本
Requires: fastapi, uvicorn
Run: uvicorn api_app:app --reload

特性：
- 业务内容全面中文化（标题、描述、字段说明、示例）
- Swagger UI 框架全面中文化（按钮、标签、提示文本）
- 使用 MutationObserver 动态替换所有英文界面文本
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
from logger import get_logger

logger = get_logger('api_app')

# 创建 FastAPI 应用实例（中文化配置）
app = FastAPI(
    title='用户管理系统 API',
    description='这是一个用于演示的 CRUD 接口文档。提供用户的增删改查功能，以及统计信息查询。',
    version='1.0.0',
    docs_url=None,  # 禁用默认 docs 路由，我们将自定义
    redoc_url='/redoc',  # ReDoc 保留（可选也中文化）
    openapi_tags=[
        {
            'name': '用户管理',
            'description': '用户信息的增删改查操作',
        },
        {
            'name': '健康检查',
            'description': '系统健康状态检查',
        },
        {
            'name': '统计信息',
            'description': '用户数据统计',
        },
    ],
)


# ==================== Pydantic 数据模型（中文化） ====================


class User(BaseModel):
    """用户数据模型"""
    id: Optional[int] = Field(None, description='用户ID（自动生成）', example=1)
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description='用户姓名（1-100个字符）',
        example='张三',
    )
    email: str = Field(
        ...,
        pattern=r'^[^@]+@[^@]+\.[^@]+$',
        description='用户邮箱（必须符合邮箱格式）',
        example='zhangsan@example.com',
    )
    age: Optional[int] = Field(
        None,
        ge=0,
        le=150,
        description='用户年龄（0-150岁之间）',
        example=25,
    )

    class Config:
        """Pydantic 模型配置"""
        json_schema_extra = {
            'examples': [
                {
                    'summary': '创建用户示例',
                    'description': '典型的用户创建请求',
                    'value': {
                        'name': '张三',
                        'email': 'zhangsan@example.com',
                        'age': 25,
                    },
                }
            ]
        }


class UserResponse(BaseModel):
    """用户响应模型"""
    message: str = Field(..., description='操作结果消息', example='用户创建成功')
    user: Optional[User] = Field(None, description='单个用户信息')
    users: Optional[List[User]] = Field(None, description='用户列表')

    class Config:
        json_schema_extra = {
            'examples': [
                {
                    'summary': '成功响应示例',
                    'value': {
                        'message': '用户创建成功',
                        'user': {
                            'id': 1,
                            'name': '张三',
                            'email': 'zhangsan@example.com',
                            'age': 25,
                        },
                    },
                }
            ]
        }


# ==================== 内存数据库（演示用） ====================

# 模拟数据库
users_db = []
next_id = 1


# ==================== 事件处理器 ====================


@app.on_event('startup')
async def startup_event():
    """应用启动时执行"""
    logger.info('API 应用启动中...')

    # 添加示例数据
    global next_id
    users_db.append(User(id=1, name='张三', email='zhangsan@example.com', age=30))
    users_db.append(User(id=2, name='李四', email='lisi@example.com', age=25))
    next_id = 3

    logger.info(f'已加载 {len(users_db)} 条示例用户数据')


@app.on_event('shutdown')
async def shutdown_event():
    """应用关闭时执行"""
    logger.info('API 应用关闭中...')


# ==================== 自定义 Swagger UI 路由（核心中文化） ====================


@app.get('/docs', include_in_schema=False)
async def custom_swagger_ui_html():
    """
    自定义 Swagger UI 页面（全面中文化）
    通过注入 JavaScript 动态替换所有英文界面文本
    """
    # 1. 先接收 get_swagger_ui_html() 返回的 response 对象
    response = get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f'{app.title} - API 文档',
        swagger_js_url='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js',
        swagger_css_url='https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css',
    )

    # 2. 通过 response.body.decode('utf-8') 获取 HTML 字符串内容
    html_content = response.body.decode('utf-8')

    # 注入中文化 JavaScript 代码
    chinese_js = """
    <script>
    // Swagger UI 中文化脚本
    (function() {
        'use strict';
        
        // 文本替换映射表
        const textReplacements = {
            // 顶部按钮和链接
            'Try it out': '试一试',
            'Execute': '执行',
            'Clear': '清除',
            'Cancel': '取消',
            'Authorize': '授权',
            'Logout': '退出登录',
            'Select a file': '选择文件',
            'Download file': '下载文件',
            
            // 响应区域
            'Responses': '响应结果',
            'Response': '响应',
            'Response body': '响应体',
            'Response headers': '响应头',
            'Code': '状态码',
            'Details': '详情',
            'No response body': '无响应体',
            'No responses': '暂无响应',
            'Example': '示例',
            'Examples': '示例',
            'Schema': '数据结构',
            'Model': '模型',
            'Model Schema': '模型数据结构',
            
            // 参数区域
            'Parameters': '参数',
            'Parameter': '参数',
            'Name': '名称',
            'Value': '值',
            'Description': '描述',
            'Type': '类型',
            'Required': '必填',
            'Optional': '可选',
            
            // 认证区域
            'Authorize': '授权',
            'Available authorizations': '可用的授权方式',
            'Authorization': '授权',
            'API key': 'API 密钥',
            'Bearer': 'Bearer 令牌',
            
            // 其他界面文本
            'Filters': '过滤器',
            'Search': '搜索',
            'Show/Hide': '显示/隐藏',
            'Expand all': '展开全部',
            'Collapse all': '折叠全部',
            'List operations': '操作列表',
            'List operations in alphabetical order': '按字母顺序列出操作',
            'Group operations by tag': '按标签分组操作',
            
            // HTTP 方法和描述
            'GET': 'GET',
            'POST': 'POST',
            'PUT': 'PUT',
            'DELETE': 'DELETE',
            'PATCH': 'PATCH',
            'HEAD': 'HEAD',
            'OPTIONS': 'OPTIONS',
            
            // 错误和状态消息
            'Error': '错误',
            'Success': '成功',
            'Warning': '警告',
            'Info': '信息',
            
            // 分页和计数
            'Showing': '显示',
            'of': '/',
            'results': '条结果',
            
            // 按钮和链接
            'Submit': '提交',
            'Reset': '重置',
            'Close': '关闭',
            'Save': '保存',
            'Edit': '编辑',
            'Delete': '删除',
            'Cancel': '取消',
            'Confirm': '确认',
        };
        
        // 使用 MutationObserver 监听 DOM 变化
        function replaceTextInNode(node) {
            if (node.nodeType === Node.TEXT_NODE) {
                let text = node.textContent.trim();
                if (textReplacements[text]) {
                    node.textContent = node.textContent.replace(text, textReplacements[text]);
                }
            } else if (node.nodeType === Node.ELEMENT_NODE && node.childNodes) {
                for (let child of node.childNodes) {
                    replaceTextInNode(child);
                }
            }
        }
        
        // 创建 MutationObserver 监听 DOM 变化
        function observeDOM() {
            const observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.addedNodes) {
                        mutation.addedNodes.forEach(function(node) {
                            replaceTextInNode(node);
                        });
                    }
                });
                
                // 也检查现有节点
                replaceTextInNode(document.body);
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true,
            });
        }
        
        // 定时检查（备用方案，确保动态加载的内容也能被替换）
        function periodicCheck() {
            replaceTextInNode(document.body);
        }
        
        // 页面加载完成后执行
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                observeDOM();
                setInterval(periodicCheck, 1000);  // 每秒检查一次
            });
        } else {
            observeDOM();
            setInterval(periodicCheck, 1000);
        }
        
        // 初始执行一次
        setTimeout(function() {
            replaceTextInNode(document.body);
        }, 500);
        
        console.log('[Swagger UI 中文化] 脚本已加载');
    })();
    </script>
    """

    # 3. 对字符串使用 .replace() 注入中文 JS 代码
    # 在 </body> 标签前注入 JavaScript
    modified_html = html_content.replace('</body>', chinese_js + '\n</body>')

    # 4. 返回一个新的 HTMLResponse(content=修改后的字符串)
    return HTMLResponse(content=modified_html, status_code=200)


# ==================== 路由定义（全面中文化） ====================


# 根路由 - 健康检查
@app.get(
    '/',
    tags=['健康检查'],
    summary='根路径 - 健康检查',
    description='检查 API 服务是否正常运行，返回服务基本信息。',
    response_description='服务健康状态信息',
)
async def root():
    """根路径 - 健康检查"""
    return {
        'status': 'ok',
        'app_name': '用户管理系统 API',
        'version': '1.0.0',
        'timestamp': datetime.datetime.now().isoformat(),
        'message': '服务运行正常',
    }


# 健康检查端点
@app.get(
    '/health',
    tags=['健康检查'],
    summary='健康检查',
    description='详细的健康检查端点，用于监控系统状态。',
    response_description='健康状态',
)
async def health_check():
    """健康检查端点"""
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
    }


# 获取所有用户（分页）
@app.get(
    '/users',
    response_model=UserResponse,
    tags=['用户管理'],
    summary='获取用户列表',
    description='''
    获取所有用户信息的列表，支持分页查询。
    
    **参数说明：**
    - `skip`: 跳过的用户数量（用于分页）
    - `limit`: 返回的最大用户数量（最大 100）
    
    **返回：**
    - 用户列表
    - 查询结果消息
    ''',
    response_description='包含用户列表的响应对象',
)
async def get_users(skip: int = 0, limit: int = 10):
    """
    获取所有用户（支持分页）
    
    - **skip**: 跳过的用户数量
    - **limit**: 返回的最大用户数量（最大 100）
    """
    limit = min(limit, 100)  # 限制最大 100
    users = users_db[skip : skip + limit]
    return UserResponse(message=f'找到 {len(users)} 个用户', users=users)


# 根据 ID 获取用户
@app.get(
    '/users/{user_id}',
    response_model=UserResponse,
    tags=['用户管理'],
    summary='获取用户详情',
    description='''
    根据用户 ID 获取单个用户的详细信息。
    
    **参数说明：**
    - `user_id`: 用户 ID（路径参数）
    
    **返回：**
    - 用户信息（如果存在）
    - 404 错误（如果用户不存在）
    ''',
    response_description='包含单个用户信息的响应对象',
)
async def get_user(user_id: int):
    """
    根据 ID 获取用户
    
    - **user_id**: 用户 ID
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'用户 {user_id} 不存在')
    return UserResponse(message='找到用户', user=user)


# 创建新用户
@app.post(
    '/users',
    response_model=UserResponse,
    status_code=201,
    tags=['用户管理'],
    summary='创建新用户',
    description='''
    创建一个新的用户账号。
    
    **请求体：**
    - `name`: 用户姓名（必填，1-100字符）
    - `email`: 用户邮箱（必填，必须符合邮箱格式）
    - `age`: 用户年龄（可选，0-150之间）
    
    **返回：**
    - 创建成功的用户信息
    - 201 状态码
    ''',
    response_description='包含新创建用户信息的响应对象',
)
async def create_user(user: User):
    """
    创建新用户
    
    - **user**: 用户数据
    """
    global next_id
    user.id = next_id
    next_id += 1
    users_db.append(user)
    logger.info(f'创建用户: {user.name} (ID: {user.id})')
    return UserResponse(message='用户创建成功', user=user)


# 更新用户信息
@app.put(
    '/users/{user_id}',
    response_model=UserResponse,
    tags=['用户管理'],
    summary='更新用户信息',
    description='''
    根据用户 ID 更新用户信息。
    
    **参数说明：**
    - `user_id`: 用户 ID（路径参数）
    - `user_update`: 更新的用户数据（请求体）
    
    **返回：**
    - 更新后的用户信息
    - 404 错误（如果用户不存在）
    ''',
    response_description='包含更新后用户信息的响应对象',
)
async def update_user(user_id: int, user_update: User):
    """
    根据 ID 更新用户
    
    - **user_id**: 用户 ID
    - **user_update**: 更新的用户数据
    """
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'用户 {user_id} 不存在')

    user.name = user_update.name
    user.email = user_update.email
    if user_update.age is not None:
        user.age = user_update.age

    logger.info(f'更新用户: {user.name} (ID: {user.id})')
    return UserResponse(message='用户更新成功', user=user)


# 删除用户
@app.delete(
    '/users/{user_id}',
    response_model=UserResponse,
    tags=['用户管理'],
    summary='删除用户',
    description='''
    根据用户 ID 删除用户账号。
    
    **参数说明：**
    - `user_id`: 用户 ID（路径参数）
    
    **返回：**
    - 删除的用户信息
    - 404 错误（如果用户不存在）
    ''',
    response_description='包含被删除用户信息的响应对象',
)
async def delete_user(user_id: int):
    """
    根据 ID 删除用户
    
    - **user_id**: 用户 ID
    """
    global users_db
    user = next((u for u in users_db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail=f'用户 {user_id} 不存在')

    users_db = [u for u in users_db if u.id != user_id]
    logger.info(f'删除用户: {user.name} (ID: {user.id})')
    return UserResponse(message='用户删除成功', user=user)


# 获取统计信息
@app.get(
    '/stats',
    tags=['统计信息'],
    summary='获取用户统计信息',
    description='''
    获取用户数据的统计信息，包括总用户数、平均年龄、最小年龄、最大年龄。
    
    **返回：**
    - `total_users`: 总用户数
    - `avg_age`: 平均年龄
    - `min_age`: 最小年龄
    - `max_age`: 最大年龄
    ''',
    response_description='用户统计信息',
)
async def get_stats():
    """获取用户统计信息"""
    if not users_db:
        return {
            'total_users': 0,
            'avg_age': 0,
            'min_age': None,
            'max_age': None,
            'message': '暂无用户数据',
        }

    total = len(users_db)
    users_with_age = [u.age for u in users_db if u.age is not None]

    if not users_with_age:
        return {
            'total_users': total,
            'avg_age': 0,
            'min_age': None,
            'max_age': None,
            'message': '部分用户未设置年龄',
        }

    avg_age = sum(users_with_age) / len(users_with_age)

    return {
        'total_users': total,
        'avg_age': round(avg_age, 2),
        'min_age': min(users_with_age),
        'max_age': max(users_with_age),
        'message': '统计信息获取成功',
    }


# ==================== 错误处理器 ====================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """自定义 HTTP 异常处理器"""
    return JSONResponse(
        status_code=exc.status_code,
        content={'message': exc.detail, 'status_code': exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """全局异常处理器"""
    logger.error(f'未处理的异常: {exc}')
    return JSONResponse(
        status_code=500,
        content={'message': '服务器内部错误，请稍后重试', 'detail': str(exc)},
    )


# ==================== 运行说明 ====================

if __name__ == '__main__':
    import uvicorn

    print('=' * 60)
    print('启动 FastAPI 应用...')
    print('=' * 60)
    print('\nAPI 文档（已中文化）:')
    print('  - Swagger UI: http://localhost:8000/docs')
    print('  - ReDoc: http://localhost:8000/redoc')
    print('\nAPI 端点:')
    print('  - GET  /           - 健康检查')
    print('  - GET  /users      - 获取所有用户')
    print('  - GET  /users/{id} - 根据 ID 获取用户')
    print('  - POST /users      - 创建用户')
    print('  - PUT  /users/{id} - 更新用户')
    print('  - DEL  /users/{id} - 删除用户')
    print('  - GET  /stats      - 获取统计信息')
    print('\n' + '=' * 60)
    print('提示：访问 http://localhost:8000/docs 查看中文化 API 文档')
    print('=' * 60)

    uvicorn.run(app, host='0.0.0.0', port=8000)
