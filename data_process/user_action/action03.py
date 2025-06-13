from selenium.webdriver.common.by import By

def run(driver):
    """
    脚本03的操作流程：
    2. 点击第2个商品卡片
    3. 点击数量下拉框并选择数量3
    4. 点击“加入购物车”
    5. 点击“返回”按钮
    6. 点击第4个商品卡片
    7. 点击“加入购物车”
    8. 点击“查看购物车”按钮
    9. 点击“Continue Shopping”链接
    """

    # 2. 点击第2个商品卡片
    driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(2) .hot-product-card-img-overlay").click()

    # 3. 点击数量下拉框并选择数量3
    driver.find_element(By.ID, "quantity").click()
    dropdown_qty = driver.find_element(By.ID, "quantity")
    dropdown_qty.find_element(By.XPATH, "//option[. = '3']").click()

    # 4. 点击加入购物车
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click()

    # 5. 点击返回按钮
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-secondary").click()

    # 6. 点击第4个商品卡片
    driver.find_element(By.CSS_SELECTOR, ".col-md-4:nth-child(4) .hot-product-card-img-overlay").click()

    # 7. 再次点击加入购物车
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary").click()

    # 8. 点击查看购物车按钮
    driver.find_element(By.CSS_SELECTOR, ".cymbal-button-primary:nth-child(1)").click()

    # 9. 点击 Continue Shopping 链接
    driver.find_element(By.LINK_TEXT, "Continue Shopping").click()
