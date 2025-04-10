import os
import json
import time
import signal
import sys
import atexit
import subprocess
import psutil
from pathlib import Path
from pyngrok import ngrok, conf

# 配置文件路径
NGROK_CONFIG_PATH = Path(__file__).parent.parent.parent / "ngrok_config.json"
# 进程ID文件路径
NGROK_PID_PATH = Path(__file__).parent.parent.parent / "ngrok_pid.txt"

# 全局变量，用于存储隧道信息
active_tunnel = None
ngrok_process = None

def cleanup_ngrok():
    """
    清理ngrok进程
    """
    try:
        # 尝试从PID文件中读取进程ID
        if NGROK_PID_PATH.exists():
            with open(NGROK_PID_PATH, "r") as f:
                content = f.read().strip()
                if content:  # 确保内容不为空
                    try:
                        pid = int(content)
                        
                        # 尝试终止进程
                        try:
                            process = psutil.Process(pid)
                            if "ngrok" in process.name().lower() or "python" in process.name().lower():
                                process.terminate()
                                print(f"已终止ngrok进程 (PID: {pid})")
                        except psutil.NoSuchProcess:
                            pass
                    except ValueError:
                        print(f"PID文件内容无效: {content}")
            
            # 删除PID文件
            try:
                NGROK_PID_PATH.unlink()
            except:
                pass
    except Exception as e:
        print(f"清理ngrok进程时出错: {e}")
    
    # 确保所有ngrok进程都被终止
    try:
        ngrok.kill()
    except:
        pass

def ensure_ngrok_installed():
    """
    确保ngrok已安装
    """
    try:
        import pyngrok
        return True
    except ImportError:
        print("pyngrok未安装，正在安装...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])
            print("pyngrok安装成功")
            return True
        except Exception as e:
            print(f"安装pyngrok时出错: {e}")
            return False

def get_or_create_tunnel(port=8080):
    """
    获取或创建ngrok隧道
    
    如果已经存在绑定到指定端口的隧道，则返回该隧道
    否则创建一个新的隧道并保存配置
    """
    global active_tunnel
    
    # 确保ngrok已安装
    if not ensure_ngrok_installed():
        return None
    
    # 首先检查全局变量中是否已有活跃的隧道
    if active_tunnel:
        # 验证隧道是否仍然活跃
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if tunnel.public_url == active_tunnel:
                print(f"使用已有的活跃隧道: {active_tunnel}")
                return active_tunnel
    
    # 检查配置文件是否存在
    if NGROK_CONFIG_PATH.exists():
        try:
            # 读取配置文件
            with open(NGROK_CONFIG_PATH, "r") as f:
                config = json.load(f)
            
            # 检查配置是否有效
            if "public_url" in config and "port" in config and config["port"] == port:
                # 检查隧道是否仍然活跃
                tunnels = ngrok.get_tunnels()
                for tunnel in tunnels:
                    if tunnel.public_url == config["public_url"]:
                        print(f"使用现有的ngrok隧道: {tunnel.public_url}")
                        active_tunnel = tunnel.public_url
                        return active_tunnel
                
                # 如果隧道不再活跃，尝试使用相同的配置重新创建
                try:
                    # 尝试关闭所有隧道并重新启动
                    ngrok.kill()
                    time.sleep(1)  # 等待进程完全终止
                    
                    # 重新创建隧道
                    tunnel = ngrok.connect(port)
                    
                    # 更新配置
                    config = {
                        "public_url": tunnel.public_url,
                        "port": port,
                        "created_at": time.time()
                    }
                    with open(NGROK_CONFIG_PATH, "w") as f:
                        json.dump(config, f)
                    
                    print(f"重新创建ngrok隧道: {tunnel.public_url}")
                    active_tunnel = tunnel.public_url
                    return active_tunnel
                except Exception as e:
                    print(f"重新创建隧道时出错: {e}")
        except Exception as e:
            print(f"读取配置文件时出错: {e}")
    
    # 如果没有有效的配置或无法重用现有隧道，创建新的隧道
    try:
        # 确保没有活跃的隧道
        ngrok.kill()
        time.sleep(1)  # 等待进程完全终止
        
        # 创建新的隧道
        tunnel = ngrok.connect(port)
        
        # 保存配置
        config = {
            "public_url": tunnel.public_url,
            "port": port,
            "created_at": time.time()
        }
        with open(NGROK_CONFIG_PATH, "w") as f:
            json.dump(config, f)
        
        print(f"创建新的ngrok隧道: {tunnel.public_url}")
        active_tunnel = tunnel.public_url
        return active_tunnel
    except Exception as e:
        print(f"创建隧道时出错: {e}")
        return None

def start_ngrok_daemon(port=8080):
    """
    启动ngrok作为守护进程
    
    这个函数会启动一个独立的Python进程来运行ngrok，
    并将进程ID保存到文件中，以便后续清理
    """
    global ngrok_process
    
    # 确保没有其他ngrok进程在运行
    cleanup_ngrok()
    
    # 直接在当前进程中启动ngrok
    try:
        # 禁用监控线程，避免在主进程退出时关闭隧道
        conf.get_default().monitor_thread = False
        
        # 连接到指定端口
        tunnel = ngrok.connect(port)
        
        # 保存配置
        config = {
            "public_url": tunnel.public_url,
            "port": port,
            "created_at": time.time()
        }
        with open(NGROK_CONFIG_PATH, "w") as f:
            json.dump(config, f)
        
        # 保存当前进程ID
        with open(NGROK_PID_PATH, "w") as f:
            f.write(str(os.getpid()))
        
        print(f"Ngrok隧道已打开: {tunnel.public_url}")
        return True
    except Exception as e:
        print(f"启动Ngrok隧道时出错: {e}")
        return False

def get_tunnel_url():
    """
    获取当前活跃的隧道URL
    
    如果没有活跃的隧道，则返回None
    """
    if NGROK_CONFIG_PATH.exists():
        try:
            with open(NGROK_CONFIG_PATH, "r") as f:
                config = json.load(f)
            if "public_url" in config:
                return config["public_url"]
        except:
            pass
    return None

# 注册退出处理函数
atexit.register(cleanup_ngrok)

if __name__ == "__main__":
    # 如果直接运行此脚本，启动ngrok守护进程
    if start_ngrok_daemon():
        print("Ngrok守护进程已启动，按Ctrl+C终止程序")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("正在关闭ngrok...")
            cleanup_ngrok()
