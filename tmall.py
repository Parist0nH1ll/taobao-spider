#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re,time
import os, sys
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
import browser_cookie3
from urllib.parse import unquote



TB_LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'

options = webdriver.ChromeOptions()
options.add_argument('lang=zh_CN.UTF-8')
options.add_argument('accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
options.add_argument('accept-encoding=gzip, deflate, br')
options.add_argument('user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
#1是加载图片，2是不加载图片
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
#options.add_argument('--proxy-server=http://127.0.0.1:9000')
options.page_load_strategy = 'eager'
options.add_argument('disable-infobars')
#options.add_argument('--headless')
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--disable-dev-shm-usage')
browser=webdriver.Chrome(chrome_options=options)
wait=WebDriverWait(browser, 10)

class Login:

    def __init__(self, account, password):
        self.browser = browser
        self.account = account
        self.password = password

    def open(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(20)

    def start(self):
        # 2 打开淘宝登录页
        self.browser.get(TB_LOGIN_URL)
        cookies = browser_cookie3.chrome(domain_name='.taobao.com',cookie_file=os.path.join(os.getenv('APPDATA', '')) + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies')
        for c in cookies:
            cookie = {'name': c.name, 'value': unquote(c.value, 'utf-8')}
            #print(cookie)
            browser.add_cookie(cookie)
        browser.refresh()
        time.sleep(1)
        # 3 输入用户名
        self.write_username(self.account)
        time.sleep(1.5)
        # 4 输入密码
        self.write_password(self.password)
        time.sleep(1.5)
        # 5 如果有滑块 移动滑块
        if self.lock_exist():
            self.unlock()
        # 6 点击登录按钮
        self.submit()
        # 7 登录成功，直接请求页面
        print("登录成功，跳转至目标页面")
        time.sleep(3.5)

    def switch_to_password_mode(self):
        if self.browser.find_element_by_id('J_QRCodeLogin').is_displayed():
            self.browser.find_element_by_id('J_Quick2Static').click()

    def write_username(self, username):
        try:
            username_input_element = self.browser.find_element_by_id('fm-login-id')
        except:
            username_input_element = self.browser.find_element_by_id('TPL_username_1')
        username_input_element.clear()
        username_input_element.send_keys(username)

    def write_password(self, password):
        try:
            password_input_element = self.browser.find_element_by_id("fm-login-password")
        except:
            password_input_element = self.browser.find_element_by_id('TPL_password_1')
        password_input_element.clear()
        password_input_element.send_keys(password)

    def lock_exist(self):
        return self.is_element_exist('#nc_1_wrapper') and self.browser.find_element_by_id(
            'nc_1_wrapper').is_displayed()

    def unlock(self):
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.browser.find_element_by_css_selector("#nocaptcha > div > span > a").click()

        bar_element = self.browser.find_element_by_id('nc_1_n1z')
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 258, 0).perform()
        if self.is_element_exist("#nocaptcha > div > span > a"):
            self.unlock()
        time.sleep(0.5)

    def submit(self):
        try:
            self.browser.find_element_by_css_selector("#login-form > div.fm-btn > button").click()
        except:
            self.browser.find_element_by_id('J_SubmitStatic').click()

        time.sleep(0.5)
        if self.is_element_exist("#J_Message"):
            self.write_password(self.password)
            self.submit()
            time.sleep(5)

    def is_element_exist(self, selector):
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False

def search(url, i):
    print('正在搜索')
    try:      
        browser.get(url+'&pageNo='+str(i))
        #添加本地Cookies
        cookies = browser_cookie3.chrome(domain_name='.tmall.com',cookie_file=os.path.join(os.getenv('APPDATA', '')) + '\\..\\Local\\Google\\Chrome\\User Data\\Default\\Network\\Cookies')
        for c in cookies:
            cookie = {'name': c.name, 'value': unquote(c.value, 'utf-8')}
            #print(cookie)
            browser.add_cookie(cookie)
        browser.refresh()
        
        html=browser.page_source
        if '没找到符合条件的商品' in html:
            return 0   

        #等待页面加载
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pagination")))

        time.sleep(30)
        #TODO 获取产品信息，执行函数
        get_products()

        #返回页数信息
        return i
    #判断超时
    except Exception as e:
        print(e)
        #重新执行
        #return search()
        
def get_sales(link):
    browser.get(link)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "tm-count")))
    html=browser.page_source
    with open('test.txt', 'w', encoding='utf-8') as f:
        f.write(html)
    sales = re.findall('tm-count.+?\>(.+?)\<', html)
    if sales:
        sales = sales[0]
    print(sales)
    return sales

def get_products():
    #获取网页源码
    html=browser.page_source
    #PyQuery解析
    doc=pq(html)
    #信息提取
    items=doc('.item').items()
    #保存数据
    n=keys+'.csv'
    fw = open(n, 'a+', encoding='utf-8-sig')
    for item in items:
        product_name = item.find('.item-name').text().replace(' ', '').replace(',','')
        #print(product_name)  
        if ('包' in product_name) or ('帽' in product_name) or ('袜' in product_name):
            product_link = 'https:' + item.find('.item-name').attr('href')
            sales = ''#get_sales(product_link)
            fw.write(product_name + ',' +
                     product_link + ',' +
                     item.find('.c-price').text().strip().replace('¥', '').replace('.00', '') + ',' +
                     sales + ','
                     '\n')
                     
def main(url):
    try:
        #开始搜索
        #循环遍历所有页数
        for i in range(1,101):
            print('Searching for page' + str(i))
            if not search(url, i):
                print('搜索完毕')
                return
        print('信息写入完成，可以查看文件.')
        # 浏览器关闭
        browser.close()
    except Exception:
        print('错误了，请检查')
    finally:
        pass


if __name__ == '__main__':
    # 输入你的账号名
    account = ''
    # 输入你密码
    password = ''
    Login(account,password).start()
    keys='nike'
    #创建excel
    n = keys + '.csv'
    with open(n, 'w', encoding="utf-8-sig") as f:
        productlist =  '商品名称' + ',' + '商品链接' + ',' + '价格' + ',' + '销量' + '\n'
        f.write(productlist)
    url = 'https://nike.world.tmall.com/category-1394890757.htm?search=y'
    main(url)
