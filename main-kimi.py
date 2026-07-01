# -*- coding: utf-8 -*-
import io
import os
import sys
import time
import json
import random
import datetime
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

config_json = 'chat_config.json'

with open(config_json, 'r', encoding='utf-8') as file:
    config_data = json.load(file)
        
class IOLogger:
    def __init__(self, filename):
        self.terminal_out = sys.stdout
        self.terminal_in = sys.stdin
        self.log = open(filename, "a", encoding='utf-8')
        
    def write(self, message):
        timestamp = time.time()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
        self.terminal_out.write(message)
        if not(message==''):
            self.log.write(formatted_time+message)

    def readline(self):
        timestamp = time.time()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
        input_text = self.terminal_in.readline()
        self.log.write(formatted_time+input_text)
        return input_text

    def flush(self):
        self.terminal_out.flush()
        self.log.flush()

# 创建IOLogger实例，并重定向stdout和stdin
logger = IOLogger(config_data["log_name"])
sys.stdout = logger
sys.stdin = logger
'''
def download_file(url, directory):
    # 确保目录存在
    if not os.path.exists(directory):
        os.makedirs(directory)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 确保请求成功
        filename = os.path.join(directory, os.path.basename(url))
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"File downloaded: {filename}")
        return filename
    except requests.exceptions.RequestException as e:
        # 捕获来自requests库的异常
        print(f"Request error downloading file: {e}")
    except OSError as e:
        # 捕获文件操作相关的异常
        print(f"File error: {e}")
    except Exception as e:
        # 捕获其他未预料到的异常
        print(f"An unexpected error occurred: {e}")
    return None
'''
def send(driver,group_name,msg):
    time.sleep(2)
    # 查找并点击包含特定文本的 span 元素的上级 div 元素的上级 div 元素
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            # 找到 span 元素的上3级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
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
    time.sleep(1)

def send_file(driver,group_name,file_path):
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            # 找到 span 元素的上3级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
            # 点击上3级 div
            ancestor_div.click()
            print("Clicked the ancestor div")
        except Exception as e:
            print(f"An error occurred: {e}")
        
    except Exception as e:
        print(f"Click Failed：{e}")
        
    file_input = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[3]/div[1]/a[3]/div[2]/input")

    # 发送文件路径到input元素
    file_input.send_keys(file_path)

def send_random_emoji(driver,group_name,key_words,pageSize):
    response = requests.get("https://doutu.lccyy.com/t/doutu/items?pageNum=1&pageSize="+str(pageSize)+"&keyword="+key_words).json()
    if(response["pageSize"]==1):
        send(driver,group_name,"呀(っ°Д°;)っ，我缺图了，没表情包了，呜呜呜……")
    else:
        img=requests.get(response["items"][random.randint(1,response["pageSize"]-1)]["url"]).content
        random.seed(int(time.time()*1000))
        seed=int(str(random.random()).replace('.', ''))
        with open(os.getcwd()+"\\doutu\\"+key_words+str(seed)+".png", 'wb') as file:
            file.write(img)
        send_file(driver,group_name,os.getcwd()+"\\doutu\\"+key_words+str(seed)+".png")

def get_last_content(driver):
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            # 找到 span 元素的上3级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
            # 点击上3级 div
            ancestor_div.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        
    except Exception as e:
        print(f"Click Failed：{e}")
    try:
        # 定位到最后一个 <div class="content"> 元素
        last_content_div = driver.find_elements(By.XPATH, '//div[@class="content"]')[-1]
        name = last_content_div.find_element(By.XPATH,"./preceding-sibling::img").get_attribute("title")
        # 定位到子元素 <div>/<div>/<div>/<pre>，并获取其文本
        text = last_content_div.find_element(By.XPATH, './div/div/div/pre').text
        return (name,text)
    except IndexError:
        print("No elements with class 'content' found.")
    '''
    except Exception as e:
        print(f"Failed to get text: {e}")
    '''
    
def name_in(s,l):
    for item in l:
        if item in s:
            return True
    return False

def attack(txt_name):
    #https://github.com/cndiandian/zuanbot.com
    with open(txt_name, "r") as file:
        lines = file.readlines()
    random_line = random.choice(lines).split(".")[1]
    return random_line

def img_recognition(image_path):
    api_url = "https://api.oioweb.cn/api/ocr/recognition"
    with Image.open(image_path) as img:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
    files = {'file': ('image.jpg', img_byte_arr, 'image/jpeg')}
    data = {}
    response = requests.post(api_url, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        output=[]
        for item in result.get('result', []):
            #名称, 置信度, 分类
            output.append([item['name'],item['score'],item['root']])
        return output
    else:
        print('Image recognition failed', response.status_code)
        return -1

def fetch_bilibili_hotlist(index):
    url = "https://api.vvhan.com/api/hotlist/bili"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            hotlist = data['data']
            videos_info=[]
            for item in hotlist[:index]:
                videos_info.append(f"标题：{item['title']}, 热度：{item['hot']}万, 链接：{item['url']}")
            return videos_info
        else:
            print('Bilibili hotlist get failed')
            return None
    else:
        print('Bilibili hotlist get failed', response.status_code)
        return None

def send_moyu_calendar(driver,group_name):
    api_url = "https://api.vvhan.com/api/moyu?type=json"
    response = requests.get(api_url)
    if response.status_code == 200:
        title=response.json()["title"]
        img_url=response.json()["url"]#"https://"+response.json()["url"].split("https://")[2]
        response = requests.get(img_url)
        if response.status_code == 200:
            with open(os.getcwd()+"\\moyu_calendar\\"+title+".jpg", 'wb') as file:
                file.write(response.content)
            send_file(driver,group_name,os.getcwd()+"\\moyu_calendar\\"+title+".jpg")
        else:
            print('Calendar image download failed', response.status_code)
    else:
        print('Calendar image download failed', response.status_code)
'''
def get_last_content(driver, directory="./downloads"):
    time.sleep(2)
    try:
        # 定位到最后一个 <div class="content"> 元素
        last_content_div = driver.find_elements(By.XPATH, '//div[@class="content"]')[-1]

        # 定位到子元素 <div>/<div>/<div>/<pre>，并获取其文本
        text = last_content_div.find_element(By.XPATH, './div/div/div/pre').text

        # 检查文本中是否包含文件下载链接
        if text and "download" in text:
            # 使用BeautifulSoup解析HTML以找到所有<a>标签
            soup = BeautifulSoup(text, 'html.parser')
            for a_tag in soup.find_all('a'):
                if a_tag.get('href') and a_tag.get('download'):
                    # 获取文件下载链接
                    file_url = a_tag['href']
                    # 下载文件
                    downloaded_file = download_file(file_url, directory)
                    if downloaded_file:
                        print(f"File downloaded: {downloaded_file}")
                        # 这里可以添加代码来处理下载的文件，例如发送文件等
                    else:
                        print("Failed to download the file.")
        return text
    except IndexError:
        print("No elements with class 'content' found.")
    except Exception as e:
        print(f"Failed to get text or download file: {e}")
'''
# 创建 EdgeOptions 实例
edge_options = webdriver.EdgeOptions()
'''
edge_options.add_argument("--headless")  # 启用无头模式
edge_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（通常与无头模式一起使用）
'''
# 设置Edge WebDriver的路径
service_chat = Service(executable_path=config_data["driver_path"])

# 初始化WebDriver，使用Edge浏览器，并传入Service对象
driver_chat = webdriver.Edge(service=service_chat,options=edge_options)

# 打开网页
driver_chat.get("https://kimi.moonshot.cn/")

# 解压后的扩展路径
extension_path = config_data["extension_path"]

# 创建 EdgeOptions 实例
edge_options = webdriver.EdgeOptions()
edge_options.add_argument(f'--load-extension={extension_path}')
'''
edge_options.add_argument("--headless")  # 启用无头模式
edge_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（通常与无头模式一起使用）
'''
# 创建 WebDriver 服务实例
service_we = Service(executable_path=config_data["driver_path"])

# 启动浏览器并加载扩展
driver_we = webdriver.Edge(service=service_we, options=edge_options)
driver_we.get('https://wx.qq.com/')
group_name=config_data["group_name"]

time.sleep(5)
timestamp = time.time()
dt_object = datetime.datetime.fromtimestamp(timestamp)
formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
send(driver_we,group_name,formatted_time+"Process start")
send(driver_we,group_name,"阿米诺斯！是谁在召唤劳资？(╯‵□′)╯︵┻━┻")
send_moyu_calendar(driver_we,config_data["group_name"])
last_name=""
last_input_text=""
while True:
    wait = WebDriverWait(driver_chat, 10)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="msh-chatinput-editor"]')))
    input_box = driver_chat.find_element(By.CSS_SELECTOR, '[data-testid="msh-chatinput-editor"]')
    try:
        name,input_text=get_last_content(driver_we)
    except:
        continue
    if(last_name!=name and last_input_text!=input_text):
        timestamp = time.time()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
        print(formatted_time+"User\""+name+"\"reply:"+input_text)
    elif(last_name==name and last_input_text==input_text):
        continue
    last_name=name
    last_input_text=input_text
    if("--cmd" in input_text):
        if(len(input_text.split("--cmd"))==2):
            timestamp = time.time()
            dt_object = datetime.datetime.fromtimestamp(timestamp)
            formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
            try:
                eval(input_text.split("--cmd"))
                print("Execute Command:"+input_text.split("--cmd")[1])
                send(driver_we,group_name,formatted_time+"Execute Command:"+input_text.split("--cmd")[1])
            except Exception as e:
                print("Command\""+input_text+"\"execution error.")
                send(driver_we,group_name,formatted_time+"Command\""+input_text+"\"execution error.")
        else:
            print("The command\""+input_text+"\"is in the wrong format.")
            send(driver_we,group_name,formatted_time+"The command\""+input_text+"\"is in the wrong format.")
    if((input_text is None)or(not("@人机" in input_text))):
        continue
    elif(name_in(name,config_data["attack_names"])and config_data["able_attack"]):
        timestamp = time.time()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
        send(driver_we,group_name,formatted_time+"\""+name+"\""+"is in list attack_names")
        send(driver_we,group_name,"凭你也配使唤劳资？"+name+"(╯‵□′)╯︵┻━┻")
        send(driver_we,group_name,attack(config_data["attack_txt_name"]))
    elif("我是你爸爸，你爸爸是我" ==input_text.split("@人机")[1] and name==config_data["admin_name"]):
        timestamp = time.time()
        dt_object = datetime.datetime.fromtimestamp(timestamp)
        formatted_time = dt_object.strftime("[%Y-%m-%d %H:%M:%S]")
        send(driver_we,group_name,formatted_time+"Admin Name:"+config_data["admin_name"])
        send(driver_we,group_name,formatted_time+"Confirm that the admin status is confirmed.")
        send(driver_we,group_name,formatted_time+"Process exit")
        driver_chat.quit()
        driver_we.quit()
        sys.stdout = sys.__stdout__
        sys.stdin = sys.__stdin__
        exit()
    print("Normal user input")
    input_text=input_text.split("@人机")[1]
    try:
        input_text="[System Prompt]"+config_data["prompt"]+"[Bilibili hotlist]"+str(fetch_bilibili_hotlist(5))+"[User Name]"+name+"[User Input]"+input_text
    except:
        input_text="[System Prompt]"+config_data["prompt"]+"[User Name]"+name+"[User Input]"+input_text
    input_box.send_keys(input_text)
    # 定位按钮，并点击
    button = driver_chat.find_element(By.ID, 'send-button')
    button.click()
    # 增加调试信息
    print("Button clicked, waiting for it to disappear...")
    try:
        time.sleep(5)
        wait = WebDriverWait(driver_chat, 20)
        wait.until(EC.invisibility_of_element_located((By.CSS_SELECTOR, '.MuiButtonBase-root.MuiButton-root.MuiLoadingButton-root')))
        print("Button disappeared.")
        # 首先，使用CSS选择器找到页面上所有的div元素
        div_elements = driver_chat.find_elements(By.CSS_SELECTOR,"div")
        # 然后，使用列表推导式过滤出class属性中包含"markdown"的div元素
        try:
            markdown_divs = [div for div in div_elements if "markdown" in div.get_attribute("class")]
            content=markdown_divs[-1].text
        except Exception as e:
            print("Content is not found.")
            content=str(e)
        try:
            if("--draw" in content):
                if len(content.split("--draw"))==2 :
                    try:
                        description=eval(content.split("--draw")[1])
                        content=content.split("--draw")[0]
                    except:
                        print("draw op error")
                        send(driver_we,group_name,"哈哈，尴尬了……")
                        continue
                else:
                    print("draw op error")
                    send(driver_we,group_name,"哈哈，尴尬了……")
                    continue
                print("description:"+description)
                response = requests.get("https://image.pollinations.ai/prompt/"+description+"?width=16&height=16&seed="+str(random.randint(0,114514))+"&nologo=true")
                if response.status_code == 200:
                    # 将图片内容写入文件
                    with open(os.getcwd()+"\\images\\"+description+".jpg", 'wb') as file:
                        file.write(response.content)
                    print("The download was successful.\nImage name:"+".\\images\\"+description+".jpg")
                    if(content!=""):
                        send(driver_we,group_name,content)
                    send_file(driver_we,group_name,os.getcwd()+"\\images\\"+description+".jpg")
                    continue
                else:
                    print(f"The download failed:{response.status_code}")
                    send(driver_we,group_name,"哈哈，尴尬了……网速不太好，图片丢了ε┬┬﹏┬┬3")
                    continue
            elif("--emoji" in content):
                if len(content.split("--emoji"))==2 :
                    try:
                        key_words=eval(content.split("--emoji")[1])
                        content=content.split("--emoji")[0]
                    except:
                        print("emoji op error")
                        send(driver_we,group_name,"哈哈，尴尬了……我技术不行，搞错了，重来叭")
                        continue
                else:
                    print("emoji op error")
                    send(driver_we,group_name,"哈哈，尴尬了……我技术不行，搞错了，重来叭")
                    continue
                print("key words:"+key_words)
                try:
                    if(content!=""):
                        send(driver_we,group_name,content)
                    send_random_emoji(driver_we,config_data["group_name"],key_words,20)
                    continue
                except Exception as e:
                    if(content!=""):
                        send(driver_we,group_name,content)
                    send(driver_we,group_name,"哈哈，尴尬了……网速不太好，表情包丢了ε┬┬﹏┬┬3")
                    print(f"The emoji send failed:{e}")
                    continue
            print("Output:"+content)
            send(driver_we,group_name,content)
        except Exception as e:
            send(driver_we,group_name,"？！发生神墨O_o??事情了？？？")
            print("Content error.")
    except TimeoutException as e:
        print("TimeoutException occurred:", e)
        try:
            button = driver_chat.find_elements(By.CSS_SELECTOR, '[data-testid="msh-chat-segment-reAnswer"]')
            if button:
                button.click()
                print("Clicked the last button with specified class.")
            else:
                print("No buttons with the specified class found.")
        except Exception as click_exception:
            send(driver_we,group_name,"Kimi不理我，呜呜呜ε┬┬﹏┬┬3")
            print("Exception occurred while trying to click the button:", click_exception)
        # 可以增加更多调试信息，比如页面截图等
        driver_chat.save_screenshot('timeout_exception.png')
        break
