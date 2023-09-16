"""
AppName:Auto-Shutdown
Description:Automatically shut down when the computer is idle.
Created By WhiteCloudCN
"""

import os, ctypes, time, tkinter
import tkinter.messagebox

sidletime = 1000 * 60 * 90  # 单位：ms
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
    os.system('%s%s' % ("taskkill /F /IM ",pro_name))
    return

#程序主体
def app():
    while True:
        idle_time = get_idle_time()
        print(f"系统空闲时间: {idle_time}ms")
        if idle_time >= sidletime:
            shutdown_s()
            t = time.localtime()
            if not tkinter.messagebox.askyesno('提示：系统即将关机','系统将于 %s时%s分%s秒 关机\n是否执行关机操作\n（关机：是，取消关机：否）' % (t.tm_hour, t.tm_min + waittime, t.tm_sec)):
                shutdown_c()
            else:
                if not tkinter.messagebox.askyesno('提示：系统即将关机', '你确定要关机吗\n（关机：是，取消关机：否）'):
                    shutdown_c()
                else:
                    time.sleep(5 * 60 * 1000)

        time.sleep(1)


#运行程序段
if __name__ == '__main__':
    app()