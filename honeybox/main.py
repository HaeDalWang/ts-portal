"""
HoneyBox - AWS 소식 RSS 수집기
실행 진입점
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 