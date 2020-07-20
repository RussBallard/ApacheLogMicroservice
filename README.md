# Apache Log Microservice

# ТЗ к проекту:

Разработать Django приложение для обработки и агрегации Apache лога.

В составе приложения должна быть Management command, которая на вход принимает ссылку на лог файл определенного формата, скачивает ее, парсит и записывает в БД. При загрузке, обработке и записи данных в бд нужно выводить прогресс бар.

Ссылка для теста http://www.almhuette-raith.at/apache-log/access.log

В приложении должна быть модель, которая описывает распарсенные данные из лога. Поля модели должны содержать минимум: IP адрес, Дата из лога, http метод (GET, POST,...), URI запроса, Код ошибки, Размер ответа. Другие данные из лога - опциональны.

На фронтенд необходимо реализовать вывод данных, описанных в модели, с пагинацией и поиском.

Под таблицей также необходимо вывести статистику которая будет содержать следующие данные:

Количество уникальных IP
Top 10 самых распространенных IP адресов, в формате таблички где указан IP адрес и количество его вхождений
Количество GET, POST, ... (http методов)
Общее кол-во переданных байт (суммарное значение по полю "размер ответа")
Учесть, что эти агрегированные данные должны меняться при использовании поиска.

Плюсами будут:

Хорошее оформление и комментирование кода (не излишнее, но хорошее);
Оформление frontend части;
Упаковка проекта в docker/docker-compose;
Оптимизация запросов к БД;
Кнопка экспорта данных на таблице с результатами, при нажатии на которую будет скачиваться файлик в формате XLSX с результатами выдачи;
