import sys
import requests
import urllib.request
import datetime

from PyQt5.QtCore import * #QTime, QTimer, QDateTime
from PyQt5.QtWidgets import * #QApplication, QLCDNumber, QWidget, QLabel
from PyQt5.QtGui import *
import MainWindow as mw

api_url = 'http://openweathermap.org/data/2.5/weather?'
id = '2761369'
app_id = 'b1b15e88fa797225412429c1c50c122a1'
icon_url = 'http://openweathermap.org/img/w/'
quote_url= 'https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='

class WeatherWindow(QWidget):
    def __init__(self):
        super(WeatherWindow, self).__init__()
        
        #Window
        self.setWindowTitle("Wetter")
        self.showFullScreen()
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)

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
        MainWindowButton = QPushButton("MainWindow", self)
        MainWindowButton.clicked.connect(self.changeWindow)

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
        v.addWidget(MainWindowButton)
        self.setLayout(v)
        
    def changeWindow(self):
        self.ui = mw.MainWindow()
        self.hide()

        
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
    GUI = WeatherWindow()

    timer = QTimer()
    timer.timeout.connect(GUI.getWeatherIcon)
    timer.timeout.connect(GUI.getWeather)
    timer.timeout.connect(GUI.getCountry)
    timer.timeout.connect(GUI.getCity)
    timer.timeout.connect(GUI.getSunrise)
    timer.timeout.connect(GUI.getSunset)
    timer.timeout.connect(GUI.getTempMin)
    timer.timeout.connect(GUI.getTempMax)
    timer.timeout.connect(GUI.getDescription)
    timer.start(600000)

    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
     main()


