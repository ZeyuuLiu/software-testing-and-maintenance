import time
import random
import importlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

class UserSimulator:
    def __init__(self, module_names, wait_range=(5, 15)):
        """
        :param module_names: 要导入的脚本模块名列表（不含 .py 后缀），
                             每个脚本须定义一个 run(driver) 函数
        :param wait_range: 两次操作之间的随机等待区间（秒），形式如 (min_seconds, max_seconds)
        """
        # 使用 Chrome 打开浏览器，仅打开一次
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(10)

        # 随机等待的范围
        self.wait_range = wait_range
        # 将外部脚本中的 run 函数收集到 actions 列表
        self.actions = []
        for name in module_names:
            try:
                module = importlib.import_module(name)
                if hasattr(module, "run"):
                    self.actions.append(module.run)
                else:
                    print(f"警告：模块 '{name}' 中没有找到 run(driver) 函数，已跳过该模块。")
            except ImportError as e:
                print(f"警告：无法导入模块 '{name}'：{e}")

    def simulate(self, start_url, window_size=(1200, 800)):
        """
        启动后只打开一次页面，不断随机执行各个脚本中的 run(driver) 操作。
        :param start_url:  需要打开的初始网址
        :param window_size: 浏览器窗口大小，形式 (width, height)
        """
        # 首次加载页面并设置窗口
        self.driver.get(start_url)
        self.driver.set_window_size(*window_size)

        print("\n开始模拟用户操作（按 Ctrl+C 停止）...\n")
        try:
            while True:
                # 随机挑选一个脚本的 run 函数执行
                action = random.choice(self.actions)
                try:
                    print(f"执行脚本：{action.__module__}")
                    action(self.driver)
                except Exception as e:
                    print(f"脚本 '{action.__module__}' 执行失败：{e}")
                
                # 每次执行完后回到首页
                print(f"返回首页：{start_url}")
                self.driver.get(start_url)

                # 随机等待一段时间再进入下一个循环
                wait_time = random.uniform(self.wait_range[0], self.wait_range[1])
                print(f"等待 {wait_time:.2f} 秒...\n")
                time.sleep(wait_time)
        except KeyboardInterrupt:
            print("\n检测到 Ctrl+C，中断模拟。")
        finally:
            print("正在关闭浏览器...")
            self.driver.quit()



if __name__ == "__main__":
    modules = [
        "action01",
        "action02",
        "action03",
        "action04",
    ]

    simulator = UserSimulator(module_names=modules, wait_range=(5, 10))
    # 入口 URL 设为你要打开的页面
    simulator.simulate(start_url="http://127.0.0.1:11695/", window_size=(2576, 1408))
