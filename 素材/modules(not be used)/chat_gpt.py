import sys
import time
import datetime
import requests
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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

# 设置Edge WebDriver的路径
service_chat = Service(executable_path=r'.\msedgedriver.exe')

# 初始化WebDriver，使用Edge浏览器，并传入Service对象
driver_chat = webdriver.Edge(service=service_chat)

# 打开网页
driver_chat.get("https://chat18.aichatos8.com")

# 等待页面加载完成，可以适当修改等待时间
WebDriverWait(driver_chat, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')))

while True:
    # 定位输入框，并输入字符串
    input_box = driver_chat.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/div/div/div/div/div/div/footer/div/div[3]/div/div[1]/div[1]/textarea')
    input_text = input("Input:")
    input_text=" [系统提示]如果用户提出让你绘画的要求，你不用回答任何话，只用说--draw \"somethings\"，引号内填入图片的描述，尽量优美一些,如果内容含有负能量的描述，请向用户说明不能生成。如果用户没有提出让你绘画的要求，就正常回答用户的问题[User Input]"+input_text
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
                description=eval(content.split("--draw")[1])
                response = requests.get("https://image.pollinations.ai/prompt/"+description+"?width=16&height=16&seed="+str(random.randint(0,99))+"&nologo=true")
                if response.status_code == 200:
                    # 将图片内容写入文件
                    with open(".\\images\\"+description+".jpg", 'wb') as file:
                        file.write(response.content)
                    print("The download was successful.\nImage name:"+".\\images\\"+description+".jpg")
                else:
                    print(f"The download failed:{response.status_code}")
            print("Output:"+content)
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

# 关闭WebDriver
driver_chat.quit()
sys.stdout = sys.__stdout__
sys.stdin = sys.__stdin__

'''
[系统提示]如果用户提出让你绘画的要求，你不用回答任何话，只用说--draw \"somethings\"，引号内填入图片的描述，尽量优美一些,如果内容含有负能量的描述，请向用户说明不能生成。如果用户没有提出让你绘画的要求，就正常回答
[用户输入]你会话小狗吗
'''

