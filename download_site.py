import os
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# Отключаем предупреждения об отсутствии SSL-сертификации
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

START_URL = "https://theauraclub.ru"
DOMAIN = urlparse(START_URL).netloc
PROJECT_DIR = os.getcwd()


def download_file(url, folder):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        # Игнорируем проверку SSL (verify=False) для стабильного скачивания
        response = requests.get(url, headers=headers, timeout=15, verify=False)
        if response.status_code == 200:
            path = urlparse(url).path
            if path.endswith('/') or not path:
                path += 'index.html'

            local_path = os.path.join(folder, path.lstrip('/'))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)

            with open(local_path, 'wb') as f:
                f.write(response.content)
            print(f"Скачан файл: {path}")
            return response.content
    except Exception as e:
        print(f"Ошибка при скачивании {url}: {e}")
    return None


# 1. Скачиваем главную страницу
print("Скачиваем главную страницу...")
html_content = download_file(START_URL, PROJECT_DIR)

# 2. Парсим страницу и собираем все ресурсы (картинки, стили, скрипты)
if html_content:
    soup = BeautifulSoup(html_content, 'html.parser')
    resource_urls = set()

    # Ищем картинки, стили и скрипты
    for tag in soup.find_all(['img', 'link', 'script']):
        src = tag.get('src') or tag.get('href')
        if src:
            full_url = urljoin(START_URL, src)
            if urlparse(full_url).netloc == DOMAIN:
                resource_urls.add(full_url)

    print(f"Найдено ресурсов для скачивания: {len(resource_urls)}")
    for res_url in resource_urls:
        download_file(res_url, PROJECT_DIR)
    print("\n[Успех] Скачивание структуры сайта завершено!")
