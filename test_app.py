"""Run: python test_app.py"""
from app import app, compact

client = app.test_client()

home = client.get("/")
assert home.status_code == 200
assert b"Dune: Part Two" in home.data and b"Top Rated Albums" in home.data

assert compact(142000) == "142K" and compact(2_100_000) == "2.1M" and compact(48) == "48"

signup = lambda email, password: client.post("/signup", data={"name": "Test User", "email": email, "password": password})
assert signup("t@example.com", "short").status_code == 400
assert signup("t@example.com", "longenough").status_code == 302
assert b"Test User" in client.get("/").data  # signup logs you in
assert signup("T@EXAMPLE.com", "longenough").status_code == 400  # duplicate, case-insensitive
assert b"already exists" in signup("t@example.com", "longenough").data

assert client.post("/logout").status_code == 302
assert b"Test User" not in client.get("/").data

login = lambda email, password: client.post("/login", data={"email": email, "password": password})
assert login("t@example.com", "wrongpassword").status_code == 400
assert login("nobody@example.com", "longenough").status_code == 400
assert login("T@example.com", "longenough").status_code == 302
assert b"Test User" in client.get("/").data

print("ok")
