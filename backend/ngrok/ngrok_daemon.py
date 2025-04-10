#!/usr/bin/env python
"""
独立的ngrok隧道守护进程

这个脚本用于启动一个持久化的ngrok隧道，并将其保持活跃状态
即使FastAPI应用重新加载，隧道也不会关闭
"""

import os
import sys
import time
import json
import signal
import atexit
from pathlib import Path
from pyngrok import ngrok, conf

# 配置文件路径
NGROK_CONFIG_PATH = Path(__file__).parent / "ngrok_config.json"
# 进程ID文件路径
NGROK_PID_PATH = Path(__file__).parent / "ngrok_pid.txt"
# 隧道状态文件路径
NGROK_STATUS_PATH = Path(__file__).parent / "ngrok_status.txt"

# 全局变量，用于存储隧道信息
active_tunnel = None

def signal_handler(sig, frame):
    """
    处理信号，优雅地关闭程序
    """
    cleanup()
    sys.exit(0)

def cleanup():
    """
    清理ngrok进程
    """
    try:
        # 删除状态文件
        if NGROK_STATUS_PATH.exists():
            NGROK_STATUS_PATH.unlink()
        
        # 删除PID文件
        if NGROK_PID_PATH.exists():
            NGROK_PID_PATH.unlink()
        
        # 关闭所有ngrok隧道
        ngrok.kill()
    except Exception as e:
        print(f"清理ngrok进程时出错: {e}")

def get_or_create_tunnel(port=8080):
    """
    获取或创建ngrok隧道
    
    如果已经存在绑定到指定端口的隧道，则返回该隧道
    否则创建一个新的隧道并保存配置
    """
    global active_tunnel
    
    # 首先检查全局变量中是否已有活跃的隧道
    if active_tunnel:
        # 验证隧道是否仍然活跃
        tunnels = ngrok.get_tunnels()
        for tunnel in tunnels:
            if tunnel.public_url == active_tunnel:
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
                    
                    active_tunnel = tunnel.public_url
                    return active_tunnel
                except Exception:
                    pass
        except Exception:
            pass
    
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
        
        active_tunnel = tunnel.public_url
        return active_tunnel
    except Exception:
        return None

def update_status(status="running", url=None):
    """
    更新隧道状态文件
    """
    try:
        status_data = {
            "status": status,
            "url": url,
            "timestamp": time.time()
        }
        with open(NGROK_STATUS_PATH, "w") as f:
            json.dump(status_data, f)
    except Exception as e:
        print(f"更新状态文件时出错: {e}")

def run_daemon(port=8080):
    """
    运行ngrok守护进程
    """
    # 注册信号处理器
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # 注册退出处理函数
    atexit.register(cleanup)
    
    # 保存进程ID
    with open(NGROK_PID_PATH, "w") as f:
        f.write(str(os.getpid()))
    
    # 设置ngrok配置
    conf.get_default().monitor_thread = False  # 禁用监控线程，避免在主进程退出时关闭隧道
    
    # 获取或创建隧道
    public_url = get_or_create_tunnel(port)
    
    if public_url:
        print(f"Ngrok隧道已打开: {public_url}")
        
        # 更新状态文件
        update_status("running", public_url)
        
        # 保持进程运行
        try:
            while True:
                time.sleep(10)  # 每10秒检查一次
                
                # 检查隧道是否仍然活跃
                tunnels = ngrok.get_tunnels()
                if not any(t.public_url == public_url for t in tunnels):
                    public_url = get_or_create_tunnel(port)
                    if public_url:
                        update_status("running", public_url)
                    else:
                        update_status("error")
                else:
                    # 更新状态文件的时间戳
                    update_status("running", public_url)
        except KeyboardInterrupt:
            pass
        finally:
            update_status("stopped")
            cleanup()
    else:
        update_status("error")

if __name__ == "__main__":
    # 默认端口
    port = 8080
    
    # 如果提供了端口参数，使用提供的端口
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print(f"无效的端口号: {sys.argv[1]}")
            sys.exit(1)
    
    # 运行守护进程
    run_daemon(port)
