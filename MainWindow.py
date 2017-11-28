import sys
import requests
import urllib.request

from PyQt5.QtCore import * #QTime, QTimer, QDateTime
from PyQt5.QtWidgets import * #QApplication, QLCDNumber, QWidget, QLabel
from PyQt5.QtGui import *

api_url = 'http://openweathermap.org/data/2.5/weather?'
id = '2761369'
app_id = 'b1b15e88fa797225412429c1c50c122a1'
icon_url = 'http://openweathermap.org/img/w/'
quote_url= 'https://quotesondesign.com/wp-json/posts?filter[orderby]=rand&filter[posts_per_page]=1&callback='

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        #Window
        self.setWindowTitle("Hallo")
        self.showFullScreen()

        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.black)
        self.setPalette(p)


        time = self.getTime()

        #lcd_time = self.getLCDTime()

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
        

        #LCD
##        self.lcd_anzeige = QLCDNumber(self)
        #self.lcd_anzeige.display(lcd_time)

        # Struktur
        h = QHBoxLayout()

        v = QVBoxLayout()

        #h.addStretch(1)
##        v.addWidget(self.lcd_anzeige)
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

        self.setLayout(v)


    #Zeit
    def getTime(self):
        time = QTime.currentTime().toString()
        return time

    def updateTime(self):
        time = QTime.currentTime().toString()
        print("Time: " + time)
        self.time_label.setText(time)
        #self.lcd_anzeige.display(time)
        return time


##    #Zeit für LCD Anzeige
##    def getLCDTime(self):
##        lcd_time = QTime.currentTime().toString('hh:mm')
##        return lcd_time
##
##    def updateLCDTime(self):
##        lcdtime = QTime.currentTime()
##        lcd_time = lcdtime.toString('hh:mm')
##        print("LCD Time: " + lcd_time)
##        if (lcdtime.second() % 2) == 0:
##            text = lcd_time[:2] + ' ' + lcd_time[3:]
##        self.lcd_anzeige.display(lcd_time)
##        return lcd_time


    #Datum
    def getDate(self):
        date = QDateTime.currentDateTime().toString("dddd " + "dd" + "." + "MMM" "yyyy")
        return date

    #def updateDate(self):
        #date = QDateTime.currentDataTime().toString("dddd " + "dd" + "." + "MMM" "yyyy")
        #print("Datum: " + date)
        #self.data_label.setText(date)
        #return date
        
    #Wetter    
    def getWeather(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        return temp_c
        
    def updateWeather(self):
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        temp_c_float = r['main']['temp']
        temp_c = str(temp_c_float)
        print(temp_c)
        self.weather_label.setText(temp_c)
        return temp_c
    
    def getWeatherIcon(self):
        #Icon Nummer
        r = requests.get(api_url+'id='+id+'&'+'appid='+app_id).json()
        number = r['weather'][0]['icon']
        #Icon URL
        image = urllib.request.urlopen(icon_url+number+'.png').read()
        return image
        
    #def updateWeatherIcon
    
    def getQuote(self):
        r = requests.get(quote_url).json()
        quote = r[0]['content']
        return quote

    
    def getQuoteAuthor(self):
        r = requests.get(quote_url).json()
        quote_author = r[0]['title']
        return quote_author
    
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Esc:
            self.close()

def main():
    app = QApplication(sys.argv)
    ex = MainWindow()

    timer = QTimer()
    timer.timeout.connect(ex.updateTime)
    #timer.timeout.connect(ex.updatedate)
    #timer.timeout.connect(ex.updateWeather)
    timer.start(1000)

##    timer_weather = QTimer()
##    timer.timeout.connect(ex.updateWeather)
##    timer_weather.start(600000)

    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
     main()

