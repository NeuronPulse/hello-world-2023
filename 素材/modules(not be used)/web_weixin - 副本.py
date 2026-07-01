from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
import time
import os
import requests
from urllib.parse import urlparse, parse_qs, unquote

def send(driver,group_name,msg):
    # 查找并点击包含特定文本的 span 元素的上级 div 元素的上级 div 元素
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        time.sleep(5)
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            print("Found the span element")
    
            # 找到 span 元素的上3级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
            print("Found the ancestor div")
    
            # 点击上3级 div
            ancestor_div.click()
            print("Clicked the ancestor div")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    except Exception as e:
        print(f"Click Failed：{e}")
    
    # 定位输入框，并输入字符串
    input_box = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/div[2]/pre')
    input_box.send_keys(msg)
    # 定位按钮，并点击
    button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[2]/div/div[3]/div[3]/a')
    button.click()
    

def get_last_content(driver):
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        time.sleep(5)
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            print("Found the span element")
    
            # 找到 span 元素的上3级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
            print("Found the ancestor div")
    
            # 点击上3级 div
            ancestor_div.click()
            print("Clicked the ancestor div")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    except Exception as e:
        print(f"Click Failed：{e}")
    try:
        # 定位到最后一个 <div class="content"> 元素
        last_content_div = driver.find_elements(By.XPATH, '//div[@class="content"]')[-1]

        # 定位到子元素 <div>/<div>/<div>/<pre>，并获取其内容
        try:
            text = last_content_div.find_element(By.XPATH, './div/div/div/pre').text
            return text
        except:
            try
                url = last_content_div.find_element(By.XPATH, './div/div/div/div/div[2]/div/a').get_attribute('href')
                driver.get(url)
                WebDriverWait(driver, 10).until(EC.alert_is_present())
                # 处理提示框
                alert = driver.switch_to.alert
                alert.accept()
                return url
            except:
                img_element = last_content_div.find_elements(By.XPATH, './/img[@class="msg_img"]')
                img_element.click()
                a_download_link_xpath = '/html/body/div[6]/div[2]/div[2]/ul/li[2]/a'
                a_download_link = driver.find_element(By.XPATH, a_download_link_xpath)
                a_download_link.click()
                return None
                #<div class="card">
    except IndexError:
        print("No elements with class 'content' found.")
    except Exception as e:
        print(f"Failed to get text: {e}")

# Edge WebDriver 路径
edge_driver_path = r'..\msedgedriver.exe'

# 解压后的扩展路径
extension_path = r'C:\Users\五十度灰\Desktop\bot\wechat-need-web v1.1.1'

# 创建 EdgeOptions 实例
edge_options = webdriver.EdgeOptions()
edge_options.add_argument(f'--load-extension={extension_path}')
edge_options.add_experimental_option("prefs", {
    "download.default_directory": os.getcwd()+"\\download_files",
    "download.prompt_for_save_location": False,  # 禁止下载前提示保存位置
})

# 创建 WebDriver 服务实例
service_we = Service(edge_driver_path)

# 启动浏览器并加载扩展
driver_we = webdriver.Edge(service=service_we, options=edge_options)
time.sleep(5)  # 给扩展一些时间来加载

driver_we.get('https://wx.qq.com/')

group_name="文件传输助手"

send(driver_we,group_name,"test")

while(1):
    print(get_last_content(driver_we))
    time.sleep(1)

# 关闭浏览器
#driver.quit()



#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div/pre
#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[3]/div/div/div/div/div/div/div/pre

#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[4]/div/div/div/div[2]/div/div/div/pre

#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div/pre
#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[3]/div/div/div/div/div/div/div/pre
#//*[@id="chatArea"]/div[2]/div[1]/div[1]/div[4]/div/div/div/div[2]/div/div/div/pre





#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[2]/div/div/div/div[2]/div/div/div/pre
#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[3]/div/div/div/div/div/div/div/pre
#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/pre

#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div/div[2]/div/div/div/pre

#/html/body/div[2]/div/div[2]/div/div[2]/div[1]/div[1]/div[5]/div/div/div/div[2] <div class="content">
