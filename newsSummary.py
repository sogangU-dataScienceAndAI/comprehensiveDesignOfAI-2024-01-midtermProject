import requests
import json
from datetime import date

def get_news(api_key):
    """뉴스 API에서 오늘자 뉴스를 가져오는 함수"""
    today = date.today().strftime("%Y-%m-%d")
    url = f'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=96c06b13157d45c2b94eb7cdd7c20760'
    # url = f'https://newsapi.org/v2/everything?q=technology&from={today}&sortBy=publishedAt&apiKey={api_key}'
    response = requests.get(url)
    if response.status_code != 200:
        print("Failed to fetch news:", response.status_code, response.text)
        return []
    articles = response.json().get('articles', [])
    return articles

def summarize_text(api_key, text):
    """OpenAI API를 사용하여 텍스트를 요약하는 함수"""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "gpt-3.5-turbo",  # 최신 모델로 변경
        "prompt": f"Summarize this article: {text}",
        "temperature": 0,
        "max_tokens": 150
    }

    response = requests.post('https://api.openai.com/v1/completions', headers=headers, json=data)  # 올바른 엔드포인트 사용
    if response.status_code != 200:
        print("Failed to summarize text:", response.status_code, response.json())  # 오류 정보를 더 자세히 출력
        return "No summary available"
    summary = response.json().get('choices', [{}])[0].get('text', '').strip()
    return summary

def main():
    news_api_key = '96c06b13157d45c2b94eb7cdd7c20760'
    openai_api_key = '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'
    articles = get_news(news_api_key)
    if articles:
        for article in articles[:5]:  # 최대 5개 기사 요약
            print(f"Title: {article['title']}\n")
            print(f"Original Content: {article['content']}\n")
            summary = summarize_text(openai_api_key, article['content'])
            print(f"Summary: {summary}\n")
            print('-' * 80)

if __name__ == '__main__':
    main()
