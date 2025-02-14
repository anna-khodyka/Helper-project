﻿Personal Helper CLI

Консольное приложение Персональный Помощник – это приложение по работе с Книгой Контактов и Книгой Заметок. Дополнительная возможность - разбор папок по типу файлов.

Версия 1.0.5

https://github.com/mrGarmr/Helper-project

Авторы: • Никифорец Владимир (https://github.com/mrGarmr) • Фоменко Ольга (https://github.com/tritochky) • Ходыка Анна (https://github.com/anna-khodyka)

Установка

Перед установкой необходимо клонировать Helper-project на свой компьютер.
Далее в командной стороке набрать следующую команду:
pip install абсолютный*путь*к_папке_с_setup.py
Либо находясь в папке с setup.py вызвать командную строку и утановить коммандой pip install -e .
Персональный Помощник установлен. Для начала диалога в командной строке набрать helper

Инструкция по работе с Персональным Помощником

Работа с Персональным Помощником осуществляется через консоль. Помощник предлагает список команд, которые нужно ввести пользователю, после чего Помощник выводит результат выполнения команд. В начале работы пользователю необходимо выбрать, хочет ли он создать новые Книгу Контактов и Книгу Заметок (команда new) или загрузить Книги из файла (команда load).

Далее доступны следующие команды:

ОБЩЕГО НАЗНАЧЕНИЯ

"save" – сохранить Книгу Контактов и Книгу Заметок в файл; "load" – загрузить Книгу Контактов и Книгу Заметок из файла; "clear" - очистить терминал; "exit" – выйти из приложения

ПО РАБОТЕ С КНИГОЙ КОНТАКТОВ

"add" – добавить новый контакт; "change" – изменить имя, телефон, адрес, дату рождения, e-mail в существующем контакте; "find" – найти контакт и посмотреть всю информацию о нем; "show" – посмотреть все контакты в Книге Контактов (возможен вывод по заданному количеству записей); "delete" – удалить контакт; "birthday" – предлагает несколько вариантов поиска именинников в книге контактов

ПО РАБОТЕ С КНИГОЙ ЗАМЕТОК

"add note" – добавить запись; "delete note" – удалить запись; "edit note" – изменить запись; "sort notes" – сортировать записи. Возможны 4 варианта сортировки: 1 – от А до Я, 2 - от Я до А, 3 - от старых к новым, 4 - от новых к старым; "show notes" – посмотреть все заметки в Книге Заметок; "find notes" – найти все заметки, которые содержат искомое ключевое слово

ПО РАБОТЕ С СОРТИРОВЩИКОМ ПАПОК

"clean folder" – разобрать заданную папку по типам файлов: видео, аудио, фото, текстовые, другие

Благодарности

Команда разработчиков приносит благодарность компании GOIT за базовый курс по изучению Python, а также за проведение командного проекта, в результате которого было разработано данное приложение.
