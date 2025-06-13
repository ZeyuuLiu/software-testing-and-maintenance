from selenium.webdriver.common.by import By

def run(driver):
    """
    脚本04的操作流程：
    2. 点击货币下拉框并选择 JPY
    3. 点击第5个商品卡片
    4. 点击数量下拉框并选择数量5
    5. 点击“加入购物车”
    6. 点击“查看购物车”按钮
    7. 点击“Continue Shopping”链接
    """
    # 2. 点击货币下拉框并选择 JPY
    driver.find_element(By.NAME, "currency_code").click()
    dropdown_currency = driver.find_element(By.NAME, "currency_code")
    dropdown_currency.find_element(By.XPATH, "//option[. = 'JPY']").click()

    # 3. 点击第5个商品卡片
    driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(5) .hot-product-card-img-overlay").click()

    # 4. 点击数量下拉框并选择数量5
    driver.find_element(By.ID, "quantity").click()
    dropdown_qty = driver.find_element(By.ID, "quantity")
    dropdown_qty.find_element(By.XPATH, "//option[. = '5']").click()

    # 5. 点击加入购物车
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click()

    # 6. 点击查看购物车按钮
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)").click()

    # 7. 点击 Continue Shopping 链接
    driver.find_element(By.LINK_TEXT, "Continue Shopping").click()
