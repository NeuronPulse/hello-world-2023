# hello-world-2023

> 你好，世界。

这是我在2023年写的代码，那一年我10岁。

ChatGPT刚刚爆火，国内大模型生态还是一片荒地。我在卧室的电脑上，用Selenium驱动浏览器，把Kimi AI接进了微信群。除了聊天，我还给它装了各种"工具"——画画、搜表情包、查B站热榜、发摸鱼日历。后来我才知道，这套"指令解析→工具调度"的设计，就是业界后来标准化的Function Calling。

但当时的我并不知道这些。我只是觉得，AI应该能帮我做更多事情。

这个仓库是存档，也是一份纪念。代码很稚嫩，安全漏洞不少，微信网页版也早已关停。但它记录了一个孩子第一次对"创造"这件事感到兴奋的样子。

Hello World, 2023. 一切从这里开始。

---

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                      微信网页版 (wx.qq.com)                    │
│                  wechat-need-web 扩展绕过限制                   │
└──────────────────────────┬──────────────────────────────────┘
                           │ Selenium 驱动
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                       main-kimi.py                           │
│                                                             │
│   ┌──────────┐    ┌──────────┐    ┌──────────────────────┐  │
│   │ 消息监听  │───▶│ 指令解析  │───▶│     工具调度器        │  │
│   │ get_last  │    │ 关键词匹配 │    │  --draw / --emoji    │  │
│   └──────────┘    └──────────┘    └──────────┬───────────┘  │
│                                              │              │
│                           ┌──────────────────┼──────────┐   │
│                           ▼                  ▼          ▼   │
│                    ┌──────────┐       ┌──────────┐ ┌──────┐ │
│                    │ Pollin.  │       │ 表情包API │ │B站热榜│ │
│                    │ AI绘画   │       │ 搜索发送  │ │API   │ │
│                    └──────────┘       └──────────┘ └──────┘ │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                      Kimi AI (kimi.moonshot.cn)              │
│                Selenium 自动化操作浏览器交互                    │
└─────────────────────────────────────────────────────────────┘
```

## 核心流程

1. **双浏览器实例**：一个打开 Kimi AI 页面，一个打开微信网页版
2. **消息轮询**：`get_last_content()` 不断读取微信群最新消息
3. **指令解析**：消息包含 `@人机` 时触发，解析用户意图
4. **工具调用**：Kimi 返回带特殊标记的响应，本地解析并执行：
   - `--draw "描述"` → 调用 Pollinations AI 生成图片并发送
   - `--emoji "关键词"` → 从表情包API随机获取并发送
5. **回复发送**：通过 Selenium 操作微信输入框完成消息投递

## 工具集

| 工具 | 功能 | 实现方式 |
|------|------|----------|
| AI 绘画 | 文字描述生成图片 | Pollinations AI API |
| 表情包搜索 | 关键词随机表情包 | doutu.lccyy.com API |
| B站热榜 | 获取热搜前N条 | vvhan.com API |
| 摸鱼日历 | 每日摸鱼图片 | vvhan.com API |
| OCR 识别 | 图片文字识别 | oioweb.cn API |
| 攻击语录 | 随机嘲讽回复 | 本地文本文件 |

## 文件结构

```
WeChat_bot_kimi/
├── main-kimi.py              # 主程序
├── chat_config.json          # 配置文件（群名、路径、Prompt等）
├── msedgedriver.exe          # Edge WebDriver
├── attack_no_emoji🔫.txt      # 攻击语录（无emoji版）
├── attack_emoji🔫.txt         # 攻击语录（emoji版）
├── dabian💩.txt               # 语料文件
├── images/                   # AI生成图片存放
├── doutu/                    # 表情包存放
├── moyu_calendar/            # 摸鱼日历存放
├── 素材/                     # 其他素材
└── wechat-need-web v1.1.1/   # 浏览器扩展（绕过微信网页版限制）
```

## 配置说明

`chat_config.json`：

```json
{
  "group_name": "群聊名称",
  "driver_path": "msedgedriver.exe 路径",
  "extension_path": "wechat-need-web 扩展路径",
  "prompt": "Kimi 的系统提示词",
  "log_name": "日志文件名",
  "admin_name": "管理员昵称",
  "attack_names": ["需要攻击的用户"],
  "able_attack": 1,
  "attack_txt_name": "attack_no_emoji🔫.txt"
}
```

## 运行

```bash
pip install selenium Pillow requests
python main-kimi.py
```

> ⚠️ 微信网页版已关停，此项目仅供存档纪念，无法实际运行。

## 技术栈

- Python 3
- Selenium WebDriver (Edge)
- Pillow (图片处理)
- Requests (HTTP 请求)
- Kimi AI (moonshot.cn)
- wechat-need-web (浏览器扩展)

## License

[MIT](LICENSE)
