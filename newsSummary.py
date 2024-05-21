import requests
from datetime import date
from gtts import gTTS
from playsound import playsound
import os


def get_news(api_key):
    """뉴스 API에서 오늘자 뉴스를 가져오는 함수"""
    today = date.today().strftime("%Y-%m-%d")
    url = f'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api_key}'
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
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize this article: {text}"}
        ]
    }
    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
    if response.status_code != 200:
        print("Failed to summarize text:", response.status_code, response.json())
        return "No summary available"
    summary = response.json().get('choices', [{}])[0].get('message', {}).get('content', 'No summary available').strip()
    return summary


def translate_text(api_key, text, target_language='ko'):
    """Google Cloud Translation API를 사용하여 텍스트를 번역하는 함수"""
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        'q': text,
        'target': target_language,
        'key': api_key
    }
    response = requests.get(url, params=params)
    result = response.json()
    return result['data']['translations'][0]['translatedText']


def text_to_speech(text, filename, lang='ko'):
    """텍스트를 음성으로 변환하고 파일로 저장하는 함수"""
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    playsound(filename)
    os.remove(filename)  # 재생 후 파일 삭제


def main():
    news_api_key = 'news_api_key'
    openai_api_key = 'openai_api_key'
    google_api_key = 'google_api_key'
    articles = get_news(news_api_key)

    if articles:
        for article in articles[:5]:  # 최대 5개 기사 요약

            if article['content']:  # 내용이 있는 경우만 처리
                print(f"Title: {article['title']}\n")
                print(f"Original Content: {article['content']}\n")
                summary = summarize_text(openai_api_key, article['content'])
                print(f"Summary: {summary}\n")

                korean_summary = translate_text(google_api_key, summary)  # 영어 요약을 한국어로 번역
                print("Korean Summary:", korean_summary)
                text_to_speech(korean_summary, "korean_summary.mp3")
            else:
                print(f"Title: {article['title']}\nNo content available.\n")


if __name__ == '__main__':
    main()
