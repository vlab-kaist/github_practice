import re
import json
from collections import Counter
from urllib.parse import urlparse, urljoin


class SimpleHTMLParser:
    def __init__(self, html):
        self.html = html

    def get_title(self):
        match = re.search(r"<title>(.*?)</title>", self.html, re.DOTALL)
        return match.group(1).strip() if match else None

    def get_links(self):
        return re.findall(r'href=["\']([^"\']+)["\']', self.html)

    def get_images(self):
        return re.findall(r'src=["\']([^"\']+)["\']', self.html)

    def get_text(self):
        text = re.sub(r"<script.*?</script>", "", self.html, flags=re.DOTALL)
        text = re.sub(r"<style.*?</style>", "", text, flags=re.DOTALL)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text.strip()

    def get_meta_tags(self):
        metas = {}
        for match in re.finditer(
            r'<meta\s+(?:name|property)=["\']([^"\']+)["\']'
            r'\s+content=["\']([^"\']+)["\']',
            self.html,
        ):
            metas[match.group(1)] = match.group(2)
        return metas

    def get_headings(self):
        headings = {}
        for level in range(1, 7):
            pattern = f"<h{level}[^>]*>(.*?)</h{level}>"
            headings[f"h{level}"] = re.findall(pattern, self.html, re.DOTALL)
        return headings

    def word_frequency(self, top_n=20):
        text = self.get_text().lower()
        words = re.findall(r"\b[a-zA-Z가-힣]+\b", text)
        return Counter(words).most_common(top_n)


class URLAnalyzer:
    def __init__(self, url):
        self.parsed = urlparse(url)

    @property
    def scheme(self):
        return self.parsed.scheme

    @property
    def domain(self):
        return self.parsed.netloc

    @property
    def path(self):
        return self.parsed.path

    @property
    def query_params(self):
        params = {}
        if self.parsed.query:
            for param in self.parsed.query.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    params[key] = value
        return params

    def is_valid(self):
        return bool(self.parsed.scheme and self.parsed.netloc)

    def resolve(self, relative_url):
        return urljoin(str(self.parsed.geturl()), relative_url)

    def to_dict(self):
        return {
            "scheme": self.scheme,
            "domain": self.domain,
            "path": self.path,
            "query_params": self.query_params,
            "is_valid": self.is_valid(),
        }


class DataExtractor:
    @staticmethod
    def extract_emails(text):
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

    @staticmethod
    def extract_phones(text):
        patterns = [
            r"\d{3}-\d{3,4}-\d{4}",
            r"\d{2,3}-\d{3,4}-\d{4}",
            r"\(\d{2,3}\)\s*\d{3,4}-\d{4}",
        ]
        phones = []
        for pattern in patterns:
            phones.extend(re.findall(pattern, text))
        return phones

    @staticmethod
    def extract_dates(text):
        patterns = [
            r"\d{4}-\d{2}-\d{2}",
            r"\d{4}/\d{2}/\d{2}",
            r"\d{4}년\s*\d{1,2}월\s*\d{1,2}일",
        ]
        dates = []
        for pattern in patterns:
            dates.extend(re.findall(pattern, text))
        return dates

    @staticmethod
    def extract_prices(text):
        patterns = [
            r"₩[\d,]+",
            r"\$[\d,]+\.?\d*",
            r"[\d,]+원",
        ]
        prices = []
        for pattern in patterns:
            prices.extend(re.findall(pattern, text))
        return prices

    @staticmethod
    def extract_hashtags(text):
        return re.findall(r"#[a-zA-Z가-힣0-9_]+", text)

    @staticmethod
    def extract_mentions(text):
        return re.findall(r"@[a-zA-Z0-9_]+", text)


if __name__ == "__main__":
    sample_html = """
    <html>
    <head><title>테스트 페이지</title></head>
    <body>
        <h1>안녕하세요</h1>
        <h2>소개</h2>
        <p>이것은 테스트 페이지입니다.</p>
        <a href="https://example.com">링크1</a>
        <a href="/about">링크2</a>
        <img src="image.jpg">
    </body>
    </html>
    """

    parser = SimpleHTMLParser(sample_html)
    print(f"제목: {parser.get_title()}")
    print(f"링크: {parser.get_links()}")
    print(f"이미지: {parser.get_images()}")
    print(f"헤딩: {parser.get_headings()}")

    sample_text = """
    연락처: kim@example.com, 010-1234-5678
    날짜: 2024년 3월 15일, 2024-03-15
    가격: ₩50,000, $29.99, 15,000원
    태그: #파이썬 #코딩 #개발자
    멘션: @user1 @dev_team
    """

    extractor = DataExtractor()
    print(f"\n이메일: {extractor.extract_emails(sample_text)}")
    print(f"전화번호: {extractor.extract_phones(sample_text)}")
    print(f"날짜: {extractor.extract_dates(sample_text)}")
    print(f"가격: {extractor.extract_prices(sample_text)}")
    print(f"해시태그: {extractor.extract_hashtags(sample_text)}")
    print(f"멘션: {extractor.extract_mentions(sample_text)}")
