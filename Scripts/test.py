import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

print("")
print("네이버 이미지 줍줍이입니다.")
print("")
maxium_img = input("몇장 : ")
print("")
query = input("검색창 : ")
print("")
print("진행 상황 : ")


driver = webdriver.Chrome("C:\\Users\\HYEONGJUN\\Desktop\\파이썬\\selenium\\chromedriver.exe")
driver.get("https://search.naver.com/search.naver?where=image")
elem = driver.find_element_by_id("nx_query")
elem.send_keys(query)
elem.send_keys(Keys.RETURN)
time.sleep(2)

#스크롤 끝까지 내리기
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

imgs = driver.find_elements_by_css_selector("img._listImage")

links = []

for img in imgs:
    click = img.click()
    time.sleep(2)
    link = driver.find_element_by_xpath("/html/body/div[3]/div[2]/div/div[1]/section/div[2]/div[2]/div/div[1]/div[1]/div[1]/div/div/div[1]/div[1]/img").get_attribute("src")
    if "http" in link:
        links.append(link)
        if len(links) >= int(maxium_img):
            break

if not os.path.isdir(os.getcwd()+"\\"+query):
    os.mkdir(os.getcwd()+"\\"+query)

count = 1
for i in range(len(links)):
    urllib.request.urlretrieve(links[i], os.getcwd()+"\\"+query+"\\" +str(count)+".jpg")
    count=count+1

driver.close()
print("")
print("완료")
