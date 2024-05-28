import time
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, \
    QMessageBox
import UI.untitled as untitled


class Label(QLabel):
    def __init__(self, text: str, height: int = 30):
        super().__init__(text)
        if text == '':
            return
        if int(text) < 0:
            self.setStyleSheet('background-color: pink; color: #ffffff;'
                               'border: 2px solid #000000; border-radius: 10px; padding: 7px;')
        else:
            self.setStyleSheet('background-color: #000000; color: #ffffff;'
                               'border: 2px solid #000000; border-radius: 10px; padding: 7px;')
        self.Height = int(height)
        self.Text = text

        # 限制标签的高度
        self.setFixedHeight(self.Height)

    def setbackground(self, color: str) -> None:
        # self.setAutoFillBackground(True)
        # palette = QPalette()
        # palette.setColor(QPalette.Window, Qt.red)
        # self.setPalette(palette)
        # palette.setColor(QPalette.Window, QColor(33, 150, 243))  # Window role用于设置标签的背景色
        self.setStyleSheet(f'background-color: {color}; color: white;'
                           'border: 2px solid #000000; border-radius: 10px; padding: 7px;')

    def setHeight(self, height: int) -> None:
        self.setFixedHeight(height)

    # def setTitle(self, Text: str) -> None:
    #     self.setText(Text)


# 数据归一化到0-1之间
def min_max_normalization(data):
    min_val = min(data)
    max_val = max(data)
    normalized_data = [(abs(x) - min_val) / (max_val - min_val) for x in data]
    return normalized_data


class Thread_sort(QtCore.QThread):
    def __init__(self, parent=None):
        super(Thread_sort, self).__init__(parent)
        self.parent = parent

    def run(self):
        self.parent.ui.pushButton.setText(f'Loading...')
        time.sleep(1)
        cnt = 0
        for i in range(self.parent.number_cnt - 1):
            # if i > 0:
            #     self.parent.labelList[i].setbackground('blue')
            #     self.parent.labelList[i - 1].setbackground('black')
            # else:
            #     self.parent.labelList[i].setbackground('blue')
            for j in range(0, self.parent.number_cnt - i - 1):
                if self.parent.number_list[j] < self.parent.number_list[j + 1]:
                    self.parent.ui.pushButton.setText(f'正在排序第{i + 1}趟 第{j + 1}次排序 共{cnt + 1}次')
                    time.sleep(0.01)
                    self.parent.swap_label(j, j + 1)
                    print(f'第{i + 1}趟第{j + 1}次排序结果为：{self.parent.number_list}')
                    cnt += 1
                    time.sleep(1)

        self.parent.ui.pushButton.setText(f'排序完成！')
        self.parent.ui.pushButton.setStyleSheet('background-color: green; color: black;'
                                                'border: 2px solid #000000; border-radius: 10px; padding: 7px;')


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.labelList = []
        self.Yscreen = None
        self.Xscreen = None

        un = untitled.Ui_Form()
        self.ui = un
        self.ui.setupUi(self)
        self.setWindowTitle('冒泡排序')
        s = QIcon('../src/icon.ico')
        self.setWindowIcon(s)
        # self.ui.horizontalLayout_2.setAlignment(Qt.AlignLeft)
        self.ui.horizontalLayout_2.setAlignment(Qt.AlignCenter)
        self.ui.verticalLayout.setAlignment(Qt.AlignCenter)
        vbox = QVBoxLayout(self)
        label = Label('', 0)
        vbox.addWidget(label, alignment=Qt.AlignLeft)
        vbox.setAlignment(Qt.AlignBottom)
        self.ui.horizontalLayout_2.addLayout(vbox)

        # 按键触发
        self.ui.pushButton.clicked.connect(self.on_click)

        self.ui.lineEdit_2.setPlaceholderText('请输入数组长度')
        self.ui.lineEdit.setPlaceholderText('请输入数组元素(用空格分隔)')
        self.ui.pushButton.setStyleSheet('background-color: rgb(255, 110, 66); color: black;'
                                         'border: 2px solid #000000; border-radius: 10px; padding: 7px;')

        self.number_list = None
        self.number_cnt = None
        self.avg = None
        self.normalized_data = None


    def init(self, n: int, arr: list) -> None:
        self.avg = sum(arr) / n
        self.number_list = arr
        self.number_cnt = n
        self.Yscreen = min(960, n * 30)
        self.Xscreen = min(1920 - 10, n * 40)
        self.Yscreen = max(self.Yscreen, 100)
        self.Xscreen = max(self.Xscreen, 100)
        self.resize(max(self.Xscreen, 600), max(self.Yscreen, 500))

        # 得到归一化数据
        self.normalized_data = min_max_normalization(arr)
        # self.ui.setMinimumSize(0, 0)
        self.ui.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, max(self.Xscreen, 600), max(self.Yscreen, 500)))
        for i in range(n):
            vbox = QVBoxLayout(self)
            label = Label(str(arr[i]), height=self.get_label_height(self.normalized_data[i] * 10 + 1))  # 实例化label的高度
            self.labelList.append(label)
            vbox.addWidget(label, alignment=Qt.AlignLeft)
            vbox.setAlignment(Qt.AlignBottom)
            self.ui.horizontalLayout_2.addLayout(vbox)

    def on_click(self):
        try:
            self.number_cnt = int(self.ui.lineEdit_2.text())
        except ValueError:
            QMessageBox.warning(self, '错误', '请输入整数数组长度！', QMessageBox.Yes)
            return
        self.number_list = list(map(int, self.ui.lineEdit.text().split()))
        if len(self.number_list) != self.number_cnt:
            QMessageBox.warning(self, '错误', '数组长度与输入元素个数不匹配！', QMessageBox.Yes)
            return
        if self.number_cnt is None or self.number_list is None:
            QMessageBox.warning(self, '错误', '请输入数组长度和数组元素！', QMessageBox.Yes)
            return
        self.init(self.number_cnt, self.number_list)
        start = Thread_sort(self)
        start.start()
        self.ui.pushButton.setEnabled(False)  # 禁用按钮

        # for i in range(len(self.labelList)):
        #     self.labelList[i].setHeight(self.labelList[self.number_cnt - 1 - i].Height)
        #     self.labelList[i].setText(str(self.labelList[self.number_cnt - 1 - i].Text))
        #     self.labelList[i].setbackground('red')

    def swap_label(self, i: int, j: int):
        self.labelList[i].setbackground('blue')
        time.sleep(0.01)
        self.labelList[j].setbackground('red')
        time.sleep(0.5)  # 动画效果
        self.number_list[i], self.number_list[j] = self.number_list[j], self.number_list[i]
        th = self.labelList[i].Height
        ts = self.labelList[i].Text
        self.labelList[i].Height = self.labelList[j].Height
        self.labelList[i].Text = self.labelList[j].Text
        self.labelList[i].setHeight(self.labelList[j].Height)
        self.labelList[i].setText(str(self.labelList[j].Text))
        time.sleep(0.01)
        self.labelList[j].Height = th
        self.labelList[j].Text = str(ts)
        self.labelList[j].setHeight(th)
        self.labelList[j].setText(str(ts))

        time.sleep(0.01)  # 动画效果
        self.labelList[i].setbackground('red')
        time.sleep(0.01)
        self.labelList[j].setbackground('blue')
        time.sleep(0.7)
        if int(self.labelList[i].Text) < 0:
            self.labelList[i].setbackground('pink')
        else:
            self.labelList[i].setbackground('black')
        time.sleep(0.01)
        if int(self.labelList[j].Text) < 0:
            self.labelList[j].setbackground('pink')
        else:
            self.labelList[j].setbackground('black')

    def get_label_height(self, x: float) -> int:
        t = self.number_cnt
        # y = x * 1080*(-0.025x^2+1.73x-8.2) // self.Yscreen + 10
        #
        return int(min(self.Yscreen * 2.5,
                   abs(x) * 1080 * max(- 0.025 * (t ** 2) + 1.65 * t - 8.2, 2) // self.Yscreen + 10))

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            if self.ui.lineEdit.text() == '' and self.ui.lineEdit_2.text() != '':
                self.focusNextChild()
            else:
                self.on_click()

# 5 -- 2.5
# 10 -- 7
# 20 -- 15
# 30 -- 23
# 40 -- 20
# 50 -- 16
# y = x*0.2+9
