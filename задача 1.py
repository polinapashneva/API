import sys

import requests
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class MainWindow(QMainWindow):
    g_map: QLabel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('main_window.ui', self)
        self.press_delta = 0.00001
        self.map_zoom = 5
        self.map_ll = [37.977751, 55.757718]
        self.map_l = 'map'
        self.map_key = ''

        self.update_map()

    def keyPressEvent(self, event):
        pass

    def update_map(self):
        map_params = {
            "ll": ','.join(map(str, self.map_ll)),
            "l": self.map_l,
            'z': self.map_zoom
        }
        # создаем сессию запросов
        session = requests.Session()
        # устанавливаем настройки для повторного подключения
        retry = Retry(total=10, connect=5, backoff_factor=0.5)
        # задаем настройки количества попыток и т д
        adapter = HTTPAdapter(max_retries=retry)
        # регистрируем адаптеры для подключения
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        # выполняем запрос с нашими параметрами
        response = session.get('https://static-maps.yandex.ru/1.x/',
                               params=map_params)
        # создаем файл для записи картинки из запроса
        with open('tmp.png', mode='wb') as tmp:
            tmp.write(response.content)

        pixmap = QPixmap()
        pixmap.load('tmp.png')
        self.g_map.setPixmap(pixmap)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())
