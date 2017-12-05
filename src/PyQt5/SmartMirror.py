import sys
import requests
import urllib.request
import datetime

from PyQt5.QtCore import * #QTime, QTimer, QDateTime
from PyQt5.QtWidgets import * #QApplication, QLCDNumber, QWidget, QLabel
from PyQt5.QtGui import *

from PyQt5 import QtCore, QtGui

api_url = 'http://openweathermap.org/data/2.5/weather?'
id = '2761369'
app_id = 'b1b15e88fa797225412429c1c50c122a1'
icon_url = 'http://openweathermap.org/img/w/'
quote_url= 'https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        start_widget = StartWindowWidget(self)
        start_widget.changeButton.clicked.connect(self.start)
        self.central_widget.addWidget(start_widget)
        
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)
        
        
    def start(self):
        weather_widget = WeatherWindowWidget(self)
        self.central_widget.addWidget(weather_widget)
        self.central_widget.setCurrentWidget(weather_widget)
        weather_widget.MainWindowButton.clicked.connect(self.main)

    def main(self):
        start_widget = StartWindowWidget(self)
        self.central_widget.addWidget(start_widget)
        self.central_widget.setCurrentWidget(start_widget)
        start_widget.changeButton.clicked.connect(self.start)

class StartWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(StartWindowWidget, self).__init__(parent)
        
        time = self.getTime()

        date = self.getDate()
        
        weather= self.getWeather()
        
        image = self.getWeatherIcon()
        
        quote = self.getQuote()
        
        quote_author = self.getQuoteAuthor
        
        #Image
        icon = QImage()
        icon.loadFromData(image) 

        # Label
        self.time_label = QLabel(time, self)
        self.data_label = QLabel(date, self)
        self.weather_label = QLabel(weather+"°C", self)
        weather_icon = QLabel(self)
        self.quote_label = QLabel(quote, self)
        #self.quote_author_label = QLabel(quote_author, self)

        weather_icon.setPixmap(QPixmap(icon))

        self.time_label.setFont(QFont("Vendera", 25, QFont.Bold))
        self.data_label.setFont(QFont("Vendera", 15, QFont.Bold))
        self.weather_label.setFont(QFont("Vendera", 25, QFont.Bold))

        self.time_label.setStyleSheet('color: white')
        self.data_label.setStyleSheet('color: white')
        self.weather_label.setStyleSheet('color: white')
        self.quote_label.setStyleSheet('color: white')
        
        self.quote_label.resize (100, 100)
        
        #Button
        self.changeButton = QPushButton('Change Window')
        
        

        # Struktur
        h = QHBoxLayout()

        v = QVBoxLayout()

        h.addWidget(self.time_label)
        h.addStretch(1)
        h.addWidget(self.weather_label)
        h.addWidget(weather_icon)
        
        #v.addStretch(1)

        v.addLayout(h)
        v.addWidget(self.data_label)
        v.addWidget(self.quote_label)
        #v.addWidget(self.quote_author_label)
        v.addStretch(1)
        v.addWidget(self.changeButton)

        self.setLayout(v)
        

    #Zeit
    def getTime(self):
        time = QTime.currentTime().toString()
        print(time)
        return time
    
    def updateTime(self):
        time = QTime.currentTime().toString()
        print("Time: " + time)
        self.time_label.setText(time)
        #self.lcd_anzeige.display(time)
        return time
    
        #Datum
    def getDate(self):
        date = QDateTime.currentDateTime().toString("dddd " + "dd" + "." + "MMM" "yyyy")
        return date

    def updateTime_Date(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.getTime)
        self.timer.timeout.connect(self.getDate)
        self.timer.start(1000)


##    def updateDate(self):
##        self.timer = QTimer(self)
##        self.timer.timeout.connect(self.getDate)
##        self.timer.start(1000)
        
    #Wetter    
    def getWeather(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        return temp_c
    
    def getWeatherIcon(self):
        #Icon Nummer
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        number = r['weather'][0]['icon']
        #Icon URL
        image = urllib.request.urlopen(icon_url+number+'.png').read()
        return image
        
    def updateWeather(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getWeather)
        self.timer.timeout.connect(self.getWeatherIcon)
        self.timer.start(600000)
    
    def getQuote(self):
        r = requests.get(quote_url).json()
        quote = r[0]['content']
        return quote

    
    def getQuoteAuthor(self):
        r = requests.get(quote_url).json()
        quote_author = r[0]['title']
        return quote_author
    
    def updateQuote(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.getQuote)
        self.timer.timeout.connect(self.getQuoteAuthor)
        self.timer.start(600000)
    
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Esc:
            self.close()


class WeatherWindowWidget(QWidget):
    def __init__(self, parent=None):
        super(WeatherWindowWidget, self).__init__(parent)
        weather = self.getWeather()
        image = self.getWeatherIcon()
        
        #Image
        icon = QImage()
        icon.loadFromData(image)
        
        country = self.getCountry()
        city = self.getCity()
        sunrise = self.getSunrise()
        sunset = self.getSunset()
        temp_min = self.getTempMin()
        temp_max = self.getTempMax()
        description = self.getDescription()


        # Label
        self.weather_label = QLabel(weather+"°C", self)
        weather_icon = QLabel(self)
        weather_icon.setPixmap(QPixmap(icon))
        self.country_label = QLabel(country, self)
        self.city_label = QLabel(city, self)
        self.sunrise_label = QLabel("Sunrise:"+sunrise, self)
        self.sunset_label = QLabel("Sunset:"+sunset, self)
        self.temp_min_label = QLabel("Temp. min:"+temp_min, self)
        self.temp_max_label = QLabel("Temp. max:"+temp_max, self)
        self.description_label = QLabel(description, self)
        
        
        #Eigenschaften
        self.weather_label.setFont(QFont("Vendera", 45, QFont.Bold))
        self.weather_label.setStyleSheet('color: white')
        self.country_label.setStyleSheet('color: white')
        self.city_label.setStyleSheet('color: white')
        self.sunrise_label.setStyleSheet('color: white')
        self.sunset_label.setStyleSheet('color: white')
        self.temp_min_label.setStyleSheet('color: white')
        self.temp_max_label.setStyleSheet('color: white')
        self.description_label.setStyleSheet('color: white')
        
        #Button
        self.MainWindowButton = QPushButton('MainWindow')

        # Struktur
        h = QHBoxLayout()
        v = QVBoxLayout()
        h.addWidget(self.country_label)
        h.addWidget(self.city_label)
        h.addStretch(1)
        h.addWidget(weather_icon)
        h.addWidget(self.weather_label)
        v.addWidget(self.sunrise_label)
        h.addStretch(1)
        h.addWidget(self.description_label)
        v.addWidget(self.sunset_label)
        v.addWidget(self.temp_max_label)
        h.addWidget(self.temp_min_label)
        #v.addStretch(1)
        v.addLayout(h)
        v.addStretch(1)
        v.addWidget(self.MainWindowButton)
        self.setLayout(v)
        

    #Wetter    
    def getWeather(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        return temp_c
    
    def getWeatherIcon(self):
        #Icon Nummer
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        number = r['weather'][0]['icon']
        #Icon URL
        image = urllib.request.urlopen(icon_url+number+'.png').read()
        print("icon update")
        return image
    
    def getCountry(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        country = r['sys']['country']
        return country
    
    def getCity(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        city = str(r['name'])
        return city
    
    def getSunrise(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        timestamp = datetime.datetime.fromtimestamp(r['sys']['sunrise'])
        sunrise = timestamp.strftime('%H:%M')
        return sunrise
    
    def getSunset(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        timestamp = datetime.datetime.fromtimestamp(r['sys']['sunset'])
        sunset = timestamp.strftime('%H:%M')
        return sunset
    
    
    def getTempMax(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_max = str(r['main']['temp_max'])
        return temp_max
    
    def getTempMin(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_min = str(r['main']['temp_min'])
        return temp_min
    
    def getDescription(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        description = r['weather'][0]['description']
        return description
    
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Esc:
            self.close()



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
##    timer = QTimer()
##    timer.timeout.connect(GUI.updateTime)
##    timer.start(1000)

    #self.showFullScreen()
    window.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
     main()