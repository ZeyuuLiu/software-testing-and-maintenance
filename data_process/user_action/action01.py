from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

def run(driver):
    """
    脚本01的操作流程：依次执行：
    1. 点击第2个商品卡片
    2. 点击数量下拉框并选择数量3
    3. 点击“加入购物车”
    4. 鼠标拖拽 email 输入框并点击、输入邮箱
    5. 点击月份下拉框并选择 March
    6. 点击“提交”按钮
    7. 点击“Continue Shopping”按钮
    """
    # 点击第2个商品卡片
    driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay").click()

    # 点击数量下拉框并选择数量3
    driver.find_element(By.ID, "quantity").click()
    dropdown_qty = driver.find_element(By.ID, "quantity")
    dropdown_qty.find_element(By.XPATH, "//option[. = '3']").click()

    # 点击加入购物车
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click()

    # 鼠标拖拽到 email 输入框并点击
    email_input = driver.find_element(By.ID, "email")
    actions = ActionChains(driver)
    actions.move_to_element(email_input).click_and_hold().perform()
    actions.move_to_element(email_input).release().perform()
    email_input.click()

    # 在 email 输入框中输入邮箱
    email_input.send_keys("3214621635@qq.com")

    # 点击月份下拉框并选择 March
    driver.find_element(By.ID, "credit_card_expiration_month").click()
    dropdown_month = driver.find_element(By.ID, "credit_card_expiration_month")
    dropdown_month.find_element(By.XPATH, "//option[. = 'March']").click()

    # 点击提交按钮
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)").click()

    # 点击 Continue Shopping
    driver.find_element(By.LINK_TEXT, "Continue Shopping").click()
