import json
import os
import time
from progress.bar import IncrementalBar
import requests

class YANDISC:
        
    def __init__(self, token: str, yan_folder_name: str):
        self.token = token
        self.yan_folder_name = yan_folder_name 
            
    def create_folder(self):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/'
        headers = {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}
        params = {'path': f'{self.yan_folder_name}',
                'overwrite': 'false'}
        response = requests.put(url=url, headers=headers, params=params)    
            
    def get_yandex_folder(self, file_name: str):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'
        headers = {'Content-Type': 'application/json',
                'Authorization': f'OAuth {self.token}'}
        params = {'path': f'{self.yan_folder_name}/{file_name}',        
                'overwrite': 'true'}
            
        response = requests.get(url=url, headers=headers, params=params)
        href = response.json().get('href') 
        return href
               
    
    def send_to_yandex_disk(self, files_path: str, file_name: str):       
        href = self.get_yandex_folder(file_name) 
        uploader = requests.put(href, data=open(files_path, 'rb'))          
          
     
    def send_to_yandex_disk_url(self, url_foto: str, file_name: str): 
        href = self.get_yandex_folder(file_name)        
        data = requests.get(url_foto)       
        uploader = requests.put(href, data=data)  
            
        
    def transfer_photo_url(self, received_photos):
        self.create_folder()
        bar = IncrementalBar('Переносим файлы на яндекс диск', max = len(received_photos))
        for photo_name, photo_url in received_photos.items():
            self.send_to_yandex_disk_url(photo_url, photo_name)
            bar.next()
            
        bar.finish()     
            
    def transfer_photo(self):
        self.create_folder()
        photos_list = os.listdir(self.yan_folder_name)    
        bar = IncrementalBar('Переносим файлы на яндекс диск', max = len(photos_list)) 
        for photo in photos_list:
            bar.next()
            time.sleep(0.5)
            files_path = os.getcwd() + f'\\{self.yan_folder_name}\\' + photo
            self.send_to_yandex_disk(files_path, photo)
            
        bar.finish()    
        print(f'Фотографий загружено на Яндекс диск: {len(photos_list)}') 