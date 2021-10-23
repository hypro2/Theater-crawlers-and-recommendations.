import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas


#연극 사이트 입력 및 크롬 실행 연극 사이트 주소
query = "http://ticket.interpark.com/TPGoodsList.asp?Ca=Dra"
driver = webdriver.Chrome("C:\\Users\\HYEONGJUN\\Desktop\\파이썬\\selenium\\chromedriver.exe")
driver.get(query)
time.sleep(1)
number = 100

addresslist=[]
# 연극 상세 페이지 이동
for i in range(1,int(number)+1): 
    elem = driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td[3]/div/div/div[2]/div/table/tbody/tr["+str(i)+"]/td[1]/a").get_attribute("href")
    addresslist.append(elem)

for lis in addresslist:
    query = lis
    driver.get(query)
    time.sleep(1)
    
    try:
        # 연극 관람후기로 이동
        title = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[2]/div[1]/div/div[1]/h2").text
        elem = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/nav/div/div/ul/li[4]/a")

        #리뷰페이지로 이동 가끔 3번째에 있을때도 있음
        dataTarget = elem.get_attribute("data-target")
        if(dataTarget != "REVIEW"):
            elem = driver.find_element_by_xpath("/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/nav/div/div/ul/li[3]/a")

        elem.click()
        time.sleep(1)

        #아이디와 별점 크롤링
        ids =[]
        stars =[]

        #베스트 리뷰가 없을때 실행
        #클래스에서 베스트를 찾고 없으면 빈값을 내보냄
        try:
            best = driver.find_element_by_class_name("bastBadge").text
        except:
            best = ""

        if(best != "베스트"):
            while(True):
                try:
                    for j in range(1,11):
                        for i in range(1,16):
                            a= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/ul/li["+str(i)+"]/div/div[1]/div[2]/ul/li[1]/span[1]"
                            b= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/ul/li["+str(i)+"]/div/div[1]/div[1]/div/div[1]/div"
                            id = driver.find_element_by_xpath(a).text
                            star = driver.find_element_by_xpath(b).get_attribute("data-star")
                            ids.append(id)
                            stars.append(star)

                        #다음페이지 클릭
                        if(j<10):
                            botton = "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[3]/div[2]/ol/li["+str(j+1)+"]/a"
                            elem = driver.find_element_by_xpath(botton)
                            elem.click()
                            time.sleep(1)
                        else:
                            #10번 다음페이지
                            elem = driver.find_element_by_class_name("pageNextBtn.pageArrow")
                            elem.click()
                            time.sleep(1)
                except:
                    break

        #베스트리뷰가 있으면 실행
        else:
            while(True):
                try:
                    for j in range(1,11):
                        for i in range(1,16):
                            a= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/ul/li["+str(i)+"]/div/div[1]/div[2]/ul/li[1]/span[1]"
                            b= "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/ul/li["+str(i)+"]/div/div[1]/div[1]/div/div[1]/div"
                            id = driver.find_element_by_xpath(a).text
                            star = driver.find_element_by_xpath(b).get_attribute("data-star")
                            ids.append(id)
                            stars.append(star)

                        #다음페이지 클릭
                        if(j<10):
                            botton = "/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div/div/div[4]/div[2]/ol/li["+str(j+1)+"]/a"
                            elem = driver.find_element_by_xpath(botton)
                            elem.click()
                            time.sleep(1)
                        else:
                            #10번 다음페이지
                            elem = driver.find_element_by_class_name("pageNextBtn.pageArrow")
                            elem.click()
                            time.sleep(1)
                except:
                    break    


        #csv로 저장
        if not os.path.isdir(os.getcwd()+"\\연극데이터"):
            os.mkdir(os.getcwd()+"\\연극데이터")
        dic ={'id':ids, 'star':stars}
        df = pandas.DataFrame(dic)
        df.to_csv(os.getcwd()+"\\연극데이터\\"+title+'.csv', index=False, encoding='cp949')
    except:
        print(title+" 넘어가기")


driver.quit()