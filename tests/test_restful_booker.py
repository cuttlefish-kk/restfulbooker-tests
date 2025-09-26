import requests
import pytest

BASE = "https://restful-booker.herokuapp.com"   # 或 "http://localhost:3001" 如果你自己本地跑

def test_ping():
    r = requests.get(f"{BASE}/ping")
    assert r.status_code in (200, 201)
def test_fail():
    assert 1 == 2
def test_create_get_update_delete_booking():
    # 1. 创建 booking
    booking = {
        "firstname": "Auto",
        "lastname": "Tester",
        "totalprice": 123,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-01-01",
            "checkout": "2025-01-05"
        },
        "additionalneeds": "Breakfast"
    }
    r = requests.post(f"{BASE}/booking", json=booking)
    assert r.status_code == 200
    bookingid = r.json()["bookingid"]

    # 2. 查询 booking
    r2 = requests.get(f"{BASE}/booking/{bookingid}")
    assert r2.status_code == 200
    assert r2.json()["firstname"] == booking["firstname"]

    # 3. 获取 token
    auth = requests.post(f"{BASE}/auth", json={"username": "admin", "password": "password123"})
    assert auth.status_code == 200
    token = auth.json()["token"]

    # 4. 修改 booking
    updated = booking.copy()
    updated["firstname"] = "Updated"
    headers = {"Cookie": f"token={token}"}
    r3 = requests.put(f"{BASE}/booking/{bookingid}", json=updated, headers=headers)
    assert r3.status_code == 200
    assert r3.json()["firstname"] == "Updated"

    # 5. 删除 booking
    r4 = requests.delete(f"{BASE}/booking/{bookingid}", headers=headers)
    assert r4.status_code in (200, 201, 204)

    # 6. 再次查询，确认已删除
    r5 = requests.get(f"{BASE}/booking/{bookingid}")
    assert r5.status_code == 404
