import sys
import requests
import urllib.request
import datetime
import threading
import time

from PyQt5.QtCore import *  # QTime, QTimer, QDateTime
from PyQt5.QtWidgets import *  # QApplication, QLCDNumber, QWidget, QLabel
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

api_url = 'http://api.openweathermap.org/data/2.5/weather?id=2761369&appid=8b0928c7fca2d41f21d5c5db7eb970c9&units=metric'
forecast_url = 'http://api.openweathermap.org/data/2.5/forecast?id=2761369&appid=8b0928c7fca2d41f21d5c5db7eb970c9&units=metric'
# id = '2761369'
# app_id = '8b0928c7fca2d41f21d5c5db7eb970c9'
icon_url = 'http://openweathermap.org/img/w/'
quote_url = 'https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='
window_url = 'http://localhost:5000/window'

font_L = QFont('Helvetica', 35, QFont.Bold)
font_M = QFont('Helvetica', 25)
font_S = QFont('Helvetica', 20)
font_XS = QFont('Helvetica', 15)


class MainWindow(QMainWindow):
    ch_main = pyqtSignal()
    ch_weather = pyqtSignal()
    ch_oh = pyqtSignal()
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        start_widget = StartWindowWidget(self)

        self.ch_main.connect(lambda: self.main())
        self.ch_weather.connect(lambda: self.wetter())
        self.ch_oh.connect(lambda: self.oh())
        self.lastwindow = "Main"
        
        self.update_window()
        self.loop()

        self.central_widget.addWidget(start_widget)


        #start_widget.WeatherWindowButton.clicked.connect(self.wetter)
        #start_widget.WeatherWindowButton.clicked.connect(self.oh)

        start_widget.update1()
        start_widget.update2()

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(QPalette.Foreground, Qt.white)
        self.setPalette(p)

    def choose_window(self):

        window_json = requests.get(window_url).json()
        if len(window_json['windows']) > 0:
            window1 = window_json['windows'][0]['name']
            #print("Got window:" + window1)
            #self.lastwindow = ''
            #print(self.lastwindow)
            
            #if window is not None:
            #    if window != window1:
            #        window = window1
            #        print('window'+window)
            #        print('window1'+window1)
            #        print("window changed")
                #self.sig.change.emit()
            #    print("new window:" + window)
            return window1

    def loop(self):
        #print("loop")
        #self.sig = ChangeWindow()
        window = self.choose_window()
            
        if window != self.lastwindow: 
            if window == 'Weather':
                #self.sig.change.connect(self.wetter)
                self.ch_weather.emit()
                self.lastwindow = 'Weather'
                print("changing to Wetter")
                return self.lastwindow
            elif window == 'OH':
                self.ch_oh.emit()
                self.lastwindow = 'OH'
                print("changing to OH")
                return self.lastwindow
            elif window == 'Main':
                #self.sig.change.connect(self.main)
                self.ch_main.emit()
                self.lastwindow = 'Main' 
                print('changing to Main')
                return self.lastwindow
        #threading.Timer(3000.0, self.loop).start()

    def update_window(self):
        self.timer = QTimer(self)
        #self.timer.timeout.connect(self.choose_window)
        self.timer.timeout.connect(self.loop)
        self.timer.start(1000)

    @QtCore.pyqtSlot()
    def wetter(self):
        print("wetter")
        weather_widget = WeatherWindowWidget(self)
        self.central_widget.addWidget(weather_widget)
        self.central_widget.setCurrentWidget(weather_widget)
        #weather_widget.MainWindowButton.clicked.connect(self.main)
        #weather_widget.OHWindowButton.clicked.connect(self.oh)
        weather_widget.update3()
    @QtCore.pyqtSlot()
    def main(self):
        print("main")
        start_widget = StartWindowWidget(self)
        self.central_widget.addWidget(start_widget)
        self.central_widget.setCurrentWidget(start_widget)
        #start_widget.WeatherWindowButton.clicked.connect(self.wetter)
        #start_widget.OHWindowButton.clicked.connect(self.oh)
        start_widget.update1()
        start_widget.update2()
    @QtCore.pyqtSlot()
    def oh(self):
        oh_widget = OpenHabWidget(self)
        self.central_widget.addWidget(oh_widget)
        self.central_widget.setCurrentWidget(oh_widget)
        #oh_widget.weatherButton.clicked.connect(self.wetter)
        #oh_widget.mainButton.clicked.connect(self.main)
        # oh_widget.updatelist()
        #oh_widget.filllist()

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Esc:
            self.close()


class StartWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWindowWidget, self).__init__(parent)
        print("StartwindowWidget")
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(QPalette.Foreground, Qt.white)
        self.setPalette(p)

        # Label
        self.time_label = QLabel()
        self.date_label = QLabel()
        self.weather_label = QLabel()
        self.weather_icon = QLabel()
        self.quote_label = QLabel()
        self.quote_author_label = QLabel()

        self.time_label.setFont(font_L)
        self.date_label.setFont(font_M)
        self.weather_label.setFont(font_L)
        self.quote_label.setFont(font_S)
        self.quote_author_label.setFont(font_XS)

        self.quote_label.setMinimumWidth(1000)
        self.quote_label.setMaximumWidth(1000)
        self.quote_label.setWordWrap(True)
        self.quote_label.setAlignment(Qt.AlignCenter)

        # self.time_label.setStyleSheet('color: white')
        # self.date_label.setStyleSheet('color: white')
        # self.weather_label.setStyleSheet('color: white')
        # self.quote_label.setStyleSheet('color: white')
        # self.quote_author_label.setStyleSheet('color: white')

        # Button
        #self.WeatherWindowButton = QPushButton('Weather Window')
        #self.OHWindowButton = QPushButton('OpenHab Window')
        # Struktur
        h = QHBoxLayout()
        h1 = QHBoxLayout()
        h2 = QHBoxLayout()

        v = QVBoxLayout()

        h.addWidget(self.time_label)
        h.addStretch(1)
        h.addWidget(self.weather_icon)
        h.addWidget(self.weather_label)
        v.addLayout(h)
        v.addWidget(self.date_label)
        v.addStretch(1)

        h1.addStretch(1)
        h1.addWidget(self.quote_label)
        h1.addStretch(1)
        v.addLayout(h1)
        h2.addStretch(1)
        h2.addWidget(self.quote_author_label)
        h2.addStretch(1)
        v.addLayout(h2)
        #v.addWidget(self.WeatherWindowButton)
        #v.addWidget(self.OHWindowButton)

        self.setLayout(v)

        # Zeit

    def update1(self):
        time = QTime.currentTime().toString()
        # print("Time: " + time)
        self.time_label.setText(time)

        date = QDateTime.currentDateTime().toString("dddd " + "dd" + "." + "MMM" "yyyy")
        # print("Datum" + date)
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
        self.quote_author_label.setText("~" + quote_author)

        threading.Timer(60000.0, self.update2).start()

    # def choose_window(self):
    #     self.sig = ChangeWindow()
    #     window = ''
    #     window_json = requests.get(window_url).json()
    #     window1 = window_json['windows'][0]['name']
    #     print("API Window:" + window1)
    #     if window is not None:
    #         if window != window1:
    #             window = window1
    #             print("window changed")
    #             self.sig.change.emit()
    #             print("new window:" + window)
    #         return window
    # 
    # def loop(self):
    #     self.main = MainWindow()
    #     print("loop")
    #     self.sig = ChangeWindow()
    #     window = self.choose_window()
    # 
    #     if window == 'Weather':
    #         self.sig.change.connect(main.wetter)
    #         print("check Wetter")
    #     elif window == 'OH':
    #         self.sig.change.connect(main.oh)
    #         print("check OH")
    # 
    # def update_window(self):
    #     self.timer = QTimer(self)
    #     self.timer.timeout.connect(self.choose_window)
    #     self.timer.timeout.connect(self.loop)
    #     self.timer.start(3000)


class WeatherWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWindowWidget, self).__init__(parent)
        print("WeatherWindowWidget")

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

        # List
        self.forecast_list = QListWidget()

        # Eigenschaften
        self.weather_label.setFont(font_L)
        self.country_label.setFont(font_L)
        self.city_label.setFont(font_L)

        self.sunrise_label.setFont(font_S)
        self.sunset_label.setFont(font_S)
        self.temp_max_label.setFont(font_S)
        self.temp_min_label.setFont(font_S)
        self.description_label.setFont(font_S)
        self.forecast_list.setFont(font_XS)

        self.weather_label.setStyleSheet('color: white')
        self.country_label.setStyleSheet('color: white')
        self.city_label.setStyleSheet('color: white')
        self.sunrise_label.setStyleSheet('color: white')
        self.sunset_label.setStyleSheet('color: white')
        self.temp_min_label.setStyleSheet('color: white')
        self.temp_max_label.setStyleSheet('color: white')
        self.description_label.setStyleSheet('color: white')
        self.forecast_list.setStyleSheet('color:white')
        self.setStyleSheet("""QListWidget{background: black;}""")

        # Button
        #self.MainWindowButton = QPushButton('MainWindow')
        #self.OHWindowButton = QPushButton('OpenHab Window')

        # Struktur
        h = QHBoxLayout()
        h2 = QHBoxLayout()
        h3 = QHBoxLayout()

        v = QVBoxLayout()

        h.addWidget(self.country_label)
        h.addWidget(self.city_label)
        h.addStretch(1)
        h.addWidget(self.weather_icon)
        h.addWidget(self.weather_label)

        v.addLayout(h)

        h2.addWidget(self.sunrise_label)
        h2.addStretch(1)
        h2.addWidget(self.description_label)
        h2.addWidget(self.temp_max_label)

        v.addLayout(h2)

        h3.addWidget(self.sunset_label)
        h3.addStretch(1)
        h3.addWidget(self.temp_min_label)

        # v.addStretch(1)
        v.addLayout(h3)
        v.addStretch(1)
        v.addWidget(self.forecast_list)
        #v.addWidget(self.MainWindowButton)
        #v.addWidget(self.OHWindowButton)
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
        self.country_label.setText(country + ",")

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

        r = requests.get(forecast_url).json()

        count = r['cnt']

        for i in range(0, count, 8):
            date = r['list'][i]['dt_txt']
            description = r['list'][i]['weather'][0]['description']
            temp_max = r['list'][i]['main']['temp_max']
            temp_min = r['list'][i]['main']['temp_min']

            self.forecast_list.addItem(
                'On %s "%s" Temp will be between %s and %s °C' % (date[:-8], description, temp_max, temp_min))

        threading.Timer(60000.0, self.update3).start()


class OpenHabWidget(QWidget):
    update_list = pyqtSignal()
    
    def __init__(self, parent=None):
        super(OpenHabWidget, self).__init__(parent)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        p.setColor(QPalette.Foreground, Qt.white)
        self.setPalette(p)

        self.state = ''
        self.name = ''
        
        self.current_entries = []
        self.update_list.connect(self.updatelist)

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

        # Label
        self.items_list = QListWidget()

        # # Eigenschaften
        self.items_list.setFont(font_M)
        self.items_list.setStyleSheet('color:white')
        self.setStyleSheet("""QListWidget{background: black;}""")

        # Button
        #self.mainButton = QPushButton('Main Window')
        #self.weatherButton = QPushButton('Weather Window')

        # Struktur
        v = QVBoxLayout()
        v.addWidget(self.items_list)
        #v.addWidget(self.mainButton)
        #v.addWidget(self.weatherButton)

        self.setLayout(v)
        self.retrieve_changes()
    
    def retrieve_changes(self):
        r = requests.get('http://localhost:8080/rest/items').json()
        r = list(filter(lambda item: item['name'] not in ["Main", "Weather", "OH"], r))
        self.current_entries = r
        self.update_list.emit()
        threading.Timer(1.0, self.retrieve_changes).start()
        
    pyqtSlot()
    def updatelist(self):

        r = self.current_entries
        count = len(r)

        for i in range(0, count):
            entryName = r[i]['name']
            entryState = r[i]['state']
            entryFormatted = entryName + ": " + entryState
            existingEntries = self.items_list.findItems(entryName, Qt.MatchContains)
            if len(existingEntries) == 0:
                print("Did not find " + r[i]['name'] +", adding")
                self.items_list.addItem(entryFormatted)
            else:
                existingEntries[0].setText(entryFormatted)

        


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.showFullScreen()
    #window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


