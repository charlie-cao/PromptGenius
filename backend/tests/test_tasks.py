import pytest
from app.models.task import Task
from app.models.user import User
from app.utils.auth import get_password_hash

def test_create_task(client, auth_headers, db_session):
    """测试创建任务"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }
    
    response = client.post(
        "/api/tasks/",
        json=task_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert data["completed"] == task_data["completed"]
    assert "id" in data
    assert "user_id" in data

def test_get_tasks(client, auth_headers, db_session, test_user):
    """测试获取任务列表"""
    # 创建测试任务
    tasks = [
        Task(title=f"Task {i}", user_id=test_user.id)
        for i in range(3)
    ]
    for task in tasks:
        db_session.add(task)
    db_session.commit()
    
    # 测试不同的查询参数
    test_cases = [
        {"params": {}, "expected_count": 3},
        {"params": {"search": "Task 1"}, "expected_count": 1},
        {"params": {"status": "completed"}, "expected_count": 0},
        {"params": {"status": "pending"}, "expected_count": 3},
        {"params": {"order_by": "title_asc"}, "expected_count": 3},
    ]
    
    for case in test_cases:
        response = client.get(
            "/api/tasks/",
            params=case["params"],
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == case["expected_count"]
        assert len(data["items"]) == case["expected_count"]

def test_get_task(client, auth_headers, db_session, test_user):
    """测试获取单个任务"""
    # 创建测试任务
    task = Task(title="Test Task", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.get(
        f"/api/tasks/{task.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task.title
    assert data["id"] == task.id

def test_update_task(client, auth_headers, db_session, test_user):
    """测试更新任务"""
    # 创建测试任务
    task = Task(title="Test Task", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()
    
    update_data = {
        "title": "Updated Task",
        "completed": True
    }
    
    response = client.put(
        f"/api/tasks/{task.id}",
        json=update_data,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["completed"] == update_data["completed"]

def test_delete_task(client, auth_headers, db_session, test_user):
    """测试删除任务"""
    # 创建测试任务
    task = Task(title="Test Task", user_id=test_user.id)
    db_session.add(task)
    db_session.commit()
    
    response = client.delete(
        f"/api/tasks/{task.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # 验证任务已被删除
    task = db_session.query(Task).filter(Task.id == task.id).first()
    assert task is None

def test_task_permissions(client, auth_headers, db_session):
    """测试任务权限"""
    # 创建另一个用户
    other_user = User(
        username="otheruser",
        email="other@example.com",
        hashed_password=get_password_hash("otherpassword")
    )
    db_session.add(other_user)
    db_session.commit()
    
    # 创建属于其他用户的任务
    task = Task(title="Other's Task", user_id=other_user.id)
    db_session.add(task)
    db_session.commit()
    
    # 测试访问其他用户的任务
    endpoints = [
        ("GET", f"/api/tasks/{task.id}"),
        ("PUT", f"/api/tasks/{task.id}"),
        ("DELETE", f"/api/tasks/{task.id}")
    ]
    
    for method, endpoint in endpoints:
        response = client.request(
            method,
            endpoint,
            headers=auth_headers,
            json={"title": "Updated"} if method == "PUT" else None
        )
        assert response.status_code == 404

def test_invalid_requests(client, auth_headers):
    """测试无效请求"""
    # 测试创建无效任务
    response = client.post(
        "/api/tasks/",
        json={},  # 缺少必需字段
        headers=auth_headers
    )
    assert response.status_code == 422
    
    # 测试访问不存在的任务
    response = client.get(
        "/api/tasks/999",
        headers=auth_headers
    )
    assert response.status_code == 404 