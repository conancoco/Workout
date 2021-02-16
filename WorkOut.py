#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   main.py    
@Contact :   ikelex.ca@gmail.com
@License :   (C)Copyright 2020-2021, IKELEX
@Goal    :   灵活制定个人健身计划，包括动作的搭配及协调，时长和运动量的规划等
@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2020/5/2 15:39   ili        1.0         Initial
"""

import os
import time
import datetime as dt
import numpy as np
import pandas as pd
import pyttsx3
import winsound
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from PIL import Image


def StandardFrame(root, row: int, col: int, height: int, width=200, rowspan=1, columnspan=1) -> tk.Frame:
    '''
    @Description:
        Generate a standard frame for the GUI
    @param:
        x    :   grid number of column
        y    :   grid number of row
        height  :   height of Frame
        width   :   width of Frame
    @return:
        frame    :   tk.Frame
    @comment:
        <++>
    '''
    frame = tk.Frame(master=root, height=height, width=width, relief='groove', highlightbackground='blue', bd=5)
    frame.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)
    return frame


def StandardButton(master, text: str, row: int, col: int, height=10, width=6, rowspan=1, columnspan=1) -> tk.Button:
    '''
    @Description:
        Generate a standard Button for the GUI
    @param:
        x    :   grid number of column
        y    :   grid number of row
        height  :   height of Button
        width   :   width of Button
    @return:
        widget    :   tk.Button
    @comment:
        <++>
    '''
    widget = tk.Button(master=master, width=width, text=text, font=('华文行楷', 14))
    widget.grid(row=row, column=col, rowspan=rowspan, columnspan=columnspan)
    return widget


def StandardCheck(master, text: str, row: int, col: int, variable, height=10, width=6):
    '''
    @Description:
        Generate a standard Button for the GUI
    @param:
        x    :   grid number of column
        y    :   grid number of row
        height  :   height of Button
        width   :   width of Button
    @return:
        widget    :   tk.Button
    @comment:
        <++>
    '''
    widget = tk.Checkbutton(master=master, width=width, text=text, font=('Courier New', 14), variable=variable)
    widget.grid(row=row, column=col)
    return widget


def StandardLabel(master, row: int, col: int, text: str, height=0, width=0, chFont='华文行楷', stick='ew') -> tk.Label:
    """
    @Description:
        Generate a standard Label for the GUI
    @param:
        x    :   grid number of column
        y    :   grid number of row
        height  :   height of Label
        width   :   width of Label
    @return:
        widget    :   tk.Label
    @comment:
        <++>
    """
    widget = tk.Label(master=master, width=width, text=text, font=(chFont, 18))
    widget.grid(row=row, column=col, sticky=stick)
    return widget


def StandardTreeview(master):
    """
    @Description:
        Generate a standard Multi-columns List for the GUI
    @param:
        x    :   grid number of column
        y    :   grid number of row
        height  :   height of Label
        width   :   width of Label
    @return:
        widget    :   tk.Label
    @comment:
        <++>
    """
    col = ['code', 'name', 'cat', 'tar', 'eqp', 'lvl', 'len']
    width = [360, 180, 180, 240, 360, 120, 120, 60]
    head = ['代码', '名称', '分类', '部位', '器材', '等级', '长度']

    widget = ttk.Treeview(master=master, columns=col, show='headings')
    widget.grid(row=0, column=0, sticky='EW', columnspan=1)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=('华文行楷', 18))
    style.configure("Treeview", font=('Courier', 14))

    vsb = ttk.Scrollbar(master=master, orient="vertical", command=widget.yview)
    widget.configure(yscrollcommand=vsb.set)
    vsb.grid(row=0, column=1, sticky='NS')

    for i, val in enumerate(col):
        widget.column(val, width=width[i], anchor='center')
        widget.heading(val, text=head[i])

    return widget


class SelCourse(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry('+0+200')
        self.para = Para()
        self.varCat = [tk.BooleanVar() for i in range(len(self.para.tupleCatego))]
        self.varTar = [tk.BooleanVar() for i in range(len(self.para.tupleTarget))]
        self.varEqp = [tk.BooleanVar() for i in range(len(self.para.tupleEquip))]

        frameCheck = StandardFrame(self.root, 0, 0, 500)
        self.Frame(frameCheck)
        self.frameShow = StandardFrame(self.root, 0, 1, 420)

        self.b1 = StandardButton(self.root, '确认', 1, 0)
        self.b1.bind('<Button-1>', self.FilterSelected)

        self.engine = pyttsx3.init()
        self.engine.setProperty('voice', self.engine.getProperty('voices')[2].id)

        self.root.mainloop()

    def Frame(self, master):
        StandardLabel(master, 0, 0, '类型')
        for i, cat in enumerate(self.para.tupleCatego):
            c = StandardCheck(master, cat[1:], i + 1, 0, variable=self.varCat[i])
            c.deselect()

        StandardLabel(master, 0, 1, '部位')
        for i, tar in enumerate(self.para.tupleTarget):
            c = StandardCheck(master, tar[1:], i + 1, 1, variable=self.varTar[i])
            c.deselect()

        StandardLabel(master, 0, 2, '类型')
        for i, eqp in enumerate(self.para.tupleEquip):
            c = StandardCheck(master, eqp[1:], i + 1, 2, variable=self.varEqp[i])
            c.deselect()

    def FilterInput(self):
        cat = [each.get() for each in self.varCat]
        cat = [self.para.tupleCatego[i] for i, val in enumerate(cat) if val]

        tar = [each.get() for each in self.varTar]
        tar = [self.para.tupleTarget[i] for i, val in enumerate(tar) if val]

        eqp = [each.get() for each in self.varEqp]
        eqp = [self.para.tupleEquip[i] for i, val in enumerate(eqp) if val]

        return cat, tar, eqp

    def FilterCourse(self, cat, tar, eqp):
        dfCourse = self.para.dfCourse[['cod', 'nam', 'cat', 'tgt', 'eqp', 'lvl', 'len']]

        if cat:
            dfCourse = dfCourse[dfCourse.iloc[:, 2].apply(lambda x: (any(i in x for i in cat)))]

        if tar:
            dfCourse = dfCourse[dfCourse.iloc[:, 3].apply(lambda x: (any(i in x for i in tar)))]

        if eqp:
            dfCourse = dfCourse[dfCourse.iloc[:, 4].apply(lambda x: (any(i in x for i in eqp)))]

        return dfCourse

    def ShowCourse(self, dfCourse):
        self.coursePool = StandardTreeview(master=self.frameShow)
        button = StandardButton(self.frameShow, '确认', 1, 0)
        button.bind('<ButtonRelease-1>', self.CourseSelected)

        for i, row in dfCourse.iterrows():
            self.coursePool.insert('', 'end', values=list(row))

    def FilterSelected(self, event):
        cat, tar, eqp = self.FilterInput()
        dfCourse = self.FilterCourse(cat, tar, eqp)
        if len(dfCourse.index):
            self.ShowCourse(dfCourse)

    def CourseSelected(self, event):
        course = self.coursePool.item(self.coursePool.focus())['values']
        courseName = course[0]
        print(course)
        self.root.destroy()
        dfCourse = pd.read_excel(self.para.xlsxSource, sheet_name='detail')
        dfCourse = dfCourse[dfCourse['course'] == courseName].reset_index()

        _PlayCourse(self.engine, course, dfCourse)


class Para():
    def __init__(self):
        currentPath = str.join('/', os.path.abspath(__file__).split('\\')[0:-1]) + '/'
        self.xlsxSource = currentPath + 'motion.xlsx'
        self.txtMotionHistory = currentPath + 'record.txt'

        self.tupleCatego = tuple(pd.read_excel(self.xlsxSource, sheet_name='category', engine='openpyxl', header=0)['cat'])
        self.tupleTarget = tuple(pd.read_excel(self.xlsxSource, sheet_name='target', engine='openpyxl', header=0)['tar'])
        self.tupleEquip = tuple(pd.read_excel(self.xlsxSource, sheet_name='equipment', engine='openpyxl', header=0)['eqp'])
        self.dfCourse = pd.read_excel(self.xlsxSource, sheet_name='course', engine='openpyxl', header=0)


def _PlayCourse(engine, course: list, dfCourse: pd.DataFrame):
    """
    利用传入的DataFrame，生成语音指导训练
    :param dfCourse: 符合特定格式的DataFrame
    :return:
    """
    motionPath = str.join('/', os.path.abspath(__file__).split('\\')[0:-1]) + '/motion/'

    bg = time.time()
    tar = course[3][1] + '身' if 'Y' in course[3] else '，'.join([i[1] + '部' for i in course[3].split(',')])
    eqp = '无需器材' if 'U' in course[4] else '使用' + '，'.join([i[1:] for i in course[4].split(',')])
    title = '{}，{}，针对{}，{}'.format(course[2][1:], course[1], tar, eqp)
    sec = course[6]
    print(title)
    _text2Speech(engine, title)

    n = len(dfCourse.index) - len(dfCourse[dfCourse['cat'] == 'P姿势'].index)
    lenTrn = (np.array(dfCourse.per.replace(0, 1)) * np.array(dfCourse.qnt)).sum()
    lenCmt = len(''.join([str(i) for i in dfCourse.cmt])) * 1 * 1.1
    textBgn = '该训练共包含{}个动作，预计耗时{}{}。'.format(n, str(sec//60)+'分' if sec//60 else '', str(sec%60)+'秒' if sec%60 else '')
    print(textBgn)
    _text2Speech(engine, textBgn)
    listRecord = [0] * n
    listPlayed = ['0']
    x = -1

    for i, row in dfCourse.iterrows():
        per = int(row['per'])
        if 'P' in row['cat']:
            text = str(row['name'])
            x += 1
            _text2Speech(engine, text)
            time.sleep(row['leng'])
        else:
            '''
            motionFile = motionPath + row['code'] + '.gif'
            if os.path.exists(motion):
                _motionShow(motionFile, row['code'])
            '''

            cmt = '' if row['code'] in listPlayed or row['cmt'] == '0' else row['cmt']
            listPlayed += [row['code']]
            qnt = int(row['qnt'])
            eqp = '' if 'U' in row['eqp'] else '使用' + ','.join([i[1:] for i in row['eqp'].split(',')])
            if per:
                text = '第{}节，{}，{}\n{}，\n每次{}秒，{}次。'.format(i - x, row['name'], eqp, cmt, per, qnt)
            else:
                text = '第{}节，{}，{}\n{}，\n{}秒。'.format(i - x, row['name'], eqp, cmt, qnt)

            st = _GenSN()
            print('\n', text)
            _text2Speech(engine, text)
            time.sleep(0.25)
            per = per if per else 1
            _Beep(engine, per=int(per), qnt=qnt, bg=bg)
            _text2Speech(engine, '停！')
            ed = _GenSN()

            listRecord[i - x - 1] = [st, row['code'], str(qnt).zfill(2), ed]

    nw = int(time.time() - bg)
    textEnd = '恭喜你！完成训练！'
    _text2Speech(engine, textEnd)

    dfRecord = pd.DataFrame(listRecord, columns=['bg', 'code', 'qnt', 'ed'])
    dfRecord.to_csv(Para().txtMotionHistory, mode='a', sep=' ', index=False, header=False)

    if abs(nw - sec) > 5:
        notice = '注意！请更新档案！{}，耗时共计{}秒。'.format(course[0].split('-')[-1], nw)
        _text2Speech(engine, notice)


def _motionShow(motionFile: str, code: str):
    # todo: 播放对应工作的GIF
    img = Image.open(motionFile)
    plt.figure(figsize=(6, 6))
    plt.ion()
    plt.axis('off')
    plt.show(img)


def _GenSN() -> str:
    today = dt.datetime.today()
    birth = dt.datetime(1983, 11, 18)
    diff = today - birth
    currentTime = dt.datetime.now()
    listTime = [str(diff.days).zfill(5), str(currentTime.hour).zfill(2),
                str(currentTime.minute).zfill(2), str(currentTime.second).zfill(2)]
    sn = int(''.join([i for i in listTime]))
    return sn


def _Beep(engine, per, qnt, bg):
    frq = [int(i) for i in np.linspace(523, 1046, qnt)]
    st = 10 if qnt > 30 else 5

    _text2Speech(engine, '开始')
    for i in range(qnt, 0, -1):
        nw = int(time.time() - bg)
        print(str(qnt-i+1).zfill(3), str(nw).zfill(4))
        if i > st:
            dur = 260
            winsound.Beep(frq[qnt-i], dur)
        else:
            _text2Speech(engine, str(i))
            dur = 1100

        if per > dur * 1e-3:
            time.sleep(per - dur * 1e-3)


def _text2Speech(engine, text):
    engine.say(text)
    engine.runAndWait()


if __name__ == '__main__':
    SelCourse()
