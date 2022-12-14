import os
import sys
import subprocess # 注意Python3.X 已经删除 commands

from PyQt5 import QtCore, QtGui,QtWidgets, QtWidgets ,uic
from PyQt5.QtCore import Qt, QThread,pyqtSignal
from PyQt5.QtGui import QPalette, QBrush, QPixmap
from PIL import Image
from PIL.ImageQt import ImageQt
import time
import datetime
import socket
import requests

runDirectory = sys.path[0] #py脚本运行目录
palette = QPalette()
picInt = 0
picCount = 0
#timeUpdate = 0
tempArray = ["---"]*14
oilStrWeek = ""
countUpdate_1 = False
countUpdate_2 = False
countUpdate_3 = False
countUpdate_4 = False
platformBool = False

def UpdateWeatherIcon(tempType):  #匹配天气类型图标
    if(tempType == "大雨"  or tempType == "中到大雨"):
        return "大雨"
    elif(tempType == "暴雨"  or tempType == "大暴雨" or 
        tempType == "特大暴雨" or tempType == "大到暴雨" or
        tempType == "暴雨到大暴雨" or tempType == "大暴雨到特大暴雨"):
        return "暴雨"
    elif(tempType == "沙尘暴" or tempType == "浮尘" or
        tempType == "扬沙" or tempType == "强沙尘暴" or
        tempType == "雾霾"):
        return "沙尘暴"
    elif(tempType == "---"):
        return "无天气类型"
    return(tempType)

def LowTempStr(tempStr):
    temp_L = tempStr.replace("低温","")
    temp_L = temp_L.replace("℃","")
    temp_L = temp_L.replace(" ","")
    return temp_L

def HightTempStr(tempStr):
    temp_H = tempStr.replace("高温","")
    temp_H = temp_H.replace("℃","")
    temp_H = temp_H.replace(" ","")
    return temp_H

#获取天气
def getTemp():
    try:                                                                     # 连接超时,6秒，下载文件超时,7秒
        r = requests.get('http://t.weather.itboy.net/api/weather/city/101280701',timeout=(6,7)) 
        r.encoding = 'utf-8'
        tempList = [
        (r.json()['cityInfo']['city']),             #城市
        (r.json()['data']['forecast'][0]['low']),   #今日低温
        (r.json()['data']['forecast'][0]['high']),  #今日高温
        (r.json()['data']['forecast'][0]['type']),  #今日天气

        (r.json()['data']['forecast'][1]['low']),   #明日低温
        (r.json()['data']['forecast'][1]['high']),  #明日高温
        (r.json()['data']['forecast'][1]['type']),  #明日天气

        (r.json()['data']['forecast'][2]['low']),   #后日低温
        (r.json()['data']['forecast'][2]['high']),  #后日高温
        (r.json()['data']['forecast'][2]['type']),  #后日天气

        (r.json()['data']['forecast'][3]['low']),   #大后日低温
        (r.json()['data']['forecast'][3]['high']),  #大后日高温
        (r.json()['data']['forecast'][3]['type']),  #大后日天气

        (r.json()['data']['forecast'][0]['fx']),  #今日风向13
        (r.json()['data']['forecast'][0]['fl']),  

        (r.json()['data']['forecast'][1]['fx']),  #明日风向15
        (r.json()['data']['forecast'][1]['fl']),  

        (r.json()['data']['forecast'][2]['fx']),  #后日风向17
        (r.json()['data']['forecast'][2]['fl']),  

        (r.json()['data']['forecast'][3]['fx']),  #大后日风向19
        (r.json()['data']['forecast'][3]['fl']),  

        (r.json()['cityInfo']['updateTime'])        #更新时间21
        ]
    except:
        tempList = ["---"]*22
        return tempList
    else:
        return tempList

def UpdateData():
    global tempArray
    tempArray=getTemp()
    return tempArray



def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return str(ip)
    except:
        s.close()
        return "0.0.0.0"

def todayWeek(nowWeek):
    if nowWeek == "0":
        return"星期天"
    elif nowWeek =="1":
        return"星期一"
    elif nowWeek =="2":
        return"星期二"
    elif nowWeek =="3":
        return"星期三"
    elif nowWeek =="4":
        return"星期四"
    elif nowWeek =="5":
        return"星期五"
    elif nowWeek =="6":
        return"星期六"

def ImageLoad(imageName,scale):
    img = QPixmap(runDirectory+"/weatherType/"+imageName+".png")
    width = img.width()
    img = img.scaledToWidth(width * scale)
    return img

def ImageLoadbyName(filename,scale):
    img=QPixmap(runDirectory+filename)
    width=img.width()
    img=img.scaledToWidth(width*scale)
    return img


def setImage(filename):
    image=Image.open(runDirectory+filename)
    return image  

def CombineImage(strImage1):
    texTemp = Image.open(strImage1)
    #texTemp2 = Image.open(strImage2)
    # mode size color创建新的图像
    #target = Image.new("RGBA", texTemp.size,(128, 128, 255, 0))
    #覆盖到指定位置
    #target.paste(texTemp)
    #target.paste(texTemp2,texTemp2.getchannel("A"))
    #return target
    return texTemp


class UpdateTime(QThread):
    signal = pyqtSignal(str,str,str)   #括号里填写信号传递的参数类型，调用TimeTick的函数要和这里对应

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        global picInt
        global timeUpdate
        while True:
            timeUpdate = datetime.datetime.now() #每秒获取下时间
            strtimeS = timeUpdate.strftime('%S')

            strtimeHMS = timeUpdate.strftime('%H:%M:%S')
            strtimeW = timeUpdate.strftime('%w') #星期
            strtimeY = timeUpdate.strftime('%Y') #年
            strtimeM = timeUpdate.strftime('%m') #月
            strtimeD = timeUpdate.strftime('%d') #日

            self.signal.emit(strtimeHMS,todayWeek(strtimeW),str(strtimeY+"年"+strtimeM+"月"+strtimeD+"日"))    # 发射信号
            picInt = int(strtimeS) #每分钟更换图片

            time.sleep(1)


class UpdateBackground(QThread):
    signa2 = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        global picInt
        global picCount
        global platformBool
        # while True:
        #     if picInt == 59:#每分钟更新一次
        #
        #         picCount += 1
        #         if picCount > 5: #我就5 张图片不能大于5
        #             picCount = 0
        #         self.signa2.emit(picCount)
        #     time.sleep(1)

class UpdateWeather(QThread):
    signa3 = pyqtSignal()

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            timeUpdate = datetime.datetime.now()
            strtimeM = timeUpdate.strftime('%M') #分钟
            strtimeH = timeUpdate.strftime('%H') #小时
            strtimeW = timeUpdate.strftime('%w') #星期
            global oilStrWeek
            global tempArray

            if(strtimeW != oilStrWeek):  #每天重置更新天气
                weekStr = todayWeek(strtimeW)
                oilStrWeek = strtimeW
                countUpdate_1 = True
                countUpdate_2 = True
                countUpdate_3 = True
                countUpdate_4 = True
                tempArray = UpdateData()
                
            #天气API只有这几个点会更新,减少无用请求
            intTime = int(strtimeH)
            if(countUpdate_1 and  intTime == 7):
                tempArray = UpdateData()
                countUpdate_1 = False
            elif(countUpdate_2 and intTime == 11):
                tempArray = UpdateData()
                countUpdate_2 = False
            elif(countUpdate_3 and intTime == 16):
                tempArray = UpdateData()
                countUpdate_3 = False
            elif(countUpdate_4 and intTime == 21 ):
                tempArray = UpdateData()
                countUpdate_4 = False

            self.signa3.emit()
            time.sleep(1800) #半个小时刷新一次
 
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi(runDirectory + "/test.ui", self)
        QtGui.QFontDatabase.addApplicationFont(runDirectory +"/三极纤云简体.ttf")
        global platformBool
        if(sys.platform == "win32"):
            platformBool = True
        else:
            platformBool = False

        self.thread = UpdateTime() # 创建一个线程
        self.thread.signal.connect(self.TimeTick) #绑定信号触法的函数
        self.thread.start()    # 启动线程

        self.thread2 = UpdateBackground()
        self.thread2.signa2.connect(self.setBackground) 
        self.thread2.start()  

        self.thread3 = UpdateWeather() 
        self.thread3.signa3.connect(self.setWeather) 
        self.thread3.start() 

        #self.pushButton.clicked.connect(self.takephoto) 

        global tempArray
        tempArray = UpdateData()
        #ipTemp = get_host_ip()
        #self.label_Temp.setText("CPU温度:"+str(cpuTemp) +" GPU温度:"+ str(gpuTemp) )
        #self.label_Temp.setText("CPU:"+ str(round(cpuTemp)) + "   GPU:"+ str(round(gpuTemp)) +"  "+ tempArray[0]+" "+tempArray[21])
        #self.label_IP.setText("IP:"+ipTemp)
        self.icon_1.setPixmap(ImageLoadbyName("/icon/icon1.png",0.6))
       

        self.icon_2.setPixmap(ImageLoadbyName("/icon/icon2.png",0.6))
      
        self.show()

   


        

    def TimeTick(self,msg,msg2,msg3): #注意传参变量要写
        self.time_Label.setText(msg) 
        self.week_Label.setText(msg2)
        self.month_Label.setText(msg3)


    def setBackground(self,intCount):
        global tempArray
        img =  runDirectory+"/Background"+ str(intCount)+".jpg"

        palette = QPalette() #设置调色板
        palette.setBrush(QPalette.Background, QBrush(QPixmap(img)))
      
        self.setPalette(palette)
        #self.label_Temp.setText("CPU温度:"+str(cpuTemp) +"      GPU温度:"+ str(gpuTemp))
        #self.label_Temp.setText("CPU:"+ str(round(cpuTemp)) + "   GPU:"+ str(round(gpuTemp)) +"  "+ tempArray[0]+" "+tempArray[21])
        #self.label_IP.setText("IP:"+ipTemp)

    def setWeather(self):
        global tempArray
        self.Icon_Today.setPixmap(ImageLoad(UpdateWeatherIcon(tempArray[3]),0.8))
        self.today_Weather.setText(tempArray[3])
        self.today_Temp.setText(LowTempStr(tempArray[1]) + "~" + HightTempStr(tempArray[2]) +"度")

       

        #self.icon_3.setPixmap(ImageLoadbyName("/icon/icon3.png",0.6))
       

        self.today_wind.setText("这是啥")
       


def main():
    app=QtWidgets.QApplication(sys.argv)
    window=Ui()
    img = runDirectory+"/Background0.jpg"
    #img2 = runDirectory+"/BackgroundBlack.png"

    palette = QPalette() #启动时先设一个背景
    palette.setBrush(QPalette.Background, QBrush(QPixmap(runDirectory+"/Background4.jpg")))
    #palette.setBrush(QPalette.Background, QBrush(QPixmap.fromImage(ImageQt(CombineImage(img)))))
    window.setPalette(palette)
    if(platformBool==False):
        window.showFullScreen() #全屏显示
    app.exec_()


if __name__=="__main__":
    main()

# app = QtWidgets.QApplication(sys.argv)
# window = Ui()


# img = runDirectory+"/Background0.jpg"
# #img2 = runDirectory+"/BackgroundBlack.png"

# palette = QPalette() #启动时先设一个背景
# palette.setBrush(QPalette.Background, QBrush(QPixmap(runDirectory+"/Background4.jpg")))
# #palette.setBrush(QPalette.Background, QBrush(QPixmap.fromImage(ImageQt(CombineImage(img)))))
# window.setPalette(palette)
# if(platformBool==False):
#     window.showFullScreen() #全屏显示
# app.exec_()
