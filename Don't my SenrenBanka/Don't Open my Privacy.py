import psutil
import ctypes
import time
import sys
import threading
import subprocess

# ============================================================
#  ★ 要监控的 .EXE 程序名称（不区分大小写）
TARGET_EXE = "SenrenBanka.exe"   # <-- 修改为你的目标程序名
#
#  ★ 检测到后要打开的程序路径（填完整路径）
OPEN_PROGRAM = r"D:\1110(1)\GameViewer\GameViewer.exe"  # <-- 修改为你要打开的程序
#
#  ★ 弹窗提示文字
POPUP_MESSAGE = "*************\n\n电脑将在 5 秒后锁定屏幕！"
#
#  ★ 弹窗标题
POPUP_TITLE = "*************"
#
#  ★ 锁屏倒计时（秒）
LOCK_DELAY = 5
#
#  ★ 检测间隔（秒）
CHECK_INTERVAL = 3
# ============================================================


def kill_process(exe_name: str):
    """强制关闭所有匹配的 EXE 进程"""
    exe_name_lower = exe_name.lower()
    for proc in psutil.process_iter(["name", "pid"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == exe_name_lower:
                proc.kill()
                print(f"[关闭程序] 已终止: {proc.info['name']} (PID: {proc.info['pid']})")
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"[警告] 无法终止进程: {e}")


def is_process_running(exe_name: str) -> bool:
    """检查指定的 EXE 是否正在运行"""
    exe_name_lower = exe_name.lower()
    for proc in psutil.process_iter(["name"]):
        try:
            if proc.info["name"] and proc.info["name"].lower() == exe_name_lower:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return False


def lock_screen_after_delay(delay: int):
    """等待 delay 秒后锁定屏幕"""
    time.sleep(delay)
    print(f"[锁屏] {delay} 秒已到，正在锁定屏幕...")
    ctypes.windll.user32.LockWorkStation()


def open_program(path: str):
    """打开指定程序"""
    try:
        subprocess.Popen(path)
        print(f"[打开程序] 已启动: {path}")
    except Exception as e:
        print(f"[警告] 无法启动程序: {e}")


def handle_detection(message: str, title: str, delay: int, exe_name: str, open_path: str):
    """
    检测到目标程序后同时执行四件事：
    ① 强制关闭目标程序
    ② 打开指定的另一个程序
    ③ 倒计时 delay 秒后锁定屏幕
    ④ 弹出置顶警告窗口
    """
    # ① 立即强制关闭目标程序
    kill_process(exe_name)

    # ② 打开指定程序
    open_program(open_path)

    # ③ 启动锁屏倒计时线程
    lock_thread = threading.Thread(
        target=lock_screen_after_delay,
        args=(delay,),
        daemon=True
    )
    lock_thread.start()

    # ④ 弹出置顶提示框（阻塞，直到用户点击确定）
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x1030)


def main():
    print(f"[监控启动] 正在监控: {TARGET_EXE}，每 {CHECK_INTERVAL} 秒检测一次")
    print("按 Ctrl+C 退出\n")

    popup_showing = False

    while True:
        try:
            if is_process_running(TARGET_EXE):
                if not popup_showing:
                    print(f"[检测到] {TARGET_EXE} 正在运行，执行全部动作...")
                    popup_showing = True
                    handle_detection(POPUP_MESSAGE, POPUP_TITLE, LOCK_DELAY, TARGET_EXE, OPEN_PROGRAM)
                    popup_showing = False
            else:
                popup_showing = False

            time.sleep(CHECK_INTERVAL)

        except KeyboardInterrupt:
            print("\n[退出] 监控已停止。")
            sys.exit(0)


if __name__ == "__main__":
    main()
