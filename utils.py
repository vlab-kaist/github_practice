import hashlib
import random
import string
import re
from datetime import datetime, timedelta
from functools import wraps
import time


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[{func.__name__}] {elapsed:.4f}초 소요")
        return result
    return wrapper


def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"[retry] {attempt+1}/{max_attempts} 실패: {e}")
                    time.sleep(delay)
        return wrapper
    return decorator


def memoize(func):
    cache = {}
    @wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper


def generate_password(length=16, use_special=True):
    chars = string.ascii_letters + string.digits
    if use_special:
        chars += string.punctuation
    password = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
    ]
    if use_special:
        password.append(random.choice(string.punctuation))
    password.extend(random.choice(chars) for _ in range(length - len(password)))
    random.shuffle(password)
    return "".join(password)


def hash_string(text, algorithm="sha256"):
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    if algorithm not in algorithms:
        raise ValueError(f"지원하지 않는 알고리즘: {algorithm}")
    return algorithms[algorithm](text.encode()).hexdigest()


def validate_email(email):
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def validate_phone(phone):
    pattern = r"^0\d{1,2}-\d{3,4}-\d{4}$"
    return bool(re.match(pattern, phone))


def validate_password_strength(password):
    checks = {
        "length": len(password) >= 8,
        "uppercase": bool(re.search(r"[A-Z]", password)),
        "lowercase": bool(re.search(r"[a-z]", password)),
        "digit": bool(re.search(r"\d", password)),
        "special": bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)),
    }
    score = sum(checks.values())
    if score <= 2:
        strength = "약함"
    elif score <= 3:
        strength = "보통"
    elif score <= 4:
        strength = "강함"
    else:
        strength = "매우 강함"
    return {"checks": checks, "score": score, "strength": strength}


def slugify(text):
    text = text.lower().strip()
    text = re.sub(r"[^\w\s가-힣-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def truncate(text, max_length=100, suffix="..."):
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def flatten(nested_list):
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


def chunk_list(lst, size):
    return [lst[i : i + size] for i in range(0, len(lst), size)]


def deep_merge(dict1, dict2):
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def format_bytes(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    return f"{size:.2f} {units[unit_index]}"


def format_number(num):
    if num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}B"
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"
    return str(num)


def time_ago(dt):
    now = datetime.now()
    diff = now - dt
    seconds = diff.total_seconds()

    if seconds < 60:
        return "방금 전"
    elif seconds < 3600:
        return f"{int(seconds // 60)}분 전"
    elif seconds < 86400:
        return f"{int(seconds // 3600)}시간 전"
    elif seconds < 604800:
        return f"{int(seconds // 86400)}일 전"
    elif seconds < 2592000:
        return f"{int(seconds // 604800)}주 전"
    elif seconds < 31536000:
        return f"{int(seconds // 2592000)}개월 전"
    else:
        return f"{int(seconds // 31536000)}년 전"


class Color:
    RESET = "\033[0m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"

    @classmethod
    def red(cls, text):
        return f"{cls.RED}{text}{cls.RESET}"

    @classmethod
    def green(cls, text):
        return f"{cls.GREEN}{text}{cls.RESET}"

    @classmethod
    def yellow(cls, text):
        return f"{cls.YELLOW}{text}{cls.RESET}"

    @classmethod
    def blue(cls, text):
        return f"{cls.BLUE}{text}{cls.RESET}"

    @classmethod
    def bold(cls, text):
        return f"{cls.BOLD}{text}{cls.RESET}"


if __name__ == "__main__":
    print("=== 비밀번호 생성 ===")
    for _ in range(5):
        pw = generate_password()
        strength = validate_password_strength(pw)
        print(f"  {pw} -> {strength['strength']}")

    print("\n=== 해싱 ===")
    text = "hello world"
    for algo in ["md5", "sha1", "sha256"]:
        print(f"  {algo}: {hash_string(text, algo)}")

    print("\n=== 유효성 검사 ===")
    print(f"  email valid: {validate_email('test@example.com')}")
    print(f"  email invalid: {validate_email('not-email')}")
    print(f"  phone valid: {validate_phone('010-1234-5678')}")

    print(f"\n=== 포맷팅 ===")
    print(f"  bytes: {format_bytes(1234567890)}")
    print(f"  number: {format_number(1234567)}")
    print(f"  time: {time_ago(datetime.now() - timedelta(hours=3))}")
    print(f"  slug: {slugify('Hello World 안녕하세요!')}")
    print(f"  truncate: {truncate('이것은 매우 긴 문자열입니다 테스트용', 15)}")

    print(f"\n=== 리스트 유틸 ===")
    print(f"  flatten: {flatten([1, [2, 3], [4, [5, 6]]])}")
    print(f"  chunk: {chunk_list([1,2,3,4,5,6,7,8,9], 3)}")

    print(f"\n=== 딕셔너리 머지 ===")
    d1 = {"a": 1, "b": {"x": 10, "y": 20}}
    d2 = {"b": {"y": 30, "z": 40}, "c": 3}
    print(f"  {deep_merge(d1, d2)}")
