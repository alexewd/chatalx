import requests

def get_final_url(tiny_url):
    try:
        response = requests.head(tiny_url, allow_redirects=True)
        return response.url
    except requests.RequestException as e:
        print(f"Ошибка: {e}")
        return None

# Пример использования
tiny_url = "http://www.tinyurl.com/2yvsbv6g"  # Замените на вашу ссылку
final_url = get_final_url(tiny_url)
if final_url:
    print(f"Оригинальный URL: {final_url}")