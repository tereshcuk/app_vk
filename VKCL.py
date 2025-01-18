import json
import os
import time
from progress.bar import IncrementalBar
import requests
import configparser

class VKCLIENT:
        
    api_base_url = 'https://api.vk.com/method/' 
    received_photos = {}   
    photos = [] # Список всех фото

    def get_common_params(self):
            return {
                'access_token': self.token,
                'v': '5.199'
                }
    def get_client_id(self, screen_name: str):
        url = f'{self.api_base_url}users.get'
        params = self.get_common_params()
        params.update({'user_ids': screen_name})              
        response = requests.get(url = url, params = params).json()         
        return response['response'][0]['id'] 
            
    def get_fotos(self, count):
        url = f'{self.api_base_url}photos.get'
        params = self.get_common_params()
        params.update({'owner_id': self.client_id})             
        params.update({'album_id' : 'profile'})     
        params.update({'extended': 1})
        params.update({'photo_sizes': 1})
        params.update({'count': count})
        params.update({'offset': 0})        
        response = requests.get(url = url, params = params)        
        return response.json()  
        
    def download_fotos(self, count = 5):                     
        data = self.get_fotos(count)  
        try:                    
            data_response = data['response']
        except Exception:
            print(f'Ошибка: {data['error']}')
            return False                      
        number_of_photos  = data_response['count']        
        items = data_response['items']
        bar = IncrementalBar('Определяем фото максимального размера', max = len(items))
        for photo in items:
            bar.next()
            max_size = 0
            photos_info = {}             
            # Определяем фото максимального размера
            for size in photo['sizes']:                                                
                if size['type'] == 'z':               
                    if photo['likes']['count'] not in self.received_photos.keys():
                        file_name = photo['likes']['count']                       
                    else:
                        file_name = f"{photo['likes']['count']}_{photo['date']}"    
                    break            
                                  
            # Формируем список фотографий для упаковки в .json
            self.received_photos[file_name] = size['url']
            photos_info['file_name'] = f'{file_name}.jpg'            
            photos_info['size'] = size['type']
            self.photos.append(photos_info)
        bar.finish()        
        return True    
           
    def __init__(self, token: str, Identifier: str):
        self.token = token        
        client_id = self.get_client_id(Identifier)        
        self.client_id = client_id
        
def main():
    config = configparser.ConfigParser()
    config.read('settings.ini')
    token_vk = config['Tokens']['token_vk']    
    
    folder_name = config['folder']['folder_name']
    boot_the_drive_up = config['folder']['boot_the_drive_up']
    if 'client_id' in config['id']:
        Identifier = config['id']['client_id']
    elif 'screen_name' in config['id']:
        Identifier = config['id']['screen_name']
    else: Identifier = ''
    
    VK = VKCLIENT(token_vk, Identifier)    
    result = VK.download_fotos()     
    
    
            
if __name__ == '__main__':
    main()        