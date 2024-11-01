import pytest
from app.models.tool import Tool
from app.models.user import User
from app.utils.auth import get_password_hash
from app.schemas.tool import ToolCategory

def test_create_tool(client, auth_headers, db_session):
    """测试创建工具"""
    tool_data = {
        "name": "Test Tool",
        "description": "Test Description",
        "url": "https://example.com",
        "icon": "🔧",
        "category": ToolCategory.AI
    }
    
    response = client.post(
        "/api/tools/",
        json=tool_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tool_data["name"]
    assert data["description"] == tool_data["description"]
    assert data["url"] == tool_data["url"]
    assert data["icon"] == tool_data["icon"]
    assert data["category"] == tool_data["category"]
    assert "id" in data
    assert "user_id" in data

def test_get_tools(client, auth_headers, db_session, test_user):
    """测试获取工具列表"""
    # 创建测试工具
    tools = [
        Tool(
            name=f"Tool {i}",
            description=f"Description {i}",
            url=f"https://example{i}.com",
            category=ToolCategory.AI,
            user_id=test_user.id
        )
        for i in range(3)
    ]
    for tool in tools:
        db_session.add(tool)
    db_session.commit()
    
    # 测试不同的查询参数
    test_cases = [
        {"params": {}, "expected_count": 3},
        {"params": {"category": "ai"}, "expected_count": 3},
        {"params": {"category": "prompt"}, "expected_count": 0},
        {"params": {"search": "Tool 1"}, "expected_count": 1},
    ]
    
    for case in test_cases:
        response = client.get(
            "/api/tools/",
            params=case["params"],
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == case["expected_count"]

def test_get_tool(client, auth_headers, db_session, test_user):
    """测试获取单个工具"""
    tool = Tool(
        name="Test Tool",
        description="Test Description",
        url="https://example.com",
        category=ToolCategory.AI,
        user_id=test_user.id
    )
    db_session.add(tool)
    db_session.commit()
    
    response = client.get(
        f"/api/tools/{tool.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == tool.name
    assert data["description"] == tool.description
    assert data["url"] == tool.url
    assert data["category"] == tool.category

def test_update_tool(client, auth_headers, db_session, test_user):
    """测试更新工具"""
    tool = Tool(
        name="Test Tool",
        description="Test Description",
        url="https://example.com",
        category=ToolCategory.AI,
        user_id=test_user.id
    )
    db_session.add(tool)
    db_session.commit()
    
    update_data = {
        "name": "Updated Tool",
        "description": "Updated Description",
        "url": "https://updated.com",
        "category": ToolCategory.PROMPT
    }
    
    response = client.put(
        f"/api/tools/{tool.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["url"] == update_data["url"]
    assert data["category"] == update_data["category"]

def test_delete_tool(client, auth_headers, db_session, test_user):
    """测试删除工具"""
    tool = Tool(
        name="Test Tool",
        description="Test Description",
        url="https://example.com",
        category=ToolCategory.AI,
        user_id=test_user.id
    )
    db_session.add(tool)
    db_session.commit()
    
    response = client.delete(
        f"/api/tools/{tool.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 验证工具已被删除
    tool = db_session.query(Tool).filter(Tool.id == tool.id).first()
    assert tool is None

def test_tool_permissions(client, auth_headers, db_session):
    """测试工具权限"""
    # 创建另一个用户
    other_user = User(
        username="otheruser",
        email="other@example.com",
        hashed_password=get_password_hash("otherpassword")
    )
    db_session.add(other_user)
    db_session.commit()
    
    # 创建属于其他用户的工具
    tool = Tool(
        name="Other's Tool",
        description="Other's Description",
        url="https://other.com",
        category=ToolCategory.AI,
        user_id=other_user.id
    )
    db_session.add(tool)
    db_session.commit()
    
    # 测试访问其他用户的工具
    endpoints = [
        ("GET", f"/api/tools/{tool.id}"),
        ("PUT", f"/api/tools/{tool.id}"),
        ("DELETE", f"/api/tools/{tool.id}")
    ]
    
    for method, endpoint in endpoints:
        response = client.request(
            method,
            endpoint,
            headers=auth_headers,
            json={"name": "Updated"} if method == "PUT" else None
        )
        assert response.status_code == 404

def test_invalid_tool_data(client, auth_headers):
    """测试无效的工具数据"""
    # 测试缺少必需字段
    response = client.post(
        "/api/tools/",
        json={},
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # 测试无效的 URL
    response = client.post(
        "/api/tools/",
        json={
            "name": "Test Tool",
            "description": "Test Description",
            "url": "not-a-url",
            "category": ToolCategory.AI
        },
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # 测试无效的分类
    response = client.post(
        "/api/tools/",
        json={
            "name": "Test Tool",
            "description": "Test Description",
            "url": "https://example.com",
            "category": "invalid-category"
        },
        headers=auth_headers
    )
    assert response.status_code == 422 