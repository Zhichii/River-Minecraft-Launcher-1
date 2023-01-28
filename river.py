import os # 导入Windows模块
import time # 导入时间模块
import sys # 导入系统模块
import zipfile # 导入压缩模块
import subprocess # 导入子进程模块
try: # 为防止用户未安装模块导致导入错误, 尝试导入
    import requests # 导入网络访问模块
except: # 发现错误
    print("Downloading necessary libraries! 正在下载必要的库! 1") # 输出安装信息
    subprocess.getstatusoutput(sys.executable + " -m pip install requests -i https://pypi.doubanio.com/simple/") # 调用子进程安装requests
    import requests # 导入网络访问模块
try: # 为防止用户未安装模块导致导入错误, 尝试导入
    import pyglet # 导入pyglet模块
except: # 发现错误
    print("Downloading necessary libraries! 正在下载必要的库! 2") # 输出安装信息
    subprocess.getstatusoutput(sys.executable + " -m pip install pyglet -i https://pypi.doubanio.com/simple/") # 调用紫禁城安装pyglet
    import pyglet # 导入pyglet模块
import threading as thread # 导入多线程模块并重命名成thread
import hashlib # 导入哈希模块
import json # 导入json模块
from tkinter import * # 从tkinter模块导入所有子
from tkinter import ttk # 从tkinter模块导入ttk模块
from tkinter import PhotoImage # 从tkinter模块导入PhotoImage
import shutil # 导入工具模块
def writeLog(logger, content): # 定义写日志函数, 参数: 调用者, 日志内容
    writeContent = "["+str(time.time())[:13]+", "+logger[0].capitalize()+logger[1:]+"] "+content[0].capitalize()+content[1:] # 构造日志内容
    print(writeContent) # 输出日志
    log.write(writeContent+"\n") # 写入日志文件
    log.flush() # 保存日志文件
#import river_json as rvj

log = open(".river_log.txt", "w") # 打开日志文件
webCache = {} # 定义网络缓存
helpToProtect = 0 # 定义是否显示警告
noJava = 0 # 定义是否要安装Java
noUpdate = 0 # 定义是否要更新启动器
darkMode = subprocess.getoutput("reg QUERY HKCU\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Themes\\Personalize /v AppsUseLightTheme")[-2] == "0" # 获取系统深浅色模式

def chTheme(rt): # 定义刷新颜色函数, 参数: 父控件
    try: # 为防止父控件没有背景色或前景色属性, 尝试更改颜色
        if (darkMode): # 如果当前主题是深色模式
            rt.config(background="#202020") # 设置背景色
            rt.config(foreground="white") # 设置前景色
        else: # 如果当前主题不是深色模式
            rt.config(background="#f0f0f0") # 设置前景色
            rt.config(foreground="black") # 设置背景色
    except: # 发现错误
        pass # 占位
    for i in rt.winfo_children(): # 遍历子控件
        if (type(i) == Frame): # 如果子控件类型是框架
            chTheme(i) # 遍历该子控件的子控件
        elif (type(i) == ttk.Entry): # 如果控件类型是输入框
            continue # 不更改颜色
        else: # 如果控件类型不是输入框也不是框架
            try: # 为防止子控件没有背景色或前景色属性, 尝试更改颜色
                if (darkMode): # 如果当前主题是深色模式
                    i.config(background="#202020") # 设置背景色
                else: # 如果当前主题不是深色模式
                    i.config(background="#f0f0f0") # 设置背景色
                try: # 为防止控件没有对齐方式属性
                    if (i.config("image")[4] != ""): # 如果控件含有图片
                        if (CENTER in str(i.config("compound")[4])): # 如果图片是在
                            continue # 跳过更改前景色
                except: # 发现错误
                    pass # 占位
                if (darkMode): # 如果当前主题是深色模式
                    i.config(foreground="white") # 更改前景色
                else: # 如果当前主题不是深色模式
                    i.config(foreground="black") # 更改前景色
            except: # 发现错误
                pass # 占位

def reTheme(event): # 定义更改主题函数, 参数: 鼠标点击事件
    global themeButton # 使全局变量主题按钮可以更改
    global darkMode # 使全局变量主题可以更改
    darkMode = not darkMode # 更改主题
    img = offImage # 设置图片为关闭图标
    if (darkMode): img = onImage # 如果当前主题是深色模式, 设置图片为开启图标
    themeButton.config(image = img) # 更改主题按钮
    chTheme(root) # 刷新主窗口颜色
    chTheme(dynamicCur) # 刷新动态区域颜色
    try: # 为防止没有对话框弹出, 尝试刷新对话框颜色
        chTheme(dialogCur) # 刷新对话框颜色
    except: # 发现错误
        pass # 占位

global messages # 使消息列表变成全局变量
messages = [] # 定义消息列表
def myMessage(level, message): # 定义显示消息函数, 参数: 消息等级, 消息内容
    """level: 0-low 1-normal 2-warn 3-dangerous""" # 设置函数提示信息
    messages.append([level, time.time(), message]) # 添加到消息列表

def judge(state, command): # 定义判断函数, 参数: 条件, 命令
    if (state): # 如果条件成立
        command() # 执行命令
        pass # 占位

pyglet.font.add_file("assets\\font.ttf") # 使用pyglet加载字体
pyglet.font.load("Unifont")
theFont = ("Unifont", 10) # 设置字体

def myButton(master, textvariable=None, text="", command=""): # 定义按钮函数, 参数: 父控件, 可变文字, 静态文字, 命令
    buttonImage = PhotoImage(master=master, file="assets\\control\\button.png") # 定义按钮图片
    buttonImageActive = PhotoImage(master=master, file="assets\\control\\buttonActive.png") # 定义按钮激活图片
    if (textvariable != None): # 如果可变文字不是空的
        x = ttk.Label(master, textvariable=textvariable, image=buttonImage, compound=CENTER, foreground="white", font=theFont) # 设置控件, 参数: 父控件, 可变文字, 图片, 图文共存方式, 前景色, 字体
    else: # 如果可变文字是空的
        x = ttk.Label(master, text=text, image=buttonImage, compound=CENTER, foreground="white", font=theFont) # 设置控件, 参数: 父控件, 静态文字, 图片, 图文共存方式, 前景色, 字体
    x.bind("<Button-1>", lambda event: judge(not("disabled" in str(x.config("state")[4])), command)) # 绑定左键
    x.bind("<Enter>", lambda event: x.config(image=buttonImageActive)) # 绑定移入控件
    x.bind("<Leave>", lambda event: x.config(image=buttonImage)) # 绑定移出控件
    return x # 返回控件

def myTab(master, textvariable=None, command=""): # 定义标签页函数, 参数: 父控件, 可变文字, 命令
    tabImage = PhotoImage(master=master, file="assets\\control\\tab.png") # 定义标签页图片
    tabImageActive = PhotoImage(master=master, file="assets\\control\\tabActive.png") # 定义标签页激活图片
    x = ttk.Label(master, textvariable=textvariable, image=tabImage, compound=CENTER, foreground="white", font=theFont) # 设置控件, 参数: 父控件, 可变文字, 图片, 图文共存方式, 前景色
    x.bind("<Button-1>", lambda event: judge(not("disabled" in str(x.config("state")[4])), command)) # 绑定左键
    x.bind("<Enter>", lambda event: x.config(image=tabImageActive)) # 绑定移入控件
    x.bind("<Leave>", lambda event: x.config(image=tabImage)) # 绑定移出控件
    return x # 返回控件

def myTabY(master, text="", command=""): # 定义垂直标签页函数, 参数: 父控件, 静态文字, 命令
    tabYImage = PhotoImage(master=master, file="assets\\control\\tabY.png") # 定义垂直标签页图片
    tabYImageActive = PhotoImage(master=master, file="assets\\control\\tabYActive.png") # 定义处置标签页激活图片
    x = ttk.Label(master, text=text, image=tabYImage, compound=CENTER, foreground="white", font=theFont) # 设置控件
    x.bind("<Button-1>", lambda event: judge(not("disabled" in str(x.config("state")[4])), command)) # 绑定左键
    x.bind("<Enter>", lambda event: x.config(image=tabYImageActive)) # 绑定移入控件
    x.bind("<Leave>", lambda event: x.config(image=tabYImage)) # 绑定移出控件
    return x # 返回控件

def myPass(*kw): # 定义占位函数
    pass # 占位

class myList: # 定义列表类
    def update(this): # 定义更新函数
        tmp = this.contains # 将临时变量设置为当前列表所储存控件个数, 即长度
        for i in this.owned: # 遍历当前已有的控件
            i[2].grid_forget() # 隐藏控件
        if (this.offset < 0): # 假如偏移是负数
            this.offset = 0 # 将偏移修正为0
        for i in range(this.offset, this.offset+10): # 遍历渲染范围内的控件
            if (i >= tmp): # 如果遍历控件超过了列表最大长度
                break # 停止遍历
            this.owned[i][2].grid() # 显示控件
            if (i == this.select): # 如果控件被选中
                this.owned[i][2].config(background="#18572a") # 设置背景色
                this.owned[i][2].config(foreground="white") # 设置前景色
            else: # 如果控件没有选中
                if (darkMode): # 如果当前主题是深色模式
                    this.owned[i][2].config(background="#202020") # 设置背景色
                    this.owned[i][2].config(foreground="white") # 设置前景色
                else: # 如果当前主题不是深色模式
                    this.owned[i][2].config(background="#f0f0f0") # 设置背景色
                    this.owned[i][2].config(foreground="black") # 设置前景色
        pre = (this.offset+10)/this.contains # 计算滚动条终点比例
        if (pre >= 1.0): pre = 1.0 # 如果滚动条终点超过了高度, 设置为高度
        this.scroll(this.offset/this.contains, pre) # 让滚动条滚动
    def __init__(this, master, height=100, width=75, yscrollcommand=myPass, itemHeight=1): # 定义初始化函数, 参数: 父控件, 高度, 宽度, Y轴滚动命令
        this.offset = 0 # 设置偏移
        this.select = -1 # 设置被选中
        this.contains = 0 # 设置当前列表所储存控件个数, 即长度
        this.master = master # 设置父控件
        this.enabled = 1 # 设置是否激活
        this.size = (height, width) # 设置大小
        this.owned = [] # 设置已有的控件
        this.scroll = yscrollcommand # 设置滚动命令
        this.itemHeight = itemHeight
        this.frame = Frame(master, height=height, width=width, highlightbackground="black", highlightthickness=2) # 设置框架, 参数: 父控件, 高度, 宽度, 边框色, 边框宽度
    def activate(this, item): # 定义激活函数, 参数: 选项
        this.select = item # 选择该选项
        if ( (item > this.offset+10) or # 如果选项超过了渲染区域或者
             (item < this.offset)): #  选项在渲染区域前面
            this.yview("moveto", item) # 滚动到该选项
        this.update() # 更新
    def add(this, text, image=None, compound=LEFT): # 定义添加函数, 参数: 静态文字, 图片, 图文共存方式
        this.select = 0 # 选择第0个选项
        this.contains += 1 # 将当前列表所储存的控件个数, 即长度加1
        while (text.count("\n")+1 < this.itemHeight):
            writeLog("myList -> add", "text: " + text + "; this.itemHeight: " + str(this.itemHeight))
            text += "\n"
        x = ttk.Label(this.frame, text=text, image=image, compound=compound, width=this.size[1], font=theFont, borderwidth=5, relief=RAISED) # 设置控件, 参数: 父控件静态文字, 图片, 图文共存方式, 宽度, 字体, 边框宽度, 边框样式
        x.bind("<MouseWheel>", lambda event: this.yview("scroll", ((event.delta<0)*2-1)*5)) # 绑定滚轮
        x.bind("<Button-1>", lambda event, cnt=this.contains-1: judge(this.enabled, lambda: (this.activate(cnt)))) # 绑定左键
        x.bind("<Enter>", lambda event: judge(this.enabled, (lambda cnt=this.contains-1: x.config(background="#19a842"))), ()) # 绑定移入控件
        x.bind("<Leave>", lambda event, cnt=this.contains-1: (x.config(background="#f0f0f0"), this.update())) # 绑定移出控件
        this.owned.append((text, image, x)) # 添加控件
        this.update() # 更新
    def bind(this, key, command): # 定义绑定函数, 参数: 绑定按键, 命令
        this.frame.bind(key, command) # 绑定到框架
        for i in range(this.contains): # 遍历已有控件
            if ("<Button-" in key): # 如果绑定按键是鼠标按键
                cmd = lambda event, tmp=i: (this.activate(tmp), command(event)) # 将命令改为先激活该控件再执行命令
            this.owned[i][2].bind(key, cmd) # 绑定到控件
    def index(this, pass_): # 定义索引函数, 参数: 占位
        return this.select # 返回当前选择
    def get(this, pass_): # 定义获取函数, 参数: 占位
        return this.owned[this.select][0] # 返回当前选择控件字符串
    def getImage(this, pass_): # 定义获取图片函数, 参数: 占位
        return this.owned[this.select][1] # 返回当前选择控件图片
    def grid(this, column=-1, row=-1): # 定义格子化函数, 参数: 列, 行
        if (column == -1): # 如果列是-1
            if (row == -1): # 如果行是-1
                this.frame.grid() # 格子化
            else: # 如果行不是-1
                this.frame.grid(row=row) # 格子化
        else: # 如果列不是-1
            if (row == -1): # 如果行是-1
                this.frame.grid(column=column) # 格子化
            else: # 如果行不是-1
                this.frame.grid(column=column, row=row) # 格子化
    def pack(this, cnf={}, **kw): # 定义封装函数
        this.frame.tk.call( # 调用Tkinter
              ('pack', 'configure', this.frame._w) # 配置封装
              + this.frame._options(cnf, kw)) # 参数
    def config(this, state=ACTIVE): # 定义配置函数, 参数: 状态
        this.enabled = state == ACTIVE # 设置激活状态
        if not (this.enabled): # 如果没有激活
            this.select = -1 # 选择-1
            this.update() # 更新
    def yview(this, command, *kw): # 定义Y轴滚动函数, 参数
        if (command == "scroll"): # 如果命令是滚动
            pre = this.offset + int(kw[0]) # 计算滚动偏移
            if (pre <= 0): pre = 0 # 如果滚动偏移小于0, 将滚动偏移改为0
            if (pre > (this.contains-10)): # 如果滚动偏移大于最大偏移
                pre = this.contains - 10 # 将滚动偏移改为最大偏移
            this.offset = pre # 将偏移改为滚动后偏移
        if (command == "moveto"): # 如果命令是移动到
            pre = this.contains - 10 # 设置默认值
            if ( (float(kw[0])*this.contains) < (this.contains-10)): # 如果计算出来的移动偏移
                pre = float(kw[0])*this.contains
            if (pre <= 0): pre = 0
            this.offset = int(pre)
        this.update()

root = Tk("river", "river", " River L... 这是一个彩蛋! 在这的文字会因长度不够被省略掉而隐藏! ")
root.iconbitmap("assets\\title\\icon.ico")
root.geometry("880x540+150+25")
releaseImage = PhotoImage(master=root, file="assets\\icon\\release.png")
snapshotImage = PhotoImage(master=root, file="assets\\icon\\snapshot.png")
oldImage = PhotoImage(master=root, file="assets\\icon\\old.png")
fabricImage = PhotoImage(master=root, file="assets\\icon\\fabric.png")
optifineImage = PhotoImage(master=root, file="assets\\icon\\optifine.png")
onImage = PhotoImage(master=root, file="assets\\icon\\on.png")
offImage = PhotoImage(master=root, file="assets\\icon\\off.png")

true = True
false = False
null = None
curBuild = 14
builds = {1: "v0.1", 2: "v0.2", 3: "v0.3", 4: "v0.4", 5: "v0.5", 6: "v0.6", 7: "v0.7", 8: "v0.8.0", 9: "v0.8.1", 10: "v0.9", 11: "v0.9.1", 12: "v0.10", 13: "v0.10.1", 14: "v0.10.2"}


def makeDir(dirName):
    if (not os.path.isdir(dirName)):
        os.makedirs(dirName, mode = 755)

def testHash(byte, sha1):
    return hashlib.sha1(byte).hexdigest() == sha1

def sp(string, a, b):
    x = string[string.find(a)+len(a):]
    x = x[:x.find(b)]
    return x

def switchLang(langName):
    global lang
    cfg["lang"] = langName
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()
    targetLang = eval(open("assets\\lang\\" + langName + ".py", encoding="utf-8").read())
    for i in targetLang:
        if (type(targetLang[i]) == str):
            lang[i].set(targetLang[i])
        else:
            lang[i] = targetLang[i]
    try:
        settings["info"]["value"] = lang["sets.info.value"].get().replace("%1", builds[curBuild])
    except:
        pass
    finally:
        cfg["settings"]["info"]["value"] = lang["sets.info.value"].get().replace("%1", builds[curBuild])
    root.title(lang["title.main"].get())

if (".river_cfg.json" in os.listdir()):
    config = open(".river_cfg.json")
    read = config.read()
    config.close()
    os.remove(".river_cfg.json")
    config = open(".river_cfg.py", "w")
    config.write(read)
    config.close()
    writeLog("main", "migrated from .river_cfg.json to .river_cfg.py! ")

def get(url, saveIn = None, saveAs = None, hashHex = None, headers={}, data={}, params={}):
    writeLog("get", "web: "+url)
    got = None
    if (url in webCache):
        tmp = webCache[url]
        if ( (time.time()-tmp["time"]) < 300):
            got = tmp["content"]
            writeLog("url getting", "using web temp: "+url+"; time: "+str(tmp["time"]))
    if (saveAs is None):
        if (saveIn is None):
            filePath = ""
        else:
            filePath = saveIn + "\\" + os.path.split(url)[1]
    else:
        if (saveIn is None):
            filePath = saveAs
        else:
            filePath = saveIn + "\\" + saveAs
    if (os.path.isfile(filePath)):
        file = open(filePath, "rb")
        if (hashHex != None):
            if (hashlib.sha1(file.read()).hexdigest() == hashHex):
                got = file.read()
    if (got is None):
        try:
            got = requests.get(url, headers=headers, data=data, params=params).content
            webCache[url] = {"time": time.time(), "content": got}
        except requests.exceptions.ConnectionError as err:
            writeLog("get", "failed to get: " + url + "; error: " + str(err))
            got = b""
    if not (os.path.isfile(filePath)):
        if (filePath != ""):
            file = open(filePath, "wb")
            file.write(got)
            file.close()
    try:
        got = got.decode("utf-8")
    except:
        pass
    writeLog("get", "finish")
    return got

global per
per = 0
def getPer(url, saveIn = None, saveAs = None, hashHex = None):
    global per
    per += 1
    return get(url, saveIn, saveAs, hashHex)

global downloadButtonLocked
downloadButtonLocked = 0
makeDir(".minecraft")
makeDir(".minecraft\\versions")
makeDir(".minecraft\\assets")
makeDir(".minecraft\\libraries")
makeDir(".minecraft\\assets\\indexes")
makeDir(".minecraft\\assets\\objects")
makeDir(".minecraft\\mods")
if (".river_tmp" in os.listdir()):
    os.system("del .river_tmp /s /f /q")
else:
    makeDir(".river_tmp")

lang = {}
defaultLang = "zh_cn"
targetLang = eval(open("assets\\lang\\"+defaultLang+".py", encoding="utf-8").read())
for i in targetLang:
    if (type(targetLang[i]) == str):
        lang[i] = StringVar(value=targetLang[i])
    else:
        lang[i] = targetLang[i]
defaultCfg = {"java": 0, "lang": defaultLang, "version": curBuild, "latest": "", "accounts": [], "selectedAccount": 0, "settings": {"resolutionWidth": {"value": 1618, "type": "int"}, "resolutionHeight": {"value": 1000, "type": "int"}, "startupPage": {"value": "launch", "type": "page"}, "info": {"value": lang["sets.info.value"].get().replace("%1", builds[curBuild]), "type": "static"}}, "THANKS_FOR": {"Python": "source support", "Tkinter & Ttk": "GUI support", "Minecraft":"game to launch", "PCL & HMCL":"launch bat refrence", "HlHill":"write source code"}}
def setLatestMinecraft():
    versions = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    try:
        defaultCfg["latest"] = eval(versions)["versions"][0]["id"]
    except:
        writeLog("default config", "failed to get the latest version")

thread._start_new_thread(setLatestMinecraft, ())
if (not os.path.isfile(".river_cfg.py")):
    config = open(".river_cfg.py", "w")
    config.write(str(defaultCfg))
    config.close()
    helpToProtect = 1
config = open(".river_cfg.py", "r")
try:
    cfg = eval(config.read())
except:
    cfg = defaultCfg
    x = open(".river_cfg.py", "w")
    x.write(str(cfg))
    x.close()
    config = open(".river_cfg.py", "r")
if (type(cfg["accounts"]) == dict):
    cfg["accounts"] = list(cfg["accounts"].values())
    x = open(".river_cfg.py", "w")
    x.write(str(cfg))
    x.close()
    config = open(".river_cfg.py", "r")
config.close()
cfg["THANKS_FOR"] = defaultCfg["THANKS_FOR"]
for i in defaultCfg:
    if not (i in cfg):
        cfg[i] = defaultCfg[i]
        helpToProtect = 1
x = list(defaultCfg["settings"].keys())
for i in x:
    if not (i in cfg["settings"]):
        cfg["settings"][i] = defaultCfg["settings"][i]
        helpToProtect = 1
x = list(cfg["settings"].keys())
for i in x:
    if not (i in defaultCfg["settings"]):
        cfg["settings"].pop(i)
        helpToProtect = 1
try:
    switchLang(cfg["lang"])
except FileNotFoundError:
    switchLang(defaultLang)
cfg["settings"]["info"]["value"] = lang["sets.info.value"].get().replace("%1", builds[curBuild])
selectedAccount = cfg["selectedAccount"]
settings = cfg["settings"]
accounts = cfg["accounts"]
if (time.localtime().tm_mon == 12):
    if (time.localtime().tm_mday >= 30):
        writeLog("HlHill", "good bye old year! ")
elif (time.localtime().tm_mon == 1):
    if (time.localtime().tm_mday <= 2):
        writeLog("HlHill", "happy new year! ")

def downloadJava():
    import platform
    sys = platform.system()
    try:
        writeLog("Java downloader", "downloading Java")
        if (sys == "Windows"):
            get("https://download.java.net/openjdk/jdk8u42/ri/openjdk-8u42-b03-windows-i586-14_jul_2022.zip", saveAs="javaA.zip", saveIn=".river_tmp")
            get("https://download.java.net/openjdk/jdk17/ri/openjdk-17+35_windows-x64_bin.zip", saveAs="javaB.zip", saveIn=".river_tmp")
        elif ( (sys == "Linux") or
             (sys == "Darwin")):
            get("https://download.java.net/openjdk/jdk8u42/ri/openjdk-8u42-b03-linux-x64-14_jul_2022.tar.gz", saveAs="javaA.zip", saveIn=".river_tmp")
            get("https://download.java.net/openjdk/jdk17/ri/openjdk-17+35_linux-x64_bin.tar.gz", saveAs="javaB.zip", saveIn=".river_tmp")
        else:
            writeLog("Java downloader", "unknown system: " + sys + "; default to linux")
        zipFileA = zipfile.ZipFile(".river_tmp\\javaA.zip")
        zipFileB = zipfile.ZipFile(".river_tmp\\javaB.zip")
        writeLog("Java downloader", "extracting Java")
        zipFileA.extractall("assets\\java")
        zipFileB.extractall("assets\\java")
        if ("A" in os.listdir("assets\\java")):
            shutil.rmtree("assets\\java\\A")
        if ("B" in os.listdir("assets\\java")):
            shutil.rmtree("assets\\java\\B")
        os.rename("assets\\java\\java-se-8u42-ri", "assets\\java\\A")
        os.rename("assets\\java\\jdk-17", "assets\\java\\B")
        writeLog("Java downloader", "Java download finished")
    except:
        writeLog("Java downloader", "failed to download Java")

def launchInstance(versionId):
    if (accounts == []):
        global dialogCur
        dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
        try:
            dialogCur.destroy()
        except:
            pass
        dialogCur = dialog
        dialog.iconbitmap("assets\\title\\icon.ico")
        dialog.focus_force()
        dialog.resizable(0, 0)
        message = Frame(dialog, borderwidth=30)
        check = Frame(dialog, borderwidth=30)
        ttk.Label(message, text=lang["launch.account"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 1
    try:
        launchButton
        flag = 1
    except:
        flag = 0
    if (flag):
        launchButton.config(state=DISABLED)
        launchButton.config(textvariable=lang["do.launch.working"])
    cwd = os.getcwd().replace("\\", "\\\\")+"\\"
    versionInfo = eval(open(".minecraft\\versions\\"+versionId+"\\"+versionId+".json").read())
    libraries = versionInfo['libraries']
    libs = []
    launch = []
    tmp = []
    avalible = {}
    for i in libraries:
        theVersion = i["name"].split(":")
        theVersion.pop(2)
        theVersion = ":".join(theVersion)
        mark = 0
        try:
            versionLib = i["downloads"]["artifact"]
            mark = 1
        except:
            pass
        try:
            versionLib = i["downloads"]["classifiers"]["natives-windows"]
        except KeyError:
            if (mark == 0):
                lib = i
                if ("name" in list(lib)):
                    libName = lib["name"]
                    libNameSp = libName.split(":")
                    libNameSp[0] = libNameSp[0].replace(".", "/")
                    libDir = "/".join(libNameSp)
                    libSFName = "-".join(libNameSp[-2:]) + ".jar"
                    avalible[theVersion] = (cwd + ".minecraft\\\\libraries\\\\" + libDir.replace("/", "\\\\") + "\\\\" + libSFName)
                continue
        if ("rules" in i):
            x = 0
            for j in i["rules"]:
                if (j["action"] == "allow"):
                    if ("os" in j):
                        if (j["os"]["name"] == "windows"):
                            x = 1
                    else:
                        x = 1
                if (j["action"] == "disallow"):
                    if ("os" in j):
                        if (j["os"]["name"] == "windows"):
                            x = 0
                    else:
                        x = 0
            if (x == 0):
                continue
        libName = versionLib["path"]
        libDir = os.path.split(libName)[0].replace("/", "\\\\")
        libDir = cwd+".minecraft\\\\libraries\\\\"+libDir+"\\\\"
        libName = libDir+libName.split("/")[-1]
        try:
            i["natives"]
            extract = zipfile.ZipFile(".minecraft/libraries/"+versionLib["path"])
            extractFiles = [i.filename for i in extract.infolist()]
            for i in extractFiles:
                if (i.endswith(".dll")):
                    extract.extract(i, ".minecraft\\versions\\"+versionId+"\\river_natives\\")
            continue
        except:
            pass
        avalible[theVersion] = libName
    for i in avalible:
        tmp.append(avalible[i])
    tmp.append(cwd+".minecraft\\\\versions\\\\"+versionId+"\\\\"+versionId+".jar")
    tmp = ";".join(tmp)
    file = eval(open(".minecraft\\versions\\"+versionId+"\\"+versionId+".json").read()
                .replace("${auth_player_name}", accounts[selectedAccount]["usrName"])
                .replace("${version_name}", versionId)
                .replace("${game_directory}", cwd+".minecraft\\\\")
                .replace("${assets_root}", cwd+".minecraft\\\\assets\\\\")
                .replace("${assets_index_name}", versionInfo["assets"])
                .replace("${auth_uuid}", accounts[selectedAccount]["usrId"])
                .replace("${auth_access_token}", accounts[selectedAccount]["accessToken"])
                .replace("${auth_session}", accounts[selectedAccount]["accessToken"])
                .replace("${user_type}", accounts[selectedAccount]["usrType"])
                .replace("${clientId}", accounts[selectedAccount]["usrId"])
                .replace("${launcher_name}", "river-launcher")
                .replace("${launcher_version}", builds[curBuild])
                .replace("${version_type}", versionInfo["type"])
                .replace("${resolution_width}", str(settings["resolutionWidth"]["value"]))
                .replace("${resolution_height}", str(settings["resolutionHeight"]["value"]))
                .replace("${natives_directory}", cwd+".minecraft\\\\versions\\\\"+versionId+"\\\\"+"river_natives\\\\")
                .replace("${classpath}", "\\\""+tmp+"\\\"")
                .replace("${user_properties}", "{}")
                .replace("${client_id}", "00000000402b5328")
                .replace("${classpath_separator}", ";")
                .replace("${library_directory}", cwd+".minecraft\\\\libraries")
                )
    gameArg = []
    if ("arguments" in file):
        level = 1
    elif ("minecraftArguments" in file):
        level = 0
    else:
        writeLog("game launcher", "failed to recongnize launch type! default to type 0")
        level = 0
    print(level)
    if (level == 0):
        gameArg = file["minecraftArguments"]
        jvmArg = ["-cp", "\""+tmp.replace("\\\\", "\\").replace("/", "\\")+"\""]
    if (level == 1):
        for i in file["arguments"]["game"]:
            if (type(i) == str):
                gameArg.append(i)
            else:
                tmp = i["value"]
                if (type(tmp) != str):
                    for j in tmp:
                        gameArg.append(j)
        gameArg = " ".join(gameArg)
        jvmArg = []
        for i in file["arguments"]["jvm"]:
            if (type(i) == str):
                jvmArg.append(i)
            else:
                tmp = i["value"]
                if (type(tmp) != str):
                    if (i["rules"][0]["os"]["name"] == "windows"):
                        for j in tmp:
                            jvmArg.append(j.replace("/", "\\\\"))
    jvmArg = " ".join(jvmArg)
    output = open(".minecraft\\versions\\"+versionId+"\\river_launch.bat", "w")
    output.write("@echo off\ntitle " + lang["title.log"].get())
    output.write("\ncd /d " + cwd + ".minecraft\n")
    java = subprocess.getoutput("where java").splitlines()
    fl3 = 0
    if ("java" in java[0]):
        fl3 = 1
        java = [[i,
                 sp(subprocess.getoutput("\""+i+"\" -version").splitlines()[1], " (", ")")] for i in java]
    if ( ("javaVersion" in versionInfo) and (versionInfo["javaVersion"]["majorVersion"] > 12) ):
        if (os.path.isfile(cwd+"assets\\java\\B\\bin\\java.exe")):
            output.write(cwd+"assets\\java\\B\\bin\\java.exe ")
        else:
            fl2 = 1
            if (fl3 == 1):
                for i in java:
                    j = i[1]
                    j = sp(j, "\"", "\"")
                    writeLog("launchInstance", "java: "+j)
                    if ("19"in j or
                        "18" in j or
                        "17"in j):
                        output.write("\""+i[0]+"\" ")
                        fl2 = 0
                        break
            if (fl2 == 1):
                writeLog("launchInstance", "unabled to locate newer java")
                raise FileNotFoundError("unabled to locate newer java")
    if ( (not "javaVersion" in versionInfo) or (versionInfo["javaVersion"]["majorVersion"] < 12) ):
        if (os.path.isfile(cwd+"assets\\java\\A\\bin\\java.exe")):
            output.write(cwd+"assets\\java\\A\\bin\\java.exe ")
        else:
            fl2 = 1
            if (fl3 == 1):
                for i in java:
                    j = i[1]
                    j = sp(j, "\"", "\"")
                    writeLog("launchInstance", "java: "+j)
                    if ("1.8.0" in j):
                        output.write("\""+i[0]+"\" ")
                        fl2 = 0
                        break
            if (fl2 == 1):
                writeLog("launchInstance", "unabled to locate older java")
                raise FileNotFoundError("unabled to locate older java")
    output.write("-Dminecraft.client.jar=")
    output.write(cwd+".minecraft\\versions\\"+versionId+"\\"+versionId+".jar")
    if not ("-Djava.library.path" in jvmArg):
        output.write(" -Djava.library.path="+cwd+".minecraft\\versions\\"+versionId+"\\river_natives\\")
    try:
        logging = file["logging"]["client"]
        output.write(" " + logging["argument"].replace("${path}", cwd+".minecraft\\versions\\"+versionId + "\\" + logging["file"]["id"]))
    except:
        pass
    output.write(" ")
    output.write(jvmArg.replace("-Dos.name=Windows 10", "-Dos.name=\"Windows 10\"").replace("-DFabricMcEmu= net.minecraft.client.main.Main", "-DFabricMcEmu=net.minecraft.client.main.Main"))
    output.write(" "+versionInfo["mainClass"]+" ")
    output.write(gameArg)
    if not ("--width" in gameArg):
        output.write(" --width " + str(settings["resolutionWidth"]["value"]) + " --height " + str(settings["resolutionHeight"]["value"]))
    output.close()
    if (flag):
        launchButton.config(textvariable=lang["do.launch.relogin"])
    writeLog("accounts", "relogin account state: "+str(relogin(selectedAccount)))
    if (flag):
        launchButton.config(text=lang["do.launch"].get())
        launchButton.config(state=ACTIVE)
    os.system(".minecraft\\versions\\" + versionId + "\\river_launch.bat")
    return 0


def relogin(account):
    global accounts
    i = account
    if (accounts[i]["usrType"] != "mojang"): return 2, accounts[i]["usrType"]
    if not ("refreshToken" in accounts[i]): return 1
    if (accounts[i]["refreshToken"] == ""): return 1
    t = eval(requests.get("https://login.live.com/oauth20_token.srf?client_id=00000000402b5328&client_secret=client_secret&refresh_token=<TOKEN>&grant_type=refresh_token&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf".replace("<TOKEN>", accounts[i]["refreshToken"]), headers={"Content-Type": "application/x-www-form-urlencoded"}).content)
    refreshToken = t["refresh_token"]
    t = eval(requests.post("https://user.auth.xboxlive.com/user/authenticate", json={"Properties":{"AuthMethod":"RPS", "SiteName":"user.auth.xboxlive.com", "RpsTicket":("d="+t["access_token"])}, "RelyingParty":"http://auth.xboxlive.com", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json={"Properties":{"SandboxId":"RETAIL", "UserTokens":[t["Token"]]}, "RelyingParty":"rp://api.minecraftservices.com/", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json={"identityToken":("XBL3.0 x="+t["DisplayClaims"]["xui"][0]["uhs"]+";"+t["Token"])}).content)
    profile = eval(requests.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization":"Bearer "+t["access_token"]}).content)
    usrName = profile["name"]
    usrId = profile["id"]
    usrSkin = profile["skins"][0]["url"]
    usrSkinId = profile["skins"][0]["id"].replace("-", "")
    usrCapes = profile["capes"]
    accessToken = t["access_token"]
    accounts[i] = {"usrType": "mojang", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken, "refreshToken": refreshToken}
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()
    return 0


tabs = Frame(root, width = 40)
launchPage = Frame(root, borderwidth=30)
downloadsPage = Frame(root, borderwidth=30)
modDownloadsPage = Frame(root, borderwidth=30)
modsPage = Frame(root, borderwidth=30)
accountsPage = Frame(root, borderwidth=30)
settingsPage = Frame(root, borderwidth=30)
languagePage = Frame(root, borderwidth=30)
fabricPage = Frame(root, borderwidth=30)
optifinePage = Frame(root, borderwidth=30)
dynamicCur = Frame(root, borderwidth=30)
pageCur = launchPage

def checkNew(noUpdate):
    global helpToProtect
    has = 0
    tmp = []

    if not (noUpdate):
        try:
            index = eval(get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/index.py"))
            files = index["dir"]
            if (index["version"]["build"] > curBuild):
                for i in files:
                    if (i.endswith("\\")):
                        makeDir("assets\\" + i)
                    else:
                        get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/assets/" + i, saveIn = "assets\\" + os.path.split(i)[0])
                x = requests.get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/river.py")
                y = open("river.py", "w")
                y.write(x.content.decode("utf-8"))
                y.close()
                os.system("start " + sys.executable + " -m river")
                exit()
        except:
            writeLog("check new", "failed to check launcher update")

    if (cfg["version"] != curBuild):
        helpToProtect = 1
        has = 1
        updateFrom = cfg["version"]
        updateFromVer = builds[updateFrom]
        cfg["version"] = curBuild
        config = open(".river_cfg.py", "w")
        config.write(str(cfg))
        config.close()
        up = []
        for i in range(curBuild):
            up.append(lang["update.build." + str(i+1)])
        tmp.append(lang["update.launcher.done"].get().replace("%1", updateFromVer).replace("%2", builds[curBuild]))
        for i in range(updateFrom, curBuild+1):
            if (updateFrom < i):
                if ((curBuild - updateFrom) > 1):
                    tmp.append(builds[i] + ": ")
                for j,updateContent in enumerate(up[i-1]):
                    tmp.append(str(j+1) + ". " + updateContent + "! ")

    try:
        if (cfg["latest"] != eval(versions)["versions"][0]["id"]):
            has = 1
            if (cfg["latest"] != ""):
                tmp.append(lang["update.minecraft"].get().replace("%1", eval(versions)["versions"][0]["id"]))
                cfg["latest"] = eval(versions)["versions"][0]["id"]
        config = open(".river_cfg.py", "w")
        config.write(str(cfg))
        config.close()
        if (has == 1):
            global dialogCur
            dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
            try:
                dialogCur.destroy()
            except:
                pass
            dialogCur = dialog
            dialog.iconbitmap("assets\\title\\icon.ico")
            dialog.focus_force()
            dialog.resizable(0, 0)
            message = Frame(dialog, borderwidth=30)
            check = Frame(dialog, borderwidth=30)
            ttk.Label(message, text=("\n".join(tmp)), font=theFont).grid()
            myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
            message.grid()
            check.grid()
            chTheme(dialog)
    except:
        writeLog("check new", "failed to check Minecraft update")

def processRename(src, dst):
    os.rename(".minecraft\\versions\\" + src + "\\" + src + ".jar", ".minecraft\\versions\\" + src + "\\" + dst + ".jar")
    os.rename(".minecraft\\versions\\" + src + "\\" + src + ".json", ".minecraft\\versions\\" + src + "\\" + dst + ".json")
    os.rename(".minecraft\\versions\\" + src, ".minecraft\\versions\\" + dst)
    global config
    config = open(".minecraft\\versions\\" + dst + "\\" + dst + ".json", "r")
    x = eval(config.read())
    config = open(".minecraft\\versions\\" + dst + "\\" + dst + ".json", "w")
    if ("id" in x):
        x["id"] = dst
    else:
        writeLog("rename", "no \"id\" in \"" + dst + ".json\"")
    config.write(str(x))
    config.close()

def renameVersion(version, index):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["launch.renamePrompt"].get().replace("%1", version), font=theFont).grid()
    entry = ttk.Entry(message, font=theFont)
    entry.grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        processRename(version, entry.get()),
        dialog.destroy(),
        pageLaunch(index)
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageLaunch(index)

def removeVersion(version, index):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["launch.removePrompt"].get(), font=theFont).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (subprocess.getstatusoutput("rmdir .minecraft\\versions\\" + version + " /S /Q"), dialog.destroy(), pageLaunch(index))).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageLaunch(index)

def launchPopup(click, version, index):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["launch.rename"].get(), command=lambda: renameVersion(version, index))
    popup.add_command(label=lang["launch.remove"].get(), command=lambda: removeVersion(version, index))
    popup.add_command(label=lang["launch.directory"].get(), command=lambda: subprocess.getstatusoutput("explorer .minecraft\\versions\\" + version))
    popup.add_command(label=lang["launch.fix"].get(), command=lambda: thread._start_new_thread(downloadAll, (eval(open(".minecraft\\versions\\"+version+"\\"+version+".json").read()), 1)))
    popup.tk_popup(click.x_root, click.y_root)

def pageLaunch(sel=0):
    global launchButton
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)
    message = Frame(dynamic)
    launch = []
    tmp = os.listdir(".minecraft\\versions")
    for i in tmp:
        if (os.path.isfile(".minecraft\\versions\\"+i+"\\"+i+".json")):
            launch.append(i)
    i = 0
    if (launch == []):
        ttk.Label(dynamic, textvariable=lang["launch.instead"], font=theFont).grid(column=1, row=2)
    else:
        x = ttk.Scrollbar(message)
        li = myList(message, width=75, height = 10, yscrollcommand=x.set)
        x.config(command=li.yview)
        for i in range(len(launch)):
            versionName = launch[i]
            infoFile = open(".minecraft\\versions\\" + launch[i] + "\\" + launch[i] + ".json")
            info = eval(infoFile.read())
            infoFile.close()
            infos = []
            if ("river_origin" in info):
                origin = info["river_origin"]
            elif ("clientVersion" in info):
                origin = info["clientVersion"]
            else:
                origin = versionName
            try:
                if ("net.fabricmc" in info["libraries"][-1]["name"]):
                    if ("net.fabricmc:intermediary" in info["libraries"][-2]["name"]):
                        origin = info["libraries"][-2]["name"].split(":")[-1]
                    else:
                        origin = "Unknown"
                    infos.append(lang["mod.fabric"].get() + " " + info["libraries"][-1]["name"].split(":")[-1])
                if ("net.fabricmc" in info["libraries"][-3]["name"]):
                    if ("net.fabricmc:intermediary" in info["libraries"][-5]["name"]):
                        origin = info["libraries"][-5]["name"].split(":")[-1]
                    else:
                        origin = "Unknown"
                    infos.append(lang["mod.fabric"].get() + " " + info["libraries"][-3]["name"].split(":")[-1])
            except KeyError:
                pass
            try:
                if ("net.minecraftforge" in info["libraries"][-1]["name"]):
                    origin = info["arguments"]["game"][info["arguments"]["game"].index("--fml.mcVersion")+1]
                    infos.append(lang["mod.forge"].get() + " " + info["libraries"][-1]["name"].split("-")[-1])
                if ("net.minecraftforge" in info["libraries"][-3]["name"]):
                    origin = info["arguments"]["game"][info["arguments"]["game"].index("--fml.mcVersion")+1]
                    infos.append(lang["mod.forge"].get() + " " + info["libraries"][-3]["name"].split("-")[-1])
            except KeyError:
                pass
            try:
                if ("minecraftArguments" in info): args = info["minecraftArguments"]
                if ("arguments" in info): args = info["arguments"]["game"]
                if ("optifine.OptiFineTweaker" in args):
                    tmp = ""
                    for j in info["libraries"]:
                        if ("optifine:OptiFine" in j["name"]):
                            origin = j["name"].split(":")[-1].split("_")[0]
                            tmp = "_".join(j["name"].split(":")[-1].split("_")[1:])
                    infos.append(lang["mod.optifine"].get() + " " + tmp)
            except KeyError:
                pass
            if (origin != versionName):
                infos = [origin] + infos
            infosAll = ""
            if (infos != []):
                infosAll = ", ".join(infos)
            img = oldImage
            versionType = lang["launch.type.old"].get()
            if ("type" in info):
                if (info["type"] == "release"):
                    img = releaseImage
                    versionType = lang["launch.type.release"].get()
                if (info["type"] == "snapshot"):
                    img = snapshotImage
                    versionType = lang["launch.type.snapshot"].get()
            li.add(launch[i]+"\n    "+versionType+infosAll, img)
       #li.offset = 5
        li.activate(sel)
        li.bind("<Button-3>", lambda x: launchPopup(x, li.get("active").splitlines()[0], li.index("active")))
        x.pack(side=RIGHT, fill=Y)
        li.pack(side=LEFT)
        launchButton = myButton(dynamic, text=lang["do.launch"].get(), command=lambda: thread._start_new_thread(launchInstance, (li.get("active").splitlines()[0], )))
        message.grid()
        launchButton.grid()
    launchPage.pack()
    dynamic.pack()
    pageCur = launchPage
    dynamicCur = dynamic
    chTheme(dynamic)
    try:
        li.update()
    except:
        pass

global downloadConfig
downloadConfig = {"minecraft": "", "minecraft.id": -1, "fabric": "", "optifine": ""}
def editMinecraft():
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    releaseOutImage = PhotoImage(master=dialog, file="assets\\icon\\release.png")
    snapshotOutImage = PhotoImage(master=dialog, file="assets\\icon\\snapshot.png")
    oldOutImage = PhotoImage(master=dialog, file="assets\\icon\\old.png")
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    minecraft = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    if (minecraft == ""):
        ttk.Label(message, text=lang["main.noWifi"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    minecraft = eval(minecraft)["versions"]

    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill=Y)
    li = myList(message, width=75, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get(), font=theFont).pack()
    for i in minecraft:
        img = oldOutImage
        if (i["type"] == "release"):
            img = releaseOutImage
        if (i["type"] == "snapshot"):
            img = snapshotOutImage
        theTime = i["releaseTime"].replace("T", ".").replace("+00:00", "").replace("-", ".").replace(":", ".").split(".")
        tl = []
        for j in range(6):
            tl.append(int(theTime[j]))
        releaseTime = time.mktime((tl[0], tl[1], tl[2], tl[3], tl[4], tl[5], 0, 0, 0)) - time.timezone
        RT = time.localtime(releaseTime)
        info = (lang["downloads.date"].get().replace("%1", str(RT.tm_year)).replace("%2", str(RT.tm_mon).zfill(2)).replace("%3", str(RT.tm_mday).zfill(2)).replace("%4", str(RT.tm_hour).zfill(2)).replace("%5", str(RT.tm_min).zfill(2)).replace("%6", str(RT.tm_sec).zfill(2)))
        li.add(i["id"] + "\n    " + info, image=img)
    li.pack(side=LEFT, fill=BOTH)
    x.config(command=li.yview)

    global editMinecraftLi
    editMinecraftLi = li

    myButton(check, text=lang["sel.yes"].get(), command=lambda: (exec("global downloadConfig; downloadConfig = {\"minecraft\": editMinecraftLi.get(ACTIVE).splitlines()[0], \"minecraft.id\": editMinecraftLi.index(ACTIVE), \"fabric\": \"\", \"optifine\": \"\"}"), dialog.destroy(), pageDownloads())).grid(column=0, row=0)
    if (downloadConfig["minecraft"] != ""):
        myButton(check, text=lang["mod.clear"].get(), command=lambda: (exec("global downloadConfig; downloadConfig = {\"minecraft\": \"\", \"minecraft.id\": -1, \"fabric\": \"\", \"optifine\": \"\"}"), pageDownloads(), dialog.destroy())).grid(column=1, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=2, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)

def editFabric(version = ""):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    fabricOutImage = PhotoImage(master=dialog, file="assets\\icon\\fabric.png")
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    if (version == ""):
        ttk.Label(message, text=lang["mod.instead"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 0

    try:
        fabric = eval(get("https://meta.fabricmc.net/v2/versions/loader/" + version))
    except:
        ttk.Label(message, text=lang["main.noWifi"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 0
    if (fabric == []):
        ttk.Label(message, text=lang["mod.noAvalibleMessage"].get().replace("%1", version), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (dialog.destroy())).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 0
    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill="y")
    li = myList(message, width=75, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get(), font=theFont).pack()
    for i in fabric:
        li.add(i["loader"]["version"], image=fabricOutImage)
    li.pack(side=LEFT, fill=BOTH)
    x.config(command=li.yview)
    global editFabricLi
    editFabricLi = li

    myButton(check, text=lang["sel.yes"].get(), command=lambda: (exec("downloadConfig[\"fabric\"] = editFabricLi.get(ACTIVE)"), dialog.destroy(), pageDownloads())).grid(column=0, row=0)
    if (downloadConfig["fabric"] != ""):
        myButton(check, text=lang["mod.clear"].get(), command=lambda: (exec("downloadConfig[\"fabric\"] = \"\""), pageDownloads(), dialog.destroy())).grid(column=1, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=2, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    dialog.mainloop()

def setOptifine(wrappers, selectedWrapper):
    wrapper = wrappers[selectedWrapper]
    writeLog("optifine downloader", "wrapper: " + str(wrapper))
    if (wrapper[2].startswith("http://optifine.net/adloadx?f=preview_OptiFine_")):
        wrapperName = sp(wrapper[2], "http://optifine.net/adloadx?f=preview_OptiFine_", ".jar")
    elif (wrapper[2].startswith("http://optifine.net/adloadx?f=OptiFine_")):
        wrapperName = sp(wrapper[2], "http://optifine.net/adloadx?f=OptiFine_", ".jar")
    else:
        writeLog("Unable to split optifine " + str(wrapper))
        return 0
    wrapperName2 = sp(wrapper[2], "http://optifine.net/adloadx?f=", ".jar")
    makeDir(".minecraft\\libraries\\optifine\\Optifine\\" + wrapperName)
    web = get(wrapper[2]).splitlines()
    x = ""
    for i in web:
        if ("<a href='downloadx?f=" in i):
            x = "https://optifine.net/" + sp(i, "<a href='", "' onclick='onDownload()'>" + wrapperName2.replace("_", " ").replace(".jar", "") + "</a>")
            break
    if (x != ""): get(x, saveIn = (".minecraft\\libraries\\optifine\\Optifine\\" + wrapperName), saveAs = ("OptiFine-" + wrapperName + ".jar"))
    else:
        writeLog("optifine downloader", "unable to get optifine " + str(wrapper))
        return 0
    zipFile = zipfile.ZipFile(".minecraft\\libraries\\optifine\\Optifine\\" + wrapperName + "\\OptiFine-" + wrapperName + ".jar")
    x = zipFile.filelist
    flag = 0
    for i in x:
        y = i.filename
        if ("launchwrapper" in y):
            if (".jar" in y):
                wrapperLaunchOrigin = y
                wrapperLaunch = y.replace(".jar", "").split("-")
                wrapperLaunch = ["-".join(wrapperLaunch[:-1]), wrapperLaunch[-1]]
                wrapperLaunch = "\\".join(wrapperLaunch)
                writeLog("optifine downloader", "wrapperLaunch: " + wrapperLaunch)
                zipFile.extract(y, ".minecraft\\libraries\\optifine\\" + wrapperLaunch)
                flag = 1
                break
    global downloadConfig
    if (flag == 0):
        downloadConfig["optifine"] = (wrapperName, )
    if (flag == 1):
        yN = y.replace(".jar", "").split("-")
        yN = ["-".join(yN[:-1]), yN[-1]]
        yN = ":".join(yN)
        downloadConfig["optifine"] = (wrapperName, yN)
    writeLog("set optifine", "downloadConfig[\"optifine\"]: " + str(downloadConfig["optifine"]))
    pageDownloads()

def editOptifine(version = ""):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    optifineOutImage = PhotoImage(master=dialog, file="assets\\icon\\optifine.png")
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    if (version == ""):
        ttk.Label(message, text=lang["mod.instead"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0

    x = get("https://optifine.net/downloads").splitlines()
    if (x == []):
        ttk.Label(message, text=lang["main.noWifi"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    allOpti = []
    optifine = []
    curTmp = ["", 0, 0, 0]
    curVer = ""
    for i in range(len(x)):
        if ("<h2>Minecraft" in x[i]):
            if (x[i][0].endswith(".0")):
                curVer = sp(x[i], "<h2>Minecraft ", ".0</h2>")
            else:
                curVer = sp(x[i], "<h2>Minecraft ", "</h2>")
        if ("<td class='colFile'>" in x[i]):
            curTmp[0] = curVer
            curTmp[1] = sp(x[i], "<td class='colFile'>", "</td>")
        if ("<td class='colMirror'>" in x[i]):
            curTmp[2] = sp(x[i], "<td class='colMirror'><a href=\"", "\">(Mirror)</a></td>")
        if ("<td class='colForge'>" in x[i]):
            curTmp[3] = sp(x[i], "<td class='colForge'>", "</td>")
            allOpti.append(curTmp)
            curTmp = ["", 0, 0, 0]
    for i in allOpti:
        if (i[0] == version):
            optifine.append(i)
    if (optifine == []):
        ttk.Label(message, text=lang["mod.noAvalibleMessage"].get().replace("%1", version), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (dialog.destroy())).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill="y")
    li = myList(message, width=75, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get(), font=theFont).pack()
    writeLog("optifine downloader", "allOpti: " + str(allOpti) + "; Optifine: " + str(optifine))
    for i in optifine:
        li.add(i[1], image=optifineOutImage)
    li.pack(side=LEFT, fill=BOTH)
    x.config(command=li.yview)
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (setOptifine(optifine, li.index(ACTIVE)), dialog.destroy())).grid(column=0, row=0)
    if (downloadConfig["optifine"] != ""):
        myButton(check, text=lang["mod.clear"].get(), command=lambda: (exec("downloadConfig[\"optifine\"] = \"\""), pageDownloads(), dialog.destroy())).grid(column=1, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=2, row=0)
    message.grid()
    check.grid()
    chTheme(dialog)

def editDownload(index):
    if (index == 0):
        editMinecraft()
    if (index == 1):
        editFabric(downloadConfig["minecraft"])
    if (index == 2):
        editOptifine(downloadConfig["minecraft"])

def downloadAll(versionInfo, mode=0):
    global pageDownloadsButton
    global launchButton
    if (mode==0):
        targetButton = pageDownloadsButton
    if (mode==1):
        targetButton = launchButton
    customName = versionInfo["id"]
    global per
    try:
        targetButton.config(state=DISABLED)
        flag = 1
    except:
        flag = 0
    # Assets
    assetsInfo = eval(get(versionInfo["assetIndex"]["url"], saveIn = ".minecraft\\assets\\indexes"))
    per = 0
    for i in range(len(assetsInfo["objects"])):
        j = assetsInfo["objects"][list(assetsInfo["objects"])[i]]
        makeDir(".minecraft\\assets\\objects\\" + j["hash"][:2])
        if ("hash" in j):
            thread._start_new_thread(getPer, ("https://resources.download.minecraft.net/" + j["hash"][:2] + "/" + j["hash"], ".minecraft\\assets\\objects\\" + j["hash"][:2], None, j["hash"]))
        else:
            thread._start_new_thread(getPer, ("https://resources.download.minecraft.net/" + j["hash"][:2] + "/" + j["hash"], ".minecraft\\assets\\objects\\" + j["hash"][:2]))
        if (flag == 1):
            targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.assets"].get()) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        writeLog("downloader", "assets " + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
    while 1:
        if (flag == 1):
            targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.assets"].get()) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        writeLog("downloader", "assets " + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        if (per == len(assetsInfo["objects"].keys())):
            break
    if (flag == 1):
        targetButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.assets"].get()))
    writeLog("downloader", "finish assets")
    # Libraries
    libInfo = versionInfo["libraries"]
    j = 0
    cnt = 0
    libs = []
    per = 0
    x = 0
    makeDir(".minecraft\\versions\\" + customName + "\\river_natives")
    for i in libInfo:
        mark = 0
        try:
            lib = i["downloads"]["artifact"]
            mark = 1
        except:
            pass
        try:
            lib = i["downloads"]["classifiers"]["natives-windows"]
            mark = 1
        except KeyError:
            if (mark == 0):
                lib = i
                if ("name" in lib):
                    if ("url" in lib):
                        libName = lib["name"]
                        libNameSp = libName.split(":")
                        libNameSp[0] = libNameSp[0].replace(".", "/")
                        libDir = "/".join(libNameSp)
                        libSFName = "-".join(libNameSp[-2:]) + ".jar"
                        libUrl = lib["url"] + libDir + "/" + libSFName
                        makeDir(".minecraft\\libraries\\" + libDir.replace("/", "\\"))
                        thread._start_new_thread(getPer, (libUrl, ".minecraft\\libraries\\" + libDir.replace("/", "\\"), libSFName))
                        x += 1
                continue
        x += 1
        libName = lib["path"]
        libDir = ".minecraft\\libraries\\" + os.path.split(libName)[0].replace("/", "\\")
        libName = libDir + os.path.split(libName)[1]
        libs.append(libName)
        makeDir(libDir)
        if ("sha1" in lib):
            thread._start_new_thread(getPer, (lib["url"], libDir, None, lib["sha1"]))
        else:
            thread._start_new_thread(getPer, (lib["url"], libDir))
        if (flag == 1):
            targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.libraries"].get()) + str(per).zfill(len(str(x))) + "/" + str(x))
    while 1:
        if (flag == 1):
            targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.libraries"].get()) + str(per).zfill(len(str(x))) + "/" + str(x))
        if (per == x):
            break
    if (flag == 1):
        targetButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.libraries"].get()))
    writeLog("downloader", "finish libraries")
    # Client
    if (flag == 1):
        targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.client"].get()))
    if ("sha1" in versionInfo["downloads"]["client"]):
        get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"), hashHex = versionInfo["downloads"]["client"]["sha1"])
    else:
        get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"))
    if (flag == 1):
        targetButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.client"].get()))
    writeLog("downloader", "finish client")
    # Logging
    try:
        if (flag == 1):
            targetButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.logging"].get()))
        logging = versionInfo["logging"]["client"]
        get(logging["file"]["url"], saveIn = (".minecraft\\versions\\" + customName))
        if (flag == 1):
            targetButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.logging"].get()))
        writeLog("downloader", "finish logging file")
    except:
        writeLog("downloader", "no logging file")

def startDownload(customName):
    global downloadButtonLocked
    downloadButtonLocked = 1
    try:
        pageDownloads()
        flag = 1
    except:
        flag = 0
    if (downloadConfig["minecraft"] == ""):
        global dialogCur
        dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
        try:
            dialogCur.destroy()
        except:
            pass
        dialogCur = dialog
        dialog.iconbitmap("assets\\title\\icon.ico")
        dialog.focus_force()
        dialog.resizable(0, 0)
        message = Frame(dialog, borderwidth=30)
        check = Frame(dialog, borderwidth=30)
        ttk.Label(message, text=lang["mod.instead"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 0
    global per
    selectedDownload = downloadConfig["minecraft.id"]
    try:
        downloads = eval(get("https://launchermeta.mojang.com/mc/game/version_manifest.json"))["versions"]
    except:
        dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
        try:
            dialogCur.destroy()
        except:
            pass
        dialogCur = dialog
        dialog.iconbitmap("assets\\title\\icon.ico")
        dialog.focus_force()
        dialog.resizable(0, 0)
        message = Frame(dialog, borderwidth=30)
        check = Frame(dialog, borderwidth=30)
        ttk.Label(message, text=lang["main.noWifi"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        chTheme(dialog)
        dialog.mainloop()
        return 0
    originName = downloadConfig["minecraft"]
    if (customName == ""):
        customName = originName
    makeDir(".minecraft\\versions\\" + customName)
    versionInfo = eval(get(downloads[selectedDownload]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".json")))
    versionInfo["id"] = customName
    versionInfo["river_origin"] = originName
    forge = 0
    if (downloadConfig["fabric"] != ""):
        fabric = eval(requests.get("https://meta.fabricmc.net/v2/versions/loader/" + originName + "/" + downloadConfig["fabric"] + "/profile/json").content)
        versionInfo["time"] = fabric["time"]
        versionInfo["type"] = fabric["type"]
        versionInfo["mainClass"] = fabric["mainClass"]
        versionInfo["arguments"]["game"] += fabric["arguments"]["game"]
        versionInfo["arguments"]["jvm"] += fabric["arguments"]["jvm"]
        versionInfo["libraries"] += fabric["libraries"]
    if (downloadConfig["optifine"] != ""):
        if (downloadConfig["fabric"] == ""):
            if (versionInfo["complianceLevel"] == 1):
                versionInfo["arguments"]["game"] += ["--tweakClass", "optifine.OptiFineTweaker"]
            if (versionInfo["complianceLevel"] == 0):
                if (forge == 0): versionInfo["minecraftArguments"] += " --tweakClass optifine.OptiFineTweaker"
                if (forge != 0): versionInfo["minecraftArguments"] += " --tweakClass optifine.OptiFineForgeTweaker"
            if (len(downloadConfig["optifine"]) == 2):
                versionInfo["libraries"] += [{"name": "optifine:OptiFine:" + downloadConfig["optifine"][0]}, {"name": "optifine:" + downloadConfig["optifine"][1]}]
            elif (len(downloadConfig["optifine"]) == 1):
                versionInfo["libraries"].append({"name": "optifine:OptiFine:" + downloadConfig["optifine"][0]})
            versionInfo["mainClass"] = "net.minecraft.launchwrapper.Launch"
        if (downloadConfig["fabric"] != ""):
            oldName = ".minecraft\\libraries\\optifine\\Optifine\\" + downloadConfig["optifine"][0] + "\\OptiFine-" + downloadConfig["optifine"][0] + ".jar"
            if ("pre" in downloadConfig["optifine"][0]):
                newName = ".minecraft\\mods\\preview_Optifine_"
            else:
                newName = ".minecraft\\mods\\Optifine_"
            newName += downloadConfig["optifine"][0] + ".jar"
            os.rename(oldName, newName)
            get("https://mediafilez.forgecdn.net/files/3961/344/optifabric-1.13.16.jar", saveIn = ".minecraft\\mods")
    json.dump(versionInfo, open(".minecraft\\versions\\"+versionInfo["id"]+"\\" + customName + ".json", "w"), indent=2, sort_keys=True, ensure_ascii=False)
    writeLog("downloader", "finish version info")
    downloadAll(versionInfo)
    if (flag == 1):
        pageDownloadsButton.config(text=lang["do.downloads"].get())
    downloadButtonLocked = 0
    if (flag == 1):
        pageDownloads()

arg = sys.argv
if ("--noJava" in arg):
    noJava = 1
    arg.pop(arg.index("--noJava"))
if ("--noUpdate" in arg):
    noUpdate = 1
    arg.pop(arg.index("--noUpdate"))
arg = arg[1:]
if (len(arg) > 0):
    for i in range(len(arg)):
        arg[i] = arg[i].replace("\"", "")
    for i in range(3):
        arg.append("")
    writeLog("pre-parse", "arg: " + str(arg))
    if ( (arg[0] == "help") or
         (arg[0] == "h")
         ):
        print(lang["main.usage"].get())
        exit()
    if (arg[0] == "launch"):
        root.destroy()
        launchInstance(arg[1])
        exit()
    if (arg[0] == "download"):
        root.destroy()
        minecraft = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
        minecraft = eval(minecraft)["versions"]
        flag = -1
        for i in range(len(minecraft)):
            if (minecraft[i]["id"] == arg[1]):
                flag = i
                break
        if (flag == -1):
            writeLog("pre-download", "cannot find Minecraft version \"" + arg[1] + "\"")
            raise ValueError("Cannot find Minecraft version \"" + arg[1] + "\"")
        downloadConfig = {"minecraft": arg[1], "minecraft.id": flag, "fabric": arg[2], "optifine": arg[3]}
        writeLog("pre-download", "downloadConfig: " + str(downloadConfig))
        startDownload(arg[4])
        exit()

def pageDownloads():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)

    downloadTabs = Frame(dynamic)
    downloadContent = Frame(dynamic)
    myTabY(downloadTabs, text=lang["do.downloads.game"].get(), command=pageDownloads).grid(column=0, row=0)
    myTabY(downloadTabs, text=lang["do.downloads.mods"].get(), command=pageModDownloads).grid(column=1, row=0)

    message = Frame(downloadContent)
    listArea = Frame(downloadContent)
    buttonArea = Frame(downloadContent)
    entry = ttk.Entry(message, font=theFont)
    liK = myList(listArea, width=20, height = 10)
    liV = myList(listArea, width=55, height = 10)
    if (downloadConfig["minecraft"] != ""):
        fabric = eval(get("https://meta.fabricmc.net/v2/versions/loader/"))
    else:
        fabric = []
    # Minecraft
    i = "minecraft"
    pre = lang["mod."+i].get()
    if (downloadConfig[i] == ""):
        pre2 = lang["mod.none"].get()
    else:
        pre2 = downloadConfig[i]
    liK.add("\n" + pre + "\n", image=releaseImage)
    liV.add("\n" + pre2 + "\n")
    # Fabric
    i = "fabric"
    pre = lang["mod."+i].get()
    if (downloadConfig["minecraft"] == ""):
        pre2 = lang["mod.none"].get()
    elif (fabric == []):
        pre2 = lang["mod.noAvalible"].get()
    elif (downloadConfig[i] == ""):
        pre2 = lang["mod.none"].get()
    else:
        pre2 = downloadConfig[i]
    liK.add("\n" + pre + "\n", image=fabricImage)
    liV.add("\n" + pre2 + "\n")
    # Optifine
    i = "optifine"
    pre = lang["mod."+i].get()
    if (downloadConfig["minecraft"] == ""):
        pre2 = lang["mod.none"].get()
    elif (downloadConfig[i] == ""):
        pre2 = lang["mod.none"].get()
    else:
        pre2 = downloadConfig[i][0]
    liK.add("\n" + pre + "\n", image=optifineImage)
    liV.add("\n" + pre2 + "\n")
    liV.config(state=DISABLED)

    liK.grid(column=0, row=0)
    liV.grid(column=1, row=0)
    ttk.Label(message, text=lang["downloads.custom"].get(), font=theFont).grid()
    entry.grid()

    pageDownloadsButton2 = myButton(buttonArea, text=lang["do.downloads.edit"].get(), command=lambda: editDownload(liK.index("active")))
    pageDownloadsButton2.grid(column=0, row=0)
    global pageDownloadsButton
    pageDownloadsButton = myButton(buttonArea, text=lang["do.downloads"].get(), command=lambda: thread._start_new_thread(startDownload, (entry.get(), )))
    pageDownloadsButton.grid(column=1, row=0)
    if (downloadButtonLocked):
        pageDownloadsButton.config(state=DISABLED)
        pageDownloadsButton2.config(state=DISABLED)

    col_count, row_count = buttonArea.grid_size()
    for col in range(col_count):
        buttonArea.grid_columnconfigure(col, pad=10)

    listArea.grid()
    message.grid()
    buttonArea.grid()
    downloadTabs.pack()
    ttk.Separator(dynamic, orient=HORIZONTAL).pack(fill=X)
    ttk.Label(dynamic, text=" "*1000, font=theFont).pack()
    downloadContent.pack()
    downloadsPage.pack()
    dynamic.pack()
    pageCur = downloadsPage
    dynamicCur = dynamic
    chTheme(dynamic)
    liK.update()
    liV.update()

def changeMod(index):
    oldName = os.listdir(".minecraft\\mods")[index]
    if (oldName.endswith(".disabled")):
        name = oldName[:-9]
    else:
        name = oldName + ".disabled"
    os.rename(".minecraft\\mods\\"+oldName, ".minecraft\\mods\\"+name)
    pageMods(index)

def changeModAll(mode):
    mods = os.listdir(".minecraft\\mods")
    for i in range(len(mods)):
        if ( (mods[i][-1] == "d") and (mode==0) ):
            changeMod(i)
        if ( (mods[i][-1] == "r") and (mode==1) ):
            changeMod(i)

def processRemoveMod(index):
    oldName = os.listdir(".minecraft\\mods")[index]
    os.remove(".minecraft\\mods\\"+oldName)
    pageDownloads()

def removeMod(index):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["mods.removePrompt"].get(), font=theFont).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        processRemoveMod(index),
        dialog.destroy(),
        pageMods()
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageMods()

def modsPopup(click, index):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["mods.remove"].get(), command=lambda: removeMod(index))
    popup.add_command(label=lang["mods.directory"].get(), command=lambda: subprocess.getstatusoutput("explorer .minecraft\\mods"))
    popup.tk_popup(click.x_root, click.y_root)

cursef = {"Content-Type": "application/json", "Accept": "application/json", "x-api-key": "$2a$10$ZaB581JIZAliSu7.eL8C5uVPx03yRCgl48hPz.DW1jdESMjlUMFiS"}

def downloadMod(modLink, dialog):
    get(modLink, saveIn=".minecraft\\mods")
    dialog.destroy()

def pageModVersion(modId):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    r = get("https://api.curseforge.com/v1/mods/"+str(modId)+"/files", headers=cursef)
    if (r == ""):
        ttk.Label(message, text=lang["main.noWifi"].get(), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    x = eval(r)
    r = get("https://api.curseforge.com/v1/mods/"+str(modId), headers=cursef)
    y = eval(r)
    del r
    name = y["data"]["name"]
    scroll = ttk.Scrollbar(message)
    scroll.pack(side=RIGHT, fill=Y)
    li = myList(message, yscrollcommand=scroll.set)
    scroll.config(command=li.yview)
    for i in x["data"]:
        li.add(i["displayName"] + "\n\t" + ", ".join(i["gameVersions"]))
    li.pack(side=RIGHT)
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (message.grid_forget(), check.grid_forget(), downloadMod(x["data"][li.index(ACTIVE)]["downloadUrl"], dialog))).grid(column=0, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    li.update()

def pageModDownloads(arg="sortField=Popularity&sortOrder=desc"):
    flag = 1

    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)
    downloadTabs = Frame(dynamic)
    downloadContent = Frame(dynamic)
    myTabY(downloadTabs, text=lang["do.downloads.game"].get(), command=pageDownloads).grid(column=0, row=0)
    myTabY(downloadTabs, text=lang["do.downloads.mods"].get(), command=pageModDownloads).grid(column=1, row=0)
    message = Frame(downloadContent)
    listArea = Frame(downloadContent)

    r = get("https://api.curseforge.com/v1/mods/search?gameId=432&"+arg, headers=cursef)
    x = eval(r)

    buttonArea = Frame(downloadContent)
    entry = ttk.Entry(message, font=theFont)
    entry.grid()

    myButton(buttonArea, text=lang["do.downloads"].get(), command=lambda: pageModVersion(x["data"][li.index(ACTIVE)]["id"])).grid(column=0, row=0)
    myButton(buttonArea, text=lang["do.downloads.search"].get(), command=lambda: pageModDownloads("searchFilter=\""+entry.get()+"\"")).grid(column=1, row=0)
    myButton(buttonArea, text=lang["do.downloads.fabricApi"].get(), command=lambda: pageModVersion(306612)).grid(column=2, row=0)
    col_count, row_count = buttonArea.grid_size()
    for col in range(col_count):
        buttonArea.grid_columnconfigure(col, pad=10)

    if (x["data"] != []):
        scroll = ttk.Scrollbar(listArea)
        scroll.pack(side=RIGHT, fill=Y)
        li = myList(listArea, width=40, height = 10, yscrollcommand=scroll.set)
        scroll.config(command=li.yview)
        for i in x["data"]:
            pre = i["name"] + "\n\t" + i["summary"]
            li.add(pre)
        li.pack(side=LEFT, fill=Y)
    else:
        try:
            writeLog("mod downloads page", arg.replace("searchFilter=", ""))
            x = int(arg.replace("searchFilter=", ""))
            r = get("https://api.curseforge.com/v1/mods/"+str(x), headers=cursef)
            x = eval(r)
            scroll = ttk.Scrollbar(listArea)
            scroll.pack(side=RIGHT, fill=Y)
            li = myList(listArea, width=40, height = 10, yscrollcommand=scroll.set)
            pre = x["data"]["name"] + "\n    " + x["data"]["summary"]
            li.add(pre)
            li.pack(side=LEFT)
        except:
            ttk.Label(listArea, text=lang["modDownloads.nothing"].get(), font=theFont).grid()
    listArea.grid()
    message.grid()
    buttonArea.grid()
    modDownloadsPage.pack()
    downloadTabs.pack()
    ttk.Separator(dynamic, orient=HORIZONTAL).pack(fill=X)
    ttk.Label(dynamic, text=" "*1000, font=theFont).pack()
    downloadContent.pack()
    dynamic.pack()
    pageCur = modDownloadsPage
    dynamicCur = dynamic
    chTheme(dynamic)
    li.update()

def pageMods(sel=None):
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)

    message = Frame(dynamic)
    check = Frame(dynamic)
    li = myList(message, width=75, height=10)
    if ( ("mods" in os.listdir(".minecraft\\")) and (os.listdir(".minecraft\\mods") != []) ):
        for i in os.listdir(".minecraft\\mods"):
            name = i
            disabled = 0
            if (name.endswith(".disabled")):
                disabled = 1
            name = ".".join(name.replace(".disabled", "").split(".")[:-1])
            img = onImage
            if (disabled):
                img = offImage
            zipFile = zipfile.ZipFile(".minecraft\\mods\\"+i)
            info = ""
            try:
                x = zipFile.read("fabric.mod.json")
                x = eval(x)
                info += "\n\t" + x["version"] + "; " + x["description"]
            except:
                pass
            li.add(name+info, image=img)
        if not (sel is None):
            li.activate(sel)
        li.bind("<Button-3>", lambda x: modsPopup(x, li.index(ACTIVE)))
        li.grid()
    else:
        ttk.Label(message, text=lang["mods.instead"].get(), font=theFont).grid()
    myButton(check, text=lang["do.mods"].get(), command=lambda: changeMod(li.index(ACTIVE))).grid(column=1, row=0)
    myButton(check, text=lang["do.mods.all.on"].get(), command=lambda: changeModAll(0)).grid(column=0, row=0)
    myButton(check, text=lang["do.mods.all.off"].get(), command=lambda: changeModAll(1)).grid(column=2, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    modsPage.pack()
    dynamic.pack()
    pageCur = modsPage
    dynamicCur = dynamic
    chTheme(dynamic)
    li.update()

def removeAccount(account):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["accounts.removePrompt"].get(), font=theFont).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        accounts.pop(account),
        exec("global cfg;cfg[\"accounts\"] = accounts"),
        exec("global cfg;cfg[\"selectedAccount\"] = selectedAccount"),
        exec("global config;config = open(\".river_cfg.py\", \"w\")"),
        config.write(str(cfg)),
        config.close(),
        dialog.destroy(),
        pageAccounts()
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageAccounts()

def accountsPopup(click, account):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["accounts.remove"].get(), command=lambda: removeAccount(account))
    popup.tk_popup(click.x_root, click.y_root)

def processMojang(code, dialog):
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["accounts.loading"].get(), font=theFont).grid()
    message.grid()
    t = eval(requests.get("https://login.live.com/oauth20_token.srf?client_id=00000000402b5328&client_secret=client_secret&code=<CODE>&grant_type=authorization_code&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf".replace("<CODE>", code)).content)
    refreshToken = t["refresh_token"]
    t = eval(requests.post("https://user.auth.xboxlive.com/user/authenticate", json={"Properties":{"AuthMethod":"RPS", "SiteName":"user.auth.xboxlive.com", "RpsTicket":("d="+t["access_token"])}, "RelyingParty":"http://auth.xboxlive.com", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json={"Properties":{"SandboxId":"RETAIL", "UserTokens":[t["Token"]]}, "RelyingParty":"rp://api.minecraftservices.com/", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json={"identityToken":("XBL3.0 x="+t["DisplayClaims"]["xui"][0]["uhs"]+";"+t["Token"])}).content)
    x = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers={"Authorization":"Bearer "+t["access_token"]})
    if (x.content != b""):
        x = x.json()
        flag = 0
        for i in x["items"]:
            if (i["name"] == "game_minecraft"):
                flag = 1
        if (flag == 0):
            message.grid_forget()
            message = Frame(dialog, borderwidth=30)
            check = Frame(dialog, borderwidth=30)
            ttk.Label(message, text=lang["accounts.noMinecraft"].get(), font=theFont).grid()
            dialog.mainloop()
            return 0
    profile = eval(requests.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization":"Bearer "+t["access_token"]}).content)
    usrName = profile["name"]
    usrId = profile["id"]
    usrSkin = profile["skins"][0]["url"]
    usrSkinId = profile["skins"][0]["id"].replace("-", "")
    usrCapes = profile["capes"]
    accessToken = t["access_token"]
    accounts.append({"usrType": "mojang", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken, "refreshToken": refreshToken})
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()

def createMojangAccount(dialog):
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["accounts.prompt"].get(), font=theFont).grid()
    global entry
    entry = ttk.Entry(message, font=theFont)
    entry.grid()
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (exec("global code;code = entry.get().replace(\"https://login.live.com/oauth20_desktop.srf?code=\", \"\").replace(\"&lc=\", \"\")[:-4]"), message.grid_forget(), check.grid_forget(), processMojang(code, dialog), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
    subprocess.getstatusoutput("explorer \"https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=XboxLive.signin%20offline_access&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf\"")
    message.grid()
    check.grid()
    chTheme(dialog)

def processLegacy(usrName):
    usrId = "4d696e6563726166744d696e65637261"
    usrSkin = ""
    usrSkinId = ""
    accessToken = "${auth_access_token}"
    usrCapes = []
    accounts.append({"usrType": "legacy", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken})
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()

def createLegacyAccount(dialog):
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["accounts.name"].get(), font=theFont).grid()
    global entry
    entry = ttk.Entry(message, font=theFont)
    entry.grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (processLegacy(entry.get()), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)

def createAccount():
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["accounts.type"].get(), font=theFont).grid()
    sel = -1
    myButton(check, text=lang["accounts.type.mojang"].get(), command=lambda: (exec("global sel;sel=0"), message.grid_remove(), check.grid_remove(), createMojangAccount(dialog))).grid(column=1, row=0)
    myButton(check, text=lang["accounts.type.legacy"].get(), command=lambda: (exec("global sel;sel=1"), message.grid_remove(), check.grid_remove(), createLegacyAccount(dialog))).grid(column=2, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (exec("global sel;sel=2"), dialog.destroy())).grid(column=3, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageAccounts()

def pageAccounts():
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)
    buttonArea = Frame(dynamic)
    if (accounts == []): ttk.Label(dynamic, textvariable=lang["accounts.instead"], font=theFont).grid()
    else:
        li = myList(dynamic, width=75, height = 10)
        for i in accounts:
            name = i["usrName"]
            info = lang["accounts.info"].get().replace("%1", lang["accounts.type."+i["usrType"]].get()).replace("%2", i["usrId"])
            li.add(name + " (" + info + ") ")
        li.bind("<Button-3>", lambda x: accountsPopup(x, li.index(ACTIVE)))
        li.activate(selectedAccount)
        li.grid()
        myButton(buttonArea, textvariable=lang["do.accounts"], command=lambda: (exec("global selectedAccount; selectedAccount = "+str(li.index("active"))), pageAccounts())).grid(column=0)
    myButton(buttonArea, textvariable=lang["do.accounts.new"], command=lambda: (createAccount(), pageAccounts())).grid(column=1, row=0)
    col_count, row_count = buttonArea.grid_size()
    for col in range(col_count):
        buttonArea.grid_columnconfigure(col, pad=10)
    accountsPage.pack()
    buttonArea.grid()
    dynamic.pack()
    pageCur = accountsPage
    dynamicCur = dynamic
    chTheme(dynamic)
    try:
        li.update()
    except:
        pass

def setSettings(key, val, dialog, message):
    for w in message.winfo_children():
        if (type(w) == ttk.Entry):
            entry = w
            entry.grid_forget()
            continue
        w.destroy()
    try:
        settings[key]["value"] = int(val)
        cfg["settings"] = settings
        config = open(".river_cfg.py", "w")
        config.write(str(cfg))
        config.close()
        dialog.destroy()
        pageSettings()
    except:
        ttk.Label(message, text=lang["settings.type"].get().replace("%1", lang["settings.type.int"].get()), font=theFont).grid()
        entry.grid()

def editSettings(index):
    cfg["settings"] = settings
    config = open(".river_cfg.py", "w")
    config.write(str(cfg))
    config.close()
    key = list(settings)[index]
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    if (settings[key]["type"] == "static"):
        ttk.Label(message, text=lang["settings.static"].get().replace("%1", lang["sets."+key].get()), font=theFont).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid(column=0, row=0)
        message.grid()
        check.grid()
        dialog.mainloop()
    ttk.Label(message, text=lang["settings.edit"].get().replace("%1", lang["sets."+key].get()), font=theFont).grid()
    if (settings[key]["type"] == "int"):
        entry = ttk.Entry(message, font=theFont)
        entry.grid()
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (setSettings(key, entry.get(), dialog, message))).grid(column=0, row=0)
        myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageSettings())).grid(column=1, row=0)
    if (settings[key]["type"] == "page"):
        pages = ["launch", "downloads", "mods", "accounts", "settings", "language"]
        for i in range(len(pages)):
            x = i
            x = i % 3
            y = int(i-x == 3)
            myButton(check, text=lang["title."+pages[i]].get(), command=lambda x=pages[i]: (exec("global settings\nsettings[key][\"value\"]=\""+x), pageSettings())).grid(column=x, row=y)
        myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageSettings())).grid(column=2, row=2)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=10)
    message.grid()
    check.grid()
    chTheme(dialog)
    pageSettings()

def pageSettings():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)
    listArea = Frame(dynamic)
    buttonArea = Frame(dynamic)
    liK = myList(listArea, width=45, height = 10)
    liV = myList(listArea, width=30, height = 10)
    for i in settings:
        if (settings[i]["type"] == "static"):
            content = settings[i]["value"]
        if (settings[i]["type"] == "int"):
            content = str(settings[i]["value"])
        if (settings[i]["type"] == "page"):
            content = lang["title." + settings[i]["value"]].get()
        liK.add(lang["sets."+i].get())
        liV.add(content)
    liK.grid(column=0, row=0)
    liV.config(state=DISABLED)
    liV.grid(column=1, row=0)
    myButton(buttonArea, textvariable=lang["do.settings"], command=lambda: editSettings(liK.index("active"))).grid()
    settingsPage.pack()
    listArea.grid()
    buttonArea.grid()
    dynamic.pack()
    pageCur = settingsPage
    dynamicCur = dynamic
    chTheme(dynamic)
    liK.update()

def pageLanguage():
    global lang
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = Frame(root)
    langs = os.listdir("assets\\lang")
    for i in langs:
        if (i.startswith("_")):
            langs.remove(i)
    li = myList(dynamic, width=75, height = 10)
    for x in range(len(langs)):
        i = langs[x]
        tmp = open("assets\\lang\\"+i, encoding = "utf-8")
        content = eval(tmp.read())
        li.add(content["lang.name"] + " (" + content["lang.region"] + ") ")
        if (i == (cfg["lang"]+".py")):
            li.activate(x)
        tmp.close()
    languagePage.pack()
    li.grid()
    myButton(dynamic, textvariable=lang["do.language"], command=lambda: switchLang(langs[li.index("active")].replace(".py", ""))).grid()
    dynamic.pack()
    pageCur = languagePage
    dynamicCur = dynamic
    chTheme(dynamic)
    li.update()

if not (noJava):
    if not (os.path.isfile("assets\\java\\B\\bin\\java.exe")):
        config = open(".river_cfg.py", "w")
        config.write(str(cfg))
        config.close()
        thread._start_new_thread(downloadJava, ())

titleImage = PhotoImage(master=root, file=os.getcwd()+"\\assets\\title\\main.png")
tabTitle = ttk.Label(tabs, textvariable=lang["title.main"], borderwidth=30, image=titleImage, compound=TOP, font=("Unifont", 12, "bold"))
tabTitle.grid()
myTab(tabs, textvariable=lang["title.launch"], command=lambda: pageLaunch()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.downloads"], command=lambda: pageDownloads()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.mods"], command=lambda: pageMods()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.accounts"], command=lambda: pageAccounts()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.settings"], command=lambda: pageSettings()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.language"], command=lambda: pageLanguage()).grid(sticky=W)
ttk.Label(launchPage, textvariable=lang["title.launch"], font=theFont).grid(column=1, row=0)
ttk.Label(downloadsPage, textvariable=lang["title.downloads"], font=theFont).grid(column=1, row=0)
ttk.Label(modDownloadsPage, textvariable=lang["title.downloads"], font=theFont).grid(column=1, row=0)
ttk.Label(modsPage, textvariable=lang["title.mods"], font=theFont).grid(column=1, row=0)
ttk.Label(accountsPage, textvariable=lang["title.accounts"], font=theFont).grid(column=1, row=0)
ttk.Label(settingsPage, textvariable=lang["title.settings"], font=theFont).grid(column=1, row=0)
ttk.Label(languagePage, textvariable=lang["title.language"], font=theFont).grid(column=1, row=0)


tabs.pack(side=LEFT, anchor=N)
ttk.Separator(root, orient=VERTICAL).pack(side=LEFT, fill=Y)
for x in [tabs, launchPage, downloadsPage, modDownloadsPage, modsPage, accountsPage, settingsPage, languagePage, fabricPage, optifinePage]:
    col_count, row_count = x.grid_size()
    for col in range(col_count):
        x.grid_columnconfigure(col, pad=7)
    for row in range(row_count):
        x.grid_rowconfigure(row, pad=7)
if (settings["startupPage"]["value"] == "launch"): pageLaunch()
if (settings["startupPage"]["value"] == "downloads"): pageDownloads()
if (settings["startupPage"]["value"] == "mods"): pageMods()
if (settings["startupPage"]["value"] == "accounts"): pageAccounts()
if (settings["startupPage"]["value"] == "settings"): pageSettings()
if (settings["startupPage"]["value"] == "language"): pageLanguage()
thread._start_new_thread(checkNew, (noUpdate, ))
if (helpToProtect == 1):
    global dialogCur
    dialog = Tk("river_dia", "river_dia", " " + lang["main.warn"].get())
    try:
        dialogCur.destroy()
    except:
        pass
    dialogCur = dialog
    dialog.iconbitmap("assets\\title\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = Frame(dialog, borderwidth=30)
    check = Frame(dialog, borderwidth=30)
    ttk.Label(message, text=lang["main.warnContent"].get(), font=theFont).grid()
    myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
    message.grid()
    check.grid()
    chTheme(dialog)
img = offImage
if (darkMode): img = onImage
themeButton = ttk.Label(image = img)
themeButton.bind("<Button-1>", reTheme)
themeButton.place(x=-36, y=0, relx=1)
chTheme(root)
chTheme(dynamicCur)
dialogCur = None
root.mainloop()
