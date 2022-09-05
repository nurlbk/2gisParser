from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import keyboard
import time

from selenium.webdriver.remote.webelement import WebElement

sleep_time = 0.5


def parseFirst(url: str, search_name: str) -> dict:

    chromeDriver = chromeSetting(url=url)
    goToSearch(search_name=search_name, driver=chromeDriver)
    zoomPage(1)
    data = []

    getData(chromeDriver, data, parse_all=False)
    # jd = json.dumps(data, ensure_ascii=False)
    closeDriver(chromeDriver)
    return dict(data[0])


def parseAll(url: str, search_name: str) -> dict:
    chromeDriver = chromeSetting(url=url)
    goToSearch(search_name=search_name, driver=chromeDriver)
    zoomPage(7)
    data = []

    goToNextPages(chromeDriver, data)
    # jd = json.dumps(data, ensure_ascii=False)
    closeDriver(chromeDriver)

    return {f"{search_name}": data}


def closeDriver(driver: WebDriver):
    try:
        driver.close()
        driver.quit()
    except:
        pass


def chromeSetting(url: str) -> WebDriver:
    # user_agent = UserAgent()
    options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)

    # options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(r"./chromedriver/chromedriver.exe"),
        options=options
    )
    try:
        driver.get(url=url)
        time.sleep(sleep_time)
        return driver
    except:
        print("AAAAA")
        closeDriver(driver)
    finally:
        time.sleep(sleep_time)


def goToSearch(search_name: str, driver: WebDriver):
    try:
        search_input = driver.find_element(by=By.CLASS_NAME, value="_1gvu1zk")

        search_input.send_keys(search_name)
        search_input.send_keys(Keys.ENTER)
        time.sleep(sleep_time)

        footer = driver.find_element(by=By.CLASS_NAME, value="_euwdl0")
        footer.click()

        time.sleep(sleep_time)
    except:
        closeDriver(driver)


def zoomPage(count: int):
    for _ in range(count):
        time.sleep(sleep_time)
        keyboard.press_and_release("ctrl+-")


def findElement(elements_name, driver: WebDriver = None, parent_class: WebElement = None) -> WebElement:
    if len(elements_name) == 0:
        if parent_class is None:
            pass
        else:
            return parent_class
    elif parent_class is None:
        try:
            element = driver.find_element(by=By.CLASS_NAME, value=elements_name[0])
            return findElement(elements_name=elements_name[1:], parent_class=element)
        except:
            print("zzzzz")
            pass
    else:
        try:
            element = parent_class.find_element(by=By.CLASS_NAME, value=elements_name[0])
            return findElement(elements_name=elements_name[1:], parent_class=element)
        except:
            pass


def getText(path, parent_class) -> str:
    try:
        text = findElement(elements_name=path, parent_class=parent_class).text
        return text
    except:
        return ""


def getData(driver: WebDriver, data: list, parse_all=True):
    try:
        main_blocks_class = findElement(elements_name=['_121zpzx', '_1u4plm2'], driver=driver)
        main_blocks = main_blocks_class.find_elements(by=By.CLASS_NAME, value="_r47nf")

        items_block_parent = findElement(elements_name=['_z72pvu', '_awwm2v'], parent_class=main_blocks[0])

        items_block = items_block_parent.find_elements(by=By.CLASS_NAME, value="_1hf7139")

        if len(items_block) == 0:
            items_block = driver.find_elements(By.CLASS_NAME, value='_1uckoc70')
        for item in items_block:

            time.sleep(sleep_time * 2)
            item.click()

            time.sleep(0.5)

            main_blocks_class = findElement(elements_name=['_121zpzx', '_1u4plm2'], driver=driver)
            main_blocks = main_blocks_class.find_elements(by=By.CLASS_NAME, value="_r47nf")

            current_item_block_path = ['_guxkefv', '_jcreqo']
            current_item_block_parent = findElement(elements_name=current_item_block_path,
                                                    parent_class=main_blocks[1])
            current_item_block = current_item_block_parent.find_element(by=By.CLASS_NAME, value="_18lzknl")

            try:
                upper_block = current_item_block.find_element(by=By.CLASS_NAME, value="_19sjw5q")
                lower_block = current_item_block.find_element(by=By.CLASS_NAME, value="_1b96w9b")

                object_name = getText(path=['_6htn2u', '_1p7bda', '_1dcp9fc', '_d9xbeh', '_oqoid'],
                                      parent_class=upper_block)
                object_type = getText(path=['_6htn2u', '_1p7bda', '_1dcp9fc', '_11eqcnu', '_oqoid'],
                                      parent_class=upper_block)
                object_rating = getText(path=['_6htn2u', '_1p7bda', '_1reln2c', '_1n8h0vx'],
                                        parent_class=upper_block)

                object_district = getText(path=['_t0tx82', '_8sgdp4', '_599hh', '_1p8iqzw'],
                                          parent_class=lower_block)
                object_address = getText(path=['_t0tx82', '_8sgdp4', '_599hh', '_2lcm958'],
                                         parent_class=lower_block)

                try:
                    object_link = driver.current_url
                except:
                    object_link = ''
                try:
                    object_phone = findElement(elements_name=['_t0tx82', '_8sgdp4', '_599hh', '_b0ke8', '_2lcm958'],
                                               parent_class=lower_block).get_attribute('href')[4:]
                except:
                    object_phone = ''

                place = {'name': object_name,
                         'type': object_type,
                         'phone': object_phone,
                         'address': object_address,
                         'district': object_district,
                         'rating': object_rating,
                         'link': object_link}
                data.append(place)
                if not parse_all:
                    break

            except:
                print("hehe")
                continue

    except:
        print("SSSSS")


def goToNextPages(driver: WebDriver, data: list):
    onLastPage = True
    while True:
        try:
            # scroll_block = driver.find_element(by=By.CLASS_NAME, value="_1x4k6z7")
            # ActionChains(driver) \
            #     .scroll_to_element(scroll_block) \
            #     .perform()

            time.sleep(sleep_time)
            getData(driver=driver, data=data)

            next_page_btn_path = ["_1xzra4e", '_5ocwns']
            next_page_btn_parent = findElement(elements_name=next_page_btn_path, driver=driver)
            next_page_btn = next_page_btn_parent.find_elements(by=By.CLASS_NAME, value="_n5hmn94")

            if (len(next_page_btn) == 2 and not onLastPage) or (len(next_page_btn) == 1 and onLastPage):
                onLastPage = False
                next_page_btn[len(next_page_btn) - 1].click()
            else:
                break

        except:
            print("FFFFF")
            break
