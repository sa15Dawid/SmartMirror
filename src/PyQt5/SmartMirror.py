import sys
import requests
import urllib.request
import datetime
import threading

from PyQt5.QtCore import *  # QTime, QTimer, QDateTime
from PyQt5.QtWidgets import *  # QApplication, QLCDNumber, QWidget, QLabel
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

api_url = 'http://api.openweathermap.org/data/2.5/weather?id=2761369&appid=8b0928c7fca2d41f21d5c5db7eb970c9&units=metric'
#id = '2761369'
#app_id = '8b0928c7fca2d41f21d5c5db7eb970c9'
icon_url = 'http://openweathermap.org/img/w/'
quote_url = 'https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        start_widget = StartWindowWidget(self)
        start_widget.changeButton.clicked.connect(self.start)
        self.central_widget.addWidget(start_widget)
        start_widget.update1()
        start_widget.update2()

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

    def start(self):
        weather_widget = WeatherWindowWidget(self)
        self.central_widget.addWidget(weather_widget)
        self.central_widget.setCurrentWidget(weather_widget)
        weather_widget.MainWindowButton.clicked.connect(self.main)
        weather_widget.update3()

    def main(self):
        start_widget = StartWindowWidget(self)
        self.central_widget.addWidget(start_widget)
        self.central_widget.setCurrentWidget(start_widget)
        start_widget.changeButton.clicked.connect(self.start)
        start_widget.update1()
        start_widget.update2()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Esc:
            self.close()


class StartWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWindowWidget, self).__init__(parent)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # Label
        self.time_label = QLabel()
        self.date_label = QLabel()
        self.weather_label = QLabel()
        self.weather_icon = QLabel()
        self.quote_label = QLabel()
        self.quote_author_label = QLabel()

        self.time_label.setFont(QFont("Vendera", 25, QFont.Bold))
        self.time_label.setStyleSheet('color:white')

        self.date_label.setFont(QFont("Vendera", 25, QFont.Bold))
        self.date_label.setStyleSheet('color:white')

        self.weather_label.setStyleSheet('color: white')
        self.quote_label.setStyleSheet('color: white')
        self.quote_author_label.setStyleSheet('color: white')

        # Button
        self.changeButton = QPushButton('Change Window')

        # Struktur
        #h = QHBoxLayout()

        v = QVBoxLayout()

        v.addWidget(self.time_label)
        #v.addStretch(1)
        v.addWidget(self.weather_label)
        v.addWidget(self.weather_icon)

        # v.addStretch(1)

        #v.addLayout(h)
        v.addWidget(self.date_label)

        v.addWidget(self.quote_label)
        v.addWidget(self.quote_author_label)
        #v.addStretch(1)
        v.addWidget(self.changeButton)

        self.setLayout(v)

        # Zeit

    def update1(self):
        time = QTime.currentTime().toString()
        #print("Time: " + time)
        self.time_label.setText(time)

        date = QDateTime.currentDateTime().toString("dddd " + "dd" + "." + "MMM" "yyyy")
        #print("Datum" + date)
        self.date_label.setText(date)

        threading.Timer(1.0, self.update1).start()

    def update2(self):
        r = requests.get(api_url).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        self.weather_label.setText(temp_c + "°C")

        # Icon Nummer
        number = r['weather'][0]['icon']
        # Icon URL
        image = urllib.request.urlopen(icon_url + number + '.png').read()

        icon = QImage()
        icon.loadFromData(image)

        self.weather_icon.setPixmap(QPixmap(icon))

        rq = requests.get(quote_url).json()
        quote = rq[0]['content']
        self.quote_label.setText(quote)

        quote_author = rq[0]['title']
        self.quote_author_label.setText(quote_author)

        threading.Timer(60000.0, self.update2).start()


class WeatherWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWindowWidget, self).__init__(parent)

        # Label
        self.weather_label = QLabel()
        self.weather_icon = QLabel()
        self.country_label = QLabel()
        self.city_label = QLabel()
        self.sunrise_label = QLabel()
        self.sunset_label = QLabel()
        self.temp_min_label = QLabel()
        self.temp_max_label = QLabel()
        self.description_label = QLabel()

        
        # Eigenschaften
        self.weather_label.setFont(QFont("Vendera", 45, QFont.Bold))
        self.weather_label.setStyleSheet('color: white')
        self.country_label.setStyleSheet('color: white')
        self.city_label.setStyleSheet('color: white')
        self.sunrise_label.setStyleSheet('color: white')
        self.sunset_label.setStyleSheet('color: white')
        self.temp_min_label.setStyleSheet('color: white')
        self.temp_max_label.setStyleSheet('color: white')
        self.description_label.setStyleSheet('color: white')


        # Button
        self.MainWindowButton = QPushButton('MainWindow')

        # Struktur
        h = QHBoxLayout()
        v = QVBoxLayout()

        h.addWidget(self.country_label)
        h.addWidget(self.city_label)
        h.addStretch(1)
        h.addWidget(self.weather_icon)
        h.addWidget(self.weather_label)
        v.addWidget(self.sunrise_label)
        h.addStretch(1)
        h.addWidget(self.description_label)
        v.addWidget(self.sunset_label)
        v.addWidget(self.temp_max_label)
        h.addWidget(self.temp_min_label)
        # v.addStretch(1)
        v.addLayout(h)
        v.addStretch(1)
        v.addWidget(self.MainWindowButton)
        self.setLayout(v)

    
    def update3(self):
        r = requests.get(api_url).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        self.weather_label.setText(temp_c + "°C")

        # Icon Nummer
        number = r['weather'][0]['icon']
        # Icon URL
        image = urllib.request.urlopen(icon_url + number + '.png').read()

        icon = QImage()
        icon.loadFromData(image)

        self.weather_icon.setPixmap(QPixmap(icon))

        country = r['sys']['country']
        self.country_label.setText(country)
        
        city = str(r['name'])
        self.city_label.setText(city)
        
        timestamp1 = datetime.datetime.fromtimestamp(r['sys']['sunrise'])
        sunrise = timestamp1.strftime('%H:%M')
        self.sunrise_label.setText("Sunrise:" + sunrise)
        
        timestamp2 = datetime.datetime.fromtimestamp(r['sys']['sunset'])
        sunset = timestamp2.strftime('%H:%M')
        self.sunset_label.setText("Sunset:" + sunset)
        
        temp_max = str(r['main']['temp_max'])
        self.temp_max_label.setText("Temp. max:" + temp_max)

        temp_min = str(r['main']['temp_min'])
        self.temp_min_label.setText("Temp. min:" + temp_min)

        description = r['weather'][0]['description']
        self.description_label.setText(description)

        threading.Timer(60000.0, self.update3).start()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    # self.showFullScreen()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
