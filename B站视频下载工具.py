import os,sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtWidgets import QTextEdit, QWidget, QLineEdit, QLabel, QPushButton, QFileDialog, QApplication, qApp, \
    QCheckBox
import re
import requests
import sys

#打包工具
# pyinstaller -w B站视频下载工具.py --icon billicon.ico --clean --win-private-assemblies
# pyinstaller --clean --win-private-assemblies -F XXXX.py --clean


class Window_bill(QWidget):
    def __init__(self):
        super().__init__()
        self.file_bill = ["./Download"]
        self.setWindowTitle("BillBill视频下载工具v1.5γ")
        self.setFixedSize(500, 300)
        self.setWindowIcon(QIcon("./source/billicon.png"))
        self.setWindowOpacity(0.95)
        with open("bill.qss","r") as f:
            qApp.setStyleSheet(f.read())
        # cookie标签
        self.lable_cookie = QPushButton(self)
        self.lable_cookie.move(22, 13)
        self.lable_cookie.setObjectName("lab_cookie")
        self.lable_cookie.setText("Cookie：")
        self.lable_cookie.setFlat(True)
        self.lable_cookie.setToolTip("点击查看如何获得cookie")
        self.tip = QLabel()
        self.tip.setWindowTitle("cookie值的获取")
        self.tip.setWindowIcon(QIcon("./source/billicon.png"))
        self.gif = QMovie("./source/cookie.gif")
        self.tip.setMovie(self.gif)
        self.tip.setVisible(False)
        self.lable_cookie.clicked.connect(self.cook_tip)
        # cookie输入框
        self.edit_cookie = QLineEdit(self)
        self.edit_cookie.setPlaceholderText("请输入你的cookie数据")
        self.edit_cookie.resize(340, 22)
        self.edit_cookie.move(120, 25)
        # 视频url标签
        self.lable_bill = QLabel(self)
        self.lable_bill.move(25, 75)
        self.lable_bill.setObjectName("lab_bill")
        self.lable_bill.setText("视频链接：")
        # 视频输入框
        self.edit_url = QLineEdit(self)
        self.edit_url.setPlaceholderText("请输入视频链接：")
        self.edit_url.resize(335, 22)
        self.edit_url.move(125, 80)
        # 下载按钮
        self.button = QPushButton(QIcon("./source/bill_download.png"), "下载", self)
        self.button.resize(70, 30)
        self.button.move(70, 260)
        self.button.setShortcut("Alt+D")
        self.button.clicked.connect(self.w)
        # 消息框
        self.message = QTextEdit(self)
        self.message.resize(460, 135)
        self.message.move(18, 117)
        self.message.setObjectName('message')
        self.message.setLineWrapMode(QTextEdit.NoWrap)
        #选择文件按钮
        self.btn_file = QPushButton(self)
        self.btn_file.setIcon(QIcon("./source/bill_file.png"))
        self.btn_file.move(210,260)
        self.btn_file.resize(90, 30)
        self.btn_file.setText("保存路径")
        self.btn_file.setObjectName('btn_file')
        self.btn_file.clicked.connect(self.getfile)
        #关于
        self.about = QPushButton(self)
        self.about.move(473,277)
        self.about.setIcon(QIcon("./source/aboutme.png"))
        self.about.setFlat(True)
        self.about_window = QWidget()
        self.about_window.setWindowIcon(QIcon("./source/aboutme.png"))
        self.about_window.setWindowTitle("感谢大家的支持(≧∇≦)ﾉ")
        self.about_window.setFixedSize(300,160)
        self.about_window.setVisible(False)
        self.about_software_logo = QLabel(self.about_window)
        self.about_software_logo.move(20,20)
        self.about_software_logo.setPixmap(QPixmap("./source/billicon.png"))
        self.about_software_logo.setVisible(True)
        self.about_software_text = QLabel(self.about_window)
        self.about_software_text.move(58, 25)
        self.about_software_text.setText("BillBill视频下载工具v1.5γ")
        self.about_software_text.setObjectName("about_software_text")
        self.about_software_text.setVisible(True)
        self.about_author = QLabel(self.about_window)
        self.about_author.move(95,67)
        self.about_author.setText("作者:")
        self.about_author.setObjectName('about_author')
        self.about_author.setVisible(True)
        self.about_authorname = QLabel(self.about_window)
        self.about_authorname.move(135, 65)
        self.about_authorname.setText("SamRol")
        self.about_authorname.setObjectName('about_authorname')
        self.about_authorname.setOpenExternalLinks(True)
        self.about_authorname.setVisible(True)
        self.about_feekback = QLabel(self.about_window)
        self.about_feekback.move(40, 107)
        self.about_feekback.setText("Bug反馈：")
        self.about_feekback.setObjectName('about_feekback')
        self.about_feekback.setVisible(True)
        self.about_email = QLabel(self.about_window)
        self.about_email.move(110, 107)
        self.about_email.setText("B站搜索用户SamRol_")
        self.about_email.setObjectName('about_email')
        self.about_email.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.about_email.setVisible(True)
        self.about.clicked.connect(self.about_sg)
        #视频合成按钮
        self.checkbox = QCheckBox(self)
        self.checkbox.move(360,263)
        self.checkbox.setText("合成视频")
        self.checkbox.setObjectName('checkbox')
        self.checkbox.setCheckState(Qt.Checked)
        self.checkbox.stateChanged.connect(self.cheak)
    #信号事件----gif播放
    def cook_tip(self):
        self.tip.setVisible(True)
        self.gif.start()
        self.tip.adjustSize()
    #信号事件----爬虫codes
    def w(self):
            if (self.edit_url.isModified() == False & self.edit_cookie.isModified() == False):
                self.message.insertPlainText("请输入内容!\n")
            else:
                try:
                    headers = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                        "referer": "https://www.bilibili.com/",
                        "cookie": self.edit_cookie.text().strip()
                    }
                    headers_barrage = {
                        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                    }
                    # 视频链接
                    url = "{0}".format(self.edit_url.text())
                    #获取bv号
                    bill_bv = url.rpartition('/?')
                    bill_bv = str(bill_bv[0]).rpartition('/')
                    print("BV号："+bill_bv[-1])
                    #封面链接
                    url_cover="https://api.bilibili.com/x/web-interface/search/all/v2?__refresh__=true&_extra=&context=&page=1&page_size=42&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword={0}&preload=true&com2co=true".format(bill_bv[-1])
                    # ibill链接
                    url_ibilil = f"https://www.ibilibili.com/video/{bill_bv[-1]}"
                    print(url)
                    resp = requests.get(url=url, headers=headers).text
                    resp = resp.encode("gbk", "ignore").decode("gbk", "ignore")
                    #print(resp)
                    # 正则
                    obj = re.compile(r'"baseUrl":"(.*?)"', re.S)
                    obj_name = re.compile(r'class="video-title" data-v-4f1c0915>(.*?)</h1>', re.S)
                    voide_url = obj.findall(resp)
                    voide_name = obj_name.findall(resp)
                    voide_name = str(voide_name[0]).replace(" ","").lower().replace(":","")
                    # 输出检查
                    print("视频名:", voide_name)
                    print("视频：", voide_url[0])
                    print("音频：", voide_url[-1])
                    self.message.insertPlainText("视频名：{0}\n".format(voide_name))
                    self.message.insertPlainText("视频url：{0}\n\n".format(voide_url[0]))
                    self.message.insertPlainText("音频url：{0}\n\n".format(voide_url[-1]))

                    #获取封面re解析、request
                    try:
                        resp_cover = requests.get(url=url_cover, headers=headers).json()
                        cover1 = resp_cover['data']['result'][11]['data'][0]['pic']
                        cover = "https:" + cover1
                        print(cover)
                        self.message.insertPlainText(f"封面地址:{cover}\n\n")
                    except:
                        print("获取封面失败")
                        self.message.insertPlainText("获取封面失败\n\n")
                    #获取弹幕re解析、request
                    try:
                        resp_ibill = requests.get(url_ibilil,headers=headers_barrage).text
                        url_Barrage = re.findall('<a href="(.*?)"  class="btn btn-default" target="_blank">弹幕</a>', resp_ibill)[0]
                        self.message.insertPlainText(f"弹幕地址为：{url_Barrage}\n")
                        Barrage = requests.get(url_Barrage, headers)
                        Barrage.encoding = 'utf-8'
                        content_list = re.findall('<d p=".*?">(.*?)</d>', Barrage.text)
                    except:
                        print("获取弹幕失败")
                        self.message.insertPlainText("获取弹幕失败或此视频没有弹幕\n")

                    #创建文件夹
                    try:
                        self.message.insertPlainText("正在创建文件夹...\n")
                        os.mkdir("{0}/{1}".format(self.file_bill[0],voide_name), 0o755)
                    except:
                        self.message.insertPlainText("文件夹已存在。\n")

                    # 下载视频
                    try:
                        resp_video = requests.get(voide_url[0], headers=headers)
                        with open("{0}/{1}/{2}.mp4".format(self.file_bill[0],voide_name,voide_name), mode="wb") as f:
                            f.write(resp_video.content)
                    except:
                        print("下载视频失败")
                    # 下载音频
                    try:
                        resp_audio = requests.get(voide_url[-1], headers=headers)
                        with open("{0}/{1}/{2}.mp3".format(self.file_bill[0],voide_name,voide_name), mode="wb") as f:
                            f.write(resp_audio.content)
                    except:
                        print("下载音频失败")
                    # 下载封面
                    try:
                        resp_cover_now = requests.get(url=cover, headers=headers)
                        with open("{0}/{1}/{2}.jpg".format(self.file_bill[0],voide_name,voide_name), mode="wb") as f:
                            f.write(resp_cover_now.content)
                    except:
                        print("下载封面失败")
                    #保存字幕
                    try:
                        for index in content_list:
                            with open(f'{self.file_bill[0]}/{voide_name}/{voide_name}的弹幕.txt', mode='a', encoding='utf-8') as f:
                                f.write(index)
                                f.write('\n')
                    except:
                        print("弹幕下载失败")
                    # print("下载完成")
                    self.message.insertPlainText("下载完成！\n")
                    try:
                        if(int(self.checkbox.checkState())==2):
                            self.message.insertPlainText("正在音频和视频合成<(￣︶￣)↗[GO!]\n")
                            path = os.path.abspath('./')
                            os.environ['WORKON_HOME'] = path
                            cmd = f"ffmpeg -i  {self.file_bill[0]}/{voide_name}/{voide_name}.mp3  -i {self.file_bill[0]}/{voide_name}/{voide_name}.mp4  {self.file_bill[0]}/{voide_name}/{voide_name}合成.mp4"
                            os.system(cmd)

                        else:
                            print("没选合成")
                    except:
                        self.message.insertPlainText("合成视频失败!(っ °Д °;)っ\n")
                    self.message.insertPlainText("保存路径为：{0}\n".format(self.file_bill[0]))

                except Exception as e:
                    print(e)
                    self.message.insertPlainText("请确认视频地址和Cookie值有没有输错\n")
    #信号事件----设置路径
    def getfile(self):
        file = QFileDialog.getExistingDirectory(caption="选择文件夹", directory="./")
        self.file_bill.clear()
        self.file_bill.append(file)
        print("file_bill列表：{0}".format(self.file_bill))
        self.message.insertPlainText("\n设置保存路径为：{0}\n".format(self.file_bill[0]))
    # 信号事件----关于
    def about_sg(self):
        self.about_window.setVisible(True)
    #信号事件----选择框
    def cheak(self):
        print(int(self.checkbox.checkState()))
        if(int(self.checkbox.checkState())==0):
            self.message.insertPlainText("合成关闭\n")
        else:
            self.message.insertPlainText("合成打开\n")
if __name__ == '__main__':
    app = QApplication(sys.argv)
    #billbill
    window_bill = Window_bill()
    window_bill.show()
    sys.exit(app.exec_())
