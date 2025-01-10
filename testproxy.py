import tkinter as tk
from tkinter import messagebox
import requests
import time

def get_ip_info(proxies):
    """通过代理获取外网 IP 和归属地"""
    try:
        response = requests.get("https://ipinfo.io/json", proxies=proxies, timeout=5)
        if response.status_code == 200:
            data = response.json()
            ip = data.get("ip", "未知")
            location = data.get("city", "未知") + ", " + data.get("region", "未知") + ", " + data.get("country", "未知")
            return ip, location
        else:
            return "未知", "无法获取归属地"
    except Exception as e:
        return "未知", f"错误：{str(e)}"

def test_proxy():
    proxy_type = proxy_type_var.get()
    proxy_host = host_entry.get()
    proxy_port = port_entry.get()
    test_url = url_entry.get()

    if not proxy_host or not proxy_port:
        messagebox.showerror("输入错误", "请填写代理地址和端口！")
        return

    if not test_url:
        messagebox.showerror("输入错误", "请填写测试地址！")
        return

    proxies = {
        "http": f"{proxy_type}://{proxy_host}:{proxy_port}",
        "https": f"{proxy_type}://{proxy_host}:{proxy_port}",
    }

    try:
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies, timeout=5)
        response_time = time.time() - start_time

        if response.status_code == 200:
            ip, location = get_ip_info(proxies)
            messagebox.showinfo(
                "测试结果",
                f"代理可用！\n响应时间：{response_time:.2f} 秒\n代理的 IP：{ip}\n归属地：{location}"
            )
        else:
            messagebox.showerror("测试结果", f"代理不可用，状态码：{response.status_code}")
    except Exception as e:
        messagebox.showerror("测试结果", f"代理不可用，错误：{str(e)}")

# 创建主窗口
root = tk.Tk()
root.title("代理可用性测试工具")
root.geometry("400x350")

# 代理类型选择
proxy_type_var = tk.StringVar(value="http")
tk.Label(root, text="选择代理类型：").pack(pady=5)
tk.Radiobutton(root, text="HTTP", variable=proxy_type_var, value="http").pack(anchor="w")
tk.Radiobutton(root, text="SOCKS5", variable=proxy_type_var, value="socks5").pack(anchor="w")

# 测试地址输入
tk.Label(root, text="测试地址：").pack(pady=5)
url_entry = tk.Entry(root, width=30)
url_entry.insert(0, "https://www.google.com")  # 默认测试地址
url_entry.pack(pady=5)

# 代理地址输入
tk.Label(root, text="代理地址：").pack(pady=5)
host_entry = tk.Entry(root, width=30)
host_entry.pack(pady=5)

# 代理端口输入
tk.Label(root, text="代理端口：").pack(pady=5)
port_entry = tk.Entry(root, width=10)
port_entry.pack(pady=5)

# 测试按钮
test_button = tk.Button(root, text="测试代理", command=test_proxy)
test_button.pack(pady=20)

# 运行主循环
root.mainloop()


'''
本工具用于帮助用户来判断自己的代理是否可用 并可以显示代理IP和归属地
使用方法:python3运行，需要支持GUI界面
'''
