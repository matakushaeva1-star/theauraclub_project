import http.server
import socketserver
import os

# Указываем порт, на котором запустится сайт
PORT = 8000

# Настройка веб-сервера для раздачи статических HTML/CSS/JS файлов
Handler = http.server.SimpleHTTPRequestHandler

# Переходим в директорию проекта, чтобы сервер видел файл index.html
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"Запуск сервера... Откройте в браузере: http://localhost:{PORT}")

try:
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nСервер успешно остановлен.")
