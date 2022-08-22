# -*- coding: utf-8 -*-
import pynput
from pynput import keyboard
import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
import pyautogui
import time

global base_dir


# 프로그램 초기 설정. 설정값은 여기를 바꿀 것.
base_dir = './sample_folder'
category_name = ''



# 해당 폴더 내의 파일 목록을 불러옴
img_list = os.listdir(base_dir)
# xml폴더 목록을 불러와 비교
if os.path.exists(base_dir + '_xml'):
    xml_list = os.listdir(base_dir + '_xml')
else:
    os.mkdir(base_dir + '_xml')
    xml_list = []
temp_arr = []
for item in xml_list:
    temp_arr.append(os.path.splitext(item)[0])
xml_list = temp_arr
# splittext로 분리비교

temp_arr = []
for item in img_list:
    if os.path.splitext(item)[0] not in xml_list:
        temp_arr.append(item)

work_list = temp_arr

print('작업 이전 데이터 세팅 완료')
print('* 아래의 통계 수 및 데이터가 부정확한 경우에는 문의 바랍니다.')
print('* 재작업을 원할 경우에는 이미지 파일명과 매칭되는 xml파일을 삭제 후 프로그램을 재기동하십시오.')
print('===========================================================================')
print('작업 디렉터리 : ' + base_dir)
print('전체 파일 수 : ' + str(len(img_list)))
print('작업완료 xml 파일 수 : ' + str(len(xml_list)))
print('작업대상 파일 수 : ' + str(len(work_list)))
print('===========================================================================')

global iter
iter = 0


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {
  "download.default_directory": os.path.abspath(base_dir + '_xml'),
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
})
driver = webdriver.Chrome("./chromedriver.exe", options = options)
driver.get("https://energy.linkit.me/image-annotation-tool/")

def open_image(base_dir, filename):
    driver.refresh()
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[3]/images-slider/div[1]/label[1]/input').send_keys(os.path.abspath(base_dir + '/' + filename))
    driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[2]/div[3]/images-slider/div[3]/div/img').click()

def save_image(filename):
    # splitext를 활용해 xml경로로 변경.
    xml_dir = os.path.splitext(filename)[0] + '.xml'
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/menu-dropdown/div/div[1]/i').click()
    time.sleep(0.4)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/menu-dropdown/div/div[2]/a[2]').click()
    time.sleep(0.4)
    driver.find_element(By.CSS_SELECTOR, '#saveAsPascalVOC').click()
    time.sleep(0.4)
    driver.find_element(By.CSS_SELECTOR, '#fileName').clear()
    driver.find_element(By.CSS_SELECTOR, '#fileName').send_keys(xml_dir)
    driver.find_element(By.CSS_SELECTOR, 'body > div:nth-child(46) > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-buttons > button.btn.btn-blue').click()
    time.sleep(0.5)
    driver.find_element(By.CSS_SELECTOR, 'body > div.jconfirm.jconfirm-light.jconfirm-open > div.jconfirm-scrollpane > div > div > div > div > div > div > div > div.jconfirm-closeIcon').click()
    return xml_dir

def on_press(key):
    return

def on_release(key):
    global iter
    global base_dir
    filename = work_list[iter]
    if key == pynput.keyboard.Key.esc:
        print("프로그램 종료")
        return False
    elif key == pynput.keyboard.Key.f8:
        # 파일 불러오기
        open_image(base_dir, filename)

    elif key == pynput.keyboard.Key.f4:
        driver.find_element(By.CSS_SELECTOR, '#category-select-box').send_keys(category_name)
        driver.find_element(By.CSS_SELECTOR, '#sidebar > label-panel > div > div:nth-child(2) > input').clear()
        driver.find_element(By.CSS_SELECTOR, '#sidebar > label-panel > div > div:nth-child(2) > input').send_keys(filename)
        driver.find_element(By.CSS_SELECTOR, '#sidebar > label-panel > div > div:nth-child(3) > attributes-list > div.clearfix > button').click()
        time.sleep(0.2)
        driver.find_element(By.CSS_SELECTOR, '#sidebar > label-panel > div > div:nth-child(3) > attributes-list > div.clearfix > button').click()
        time.sleep(0.2)
        driver.find_element(By.CSS_SELECTOR, '#sidebar > label-panel > div > div:nth-child(3) > attributes-list > div.clearfix > button').click()
        time.sleep(0.2)
        Select(driver.find_element(By.CSS_SELECTOR, '#attr-name_0')).select_by_visible_text("창 개수")
        Select(driver.find_element(By.CSS_SELECTOR, '#attr-name_1')).select_by_visible_text("프레임 재질")
        Select(driver.find_element(By.CSS_SELECTOR, '#attr-name_2')).select_by_visible_text("개폐방식")

    elif key == pynput.keyboard.Key.f3:
        # 결과파일 저장하기
        xml_dir = save_image(filename)
        iter = iter + 1
        if iter > len(work_list):
            print('파일목록 전부 처리 완료')
            exit()
        print('이하의 파일을 저장했습니다. [' + xml_dir + ']')
        print('해당 디렉터리 작업 진척도 : ' + str(iter) + '/' + str(len(work_list)))

listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

os.system("pause")
