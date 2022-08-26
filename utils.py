import argparse
import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

def to_bool(x):
    if x in ["False", "0", 0, False]:
        return False
    elif x in ["True", "1", 1, True]:
        return True
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")
# check if height changed
def check_height(driver, old_height):
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height != old_height
# helper function: used to scroll the page
def scroll(total_scrolls, driver, scroll_time=10, scroll_delay=1):
    old_height = 0
    current_scrolls = 0
    while True:
        try:
            if current_scrolls == total_scrolls:
                return
            old_height = driver.execute_script("return document.body.scrollHeight")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height(driver, old_height)
            )
            # to avoid suspicion by FB
            time.sleep(scroll_delay)
            current_scrolls += 1
        except TimeoutException:
            break
    return
def get_post_date_and_time(post_element, date_time_xpath):
    date = ""
    time = ""
    try:
        date = post_element.find_element(By.XPATH,date_time_xpath).text.strip()
        # date="Yesterday at 12:56 PM"
        day, month, year = "", "", ""
        current_time = datetime.now()
        hour=current_time.hour
        minutes=current_time.minute
        delta_hour=0
        delta_min=0
        delta_day=0
        # complete date: Nov 12, 2018 at 11:23AM"

        # "Nov 12" or "12h" or Nov 12, 2018"
        if "Yesterday" in date:
            # Yesterday at 9:44 AM  ""
            yesterday = current_time - timedelta(1)
            day = yesterday.day
            month = yesterday.strftime("%B")
            year = yesterday.year

            try:
                time = date.split(" at ")[1]
                # lấy thời gian
                time = date.split(" at ")[1]
                hour=int(time.split(" ")[0].split(':')[0])
                minutes=int(time.split(" ")[0].split(':')[1])
                if "PM" in time and hour<12:
                    hour+=12

            except:
                pass
        elif "Just now" in date:
            date=datetime.now()
        elif "at" not in date:
            # "Nov 12" or "12h"
            if ", " not in date:
                if ("h" in date or  "m" in date or "d" in date) and \
                        "em" not in date and "ch" not in date:
                    day = current_time.day
                    month = current_time.strftime("%B")
                    if "hrs" in date:
                        delta_hour=int(date.replace('hrs',''))
                    elif "hr" in date:
                        delta_hour=int(date.replace('hr',''))
                    elif "h" in date:
                        delta_hour=int(date.replace('h',''))
                    elif "mins" in date:
                        delta_min=int(date.replace('mins',''))
                    elif "min" in date:
                        delta_min=int(date.replace('min',''))
                    elif "m" in date:
                        delta_min=int(date.replace('m',''))
                    elif "d" in date:
                        delta_day=int(date.replace('d',''))
                else:
                    day = date.split(" ") #bug ở đây
                    month = date.split(" ")[0]
                year = current_time.year

            else:
                day = date.split(", ")[0].split(" ")[1]
                month = date.split(", ")[0].split(" ")[0]
                year = date.split(", ")[1]
        else:
            # November 9 at 8:00 PM  ·
            day = date.split(" ")[0].split(" ")[0]
            month = date.split(" at ")[0].split(" ")[1]
            year = current_time.year
            # lấy thời gian
            time = date.split(" at ")[1]
            hour=int(time.split(" ")[0].split(':')[0])
            minutes=int(time.split(" ")[0].split(':')[1])
            if "PM" in time and hour<12:
                hour+=12
          
        month = datetime.strptime(month[:3], "%b").month

        # make formatted date
        date = datetime(int(year), int(month), int(day),int(hour),int(minutes))
        date = date - timedelta(hours=delta_hour) - timedelta(minutes=delta_min) - timedelta(days=delta_day)

    except Exception:
        pass

    finally:
        return date

def chrome_webdriver(driver, headless_mode):
    options = chrome_options()
    options.binary_location = 'GoogleChromePortable64/App/Chrome-bin/chrome.exe'
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-gpu")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62")

    if headless_mode == True:
        options.headless = True

    driver = None
    driver = webdriver.Chrome(options=options)

    return driver

def match_strings_partial(string1, string2):
    return string1.lower().strip() in string2.lower().strip()


def match_strings_full(string1, string2):
    return string1.lower().strip() == string2.lower().strip()


def current_time():
    return datetime.now().strftime("%d/%m/%Y_%I-%M-%S_%p")


def safe_find_element(driver, elem_id):
    try:
        return driver.find_element(By.ID,elem_id)
    except NoSuchElementException:
        return None


def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def press_see_more_button(text_element, see_more_button_xpath):
    try:
        while (True):
            text_element.find_element(By.XPATH,see_more_button_xpath).send_keys("")
            text_element.find_element(By.XPATH,see_more_button_xpath).click()
    except:
        pass

