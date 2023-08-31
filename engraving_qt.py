#!/usr/bin/python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, \
    QApplication, QDesktopWidget, QPushButton, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator
from PyQt5.QtCore import Qt
import sys
import json
import os
from engraving import calculate


class Engraving(QWidget):

    def __init__(self):
        super().__init__()
        img_path = os.path.join(os.getcwd(), 'data', 'imgs')
        self.icon_unlock = QIcon(os.path.join(img_path, 'unlock.png'))
        self.icon_locked = QIcon(os.path.join(img_path, 'lock.png'))
        self.label = QLabel("刻印目标", self)
        self.label_stone = QLabel("能力石选择(默认77石头)", self)
        self.label_talent = QLabel("天赋槽(默认12 9)", self)
        self.label_jewelry = QLabel("首饰", self)
        self.label_res = QLabel("0/0", self)
        self.button_next = QPushButton(self)  # 输出结果翻页按钮
        self.button_go = QPushButton(self)  # 输出结果跳转按钮
        self.text_page = QLineEdit(self)  # 输出结果跳转
        self.label_jewelry_plot1 = QLabel("5", self)
        self.label_jewelry_plot2 = QLabel("3", self)
        self.combos_engraving = []  # 首饰下拉框
        self.combos_stone = []  # 能力石下拉框
        self.combos_talent = []  # 天赋下拉框
        self.combos_jewelry1 = []  # 首饰下拉框1 对应铭刻5
        self.combos_jewelry2 = []  # 首饰下拉框2 对应铭刻3
        self.buttons_jewelry = []  # 首饰锁定按钮
        self.buttons_jewelry_pressed = [False, False, False, False, False]
        self.data_engraving = []
        self.total_engraving = []  # 所有刻印列表
        self.selected_engraving = ['', '', '', '', '']  # 所有已选中刻印
        self.total_stone = []
        self.selected_stone = ['', '']  # 已选择能力石
        self.data_stone = []
        self.total_talent = []
        self.selected_talent = ['', '']  # 已选择天赋
        self.data_talent = []
        self.read_engravings()  # 初始化刻印选项
        self.read_stones()
        self.read_talent()
        self.button_cal = QPushButton(self)
        self.init_combo()  # 初始化下拉框
        self.init_ui()  # 初始化界面布局
        self.result = []  # 储存计算结果

    def init_combo(self):
        for _ in range(len(self.selected_engraving)):
            self.combos_engraving.append(QComboBox(self))
            self.combos_jewelry1.append(QComboBox(self))
            self.combos_jewelry2.append(QComboBox(self))
            self.buttons_jewelry.append(QPushButton(self))
        for _ in range(len(self.selected_stone)):
            self.combos_stone.append(QComboBox(self))
            self.combos_talent.append(QComboBox(self))

    def reload_engraving(self):
        for i in range(len(self.selected_engraving)):
            self.data_engraving[i] = [item['name'] for item in self.total_engraving
                                      if item['name'] not in self.selected_engraving
                                      or item['name'] == self.selected_engraving[i]]

    def reload_stone(self):
        for i in range(len(self.selected_stone)):
            self.data_stone[i] = [item['name'] for item in self.total_stone
                                  if item['name'] not in self.selected_stone
                                  or item['name'] == self.selected_stone[i]]

    def reload_talent(self):
        for i in range(len(self.selected_talent)):
            self.data_talent[i] = [item['name'] for item in self.total_talent
                                   if item['name'] not in self.selected_talent
                                   or item['name'] == self.selected_talent[i]]

    def read_engravings(self):
        data_path = os.path.join(os.getcwd(), 'data', 'engraving.json')
        f = open(data_path, encoding='utf-8')
        data = json.load(f)
        f.close()
        self.total_engraving = data
        for _ in range(len(self.selected_engraving)):
            self.data_engraving.append([item['name'] for item in self.total_engraving])

    def read_stones(self):
        data_path = os.path.join(os.getcwd(), 'data', 'stone.json')
        f = open(data_path, encoding='utf-8')
        data = json.load(f)
        f.close()
        self.total_stone = data
        for _ in range(len(self.selected_stone)):
            self.data_stone.append([item['name'] for item in self.total_stone])

    def read_talent(self):
        data_path = os.path.join(os.getcwd(), 'data', 'talent.json')
        f = open(data_path, encoding='utf-8')
        data = json.load(f)
        f.close()
        self.total_talent = data
        for _ in range(len(self.selected_talent)):
            self.data_talent.append([item['name'] for item in self.total_talent])

    def lock_or_unlock(self, pressed):
        sender = self.sender()
        for i in range(len(self.selected_engraving)):
            if self.buttons_jewelry[i] == sender:
                if self.buttons_jewelry_pressed[i]:
                    self.buttons_jewelry[i].setIcon(self.icon_unlock)
                    self.combos_jewelry1[i].setEnabled(True)
                    self.combos_jewelry2[i].setEnabled(True)
                    self.buttons_jewelry_pressed[i] = False
                else:
                    self.buttons_jewelry[i].setIcon(self.icon_locked)
                    self.combos_jewelry1[i].setEnabled(False)
                    self.combos_jewelry2[i].setEnabled(False)
                    self.buttons_jewelry_pressed[i] = True

    def center(self):
        # 获取窗口的大小
        window_size = self.geometry()
        # 获取屏幕的大小
        screen = QDesktopWidget().screenGeometry()
        # 计算窗口居中时的左上角位置
        x = (screen.width() - window_size.width()) // 2
        y = (screen.height() - window_size.height()) // 2
        # 将窗口移动到居中的位置
        self.move(x, y)

    def init_ui(self):
        # self.setStyleSheet("background-color: #FFFFFF;")
        for i in range(5):
            for item in self.data_engraving[i]:
                self.combos_engraving[i].addItem(item)
                self.combos_engraving[i].setCurrentIndex(-1)
                self.combos_engraving[i].move(190 + 100 * i, 50)
                self.combos_engraving[i].currentIndexChanged.connect(self.engraving_selection_changed)
            self.combos_jewelry1[i].move(190 + 100 * i, 260)
            self.combos_jewelry1[i].setCurrentIndex(-1)
            self.combos_jewelry2[i].move(190 + 100 * i, 295)
            self.combos_jewelry2[i].setCurrentIndex(-1)
            self.buttons_jewelry[i].setIcon(self.icon_unlock)  # 初始化锁定图标
            self.buttons_jewelry[i].clicked[bool].connect(self.lock_or_unlock)  # 锁定、解锁首饰配置
            self.buttons_jewelry[i].move(190 + 100 * i, 325)
        for i in range(2):
            for item in self.data_stone[i]:
                self.combos_stone[i].addItem(item)
                self.combos_stone[i].setCurrentIndex(-1)
                self.combos_stone[i].move(190 + 100 * i, 120)
                self.combos_stone[i].currentIndexChanged.connect(self.stone_selection_changed)
            for item in self.data_talent[i]:
                self.combos_talent[i].addItem(item)
                self.combos_talent[i].setCurrentIndex(-1)
                self.combos_talent[i].move(190 + 100 * i, 190)
                self.combos_talent[i].currentIndexChanged.connect(self.talent_selection_changed)
        self.label.move(50, 50)
        self.label_stone.move(50, 120)
        self.label_talent.move(50, 190)
        self.label_jewelry.move(50, 260)
        self.label_jewelry_plot1.move(170, 265)
        self.label_jewelry_plot2.move(170, 300)
        self.setGeometry(0, 0, 900, 600)
        self.center()
        self.setWindowTitle('刻印计算器V0.1')
        self.button_cal.setText('开始计算')
        self.button_cal.clicked[bool].connect(self.cal_engraving)
        self.label_res.move(710, 260)
        self.button_next.move(790, 255)
        self.button_next.setFixedSize(60, 25)
        self.button_next.setText('下一页')
        self.button_next.clicked[bool].connect(self.next_page)
        self.text_page.move(710, 290)
        self.text_page.setFixedSize(40, 25)
        self.text_page.setText('1')
        self.text_page.setAlignment(Qt.AlignCenter)  # 设置文本居中
        self.text_page.setValidator(QIntValidator())
        self.button_go.move(790, 290)
        self.button_go.setText('跳转到')
        self.button_go.setFixedSize(60, 25)
        self.button_go.clicked[bool].connect(self.go_target_page)
        self.button_cal.move(350, 400)
        self.show()

    def next_page(self):
        current_page = int(self.label_res.text().split('/')[0])
        if current_page == 0:
            self.message('你都还没开始算，翻啥？')
        elif current_page + 1 > len(self.result):
            self.message('别翻了，没有了')
        else:
            self.set_jewelries(self.result[current_page], current_page+1)

    def go_target_page(self):
        target_page = int(self.text_page.text())
        if target_page > len(self.result):
            self.message('睁大你的眼睛看看有多少页！')
        elif target_page < 1:
            self.message('第一页前面你觉得还有几页？')
        else:
            self.set_jewelries(self.result[target_page-1], target_page)

    ''' 检查是否已选择五个刻印 '''
    def check_selected_engraving(self):
        for item in self.selected_engraving:
            if item == '':
                return False
        return True

    def cal_engraving(self):
        # 读取目标刻印信息
        if self.check_selected_engraving():
            # 计算已固定首饰
            template = [(), (), (), (), ()]  # 固定首饰模板
            for i in range(len(self.buttons_jewelry_pressed)):
                if self.buttons_jewelry_pressed[i]:
                    jewelry = (self.combos_jewelry1[i].currentText(), self.combos_jewelry2[i].currentText())
                    template[i] = jewelry
            stones = (self.selected_stone[0], self.selected_stone[1])
            talents = (self.selected_talent[0], self.selected_talent[1])
            res = calculate(self.selected_engraving, template, stones, talents)
            if res:
                self.set_jewelries(res[0], 1)
                self.result = res
                self.label_res.setText('%d/%d' % (1, len(res)))
            else:
                self.message('当前选择没有可用配装方案！')
        else:
            self.message('请将五个目标刻印选择完毕！')

    @staticmethod
    def message(text):
        message_box = QMessageBox()
        message_box.setWindowTitle("警告")
        message_box.setText(text)
        message_box.addButton("确定", QMessageBox.AcceptRole)  # 确定按钮
        # 显示消息框，并等待用户操作
        message_box.exec_()
        # 启动应用程序的事件循环
        app.exec_()

    def set_jewelries(self, jewelries, page):
        for i in range(len(jewelries)):
            if self.buttons_jewelry_pressed[i]:
                continue
            self.combos_jewelry1[i].setCurrentIndex(self.combos_jewelry1[i].findText(jewelries[i][0]))
            self.combos_jewelry2[i].setCurrentIndex(self.combos_jewelry1[i].findText(jewelries[i][1]))
        self.label_res.setText('%d/%d' % (page, len(self.result)))

    def engraving_selection_changed(self, index):
        sender = self.sender()
        if sender.currentIndex() != -1:
            for i in range(5):
                self.selected_engraving[i] = self.combos_engraving[i].currentText()
            self.reload_engraving()
            for i in range(5):
                # 清空首饰可选刻印
                self.combos_jewelry1[i].clear()
                self.combos_jewelry2[i].clear()
                # 更新可选首饰刻印
                for j in range(len(self.selected_engraving)):
                    if self.selected_engraving[j]:
                        self.combos_jewelry1[i].addItem(self.selected_engraving[j])
                        self.combos_jewelry2[i].addItem(self.selected_engraving[j])
                self.combos_jewelry1[i].setCurrentIndex(-1)
                self.combos_jewelry2[i].setCurrentIndex(-1)
                # 动态更新可选铭刻列表
                if self.combos_engraving[i] != sender:
                    for item in self.data_engraving[i]:
                        if self.combos_engraving[i].findText(item) == -1:
                            self.combos_engraving[i].addItem(item)
                    items = [self.combos_engraving[i].itemText(x) for x in range(self.combos_engraving[i].count())]
                    for item in items:
                        if item not in self.data_engraving[i]:
                            self.combos_engraving[i].blockSignals(True)
                            self.combos_engraving[i].removeItem(self.combos_engraving[i].findText(item))
                            self.combos_engraving[i].blockSignals(False)

    def stone_selection_changed(self, index):
        sender = self.sender()
        if sender.currentIndex() != -1:
            for i in range(2):
                self.selected_stone[i] = self.combos_stone[i].currentText()
            self.reload_stone()
            for i in range(2):
                if self.combos_stone[i] != sender:
                    for item in self.data_stone[i]:
                        if self.combos_stone[i].findText(item) == -1:
                            self.combos_stone[i].addItem(item)
                    items = [self.combos_stone[i].itemText(x) for x in range(self.combos_stone[i].count())]
                    for item in items:
                        if item not in self.data_stone[i]:
                            self.combos_stone[i].blockSignals(True)
                            self.combos_stone[i].removeItem(self.combos_stone[i].findText(item))
                            self.combos_stone[i].blockSignals(False)

    def talent_selection_changed(self, index):
        sender = self.sender()
        if sender.currentIndex() != -1:
            for i in range(2):
                self.selected_talent[i] = self.combos_talent[i].currentText()
            self.reload_talent()
            for i in range(2):
                if self.combos_talent[i] != sender:
                    for item in self.data_talent[i]:
                        if self.combos_talent[i].findText(item) == -1:
                            self.combos_talent[i].addItem(item)
                    items = [self.combos_talent[i].itemText(x) for x in range(self.combos_talent[i].count())]
                    for item in items:
                        if item not in self.data_talent[i]:
                            self.combos_talent[i].blockSignals(True)
                            self.combos_talent[i].removeItem(self.combos_talent[i].findText(item))
                            self.combos_talent[i].blockSignals(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Engraving()
    sys.exit(app.exec_())
