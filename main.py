import pygame
import requests
import sys
import os

koord = '2.292771,48.858583'
koord1 = koord.split(',')
spn = 0.00619
l = 'sat'
response = None

def izmen_mashtab(znak, delta):
    if znak == '+':
        delta = delta + 0.005
    else:
        delta = delta - 0.005
    return delta


while True:
    try:
        map_request = "https://static-maps.yandex.ru/1.x/?l=map&ll="+koord+'&size=450,450&spn='+str(spn)+','+str(spn)+'&l='+l
        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)
    except:
        print("Запрос не удалось выполнить. Проверьте наличие сети Интернет.")
        sys.exit(1)
    # Запишем полученное изображение в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((450, 450))
    # Рисуем картинку, загружаемую из только что созданного файла.
    screen.blit(pygame.image.load(map_file), (0, 0))
    # Переключаем экран и ждем закрытия окна.
    pygame.display.flip()   
    running = True
    while running:
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN:
                #Меняем масштаб
                if event.key == 280:
                    if spn < 65:
                        spn = izmen_mashtab('+', spn)
                        running = False
                elif event.key == 281:
                    if spn > 0.002:
                        spn = izmen_mashtab('-', spn)   
                        running = False
                #Меняем центр карты
                if event.key == 276:
                    if float(koord1[1]) > -179:
                        koord = str(float(koord1[0])-10.005)+','+koord1[1]
                        koord1 = koord.split(',')
                        running = False
                elif event.key == 275:
                    if float(koord1[1]) < 179:
                        koord = str(float(koord1[0])+0.005)+','+koord1[1]
                        koord1 = koord.split(',')       
                        running = False
                elif event.key == 274:
                    if float(koord1[1]) > -89:
                        koord = koord1[0]+','+str(float(koord1[1])-0.005)
                        koord1 = koord.split(',')    
                        running = False
                elif event.key == 273:
                    if float(koord1[1]) < 89:
                        koord = koord1[0]+','+str(float(koord1[1])+0.005)
                        koord1 = koord.split(',')  
                        running = False
                    
           
pygame.quit()
 
# Удаляем за собой файл с изображением.
os.remove(map_file)