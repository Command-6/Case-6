# Case-6

## Описание проекта
Наш проект - это уникальное решение в вопросе доступа к художественной литературе, опублекованной молодыми людьми со всей России! Наш сервис явялется удобным инструментом как для писателей, так и для читателей!
## Ключевые функции
- Возможность добавления книги авторами в трех форматах: txt, fb2 и docx
- Возможность скачивания книги читателями в трех форматах: txt, fb2 и docx
- Автоматическая модерация загружаемого материала с помощью специально-обученной нейронной сети
- Возможность создания большого выбора из произведений самых различных жанров от авторов со всех уголков страны
- Поиск произведения по названию или имени автора
## Стэк технологий
- HTML, CSS, JavaScript - набор из классических языков для написания сайтов, предоставляющий наибольший простор для реализации любых идей Frontend-разработчика
- Python, FastAPI - быстрые и доступные инструменты для создания качесвтенного и защищенного Backend-кода
- SpaCy - это нейронная сеть с открытым исходным кодом для продвинутой обработки естественного языка на языках программирования Python и Cython
- PostgreSQL - мощная СУБД для хранения данных на сервере
- GIT - система для контроля версий
## Инструкция по запуску
1. Убедитесь, что ваша среда соответствует требованиям из requirements.txt (так же вам необходим установленный Python3, Uvicorn)
2. Распакуйте backup базы данных из файла bd_case_6.backup
3. Распакуйте архив client.zip в папку client.
4. Измените значение переменной URL в файлах script1.js и script2.js на ip-адрес backend-сервера, согласно шаблону в данных файлах.
5. Запустите backend-сервер строкой uvicorn base:app --host 0.0.0.0 --port 8000 (обязательно запускать в папке server из репозитория)
6. Откройте файл page1.html в вашем браузере
P.s: База данных должна находится на том же устройстве, что и backend-сервер. Frontend запускается на другом устройстве.
## Дополнительное обучение нейронной сети
Нейронная сеть позволяет изменить метод модерации: улучшить его или изменить правила модерации. Для этого необходимо в папку Neiro поместить размеченный датасет в виде файла dataset.csv, после чего следует запустить model1.py. Убедитесь, что помимо этих двух файлов в папке Neiro отсутсвуют другие папки или файлы. После запуску кода в папке Neiro появится папка с обученной моделью. Она должна называться ru_sentiment_model. Скопируйте данную папку в каталог server. После этого запустите сервер по инструкции выше.
## Демонстрация работы проекта
![alt-text](case_6.gif)
## О команде
Участники:
- Сорокина Александра
- Винтерголлер Тимофей
- Овчинников Олег
- Трусов Иван
- Кульков Владислав
- Сычева Арина
- Гуляева Эвелина
- Попов Алексей
