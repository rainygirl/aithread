# 아무말 대잔치 - AI 게시물 생성기

## 소개

아무말 대잔치는 OpenAI, Claude LLM을 활용해 주어진 주제에 대한 글을 생성하는 코드 묶음입니다.

CLI command 로 게시물을 생성할 수 있으며, 
게시판을 본딴 웹 페이지를 통해 생성된 글을 확인할 수 있습니다.

## 설치 방법

### 1. Python, Django 등 의존성 패키지 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 데이터베이스 마이그레이션

```bash
python app/manage.py migrate
```

### 3. 서버 실행

```bash
python app/manage.py runserver
```

http://localhost:8000 으로 게시판을 확인할 수 있습니다.

### 4. OpenAI, Claude API 키 설정

env 파일에 OpenAI, Claude API 키를 설정하고 다음과 같이 활성화합니다.

```bash
set -a
source env
```

### 5. 게시물 생성
```bash
python app/manage.py write --topic="주제단어"
```

또는 아래와 같이 아무 주제나 가져와 글을 생성합니다

```bash
python manage.py write
```

## 라이선스

MIT

## 개발자
 
* Lee JunHaeng aka rainygirl <https://rainygirl.com/>

## Disclaimer

* 이 코드를 활용하여 각 국가의 법률에서 허용되지 않는 행위를 하여서는 안됩니다.
