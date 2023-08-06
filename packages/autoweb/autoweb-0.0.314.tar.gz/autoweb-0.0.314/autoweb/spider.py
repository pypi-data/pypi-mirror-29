"""
对于selenium的爬虫功能的项目封装

4.根据元素属性
　　1)精准匹配：
　　　　[A]  driver.findElement(By.cssSelector("input[name=username]"));属性名=属性值,id,class,等都可写成这种形式
      [B]  driver.findElement(By.cssSelector("img[alt]"));存在属性。例如img元素存在alt属性
　　　　[C]  driver.findElement(By.cssSelector("input[type='submit'][value='Login']"));多属性
　　2)模糊匹配：（正则表达式匹配属性）
　　　　[A]  ^=  driver.findElement(By.cssSelector(Input[id ^='ctrl']));匹配到id头部 如ctrl_12
　　　　[B]  $=  driver.findElement(By.cssSelector(Input[id $='ctrl']));匹配到id尾部 如a_ctrl
　　　　[C]  *=  driver.findElement(By.cssSelector(Input[id *= 'ctrl']));匹配到id中间如1_ctrl_12
　　　　更多正则匹配原则请查看CSS3 选择器——属性选择器  http://www.w3cplus.com/css3/attribute-selectors
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import re
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import random
import platform
import getpass
import os
from .error import *


class CAutoWeb4Spider(object):
    def __init__(self, driver_type='chrome', executable_path=None):
        if driver_type == 'phantomjs':
            self._driver = webdriver.PhantomJS(executable_path=executable_path)
            pass
        elif driver_type == 'chrome':
            self._driver = webdriver.Chrome(executable_path=executable_path)
            pass
        else:
            assert False
        # 不能设置页面超时时间，会产生异常导致百度的JS无法正常执行。
        # self._driver.set_page_load_timeout(20)
        # self._driver.set_script_timeout(20)
        return

    def __del__(self):
        self._driver.quit()
        return

    def __get_dom_list(self, selector):
        try:
            return self._driver.find_elements_by_css_selector(selector)
        except NoSuchElementException:
            raise ERRAutoWeb4Spider4NotExistSelectorDom(self._driver.current_url, selector)

    def __get_dom(self, selector):
        try:
            return self._driver.find_element_by_css_selector(selector)
        except NoSuchElementException:
            raise ERRAutoWeb4Spider4NotExistSelectorDom(self._driver.current_url, selector)

    def __get_dom_attribute(self, dom, selector, attribute):
        try:
            if selector is None:
                return dom.get_attribute(attribute)
            else:
                return dom.find_element_by_css_selector(selector).get_attribute(attribute)
        except NoSuchElementException:
            raise ERRAutoWeb4Spider4NotExistSelectorDom(self._driver.current_url, selector)

    def visit(self, url, wait_seconds_to_visit=1, auto_refresh=False):
        self._driver.get(url)
        if auto_refresh:
            self._driver.refresh()  # 解决网址重定向问题，强制刷新一下
        if wait_seconds_to_visit is None or wait_seconds_to_visit == 0:
            return
        time.sleep(wait_seconds_to_visit)  # 解决ajax动态渲染页面延时一会加载
        return

    def get_text(self, selector):
        return self.__get_dom(selector).text

    def get_regex_text(self, selector, regex, group=1):
        return re.search(regex, self.__get_dom(selector).text).group(group)

    def get_attribute(self, selector, attribute):
        return self.__get_dom_attribute(self.__get_dom(selector), None, attribute)

    def input(self, selector, value):
        self.__get_dom(selector).send_keys(value)
        return

    def click(self, selector):
        self.__get_dom(selector).click()
        return

    def hover_click(self, selector, xoffset=0, yoffset=0):
        return ActionChains(self._driver).move_to_element_with_offset(self.__get_dom(selector), xoffset=xoffset,
                                                                     yoffset=yoffset).click().perform()

    def wait_until_dom_exist(self, selector, timeout_seconds=20, is_ignore_timeout_exception=False):
        # self._driver.set_page_load_timeout(timeout_seconds)
        # self._driver.set_script_timeout(timeout_seconds)
        time.sleep(1)
        locator = (By.CSS_SELECTOR, selector)
        if not is_ignore_timeout_exception:
            WebDriverWait(self._driver, timeout_seconds, 0.5).until(EC.presence_of_element_located(locator))
        else:
            try:
                WebDriverWait(self._driver, timeout_seconds, 0.5).until(EC.presence_of_element_located(locator))
            except TimeoutException:
                pass
        return

    # 随机数等待时间避免触发服务器的验证码（绕过反爬虫程序）
    @staticmethod
    def wait(seconds=0):
        if seconds == 0:
            seconds = random.choice(range(10, 30))
        time.sleep(seconds)
        return

    @staticmethod
    def wait_forever():
        while True:
            time.sleep(1)

    @staticmethod
    def download_dir():
        if platform.system() == 'Darwin':
            download_dir = '/Users/%s/Downloads' % getpass.getuser()
        elif platform.system() == 'Windows':
            download_dir = 'c:/Users/%s/Downloads' % getpass.getuser()
        else:
            assert False
        return download_dir

    @staticmethod
    def wait_download_success(filename, timeout_seconds=3600):
        """
        根据下载的文件名在指定下载目录下是否存在间接判断下载是否成功
        :param filename:
        :param timeout_seconds: 下载超时时间。
        :return:
        """
        assert timeout_seconds > 0
        for i in range(timeout_seconds):
            time.sleep(1)
            path = Spider.download_dir() + '/' + filename
            if os.path.exists(path):
                return
        raise ERRAutoWeb4Spider4DownloadTimeout(filename)
