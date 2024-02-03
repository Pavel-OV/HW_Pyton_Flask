import os
import threading
import time
import requests
import parse


urls_img = ["https://w.forfun.com/fetch/b1/b1f74a00706ac59ec75daa8ab0ac8e90.jpeg",
            "https://w.forfun.com/fetch/92/924b1d12e5b7447c0b508d9b0faa887f.jpeg",
            'https://gas-kvas.com/grafic/uploads/posts/2023-10/1696502289_gas-kvas-com-p-kartinki-lyubie-45.jpg',
            'https://gas-kvas.com/grafic/uploads/posts/2023-09/1695975281_gas-kvas-com-p-kartinki-jpg-18.jpg',
            'https://searchthisweb.com/wallpaper/siberian-tiger_4256x2832_jk6v6.jpg',
            'https://w.forfun.com/fetch/ee/eedaf3b27be4960cefec36ea8ed0b06a.jpeg',
            'http://i1.wallbox.ru/wallpapers/main/201505/dbc10cfe6cced34.jpg',
            'https://www.fonstola.ru/pic/201111/1600x900/fonstola.ru_57808.jpg',
            'https://get.wallhere.com/photo/butterflies-flying-multicolored-colorful-1097879.jpg',
            'https://getwallpapers.com/wallpaper/full/d/4/1/1169923-colorful-iphone-wallpaper-2048x1536-for-android-40.jpg']


def downladurl_threads(url_img):
    start_time = time.time()
    response = requests.get(url_img)
    file_name = os.path.join(folder, url_img.split('/')
                             [-1])  # путь создания папки
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(response.text)
    print(
        f'Загрузка {url_img.split("/")[-1]} за {time.time()- start_time:-2f} секунд')


if __name__ == '__main__':
    urls_img = parse.parse().urls or urls_img
    start_time = time.time()
    folder = "data_img"
    if not os.path.exists(folder):
        os.mkdir(folder)
    start_time = time.time()
    threads = []
    for url_img in urls_img:
        t = threading.Thread(target=downladurl_threads, args=[url_img])
        threads.append(t)
        t.start()
    for i in threads:
        i.join()
    print(
        f'Скачено {len(urls_img)} - файлов за {time.time()- start_time:-2f} секунд, многопоточный подход')
