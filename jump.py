import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mptimg
import time
import random


readyflag = False
autoflag = False
xishu = 1.454
pngname = 'jump1.png'


def on_button_press(event):
    global xstart, ystart
    xstart, ystart = event.xdata, event.ydata


def on_button_release(event):
    global readyflag, distance, autoflag
    # print(readyflag)
    xend, yend = event.xdata, event.ydata
    lines = ax.plot([xstart, xend], [ystart, yend])
    ax.figure.canvas.draw()
    preline = lines.pop(0)
    preline.remove()
    del preline
    distance = np.sqrt((xstart - xend) ** 2 + (ystart - yend) ** 2)
    readyflag = True
    # print(readyflag)
    if autoflag:
        jump(distance)
        getscreen()


def jump(dist):
    tm = dist*xishu
    x = random.uniform(580, 660)
    y = random.uniform(1580, 1660)
    swipecmd = 'adb shell input swipe %d %d %d %d %d' % (x, y, x, y, tm)
    os.system(swipecmd)
    print(swipecmd)
    time.sleep(tm/1000 + 0.5)


def getscreen():
    screencmd = 'adb shell screencap -p /sdcard/%s' % pngname
    pullcmd = 'adb pull /sdcard/%s .' % pngname
    os.system(screencmd)
    os.system(pullcmd)
    screen = mptimg.imread(pngname)
    ax.imshow(screen)
    fig.canvas.draw()


def on_key_press(event):
    global readyflag, distance, autoflag
    if event.key == 'a' and readyflag:
        jump(distance)
        readyflag = False
    if event.key == 's':
        getscreen()
    if event.key == 'd':
        autoflag = not autoflag


if __name__ == '__main__':
    fig, ax = plt.subplots()
    plt.axis('off')
    getscreen()
    fig.canvas.mpl_connect('button_press_event', on_button_press)
    fig.canvas.mpl_connect('button_release_event', on_button_release)
    fig.canvas.mpl_connect('key_press_event', on_key_press)
    fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)
    plt.show()
