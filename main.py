import turtle as te
from bs4 import BeautifulSoup
import sys

WriteStep = 15  # 贝塞尔函数的取样次数
Speed = 1000
Width = 600  # 界面宽度
Height = 600  # 界面高度
Xh = 0  # 记录前一个贝塞尔函数的手柄
Yh = 0


def Bezier(p1, p2, t):  # 一阶贝塞尔函数
    return p1 * (1 - t) + p2 * t


def Bezier_2(x1, y1, x2, y2, x3, y3):  # 二阶贝塞尔函数
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep + 1):
        x = Bezier(Bezier(x1, x2, t / WriteStep),
                   Bezier(x2, x3, t / WriteStep), t / WriteStep)
        y = Bezier(Bezier(y1, y2, t / WriteStep),
                   Bezier(y2, y3, t / WriteStep), t / WriteStep)
        te.goto(x, y)
    te.penup()


def Bezier_3(x1, y1, x2, y2, x3, y3, x4, y4):  # 三阶贝塞尔函数
    x1 = -Width / 2 + x1
    y1 = Height / 2 - y1
    x2 = -Width / 2 + x2
    y2 = Height / 2 - y2
    x3 = -Width / 2 + x3
    y3 = Height / 2 - y3
    x4 = -Width / 2 + x4
    y4 = Height / 2 - y4  # 坐标变换
    te.goto(x1, y1)
    te.pendown()
    for t in range(0, WriteStep + 1):
        x = Bezier(Bezier(Bezier(x1, x2, t / WriteStep), Bezier(x2, x3, t / WriteStep), t / WriteStep),
                   Bezier(Bezier(x2, x3, t / WriteStep), Bezier(x3, x4, t / WriteStep), t / WriteStep), t / WriteStep)
        y = Bezier(Bezier(Bezier(y1, y2, t / WriteStep), Bezier(y2, y3, t / WriteStep), t / WriteStep),
                   Bezier(Bezier(y2, y3, t / WriteStep), Bezier(y3, y4, t / WriteStep), t / WriteStep), t / WriteStep)
        te.goto(x, y)
    te.penup()


def Moveto(x, y):  # 移动到svg坐标下（x，y）
    te.penup()
    te.goto(-Width / 2 + x, Height / 2 - y)
    te.pendown()


def line(x1, y1, x2, y2):  # 连接svg坐标下两点
    te.penup()
    te.goto(-Width / 2 + x1, Height / 2 - y1)
    te.pendown()
    te.goto(-Width / 2 + x2, Height / 2 - y2)
    te.penup()


def lineto(dx, dy):  # 连接当前点和相对坐标（dx，dy）的点
    te.pendown()
    te.goto(te.xcor() + dx, te.ycor() - dy)
    te.penup()


def Lineto(x, y):  # 连接当前点和svg坐标下（x，y）
    te.pendown()
    te.goto(-Width / 2 + x, Height / 2 - y)
    te.penup()


def Horizontal(x):  # 做到svg坐标下横坐标为x的水平线
    te.pendown()
    te.setx(x - Width / 2)
    te.penup()


def horizontal(dx):  # 做到相对横坐标为dx的水平线
    te.seth(0)
    te.pendown()
    te.fd(dx)
    te.penup()


def vertical(dy):  # 做到相对纵坐标为dy的垂直线
    te.seth(-90)
    te.pendown()
    te.fd(dy)
    te.penup()
    te.seth(0)


def polyline(x1, y1, x2, y2, x3, y3):  # 做svg坐标下的折线
    te.penup()
    te.goto(-Width / 2 + x1, Height / 2 - y1)
    te.pendown()
    te.goto(-Width / 2 + x2, Height / 2 - y2)
    te.goto(-Width / 2 + x3, Height / 2 - y3)
    te.penup()


def Curveto(x1, y1, x2, y2, x, y):  # 三阶贝塞尔曲线到（x，y）
    te.penup()
    X_now = te.xcor() + Width / 2
    Y_now = Height / 2 - te.ycor()
    Bezier_3(X_now, Y_now, x1, y1, x2, y2, x, y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2


def curveto_r(x1, y1, x2, y2, x, y):  # 三阶贝塞尔曲线到相对坐标（x，y）
    te.penup()
    X_now = te.xcor() + Width / 2
    Y_now = Height / 2 - te.ycor()
    Bezier_3(X_now, Y_now, X_now + x1, Y_now + y1,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    global Xh
    global Yh
    Xh = x - x2
    Yh = y - y2


def Smooth(x2, y2, x, y):  # 平滑三阶贝塞尔曲线到（x，y）
    global Xh
    global Yh
    te.penup()
    X_now = te.xcor() + Width / 2
    Y_now = Height / 2 - te.ycor()
    Bezier_3(X_now, Y_now, X_now + Xh, Y_now + Yh, x2, y2, x, y)
    Xh = x - x2
    Yh = y - y2


def smooth_r(x2, y2, x, y):  # 平滑三阶贝塞尔曲线到相对坐标（x，y）
    global Xh
    global Yh
    te.penup()
    X_now = te.xcor() + Width / 2
    Y_now = Height / 2 - te.ycor()
    Bezier_3(X_now, Y_now, X_now + Xh, Y_now + Yh,
             X_now + x2, Y_now + y2, X_now + x, Y_now + y)
    Xh = x - x2
    Yh = y - y2


def readSVGFile(cmd):
    ulist = cmd.split(' ')
    for i in ulist:
        # print("now cmd:", i)
        if i.isdigit() is True:
            yield float(i)
        elif i.find(',') != -1:
            yield float(i[0: i.find(',')])
            yield float(i[i.find(',') + 1:])
        else:
            yield i


SVGFile = open('1.svg', mode='r')
SVG = BeautifulSoup(SVGFile.read(), 'lxml')
cmd = SVG.path.attrs['d']
te.setup(height = 1010, starty = 0, startx = 1080 - te.width() - 150)
te.tracer(100)
te.pensize(1)
te.speed(Speed)
te.penup()

input()

for i in SVG.find_all('path'):
    te.title(i.attrs['id'])
    te.color(i.attrs['fill'])

    cmd = i.attrs['d']

    f = readSVGFile(cmd)
    for i in f:
        # print(i)
        if i is 'M':
            x = float(f.__next__())
            y = float(f.__next__())
            te.end_fill()
            Moveto(x, y)
            te.begin_fill()
        elif i is 'L':
            x1 = float(f.__next__())
            y1 = float(f.__next__())
            x2 = float(f.__next__())
            y2 = float(f.__next__())
            line(x1, y1, x2, y2)
        elif i is 'C':
            x1 = float(f.__next__())
            y1 = float(f.__next__())
            x2 = float(f.__next__())
            y2 = float(f.__next__())
            x = float(f.__next__())
            y = float(f.__next__())
            # te.begin_fill()
            Curveto(x1, y1, x2, y2, x, y)
            # te.end_fill()

te.penup()
te.hideturtle()
te.update()
te.done()
