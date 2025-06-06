import os

class Config:
    # Получаем переменные окружения с заданными значениями по умолчанию
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'mydatabase')
    DB_USER = os.getenv('DB_USER', 'myuser')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'mypassword')

    # Формируем строку подключения для базы данных
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Отключаем отслеживание изменений объектов для предотвращения дополнительной нагрузки
    SQLALCHEMY_TRACK_MODIFICATIONS = False
