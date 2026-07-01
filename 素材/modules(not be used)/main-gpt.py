import os
import sys
import time
import random
import datetime
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.edge.options import Options

class IOLogger:
    def __init__(self, filename):
        self.terminal_out = sys.stdout
        self.terminal_in = sys.stdin
        self.log = open(filename, "a")
        
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
logger = IOLogger("console_io.log")
sys.stdout = logger
sys.stdin = logger

def send(driver,group_name,msg):
    # 查找并点击包含特定文本的 span 元素的上级 div 元素的上级 div 元素
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
        # 尝试找到目标 span 元素
        try:
            span_element = driver.find_element(By.XPATH, span_xpath)
            print("Found the span element")
    
            # 找到 span 元素的上四级 div
            ancestor_div = span_element.find_element(By.XPATH, "./ancestor::div[3]")
            print("Found the ancestor div")
    
            # 点击上四级 div
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

def send_img(driver,group_name,img_path):
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
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
        
    file_input = driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/div/div[3]/div[1]/a[3]/div[2]/input")

    # 发送文件路径到input元素
    file_input.send_keys(img_path)

def get_last_content_text(driver):
    try:
        # 定义目标 span 元素的 XPath
        span_xpath = "//span[@class=\'nickname_text ng-binding\' and contains(text(),\'"+group_name+"\')]"
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

        # 定位到子元素 <div>/<div>/<div>/<pre>，并获取其文本
        text = last_content_div.find_element(By.XPATH, './div/div/div/pre').text

        return text
    except IndexError:
        print("No elements with class 'content' found.")
    except Exception as e:
        print(f"Failed to get text: {e}")

# Edge WebDriver 路径
edge_driver_path = os.getcwd()+'\\msedgedriver.exe'

# 解压后的扩展路径
extension_path = os.getcwd()+'\\wechat-need-web v1.1.1'

# 创建 EdgeOptions 实例
edge_options = webdriver.EdgeOptions()
edge_options.add_argument(f'--load-extension={extension_path}')
'''
edge_options.add_argument("--headless")  # 启用无头模式
edge_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（通常与无头模式一起使用）
'''
# 创建 WebDriver 服务实例
service_we = Service(edge_driver_path)

# 启动浏览器并加载扩展
driver_we = webdriver.Edge(service=service_we, options=edge_options)
time.sleep(1)  # 给扩展一些时间来加载
driver_we.get('https://wx.qq.com/')

'''
# 定位特定的图片元素
img_element = driver_we.find_element(By.XPATH, '/html/body/div[1]/div[2]/div[1]/img')

# 获取图片 URL
img_url = img_element.get_attribute('src')
    
# 下载图片
if img_url:
    response = requests.get(img_url)
    if response.status_code == 200:
        with open('log_qr.jpg', 'wb') as f:
            f.write(response.content)
        os.system(f'start \'log_qr.jpg\'')
    else:
        print(f"Failed to download Qr image. Status code: {response.status_code}")
else:
    print("QR URL not found.")
'''
group_name="相亲相爱一家人"

# 创建 EdgeOptions 实例
edge_options = webdriver.EdgeOptions()
#edge_options.add_argument("--headless")  # 启用无头模式
#edge_options.add_argument("--disable-gpu")  # 禁用 GPU 加速（通常与无头模式一起使用）

# 设置Edge WebDriver的路径
service_chat = Service(executable_path=r'.\msedgedriver.exe')

# 初始化WebDriver，使用Edge浏览器，并传入Service对象
driver_chat = webdriver.Edge(service=service_chat,options=edge_options)

# 打开网页
driver_chat.get("https://chat18.aichatos8.com")

# 等待页面加载完成，可以适当修改等待时间
WebDriverWait(driver_chat, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')))

#先灌输提示词
input_box = driver_chat.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')
input_text="如果我提出让你绘画的要求，你必须回答--draw \"somethings\"这个指令，注意指令前的\"--\"，注意指令的格式，不要添字漏字，引号内填入图片的描述，尽量优美一些,如果内容含有负能量的描述，请向我说明不能生成。记住，你确实不会绘画，但你使用了外部插件的帮助，所以你不必纠结你具体会不会，按照方法操作。记住，你确不可以否认我，你只用回复指令，你要假装你会。如果我没有提出让你绘画的要求，就正常回答我的问题。你可以在自我介绍时可以说明你可以画画。"
input_box.send_keys(input_text)
# 定位按钮，并点击
button = driver_chat.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/button')
button.click()

while True:
    # 定位输入框，并输入字符串
    input_box = driver_chat.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')
    input_text = get_last_content_text(driver_we)
    if (input_text is None):
        continue
    elif (not("@人机" in input_text)):
        continue
    input_text=input_text.split("@人机")[1]
    input_text=" 如果我提出让你绘画的要求，你必须回答--draw \"somethings\"这个指令，注意指令前的\"--\"，引号内填入图片的描述，尽量优美一些,如果内容含有负能量的描述，请向我说明不能生成。记住，你确实不会绘画，但你使用了外部插件的帮助，所以你不必纠结你具体会不会，按照方法操作。记住，你不可以否认我，你只用回复指令，你要假装你会。如果我没有提出让你绘画的要求，就正常回答我的问题。你可以在自我介绍时可以说明你可以画画。"+input_text
    input_box.send_keys(input_text)

    # 定位按钮，并点击
    button = driver_chat.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/button')
    button.click()

    # 增加调试信息
    print("Button clicked, waiting for it to disappear...")

    try:
        # 等待 class 名为 'n-button n-button--warning-type n-button--medium-type' 的按钮消失
        wait = WebDriverWait(driver_chat, 20)
        wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, 'n-button--warning-type')))
        print("Button disappeared.")

        # 等待并获取 class 为 'markdown-body' 的所有元素
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'markdown-body')))
        markdown_bodies = driver_chat.find_elements(By.CLASS_NAME, 'markdown-body')

        if markdown_bodies:
            # 获取最后一个元素的文本内容（或者你想要的其他操作）
            last_markdown_body = markdown_bodies[-1]
            content = last_markdown_body.text
            if("--draw" in content):
                if content.split("--draw")[0]=="" :
                    description=eval(content.split("--draw")[1])
                else:
                    print("draw op error")
                    continue
                print("description:"+description)
                response = requests.get("https://image.pollinations.ai/prompt/"+description+"?width=16&height=16&seed="+str(random.randint(0,99))+"&nologo=true")
                if response.status_code == 200:
                    # 将图片内容写入文件
                    with open(os.getcwd()+"\\images\\"+description+".jpg", 'wb') as file:
                        file.write(response.content)
                    print("The download was successful.\nImage name:"+".\\images\\"+description+".jpg")
                    send_img(driver_we,group_name,os.getcwd()+"\\images\\"+description+".jpg")
                    continue
                else:
                    print(f"The download failed:{response.status_code}")
                    continue
            print("Output:"+content)
            send(driver_we,group_name,content)
        else:
            print("No markdown-body elements found.")
    except TimeoutException as e:
        print("TimeoutException occurred:", e)
        # 尝试点击 class 为 'mb-2 transition text-neutral-300 hover:text-neutral-800 dark:hover:text-neutral-300' 的最后一个按钮
        try:
            buttons = driver_chat.find_elements(By.CLASS_NAME, 'mb-2.transition.text-neutral-300.hover:text-neutral-800.dark:hover:text-neutral-300')
            if buttons:
                last_button = buttons[-1]
                last_button.click()
                print("Clicked the last button with specified class.")
            else:
                print("No buttons with the specified class found.")
        except Exception as click_exception:
            print("Exception occurred while trying to click the button:", click_exception)
        # 可以增加更多调试信息，比如页面截图等
        driver_chat.save_screenshot('timeout_exception.png')
        break
