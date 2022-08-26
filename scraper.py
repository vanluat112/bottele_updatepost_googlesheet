from email import message
import json
import os
import sys
import time
import pyotp
import telegram
from selenium.webdriver.common.by import By
import youtube
from datetime import datetime, date, timedelta
from random import randint
from ratelimit import limits, sleep_and_retry

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import utils
import config
# TOKEN = '2004211876:AAFtDfnD_4GsC4Ma_-Z8ShczIiCl9m-GECo'
# CHAT_ID = '-1001404426396'
min_delay_between_calls = 600
max_delay_between_calls = 900

min_func_calls = 100
max_func_calls = 150

min_wait_delay = 5
max_wait_delay = 8

@sleep_and_retry
@limits(calls=randint(min_func_calls, max_func_calls), period=randint(min_delay_between_calls, max_delay_between_calls))
def save_page_posts(module_name, section_name):
    try:
        element_xpath = element_selectors[module_name]["types"][section_name]["element_xpath"]
        global driver
        global page_posts
        driver.implicitly_wait(2)
        # fetch relevant section data
        elements = driver.find_elements(By.XPATH, element_xpath)
        page_posts = []
        other_selectors = element_selectors[module_name]["other_selectors"]
        for i in range(len(elements)):
            post = {
                "Date Posted": "",
                "Post Link": "",
                "Post Text": "" 
            }
            try:
                    # get post link
                    elements[i].find_element(By.XPATH,other_selectors["post_link"]).send_keys("")
                    time.sleep(1)
                    post_link = \
                        elements[i].find_element(By.XPATH,other_selectors["post_link"]).get_attribute("href").split(
                            "?")[0]
                    print(post_link)
            except Exception:
                    post_link = ""
            try:
                    # get post date
                date = utils.get_post_date_and_time(elements[i], other_selectors["post_date"])
                print(date)
            except Exception:
                date = None
                # get post text
            try:
                #utils.press_see_more_button(elements[i].find_element(By.XPATH,other_selectors["post_text"]),
                #                                element_selectors["other_script_selectors"]["see_more_button"])
                post_text = elements[i].find_element(By.XPATH,other_selectors["post_text"]).text
            except Exception:
                post_text = ""    
            # set fields
            post["Date Posted"] = str(date)
            post["Post Text"] = post_text.split('\n')[0]
            post["Post Link"] = post_link
            page_posts.append(post)  
            print(page_posts)    
        return page_posts
    except Exception:
        print("Some error occured while scraping '{}'".format(section_name))
        
@sleep_and_retry
@limits(calls=randint(min_func_calls, max_func_calls), period=randint(min_delay_between_calls, max_delay_between_calls))
def scrape_section(module_name, section_name, section_url):
    """ This function will scrape a section (e.g Tagged Photos) of a module (e.g Photos) """
    try:
        driver.get(section_url)
        if module_name in ["User Posts", "Page Posts", "Group Posts"]:
            driver.execute_script("window.scrollTo(0, 100);")
            time.sleep(6)
        if module_name not in ["User About", "User Profile Pic", "User Intro", "Page Intro"]:
            total_scrolls = int(config.total_scrolls)
            utils.scroll(total_scrolls, driver)
            driver.execute_script("window.scrollTo(0, 100);")
            time.sleep(2)
        save_page_posts(module_name, section_name)
        print("'{}' Section Done!".format(section_name))
    except Exception as e:
        print("Couldn't find data or it doesn't exist for: " + section_name)
        
@sleep_and_retry
@limits(calls=randint(min_func_calls, max_func_calls), period=randint(min_delay_between_calls, max_delay_between_calls))
def scrape_modules(item_url, modules_to_scrape):
    for module_name in modules_to_scrape:
        print("Module: '{}' ".format(module_name))
        sections = element_selectors[module_name]["types"]
        for section_name in sections.keys():
            print("Section: '{}'".format(section_name))
            if "profile.php" in item_url:
                if module_name in 'User About':
                    section_url = item_url + "&sk=" + sections[section_name]["url_for_profile_with_id"]
                else:
                    section_url = item_url + "&sk=" + sections[section_name]["url"][1:]
            else:
                section_url = item_url + sections[section_name]["url"]
            scrape_section(module_name, section_name, section_url)
      
        print("'{}' Module Completed!!".format(module_name))
    print("Finished Scraping: " + str(item_url))
    os.chdir("../..")
    return
@sleep_and_retry
@limits(calls=randint(min_func_calls, max_func_calls), period=randint(min_delay_between_calls, max_delay_between_calls))
def logout():
    global driver
    i = 0
    while(i < 2):
        try:
            driver.get("https://mbasic.facebook.com/login/save-password-interstitial")
            logout_button = driver.find_element(By.XPATH,"""//form[2]""")
            logout_button.click()
            time.sleep(2)
            break
        except Exception as e:
            pass
        i += 1
@sleep_and_retry
@limits(calls=randint(min_func_calls, max_func_calls), period=randint(min_delay_between_calls, max_delay_between_calls))
def login(email, password):
    """ Logging into the account """
    logged_in = False
    try:
        global driver
        try:
            if utils.match_strings_full(config.browser, 'Chrome'):
                driver = utils.chrome_webdriver(driver, config.headless_mode)
            elif utils.match_strings_full(config.browser, 'Edge'):
                driver = utils.edge_webdriver(driver, config.headless_mode)
            else:
                print("Error: Please select a supported browser (Chrome, Edge).")
                exit(1)
        except Exception as e:
            print("Error: The browser you selected likely isn't installed on your computer. Please verify.")
            exit(1)
        # safe wait
        driver.implicitly_wait(5)  # seconds
        fb_path = element_selectors["other_script_selectors"].get("facebook_web_link")
        driver.get(fb_path)
        driver.maximize_window()
        # filling the form
        driver.find_element(By.NAME,"email").send_keys(email)
        driver.find_element(By.NAME,"pass").send_keys(password)
        driver.find_element(By.NAME,"login").click()
        # if your account uses two-factor authentication
        mfa_enabled = utils.to_bool(config.two_factor_authentication)
        if mfa_enabled:
            mfa_selectors = element_selectors["other_script_selectors"]["mfa"]
            # enter code sent by Facebook
            mfa_code_input = driver.find_element(By.ID,mfa_selectors["code_input_bar"])
            totp = pyotp.TOTP(config.key)
            mfa_code_input.send_keys(totp.now())
            driver.find_element(By.ID,mfa_selectors["confirm_button"]).click()
            # save/not save this browser for future
            dont_save_browser_radio = utils.safe_find_element(driver, mfa_selectors["dont_save_browser_radio"])
            if dont_save_browser_radio is not None:
                dont_save_browser_radio.click()
            # there are so many screens asking you to verify things, just skip them all
            while (utils.safe_find_element(driver, mfa_selectors["confirm_button"]) is not None):
                driver.find_element(By.ID,"checkpointSubmitButton").click()
        logged_in = True
    except Exception as e:
        exit(1)
    return logged_in
def start_scraper(modules_to_scrape, urls_filename, facebook_link_prefix):
    global logged_in
    uncleaned_urls = open(urls_filename, encoding="utf-8").read().splitlines()
    cleaned_urls = []
    try:
        for uncleaned_url in uncleaned_urls:
            uncleaned_url = uncleaned_url.strip()
            new_url = facebook_link_prefix
            if not uncleaned_url.startswith("#") and not uncleaned_url == "":
                if uncleaned_url.endswith("/"):
                    new_url += uncleaned_url.split("/")[-2]
                else:
                    new_url += uncleaned_url.split("/")[-1]
                cleaned_urls.append(new_url)
    except:
        pass
    if len(cleaned_urls) > 0:
        if len(modules_to_scrape) > 0:
            if not logged_in:
                logged_in = login(email, password)
            print("\nStarting '{}' category scraping...".format(current_category))
            for url in cleaned_urls:
                driver.get(url)
                scrape_modules(url, modules_to_scrape)
        else:
            print("Error: '{}_modules' in config.py is set to empty. Please select a module to scrape.".format(
                current_category))
    else:
        print("Error: '{}s.txt' is empty or contains wrongly formatted urls.".format(current_category))

# def send_message(message):
#     try:
#         telegram_notify = telegram.Bot(TOKEN)
#         telegram_notify.send_message(chat_id=CHAT_ID, text=message)
#     except Exception as ex:
#         print(ex)

def setup_scraper():
    scrape_pages = utils.to_bool(config.scrape_pages)
    global current_category
    if scrape_pages:
        current_category = "page"
        modules_to_scrape = config.page_modules
        urls_filename = os.path.join("pages.txt")
        facebook_link_prefix = element_selectors["other_script_selectors"]["facebook_web_link"]
        start_scraper(modules_to_scrape, urls_filename, facebook_link_prefix)
    if logged_in:
        logout()
        driver.close()
        driver.quit()
session = datetime.now().strftime("%Y_%m_%d %I-%M %p")
if __name__ == "__main__":
    try:
        global bao_cao
        # Facebook
        email = config.email.strip()
        password = config.password.strip()
        if email == "" or password == "":
            exit(1)
        rate_limiting = utils.to_bool(config.rate_limiting)
        if rate_limiting:
            min_func_calls = config.min_func_calls
            max_func_calls = config.max_func_calls
            min_wait_delay = config.min_wait_delay
            max_wait_delay = config.max_wait_delay
        logged_in = False
        with open(os.path.join("element_selectors.json")) as a:
            element_selectors = json.load(a)
        driver = None
        setup_scraper()
        today = datetime.now()
        yesterday = date.today() - timedelta(days=1)
        print(yesterday)
        removes=[]
        print(page_posts)
        for i in range(len(page_posts)):
            print(i)
            date_time_obj = datetime.strptime(str(page_posts[i]["Date Posted"]), '%Y-%m-%d %H:%M:%S')
            print(date_time_obj.day)
            print(today.day)
            if today.day>2:
                if date_time_obj.day==(int(today.day)-1):
                    if date_time_obj.hour < 16:
                        print(page_posts[i])
                    removes.append(i)
                if date_time_obj.day < (int(today.day)-1):
                    removes.append(i)
            else:
                if date_time_obj.day==(int(yesterday.day)):
                    if date_time_obj.hour < 16:
                        removes.append(i)
                if date_time_obj.day <= (int(yesterday.day)-1) and date_time_obj.day !=1 and date_time_obj !=2:
                    removes.append(i)
            print(removes)
            
        for remove in sorted(removes, reverse=True):
            del page_posts[remove]

        count_post=len(page_posts)
        channel_id='UCeKrBHxTzAxp4ypgUoauBAQ'
        resul_yt = youtube.get_info_first_video(channel_id)
        if resul_yt is not None:
            line_ends = 'B. Đăng tải 01 video tự biên tập lên kênh Youtube “TIN ĐỐI CHỨNG", cụ thể: \n{} \n{}'.format(resul_yt["title"],resul_yt["link_video"])
            section ='A. '
        else:
            line_ends = ''
            section = ''
        line_starts = 'T5 báo cáo Thủ trưởng kết quả TCTT ngày {}/{}/{}: \n{}Đăng tải {} bài viết tự biên tập lên kênh Fanpage "TIN ĐỐI CHỨNG", cụ thể:'.format(today.day, today.month,today.year,section,count_post)
        lines=[]
        for i in range(count_post):
            line = '{}/ {} \n{}\n'.format((i+1),page_posts[i]["Post Text"],page_posts[i]["Post Link"])
            print(line)
            lines.append(line)
        lines = ''.join(lines)
        bao_cao ='{}\n{}\n{}'.format(line_starts,lines,line_ends)
        print(bao_cao)
    except:
        bao_cao ='Trực ban phòng làm báo cáo!'
    print(bao_cao)
    #send_message(bao_cao)
    

