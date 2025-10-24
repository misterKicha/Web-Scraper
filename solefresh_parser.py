import requests
from bs4 import BeautifulSoup
import csv
import re

def parse_solefresh():
    print('=== ДЕТАЛЬНЫЙ ПАРСИНГ SОLEFRESH НА PYTHON ===')
    
    # Загружаем страницу
    url = 'https://solefresh.ru/price/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if 
line.strip()]
        
        services_by_category = {
            'CLASSIC': [],
            'STANDART': [],
            'PREMIUM': [],
            'SNEAKERHEAD': [],
            'HIGH TOP': [],
            'ДЕТСКАЯ ОБУВЬ': [],
            'Дополнительные услуги': []
        }
        
        current_main_category = 'CLASSIC'
        current_sub_category = ''
        
        for line in lines:
            clean_line = line.strip()
            lower_line = clean_line.lower()
            
            # Определяем основную категорию
            if 'classic' in lower_line:
                current_main_category = 'CLASSIC'
            if 'standart' in lower_line or 'стандарт' in lower_line:
                current_main_category = 'STANDART'
            if 'premium' in lower_line or 'премиум' in lower_line:
                current_main_category = 'PREMIUM'
            if 'sneakerhead' in lower_line:
                current_main_category = 'SNEAKERHEAD'
            if 'high top' in lower_line or 'хай-топ' in lower_line:
                current_main_category = 'HIGH TOP'
            if 'детск' in lower_line or 'ребен' in lower_line:
                current_main_category = 'ДЕТСКАЯ ОБУВЬ'
            if any(word in lower_line for word in ['дополнительн', 'уход', 
'ремонт', 'восстановление']):
                current_main_category = 'Дополнительные услуги'
            
            # Определяем подкатегорию (тип чистки)
            if 'комплексная' in lower_line or 'комплекс' in lower_line:
                current_sub_category = 'Комплексная чистка'
            elif 'глубокая' in lower_line or 'полная' in lower_line:
                current_sub_category = 'Глубокая чистка'
            
            # Ищем строки с ценами
            if (clean_line and 
                any(marker in clean_line for marker in ['₽', 'руб']) and
                re.search(r'\d', clean_line) and
                5 < len(clean_line) < 100):
                
                # Разделяем название и цену
                price_match = re.search(r'(\d[\d\s]*)\s*[₽рубр]', 
clean_line)
                if price_match:
                    price = price_match.group(0).strip()
                    name = re.sub(r'[–—]\s*$', '', 
clean_line.replace(price, '')).strip()
                    
                    # Форматируем цену
                    formatted_price = re.sub(r'\s+', ' ', price)
                    formatted_price = re.sub(r'от(\d)', r'от \1', 
formatted_price)
                    formatted_price = re.sub(r'(\d)([₽руб])', r'\1 \2', 
formatted_price)
                    
                    # Для дополнительных услуг используем оригинальное 
название
                    if current_main_category == 'Дополнительные услуги':
                        
services_by_category[current_main_category].append({
                            'name': name,
                            'price': formatted_price,
                            'type': 'Услуга'
                        })
                    else:
                        # Для категорий чистки используем определенный тип 
чистки
                        
services_by_category[current_main_category].append({
                            'name': current_sub_category or 'Чистка',
                            'price': formatted_price,
                            'type': current_sub_category or 'Чистка'
                        })
        
        # Добавляем специальную строку для детской обуви
        services_by_category['ДЕТСКАЯ ОБУВЬ'] = [{
            'name': '-50% на химчистку до 34 размера',
            'price': '',
            'type': 'Акция'
        }]
        
        # Создаем CSV файл
        with open('услуги_solefresh_python.csv', 'w', newline='', 
encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            # Категории химчистки обуви
            cleaning_categories = ['CLASSIC', 'STANDART', 'PREMIUM', 
'SNEAKERHEAD', 'HIGH TOP', 'ДЕТСКАЯ ОБУВЬ']
            
            for category in cleaning_categories:
                if services_by_category[category]:
                    writer.writerow([category.upper()])
                    
                    for service in services_by_category[category]:
                        writer.writerow([service['name'], 
service['price']])
                    
                    writer.writerow([''])  # Пустая строка между 
категориями
            
            # Дополнительные услуги
            if services_by_category['Дополнительные услуги']:
                writer.writerow(['ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ'])
                
                for service in services_by_category['Дополнительные 
услуги']:
                    writer.writerow([service['name'], service['price']])
        
        print('✅ Файл "услуги_solefresh_python.csv" создан!')
        
        # Выводим статистику
        for category in cleaning_categories:
            if services_by_category[category]:
                print(f'📊 {category}: 
{len(services_by_category[category])} записей')
        print(f'📊 Дополнительные услуги: 
{len(services_by_category["Дополнительные услуги"])} услуг')
        
    except Exception as e:
        print(f'❌ Ошибка: {e}')

# Запускаем парсинг
if __name__ == '__main__':
    parse_solefresh()


import requests
from bs4 import BeautifulSoup
import csv
import re

def parse_solefresh():
    print('=== ДЕТАЛЬНЫЙ ПАРСИНГ SОLEFRESH НА PYTHON ===')
    
    # Загружаем страницу
    url = 'https://solefresh.ru/price/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) 
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text()
        lines = [line.strip() for line in all_text.split('\n') if 
line.strip()]
        
        services_by_category = {
            'CLASSIC': [],
            'STANDART': [],
            'PREMIUM': [],
            'SNEAKERHEAD': [],
            'HIGH TOP': [],
            'ДЕТСКАЯ ОБУВЬ': [],
            'Дополнительные услуги': []
        }
        
        current_main_category = 'CLASSIC'
        current_sub_category = ''
        
        for line in lines:
            clean_line = line.strip()
            lower_line = clean_line.lower()
            
            # Определяем основную категорию
            if 'classic' in lower_line:
                current_main_category = 'CLASSIC'
            if 'standart' in lower_line or 'стандарт' in lower_line:
                current_main_category = 'STANDART'
            if 'premium' in lower_line or 'премиум' in lower_line:
                current_main_category = 'PREMIUM'
            if 'sneakerhead' in lower_line:
                current_main_category = 'SNEAKERHEAD'
            if 'high top' in lower_line or 'хай-топ' in lower_line:
                current_main_category = 'HIGH TOP'
            if 'детск' in lower_line or 'ребен' in lower_line:
                current_main_category = 'ДЕТСКАЯ ОБУВЬ'
            if any(word in lower_line for word in ['дополнительн', 'уход', 
'ремонт', 'восстановление']):
                current_main_category = 'Дополнительные услуги'
            
            # Определяем подкатегорию (тип чистки)
            if 'комплексная' in lower_line or 'комплекс' in lower_line:
                current_sub_category = 'Комплексная чистка'
            elif 'глубокая' in lower_line or 'полная' in lower_line:
                current_sub_category = 'Глубокая чистка'
            
            # Ищем строки с ценами
            if (clean_line and 
                any(marker in clean_line for marker in ['₽', 'руб']) and
                re.search(r'\d', clean_line) and
                5 < len(clean_line) < 100):
                
                # Разделяем название и цену
                price_match = re.search(r'(\d[\d\s]*)\s*[₽рубр]', 
clean_line)
                if price_match:
                    price = price_match.group(0).strip()
                    name = re.sub(r'[–—]\s*$', '', 
clean_line.replace(price, '')).strip()
                    
                    # Форматируем цену
                    formatted_price = re.sub(r'\s+', ' ', price)
                    formatted_price = re.sub(r'от(\d)', r'от \1', 
formatted_price)
                    formatted_price = re.sub(r'(\d)([₽руб])', r'\1 \2', 
formatted_price)
                    
                    # Для дополнительных услуг используем оригинальное 
название
                    if current_main_category == 'Дополнительные услуги':
                        
services_by_category[current_main_category].append({
                            'name': name,
                            'price': formatted_price,
                            'type': 'Услуга'
                        })
                    else:
                        # Для категорий чистки используем определенный тип 
чистки
                        
services_by_category[current_main_category].append({
                            'name': current_sub_category or 'Чистка',
                            'price': formatted_price,
                            'type': current_sub_category or 'Чистка'
                        })
        
        # Добавляем специальную строку для детской обуви
        services_by_category['ДЕТСКАЯ ОБУВЬ'] = [{
            'name': '-50% на химчистку до 34 размера',
            'price': '',
            'type': 'Акция'
        }]
        
        # Создаем CSV файл
        with open('услуги_solefresh_python.csv', 'w', newline='', 
encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            
            # Категории химчистки обуви
            cleaning_categories = ['CLASSIC', 'STANDART', 'PREMIUM', 
'SNEAKERHEAD', 'HIGH TOP', 'ДЕТСКАЯ ОБУВЬ']
            
            for category in cleaning_categories:
                if services_by_category[category]:
                    writer.writerow([category.upper()])
                    
                    for service in services_by_category[category]:
                        writer.writerow([service['name'], 
service['price']])
                    
                    writer.writerow([''])  # Пустая строка между 
категориями
            
            # Дополнительные услуги
            if services_by_category['Дополнительные услуги']:
                writer.writerow(['ДОПОЛНИТЕЛЬНЫЕ УСЛУГИ'])
                
                for service in services_by_category['Дополнительные 
услуги']:
                    writer.writerow([service['name'], service['price']])
        
        print('✅ Файл "услуги_solefresh_python.csv" создан!')
        
        # Выводим статистику
        for category in cleaning_categories:
            if services_by_category[category]:
                print(f'📊 {category}: 
{len(services_by_category[category])} записей')
        print(f'📊 Дополнительные услуги: 
{len(services_by_category["Дополнительные услуги"])} услуг')
        
    except Exception as e:
        print(f'❌ Ошибка: {e}')

# Запускаем парсинг
if __name__ == '__main__':
    parse_solefresh()

