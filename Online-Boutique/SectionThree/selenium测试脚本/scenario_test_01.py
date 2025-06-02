import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class PerformanceTester:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.interaction_times = []
        self.home_load_time = 0
        self.total_start_time = time.perf_counter()

    def quit(self):
        total_duration = time.perf_counter() - self.total_start_time
        avg_interaction = sum(self.interaction_times) / len(self.interaction_times) if self.interaction_times else 0
        avg_interaction_true = 0.0
        avg_interaction_true = self.interaction_times[1] + self.interaction_times[2] + self.interaction_times[3] + self.interaction_times[4] + self.interaction_times[5] + self.interaction_times[6] + self.interaction_times[7] + self.interaction_times[8] + self.interaction_times[9]
        avg_interaction_true = avg_interaction_true / 9.0

        print("\n====== 性能指标统计 ======")
        print(f"首页加载时间: {self.home_load_time:.2f} 秒")
        print(f"平均交互响应时间: {avg_interaction:.2f} 秒")
        print(f"总执行时间: {total_duration:.2f} 秒")
        print(avg_interaction_true)

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
        # Step 1: 首页加载
        self.measure(lambda: self.driver.get("http://127.0.0.1:60462/"), "首页加载", is_home=True)

        # Step 2: 设置窗口大小（不计时）
        self.driver.set_window_size(2576, 1408)

        # Step 3: 点击第2个商品卡片
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay").click(), "点击第2个商品卡片", self.interaction_times)

        # Step 4: 点击数量下拉框
        self.measure(lambda: self.driver.find_element(By.ID, "quantity").click(), "点击数量下拉框", self.interaction_times)

        # Step 5: 选择数量3
        def select_quantity_3():
            dropdown = self.driver.find_element(By.ID, "quantity")
            dropdown.find_element(By.XPATH, "//option[. = '3']").click()
        self.measure(select_quantity_3, "选择数量3", self.interaction_times)

        # Step 6: 点击加入购物车
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click(), "点击加入购物车", self.interaction_times)

        # Step 7: 鼠标拖拽操作 email 输入框
        def mouse_drag_on_email():
            element = self.driver.find_element(By.ID, "email")
            actions = ActionChains(self.driver)
            actions.move_to_element(element).click_and_hold().perform()
            actions.move_to_element(element).perform()
            actions.release().perform()
        self.measure(mouse_drag_on_email, "鼠标操作 email 输入框", self.interaction_times)

        # Step 8: 点击 email 输入框
        self.measure(lambda: self.driver.find_element(By.ID, "email").click(), "点击 email 输入框", self.interaction_times)

        # Step 9: 输入邮箱
        self.measure(lambda: self.driver.find_element(By.ID, "email").send_keys("3214621635@qq.com"), "输入邮箱", self.interaction_times)

        # Step 10: 点击月份下拉框
        self.measure(lambda: self.driver.find_element(By.ID, "credit_card_expiration_month").click(), "点击月份下拉框", self.interaction_times)

        # Step 11: 选择 March
        def select_march():
            dropdown = self.driver.find_element(By.ID, "credit_card_expiration_month")
            dropdown.find_element(By.XPATH, "//option[. = 'March']").click()
        self.measure(select_march, "选择 March 月份", self.interaction_times)

        # Step 12: 点击提交按钮
        self.measure(lambda: self.driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)").click(), "点击提交按钮", self.interaction_times)

        # Step 13: 点击继续购物
        self.measure(lambda: self.driver.find_element(By.LINK_TEXT, "Continue Shopping").click(), "点击继续购物", self.interaction_times)


# ========= 启动脚本 ============
if __name__ == "__main__":
    tester = PerformanceTester()
    try:
        tester.run_test()
    finally:
        tester.quit()
