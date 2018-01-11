# -*- coding: utf-8 -*- #
import pyHook
import pythoncom
import csv
import time

def toCSV(event,pos_X,pos_Y,time):

    with open('DB.csv', 'ab') as csvfile:  # wb means writing in binary mode
        fieldnames = ['EVENT', 'POS_X', 'POS_Y', 'TIME']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, )
        # writer.writeheader()
        writer.writerow({'EVENT': event, 'POS_X': pos_X, 'POS_Y': pos_Y, 'TIME': time})


def left_down(event):
    print "left click"
    print "Position:", event.Position
    print "Time:", event.Time

    # timearray = time.strptime(str(event.Time), "%Y-%m-%d %H:%M:%S")

    toCSV("left click",event.Position[0],event.Position[1],event.Time)
    return True  # if return false, the event will not be passed on to other programs.
    # The cursor will appear freeze


def right_down(event):
    print "right click"
    print "Position:", event.Position
    print "Time:", event.Time

    # timearray = time.strptime(str(event.Time), "%Y-%m-%d %H:%M:%S")
    toCSV("left click", event.Position[0], event.Position[1], event.Time)
    return True


def middle_down(event):
    print "middle click"
    return True


def OnKeyboardEvent(event):
    print chr(event.Ascii)
    return True


def onMouseEvent(event):
    # 监听鼠标事件
    print "MessageName:",event.MessageName
    print "Message:", event.Message
    # print "Time:", event.Time
    # print "Window:", event.Window
    # print "WindowName:", event.WindowName
    print "Position:", event.Position
    print "Wheel:", event.Wheel
    print "Injected:", event.Injected
    print "---"

    # 返回 True 以便将事件传给其它处理程序
    # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截
    # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了
    return True

hm = pyHook.HookManager()

# hook mouse
hm.SubscribeMouseLeftDown(left_down)
hm.SubscribeMouseRightDown(right_down)
hm.SubscribeMouseMiddleDown(middle_down)
# hm.MouseAll = onMouseEvent
hm.HookMouse()

# hook keyboard
# hm.KeyDown = OnKeyboardEvent  # watch for all keyboard events
# hm.HookKeyboard()

pythoncom.PumpMessages()

hm.UnhookMouse()
hm.UnHookKeyboard()