"""
ngrok client module

This module is used to communicate with the ngrok daemon, get tunnel status and URL.
It provides functions to start, stop, and check the status of ngrok tunnels.
"""

import sys
import json
import time
import subprocess
from pathlib import Path
import ctypes
from pyngrok import ngrok
import psutil

# 项目根目录 (Project root directory)
ROOT_DIR = Path(__file__).parent.parent.parent

# ngrok目录 (ngrok directory)
NGROK_DIR = ROOT_DIR / "ngrok"

# 配置文件路径 (Configuration file path)
NGROK_CONFIG_PATH = NGROK_DIR / "ngrok_config.json"
# 进程ID文件路径 (Process ID file path)
NGROK_PID_PATH = NGROK_DIR / "ngrok_pid.txt"
# 隧道状态文件路径 (Tunnel status file path)
NGROK_STATUS_PATH = NGROK_DIR / "ngrok_status.txt"

def is_daemon_running():
    """
    Check if the ngrok daemon is running
    
    Determines this by checking if the PID file exists and if the process is active
    
    检查ngrok守护进程是否正在运行
    
    通过检查PID文件和进程是否存在来判断
    """
    if not NGROK_PID_PATH.exists():
        return False

    try:
        with open(NGROK_PID_PATH, "r", encoding="utf-8") as f:
            pid_str = f.read().strip()
            if not pid_str:
                return False
            pid = int(pid_str)
            # 检查进程是否存在
            if sys.platform == "win32":
                # Windows平台
                kernel32 = ctypes.windll.kernel32
                synchronize = 0x00100000
                process = kernel32.OpenProcess(synchronize, False, pid)
                if process:
                    kernel32.CloseHandle(process)
                    return True
                return False
    except OSError:
        return False

def get_tunnel_status():
    """
    Get the tunnel status
    
    Returns a dictionary containing status information, or None if the status file
    doesn't exist or is invalid
    """
    if not NGROK_STATUS_PATH.exists():
        return None
    try:
        with open(NGROK_STATUS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except IOError:
        return None

def get_tunnel_url():
    """
    Get the tunnel URL
    
    Returns the URL if the tunnel is running, otherwise returns None
    """
    status = get_tunnel_status()
    if status and status.get("status") == "running" and status.get("url"):
        return status.get("url")
    # 如果状态文件不存在或无效，尝试从配置文件中获取URL
    if NGROK_CONFIG_PATH.exists():
        try:
            with open(NGROK_CONFIG_PATH, "r", encoding="utf-8") as f:
                config = json.load(f)
            if "public_url" in config:
                return config["public_url"]
        except IOError:
            pass
    return None

def start_daemon(port=8080):
    """
    Start the ngrok daemon
    
    If the daemon is already running, it won't be restarted
    
    启动ngrok守护进程
    
    如果守护进程已经在运行，则不会重新启动
    """
    if is_daemon_running():
        return True
    # 启动守护进程 (Start the daemon process)
    try:
        daemon_script = NGROK_DIR / "ngrok_daemon.py"
        # 使用subprocess启动守护进程
        subprocess.Popen(
            [sys.executable, str(daemon_script), str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
        )
        # 等待一段时间，确保守护进程已经启动
        time.sleep(3)
        # 检查守护进程是否成功启动
        if is_daemon_running():
            return True
        else:
            return False
    except OSError as e:
        print(f"starting ngrok daemon failed: {e}")
        return False

def stop_daemon():
    """
    Stop the ngrok daemon
    
    Stops the daemon by sending a termination signal to the process, and directly
    uses ngrok.kill() to ensure all ngrok processes are terminated
    """
    success = False
    # try to terminate the process via PID file
    if NGROK_PID_PATH.exists():
        try:
            with open(NGROK_PID_PATH, "r", encoding="utf-8") as f:
                pid_str = f.read().strip()
                if pid_str:
                    try:
                        pid = int(pid_str)
                        #  send termination signal
                        if sys.platform == "win32":
                            kernel32 = ctypes.windll.kernel32
                            process_terminate = 0x0001
                            handle = kernel32.OpenProcess(process_terminate, False, pid)
                            if handle:
                                kernel32.TerminateProcess(handle, 0)
                                kernel32.CloseHandle(handle)
                                success = True
                    except ValueError:
                        pass
            # 删除PID文件
            try:
                NGROK_PID_PATH.unlink()
            except OSError:
                pass
        except OSError:
            pass
    # use ngrok.kill() to ensure all ngrok processes are terminated
    try:
        ngrok.kill()
        success = True
    except OSError:
        pass
    # 删除状态文件
    if NGROK_STATUS_PATH.exists():
        try:
            NGROK_STATUS_PATH.unlink()
        except OSError:
            pass
    # 查找并终止所有ngrok相关进程
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if 'ngrok' in proc.info['name'].lower():
                    proc.terminate()
                    success = True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except OSError:
        pass
    return success
