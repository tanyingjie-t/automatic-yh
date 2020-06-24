#!/usr/bin/env python
# coding: utf-8


from selenium import webdriver
import time
from PIL import ImageGrab
import re
from old_user import *
import requests
from hashlib import md5

zh="19858873684"
mm="penghui2001"
software="905873"
#超级鹰的账号密码以及软件id
class Chaojiying_Client(object):

    def __init__(self, username, password, soft_id):
        self.username = username
        password =  password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    def PostPic(self, im, codetype):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', im)}
        r = requests.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files, headers=self.headers)
        return r.json()

    def ReportError(self, im_id):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': im_id,
        }
        params.update(self.base_params)
        r = requests.post('http://upload.chaojiying.net/Upload/ReportError.php', data=params, headers=self.headers)
        return r.json()

def save_yzm_img(save_path,driver):
    """截屏获取验证 码图片，保存到本地"""
    # 传入验证码所在屏幕的坐标，屏幕不同参数不同
    ele = driver.find_element_by_xpath('//*[@id="userGetValidCodeImg"]/a/img')
    ele.screenshot(save_path)

def get_yzm(img_path):
    """通过超级鹰获取验证码"""
    # 输入超级鹰的账号，密码，和 软件ID
    chaojiying = Chaojiying_Client(zh, mm, software)	#用户中心>>软件ID 生成一个替换
    im = open(img_path, 'rb').read()  #本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    # print(chaojiying.PostPic(im, 1902))  #1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
    yzm = chaojiying.PostPic(im, 1902)['pic_str']
    print(yzm)
    return yzm

def login(driver,username,password,yzm):
    """登录"""    
    driver.find_element_by_name('loginCode').clear()
    driver.find_element_by_name('loginCode').send_keys(username)
    driver.find_element_by_name('password').clear()
    driver.find_element_by_name('password').send_keys(password)
    driver.find_element_by_name('validCode').clear()
    driver.find_element_by_name('validCode').send_keys(yzm)
    time.sleep(1)
    driver.find_element_by_id('userLoginButton').click()

def get_url(driver):
    """打开网页，并且将网页最大化"""
    url = 'http://xkctk.hangzhou.gov.cn/'
    driver.get(url)
    time.sleep(1)
    # 将屏幕最大化，方便获取验证码
    driver.maximize_window()
    time.sleep(1)
    driver.refresh()
    time.sleep(1)

def click_sq(driver):
    """点击申请表，再点击重新申请按钮"""
    # 先点击申请表按钮
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[2]/div/div[4]/table/tbody/tr[2]/td[8]/span/a').click()
    time.sleep(1)
    # 判断有没有重新申请的按钮
    match = re.search(r'<span class="tabbtn bgcolor_blue"><a href="#none" id="reApplyButton2" style="color: #fff">重新申请</a></span>', driver.page_source)
    if match:
        print('找到按钮')
        driver.find_element_by_xpath('//*[@id="reApplyButton2"]').click()
    else:
        print('未找到重新申请按钮')

def click_ok(driver):
    """点击重新申请后，再点击弹窗的确定按钮"""
    alert = driver.switch_to_alert()
    alert.accept()

def click_next(driver):
    """点击下一步"""
    from selenium.webdriver.support.ui import Select
    # 选择身份类型
    select_element = Select(driver.find_element_by_xpath('//select[@id="personType"]'))
    select_element.select_by_value('BSHJ')
    print('选择身份类型为：', select_element.all_selected_options[0].text)
    time.sleep(1)
    # 点击下一页
    driver.find_element_by_xpath('//*[@id="nextButton"]').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="secondButton"]').click()
    time.sleep(1)
    # 点击提交按钮
    driver.find_element_by_xpath('//*[@id="applyButton"]').click()

def login_operation():
    # # 主程序
    #username = "568479847"
    #password = "4654654"
    access_token = get_access_token()
    is_vip,openid = get_vip(access_token)
    username,password = get_zhma(access_token, openid)
    driver = webdriver.Chrome()
    get_url(driver)
    path = 'yzm.jpg'
    save_yzm_img(path,driver)
    yzm = get_yzm(path)
    login(driver,username,password,yzm)
    click_sq(driver)
    click_ok(driver)
    click_next(driver)
    click_ok(driver)


if __name__ == "__main__":
    login_operation()