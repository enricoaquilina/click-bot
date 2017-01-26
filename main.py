import sys
import subprocess
import time
import os
import pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from random import randint

# im = Image.open('cp2.png')
# nx, ny = im.size
# im2 = im.resize((int(nx*5), int(ny*5)), Image.BICUBIC)
# im2.save("final_pic.png")
# enh = ImageEnhance.Contrast(im)
# enh.enhance(1.3).show("30% more contrast")
# if pytesseract.image_to_string(enh.enhance(1.3)).replace(' ', '').isalpha():
#     print(pytesseract.image_to_string(enh.enhance(1.3)).replace(' ', ''))

class Clicker():

    def __init__(self):
        print('Initialising browser..')
        # display = Display(visible=0, size=(1024, 768))
        # display.start()

        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")

        self.driver = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'])
        self.driver2 = webdriver.PhantomJS(desired_capabilities=dcap, service_args=['--ignore-ssl-errors=true', '--ssl-protocol=any', '--web-security=false'])

        # self.driver.maximize_window()
        self.driver.page_source.encode('utf-8')
        self.driver2.page_source.encode('utf-8')

        self.driver.set_window_size(1024, 768)
        self.driver2.set_window_size(1024, 768)

        self.driver.set_page_load_timeout(70)
        self.driver2.set_page_load_timeout(70)

        self.actions = ActionChains(self.driver)
        self.actions2 = ActionChains(self.driver2)

        self.total_ad_amount = 0
        self.get_info()
        self.current_ad_index = 0
        self.login_page = self.details[2]
        self.ads_page = self.details[3]
        self.counter = 2
        # driver.quit()
        # display.stop()

    def get_info(self):
        with open('info.txt') as f:
            info = f.readlines()
        self.details = [x.strip() for x in info]

    def login(self):
        print('Logging in..')
        self.driver.get(self.login_page)

        time.sleep(randint(3, 9))
        self.driver.find_element_by_id("Kf1").send_keys(self.details[0])
        time.sleep(randint(2, 5))
        self.driver.find_element_by_id("Kf2").send_keys(self.details[1])
        time.sleep(randint(2, 5))

        self.driver.find_element_by_id('botao_login').click()

    def get_curr_balance(self):
        print('Getting current balance..')
        self.driver.get(self.ads_page)
        self.driver.implicitly_wait(7)
        balance_raw = self.driver.find_element_by_id("t_saldo")
        self.balance = float(balance_raw.text.strip()[1:])
    def get_available_ads(self):
        print('Getting available ads..')
        green_buttons = self.driver.find_elements_by_xpath('//*[@class="button green"]')
        green_buttons[0].click()

        self.purple_ads = self.driver.find_elements_by_class_name("adfu")
        self.purple_ad_count = len(self.purple_ads)
        self.green_ads = self.driver.find_elements_by_class_name("ad30")
        self.green_ad_count = len(self.green_ads)
        self.gold_ads = self.driver.find_elements_by_class_name("adf")
        self.gold_ad_count = len(self.gold_ads)
    def save_cookies(self, driver, file_path):
        LINE = "document.cookie = '{name}={value}; path={path}; domain={domain}; expires={expires}';\n"
        with open(file_path, 'w') as file:
            for cookie in driver.get_cookies():
                file.write(LINE.format(**cookie))
    def load_cookies(self, driver, file_path):
        with open(file_path, 'r') as file:
            driver.execute_script(file.read())
    def prepare_stuff(self):
        print('Preparing stuff..')

        self.total_ad_amount = 0
        self.get_curr_balance()
        self.get_available_ads()

        self.driver2.get(self.ads_page)
        self.save_cookies(self.driver, 'cookies.js')
        self.driver2.delete_all_cookies()
        self.load_cookies(self.driver2, 'cookies.js')

    # def click_adprizes(self):
    #     print('Clicking ad prizes..')
    #     ad_prize_text = 'ap_h'
    #     curr_ad_prizes = int(self.driver.find_element_by_id(ad_prize_text).text)
    #
    #     prizes_link = self.driver.find_element_by_id('ap_h').get_attribute('href')
    #     self.driver2.get(prizes_link)
    #
    #     while True:
    #         time.sleep(12)
    #         next_link = self.driver2.find_element_by_id('nxt_bt_a').get_attribute('href')
    #         driver_name = 'driver'+str(self.counter+1)
    #         driver_name_prev = 'driver'+str(self.counter)
    #         self.driver_name = webdriver.Chrome()
    #         self.driver_name.page_source.encode('utf-8')
    #         self.driver_name.get(next_link)
    #         self.driver_name_prev.close()
    #         self.counter+=1
    def get_ad_amount(self, ad_no):
        bottom_text = self.driver.find_element_by_id('cae' + ad_no).text
        trim_end = bottom_text.index('+')
        self.total_ad_amount += float(bottom_text[1:trim_end-1])
    def print_info(self):
        print('Done for now.. :)')
        print('Purple: ' + self.purple_ad_count)
        print('Green: ' + self.green_ad_count)
        print('Gold: ' + self.gold_ad_count)
        print('Total clicked: ' + self.total_ad_amount)
        print('Balance previous: ' + self.balance)
        print('Balance new: ' + self.new_balance)
    def click_ads(self, ads, current_ad_index):
        self.current_ad_index = current_ad_index

        print('Please hold...')
        for ad in range(0, len(ads)):
            if 'AdPrize' in ads[ad].text:
                return
            ad_no = str(ads[ad].get_attribute('id'))[3:]
            self.get_ad_amount(ad_no)

            ad_header = self.driver.find_element_by_id('tg_' + ad_no)
            self.actions.move_to_element(ad_header).click().perform()

            time.sleep(randint(1, 4))

            moving_object = self.driver.find_element_by_id('l' + ad_no)
            link = moving_object.get_attribute('href')

            try:
                self.driver2.get(link)

                ad_text_element = self.driver2.find_element_by_id('omt1')
                if 'logged in' in ad_text_element.text:
                    self.load_cookies(self.driver2, 'cookies.js')

                for frame in self.driver2.find_elements_by_tag_name('iframe'):
                    id = frame.get_attribute('id')
                    if id == 'iF':
                        self.driver2.execute_script('document.getElementById("'+id+'").parentElement.removeChild(document.getElementById("'+id+'"))')
                for window in self.driver2.window_handles:
                    if window != self.driver2.current_window_handle:
                        self.driver2.switch_to.window(window)
                        for frame in self.driver2.find_elements_by_tag_name('iframe'):
                            id = frame.get_attribute('id')
                            if id != "":
                                self.driver2.execute_script(
                                'document.getElementById("' + id + '")'
                                                                   '.parentElement'
                                                                   '.removeChild(document.getElementById("' + id + '"))')
                            self.driver2.close()
                self.driver2.switch_to.window(self.driver2.window_handles[0])

            except UnexpectedAlertPresentException as uap:
                print(uap)
                self.driver2.execute_script('window.confirm = function(msg) { return true; }')
            except NoAlertPresentException as nap:
                print(nap)
            except TimeoutException as te:
                print(te)
            except Exception as ge:
                print(ge)
            finally:
                time.sleep(60)

    def refresh(self):
        self.driver.get(self.details[3])
        self.driver.refresh()
        self.main_window = self.driver.current_window_handle

    def do_this_shit(self):
        self.refresh()
        self.prepare_stuff()
        self.click_ads(self.gold_ads, 3)
        self.click_ads(self.purple_ads, 1)
        self.click_ads(self.green_ads, 2)
        self.refresh()
        self.new_balance = float(self.driver.find_element_by_id("t_saldo").text.strip()[1:])
        if self.new_balance != (self.balance + self.total_ad_amount):
            self.do_this_shit()
        else:
            self.print_info

    def check_login_success(self):
        try:
            username = self.driver.find_element_by_id('t_conta')
            return True
        except NoSuchElementException:
            return False
    def init_procedure(self):
        if self.check_login_success():
            print('Starting procedure..')
            # cur_run = 0

            while True:
                # cur_run += 1
                # print('Run: ' + str(cur_run))

                self.do_this_shit()
                time.sleep(randint(10, 20))
                # self.click_adprizes()
                # 1hrs
                time.sleep(3600)
        else:
            print('Did not login..')
    def lazy_mode(self):
        self.login()
        self.init_procedure()

c = Clicker()
c.lazy_mode()
