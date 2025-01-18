import VKCL
import YAND
import json
import os
import time
from progress.bar import IncrementalBar
import requests
import configparser


def record_information_about_files(file_name: str, photos: list):
    with open(file_name, 'w') as file:
        json.dump(photos, file, indent = 4)
 
 
def save_to_disk(received_photos, folder_name):
    # Скачиваем фотографии
    if not os.path.exists(folder_name):
            os.mkdir(folder_name)
    for photo_name, photo_url in received_photos.items():
        with open(f'{folder_name}/{photo_name}.jpg', 'wb') as f:
            img = requests.get(photo_url)
            f.write(img.content)
            
def createcongig():
    # Создание конфигурации
    config = configparser.ConfigParser()
    config.add_section('tokens')
    config.set('tokens', 'token_yndex', '')
    config.set('tokens', 'token_vk', '')
    config.add_section('folder')
    config.set('folder', 'folder_name', 'foto_vk')
    config.set('folder', 'boot_the_drive_up', '0')
    config.add_section('my_id')
    config.set('my_id', 'client_id', '')
    config.set('my_id', 'screen_name', '')
    # Сохранение конфигурации в файл
    with open('settings.ini', 'w') as config_file:
        config.write(config_file)
            
#createcongig()  
#exit()          
    
config = configparser.ConfigParser()
config.read('settings.ini')        
token_yndex = config.get('tokens', 'token_yndex')
token_vk = config['tokens']['token_vk']
folder_name = config['folder']['folder_name']
boot_the_drive_up = config['folder']['boot_the_drive_up']
if 'client_id' in config['my_id']:
    Identifier = config['my_id']['client_id']
elif 'screen_name' in config['my_id']:
        Identifier = config['my_id']['screen_name']
else: Identifier = ''    
    

if Identifier:
    VK = VKCL.VKCLIENT(token_vk, Identifier)    
    result = VK.download_fotos()     
    if result:
        # Записываем данные о фоторафиях в файл .json
        photos = VK.photos
        record_information_about_files('photos.json', photos)
        
        YA = YAND.YANDISC(token_yndex, folder_name)
        received_photos = VK.received_photos
        
        if int(boot_the_drive_up) == 1:
            #Загрузим с диска
            save_to_disk(received_photos, folder_name)
            YA.transfer_photo()            
        else:
            #Загрузим по сылке из ВК
            YA.transfer_photo_url(received_photos)


