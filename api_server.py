"""
간단한 REST API 서버 (stdlib만 사용)
"""

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import uuid
from datetime import datetime


# In-memory database
DB = {
    "users": {},
    "posts": {},
}


def generate_id():
    return str(uuid.uuid4())[:8]


class APIHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200, content_type="application/json"):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _read_body(self):
        content_length = int(self.headers.get("Content-Length", 0))
        if content_length == 0:
            return {}
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    def _respond(self, data, status=200):
        self._set_headers(status)
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def _error(self, message, status=400):
        self._respond({"error": message}, status)

    def do_OPTIONS(self):
        self._set_headers(204)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        if path == "/api/users":
            users = list(DB["users"].values())
            search = params.get("search", [None])[0]
            if search:
                users = [u for u in users if search.lower() in u["name"].lower()]
            self._respond({"users": users, "count": len(users)})

        elif path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            user = DB["users"].get(user_id)
            if user:
                self._respond(user)
            else:
                self._error("사용자를 찾을 수 없습니다", 404)

        elif path == "/api/posts":
            posts = list(DB["posts"].values())
            author = params.get("author", [None])[0]
            if author:
                posts = [p for p in posts if p["author_id"] == author]
            posts.sort(key=lambda x: x["created_at"], reverse=True)
            self._respond({"posts": posts, "count": len(posts)})

        elif path.startswith("/api/posts/"):
            post_id = path.split("/")[-1]
            post = DB["posts"].get(post_id)
            if post:
                self._respond(post)
            else:
                self._error("게시글을 찾을 수 없습니다", 404)

        elif path == "/api/stats":
            self._respond({
                "users": len(DB["users"]),
                "posts": len(DB["posts"]),
                "server_time": datetime.now().isoformat(),
            })

        elif path == "/health":
            self._respond({"status": "ok"})

        else:
            self._error("엔드포인트를 찾을 수 없습니다", 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        try:
            body = self._read_body()
        except json.JSONDecodeError:
            self._error("잘못된 JSON 형식입니다")
            return

        if path == "/api/users":
            name = body.get("name")
            email = body.get("email")
            if not name or not email:
                self._error("name과 email은 필수입니다")
                return

            user_id = generate_id()
            user = {
                "id": user_id,
                "name": name,
                "email": email,
                "bio": body.get("bio", ""),
                "created_at": datetime.now().isoformat(),
            }
            DB["users"][user_id] = user
            self._respond(user, 201)

        elif path == "/api/posts":
            title = body.get("title")
            content = body.get("content")
            author_id = body.get("author_id")

            if not title or not content:
                self._error("title과 content는 필수입니다")
                return

            if author_id and author_id not in DB["users"]:
                self._error("존재하지 않는 사용자입니다", 404)
                return

            post_id = generate_id()
            post = {
                "id": post_id,
                "title": title,
                "content": content,
                "author_id": author_id,
                "likes": 0,
                "tags": body.get("tags", []),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
            }
            DB["posts"][post_id] = post
            self._respond(post, 201)

        else:
            self._error("엔드포인트를 찾을 수 없습니다", 404)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        try:
            body = self._read_body()
        except json.JSONDecodeError:
            self._error("잘못된 JSON 형식입니다")
            return

        if path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            user = DB["users"].get(user_id)
            if not user:
                self._error("사용자를 찾을 수 없습니다", 404)
                return
            for key in ["name", "email", "bio"]:
                if key in body:
                    user[key] = body[key]
            self._respond(user)

        elif path.startswith("/api/posts/"):
            post_id = path.split("/")[-1]
            post = DB["posts"].get(post_id)
            if not post:
                self._error("게시글을 찾을 수 없습니다", 404)
                return
            for key in ["title", "content", "tags"]:
                if key in body:
                    post[key] = body[key]
            post["updated_at"] = datetime.now().isoformat()
            self._respond(post)

        elif path.startswith("/api/posts/") and path.endswith("/like"):
            post_id = path.split("/")[-2]
            post = DB["posts"].get(post_id)
            if not post:
                self._error("게시글을 찾을 수 없습니다", 404)
                return
            post["likes"] += 1
            self._respond(post)

        else:
            self._error("엔드포인트를 찾을 수 없습니다", 404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/")

        if path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            if user_id in DB["users"]:
                del DB["users"][user_id]
                self._respond({"message": "삭제 완료"})
            else:
                self._error("사용자를 찾을 수 없습니다", 404)

        elif path.startswith("/api/posts/"):
            post_id = path.split("/")[-1]
            if post_id in DB["posts"]:
                del DB["posts"][post_id]
                self._respond({"message": "삭제 완료"})
            else:
                self._error("게시글을 찾을 수 없습니다", 404)

        else:
            self._error("엔드포인트를 찾을 수 없습니다", 404)

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def seed_data():
    users = [
        {"name": "김철수", "email": "chulsoo@example.com", "bio": "백엔드 개발자"},
        {"name": "이영희", "email": "younghee@example.com", "bio": "프론트엔드 개발자"},
        {"name": "박민수", "email": "minsoo@example.com", "bio": "풀스택 개발자"},
    ]

    user_ids = []
    for u in users:
        uid = generate_id()
        DB["users"][uid] = {**u, "id": uid, "created_at": datetime.now().isoformat()}
        user_ids.append(uid)

    posts = [
        {"title": "파이썬 입문 가이드", "content": "파이썬은 배우기 쉬운 언어입니다...", "tags": ["python", "beginner"]},
        {"title": "REST API 설계 원칙", "content": "좋은 API를 설계하려면...", "tags": ["api", "design"]},
        {"title": "Git 사용법 정리", "content": "Git은 버전 관리 도구입니다...", "tags": ["git", "tutorial"]},
    ]

    for i, p in enumerate(posts):
        pid = generate_id()
        DB["posts"][pid] = {
            **p,
            "id": pid,
            "author_id": user_ids[i % len(user_ids)],
            "likes": 0,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
        }


if __name__ == "__main__":
    seed_data()
    port = 8080
    server = HTTPServer(("", port), APIHandler)
    print(f"API 서버 시작: http://localhost:{port}")
    print("엔드포인트:")
    print("  GET    /api/users")
    print("  GET    /api/users/:id")
    print("  POST   /api/users")
    print("  PUT    /api/users/:id")
    print("  DELETE /api/users/:id")
    print("  GET    /api/posts")
    print("  GET    /api/posts/:id")
    print("  POST   /api/posts")
    print("  PUT    /api/posts/:id")
    print("  DELETE /api/posts/:id")
    print("  PUT    /api/posts/:id/like")
    print("  GET    /api/stats")
    print("  GET    /health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n서버 종료")
        server.server_close()
