import time
from selenium import webdriver
from selenium.webdriver.common.by import By

class PerformanceTester:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.interaction_times = []
        self.total_start_time = time.perf_counter()
        self.home_load_time = 0  # 首页加载时间

    def quit(self):
        total_duration = time.perf_counter() - self.total_start_time
        avg_interaction = sum(self.interaction_times) / len(self.interaction_times) if self.interaction_times else 0

        print("\n====== 性能指标统计 ======")
        print(f"首页加载时间: {self.home_load_time:.2f} 秒")
        print(f"平均交互响应时间: {avg_interaction:.2f} 秒")
        print(f"总执行时间: {total_duration:.2f} 秒")

        self.driver.quit()

    def measure(self, action, label, time_list=None, is_home=False):
        start = time.perf_counter()
        action()
        end = time.perf_counter()
        duration = end - start
        if is_home:
            self.home_load_time = duration
        elif time_list is not None:
            time_list.append(duration)
        print(f"{label}耗时: {duration:.2f} 秒")

    def run_test(self):
        # 1. 首页加载
        self.measure(lambda: self.driver.get("http://127.0.0.1:60462/"), "首页加载", is_home=True)
        self.driver.set_window_size(2576, 1408)

        # 2. 点击第2个商品卡片
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay").click(), "点击第2个商品卡片", self.interaction_times)

        # 3. 点击数量下拉框
        self.measure(lambda: self.driver.find_element(By.ID, "quantity").click(), "点击数量下拉框", self.interaction_times)

        # 4. 选择数量3
        def select_quantity_3():
            dropdown = self.driver.find_element(By.ID, "quantity")
            dropdown.find_element(By.XPATH, "//option[. = '3']").click()
        self.measure(select_quantity_3, "选择数量3", self.interaction_times)

        # 5. 点击加入购物车
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click(), "点击加入购物车", self.interaction_times)

        # 6. 点击“继续购物”
        self.measure(lambda: self.driver.find_element(By.LINK_TEXT, "Continue Shopping").click(), "点击继续购物", self.interaction_times)

        # 7. 点击第4个商品卡片
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(4) .hot-product-card-img-overlay").click(), "点击第4个商品卡片", self.interaction_times)

        # 8. 再次点击加入购物车
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click(), "再次点击加入购物车", self.interaction_times)

        # 9. 点击查看购物车按钮
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)").click(), "点击查看购物车", self.interaction_times)

        # 10. 最后点击“继续购物”
        self.measure(lambda: self.driver.find_element(By.LINK_TEXT, "Continue Shopping").click(), "再次点击继续购物", self.interaction_times)


# ========= 启动脚本 ============
if __name__ == "__main__":
    tester = PerformanceTester()
    try:
        tester.run_test()
    finally:
        tester.quit()
