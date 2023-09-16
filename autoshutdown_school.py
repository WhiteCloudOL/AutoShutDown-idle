"""
AppName:Auto-Shutdown
Description:Automatically shut down when the computer is idle.
Created By WhiteCloudCN
"""

import os, ctypes, time, tkinter, sys
import tkinter.messagebox

sidletime = 1000 * 60 * 70  # 单位：ms
waittime = 60 * 5  # 单位：s


def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_uint),
            ('dwTime', ctypes.c_uint),
        ]

    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(lastInputInfo)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo))

    millis = ctypes.windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis


# 开始关机操作
def shutdown_s():
    os.system("Shutdown -s -t %s" % waittime)
    return


# 取消关机操作
def shutdown_c():
    print("取消关机")
    os.system("shutdown -a")
    return


def end_program(pro_name):
    os.system('%s%s' % ("taskkill /F /IM ", pro_name))
    return


# 询问是否关机
def askcc():
    # 确认关机操作
    if not tkinter.messagebox.askyesno('提示：现已进入空闲状态，当前时间' + tget,
                                       '系统将于 5分钟后 关机\n是否执行关机操作\n（关机：是，取消关机：否）'):
        shutdown_c()
    else:
        # 二次确认关机操作，防止误触
        if not tkinter.messagebox.askyesno('提示：系统即将关机', '你确定要关机吗\n（关机：是，取消关机：否）'):
            shutdown_c()
        else:
            sys.exit()


def sstc():
    if not tkinter.messagebox.askyesno('提示：现在已经是' + tget,
                                       '系统将于 5分钟后 关机\n是否执行关机操作\n（关机：是，取消关机：否）'):
        shutdown_c()
        time.sleep(90)
    else:
        # 二次确认关机操作，防止误触
        if not tkinter.messagebox.askyesno('提示：系统即将关机', '你确定要关机吗\n（关机：是，取消关机：否）'):
            shutdown_c()
            time.sleep(90)
        else:
            sys.exit()


# 程序主体
def app():
    sttime = ['12时26分', '17时26分', '21时28分']
    while True:
        global t, tget, th, tm, ts
        idle_time = get_idle_time()
        print(f"系统空闲时间: {idle_time}ms")
        t = time.localtime()
        th, tm, ts = t.tm_hour, int(t.tm_min) + waittime, t.tm_sec
        tget = str(t.tm_hour) + '时' + str(t.tm_min) + '分'
        if idle_time >= sidletime:
            shutdown_s()
            askcc()
        if tget in sttime:
            shutdown_s()
            sstc()
        time.sleep(5)


# 运行程序段
if __name__ == '__main__':
    app()
