# Курсовая работа «Резервное копирование»

### parameters.ini
Перед запуском программы необходимо заполнить файл с параметрами: "settings.ini". Данные в файле хранятся в виде "ключ = значение" в соответсвующим разделе. Нужно для каждого ключа указать свое значение:
1. "token_vk" - токен для работы ВК (строка)
2. "token_yndex" - токен с Полигона Яндекс.Диска.(строка)
3. "client_id" - идентификатор пользователя ВК (число), опиционально
4. "screen_name" - идентификатор пользователя ВК (строка), опционально
5. "folder_name"  - имя папки для загруженных фотографий (строка)
6. "boot_the_drive_up" - признак загрузки фото на локальный диск (1- с локаьного диска, 0 - по url ВК)

Пример файла:
```
[tokens]
token_yndex = 
token_vk = 

[folder]
folder_name = foto_vk
boot_the_drive_up = 0

[my_id]
client_id = 
screen_name = 
```

### requirements.txt
Зависимости указаны в файле requiremеnts.txt
