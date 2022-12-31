import os
import time
import sys
import zipfile
import subprocess
try: 
    import requests
except:
    print("Downloading necessary libraries! 正在下载必要的库! ")
    subprocess.getstatusoutput(sys.executable + " -m pip install requests -i https://pypi.doubanio.com/simple/")
    import requests
import threading as thread
import hashlib
import json
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)

log = open(".river_log.txt", "w")
webCache = {}


def myMessage(level, message):
    """level: 0-low 1-normal 2-warn 3-dangerous"""

def judge(state, command):
    if (state):
        command()
    else:
        writeLog("judge", "not True: " + str(state))

root = Tk("river", "river", " River L... 这是一个彩蛋! 在这的文字会因长度不够被省略掉而隐藏! ")
root.iconbitmap("icon.ico")
root.geometry("2200x1140+100+100")
def myButton(master, textvariable=None, text="", command=""):
    buttonImage = PhotoImage(master=master, file=os.getcwd()+"\\assets\\control\\button.png")
    buttonImageActive = PhotoImage(master=master, file=os.getcwd()+"\\assets\\control\\buttonActive.png")
    if (textvariable != None): 
        x = ttk.Label(master, textvariable=textvariable, image=buttonImage, compound=CENTER, foreground="white")
    else: 
        x = ttk.Label(master, text=text, image=buttonImage, compound=CENTER, foreground="white")
    x.bind("<Button-1>", lambda event: judge("normal" in str(x.config("state")[4]), command))
    x.bind("<Enter>", lambda event: x.config(image=buttonImageActive))
    x.bind("<Leave>", lambda event: x.config(image=buttonImage))
    return x

def myTab(master, textvariable=None, command=""):
    tabImage = PhotoImage(master=master, file=os.getcwd()+"\\assets\\control\\tab.png")
    tabImageActive = PhotoImage(master=master, file=os.getcwd()+"\\assets\\control\\tabActive.png")
    x = ttk.Label(master, textvariable=textvariable, image=tabImage, compound=CENTER, foreground="white")
    x.bind("<Button-1>", lambda event: judge("normal" in str(x.config("state")[4]), command))
    x.bind("<Enter>", lambda event: x.config(image=tabImageActive))
    x.bind("<Leave>", lambda event: x.config(image=tabImage))
    return x

true = True
false = False
curBuild = 13
builds = {1: "v0.1", 2: "v0.2", 3: "v0.3", 4: "v0.4", 5: "v0.5", 6: "v0.6", 7: "v0.7", 8: "v0.8.0", 9: "v0.8.1", 10: "v0.9", 11: "v0.9.1", 12: "v0.10", 13: "v0.10.1"}


def makeDir(dirName):
    if (not os.path.isdir(dirName)):
        os.makedirs(dirName, mode = 755)
        
def testHash(byte, sha1):
    return hashlib.sha1(byte).hexdigest() == sha1

def sp(string, a, b):
    return string[string.find(a)+len(a):string.find(b)]

def switchLang(langName):
    global lang
    cfg["lang"] = langName
    config = open(".river_cfg.json", "w")
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

def writeLog(logger, content):
    writeContent = "["+str(time.time())[:13]+", "+logger[0].capitalize()+logger[1:]+"] "+content[0].capitalize()+content[1:]
    print(writeContent)
    log.write(writeContent+"\n")
    log.flush()

def get(url, saveIn = None, saveAs = None, hashHex = None):
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
            got = requests.get(url).content
        except:
            writeLog("get", "failed to get: " + url)
            got = ""
        webCache[url] = {"time": time.time(), "content": got}
    if not (os.path.isfile(filePath)):
        if (filePath != ""): 
            file = open(filePath, "wb")
            file.write(got)
            file.close()
    try:
        got = got.decode("utf-8")
    except:
        pass
    return got

global per
per = 0
def getPer(url, saveIn = None, saveAs = None, hashHex = None):
    global per
    per += 1
    return get(url, saveIn, saveAs, hashHex)

global downloadButtonLocked
downloadButtonLocked = 0
helpToProtect = 1
makeDir(".minecraft")
makeDir(".minecraft\\versions")
makeDir(".minecraft\\assets")
makeDir(".minecraft\\libraries")
makeDir(".minecraft\\assets\\indexes")
makeDir(".minecraft\\assets\\objects")
makeDir(".minecraft\\mods")
versions = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
lang = {}
defaultLang = "zh_cn"
targetLang = eval(open("assets\\lang\\"+defaultLang+".py", encoding="utf-8").read())
for i in targetLang:
    if (type(targetLang[i]) == str): 
        lang[i] = StringVar(value=targetLang[i])
    else:
        lang[i] = targetLang[i]
defaultCfg = {"lang": defaultLang, "version": curBuild, "latest": "", "accounts": {}, "selectedAccount": 0, "settings": {"resolutionWidth": {"value": 1618, "type": "int"}, "resolutionHeight": {"value": 1000, "type": "int"}, "startupPage": {"value": "launch", "type": "page"}, "info": {"value": lang["sets.info.value"].get().replace("%1", builds[curBuild]), "type": "static"}}, "THANKS_FOR": {"Python": "source support", "Tkinter & Ttk": "GUI support", "Minecraft":"game to launch", "PCL & HMCL":"launch bat refrence", "HlHill":"write source code"}}
try:
    defaultCfg["latest"] = eval(versions)["versions"][0]["id"]
except:
    writeLog("default config", "failed to get the latest version")
if (not os.path.isfile(".river_cfg.json")):
    config = open(".river_cfg.json", "w")
    config.write(str(defaultCfg))
    config.close()
    helpToProtect = 1
config = open(".river_cfg.json", "r")
cfg = eval(config.read())
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

def launchVersion(versionId):
    if (accounts == {}):
        print(lang["launch.instead"])
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
                .replace("${auth_player_name}", list(accounts)[selectedAccount])
                .replace("${version_name}", versionId)
                .replace("${game_directory}", cwd+".minecraft\\\\")
                .replace("${assets_root}", cwd+".minecraft\\\\assets\\\\")
                .replace("${assets_index_name}", versionInfo["assets"])
                .replace("${auth_uuid}", accounts[list(accounts)[selectedAccount]]["usrId"])
                .replace("${auth_access_token}", accounts[list(accounts)[selectedAccount]]["accessToken"])
                .replace("${auth_session}", accounts[list(accounts)[selectedAccount]]["accessToken"])
                .replace("${user_type}", accounts[list(accounts)[selectedAccount]]["usrType"])
                .replace("${clientId}", accounts[list(accounts)[selectedAccount]]["usrId"])
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
    if ( (not "complianceLevel" in file) or (file["complianceLevel"] == 0) ): 
        gameArg = file["minecraftArguments"]
        jvmArg = ["-cp", "\""+tmp.replace("\\\\", "\\").replace("/", "\\")+"\""]
    if ( ("complianceLevel" in file) and file["complianceLevel"] == 1): 
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
    output.write("\ncd /d " + cwd + "\n")
    if ( (not "javaVersion" in versionInfo) or (versionInfo["javaVersion"]["majorVersion"] < 12) ):output.write("assets\\java\\A\\bin\\java.exe ")
    if ( ("javaVersion" in versionInfo) and (versionInfo["javaVersion"]["majorVersion"] > 12) ):output.write("assets\\java\\B\\bin\\java.exe ")
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
    writeLog("accounts", "relogin account state: "+str(relogin(list(accounts)[selectedAccount])))
    if (flag): 
        launchButton.config(textvariable=lang["do.launch"])
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
    accounts[usrName] = {"usrType": "mojang", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken, "refreshToken": refreshToken}
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.json", "w") 
    config.write(str(cfg))
    config.close()
    return 0


tabs = ttk.Frame(root, width = 40)
launchPage = ttk.Frame(root, padding = 30)
downloadsPage = ttk.Frame(root, padding = 30)
modsPage = ttk.Frame(root, padding = 30)
accountsPage = ttk.Frame(root, padding = 30)
settingsPage = ttk.Frame(root, padding = 30)
languagePage = ttk.Frame(root, padding = 30)
fabricPage = ttk.Frame(root, padding = 30)
optifinePage = ttk.Frame(root, padding = 30)
dynamicCur = ttk.Frame(root, padding = 30)
pageCur = launchPage

def updateLauncher(dialog, index, files):
    for i in files:
        get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/" + i, saveIn = os.path.split(i)[0])
    get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/b" + str(list(index)[-1]) + index[list(index)[-1]]["name"] + ".py", saveAs = "river.py")
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["update.launcher.restart"].get()).grid()
    myButton(check, text=lang["sel.yes"].get(), command=exit).grid()
    message.grid()
    check.grid()
    dialog.mainloop()

def checkNew():
    global helpToProtect
    has = 0
    tmp = []

    try: 
        index = eval(get("https://gitee.com/qiu_yixuan/river-launcher-index/raw/master/index.py"))
        files = index.pop("files")
        if (list(index)[-1] > curBuild):
            tmp.append(lang["update.launcher"].get().replace("%1", index[list(index)[-1]]["name"]))
            for i in range(curBuild+1, list(index)[-1]+1):
                if (curBuild < i):
                    if ((list(index)[-1] - curBuild) > 1):
                        tmp.append(builds[i] + ": ")
                    for j,updateContent in enumerate(index[i]["updateContent"][cfg["lang"]]):
                        tmp.append(str(j+1) + ". " + updateContent + "! ")
            dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
            dialog.iconbitmap("icon.ico")
            dialog.focus_force()
            dialog.resizable(0, 0)
            message = ttk.Frame(dialog, padding=30)
            check = ttk.Frame(dialog, padding=30)
            ttk.Label(message, text=("\n".join(tmp))).grid()
            myButton(check, text=lang["sel.yes"].get(), command=lambda: (
                message.grid_remove(), 
                check.grid_remove(), 
                updateLauncher(dialog, index, files),
                exit()
            )).grid(column=0, row = 1)
            myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row = 1)
            message.grid()
            check.grid()
            dialog.mainloop()
    except:
        writeLog("check new", "failed to check launcher update")

    if (cfg["version"] != curBuild):
        helpToProtect = 1
        has = 1
        updateFrom = cfg["version"]
        updateFromVer = builds[updateFrom]
        cfg["version"] = curBuild
        config = open(".river_cfg.json", "w")
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
        config = open(".river_cfg.json", "w")
        config.write(str(cfg))
        config.close()
        if (has == 1):
            dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
            dialog.iconbitmap("icon.ico")
            dialog.focus_force()
            dialog.resizable(0, 0)
            message = ttk.Frame(dialog, padding=30)
            check = ttk.Frame(dialog, padding=30)
            ttk.Label(message, text=("\n".join(tmp))).grid()
            myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
            message.grid()
            check.grid()
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
        py("rename", "no \"id\" in \"" + dst + ".json\"")
    config.write(str(x))
    config.close()
    
def renameVersion(version):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["launch.renamePrompt"].get().replace("%1", version)).grid()
    entry = ttk.Entry(message)
    entry.grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        processRename(version, entry.get()), 
        dialog.destroy(),
        pageLaunch()
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageLaunch()

def removeVersion(version):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["launch.removePrompt"].get()).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (subprocess.getstatusoutput("rmdir .minecraft\\versions\\" + version + " /S /Q"), dialog.destroy(), pageLaunch())).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageLaunch()

def launchPopup(click, version):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["launch.rename"].get(), command=lambda: renameVersion(version))
    popup.add_command(label=lang["launch.remove"].get(), command=lambda: removeVersion(version))
    popup.add_command(label=lang["launch.directory"].get(), command=lambda: subprocess.getstatusoutput("explorer .minecraft\\versions\\" + version))
    popup.tk_popup(click.x_root, click.y_root)

def pageLaunch():
    global launchButton
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=30)
    launch = []
    tmp = os.listdir(".minecraft\\versions")
    for i in tmp:
        if (os.path.isfile(".minecraft\\versions\\"+i+"\\"+i+".json")):
            launch.append(i)
    i = 0
    if (launch == []):
        ttk.Label(dynamic, textvariable=lang["launch.instead"]).grid(column=1, row=2)
    else: 
        li = Listbox(dynamic, width=50, height = 10)
        li.bind("<Button-3>", lambda x: launchPopup(x, li.get("active").split(" (")[0]))
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
                if ("optifine.OptiFineTweaker" in info["arguments"]["game"]):
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
                infosAll = " (" + ", ".join(infos) + ") "
            li.insert(END, launch[i]+infosAll)
        li.grid()
        launchButton = myButton(dynamic, textvariable=lang["do.launch"], command=lambda: thread._start_new_thread(launchVersion, (li.get("active").split(" (")[0], )))
        launchButton.grid()
    launchPage.pack()
    dynamic.pack()
    pageCur = launchPage
    dynamicCur = dynamic

global downloadConfig
downloadConfig = {"minecraft": "", "minecraft.id": -1, "fabric": "", "optifine": ""}
def editMinecraft(): 
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    minecraft = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    minecraft = eval(minecraft)["versions"]
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)

    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill=Y)
    li = Listbox(message, width=50, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get()).pack()
    for i in minecraft:
        li.insert(END, i["id"])
    li.pack(side=LEFT, fill=BOTH)
    x.config(command=li.yview)
    
    global editMinecraftLi
    editMinecraftLi = li
    
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (exec("global downloadConfig; downloadConfig = {\"minecraft\": editMinecraftLi.get(ACTIVE), \"minecraft.id\": editMinecraftLi.index(ACTIVE), \"fabric\": \"\", \"optifine\": \"\"}"), dialog.destroy(), pageDownloads())).grid(column=0, row=0)
    if (downloadConfig["minecraft"] != ""):
        myButton(check, text=lang["mod.clear"].get(), command=lambda: (exec("global downloadConfig; downloadConfig = {\"minecraft\": \"\", \"minecraft.id\": -1, \"fabric\": \"\", \"optifine\": \"\"}"), pageDownloads(), dialog.destroy())).grid(column=1, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=2, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()

def editFabric(version = ""):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    if (version == ""):
        ttk.Label(message, text=lang["mod.instead"].get()).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0

    fabric = eval(get("https://meta.fabricmc.net/v2/versions/loader/" + version))
    if (fabric == []):
        ttk.Label(message, text=lang["mod.noAvalibleMessage"].get().replace("%1", version)).grid()
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (dialog.destroy())).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill="y")
    li = Listbox(message, width=50, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get()).pack()
    for i in fabric:
        li.insert(END, i["loader"]["version"])
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
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
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
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    if (version == ""):
        ttk.Label(message, text=lang["mod.instead"].get()).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    
    x = get("https://optifine.net/downloads").splitlines()
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
        ttk.Label(message, text=lang["mod.noAvalibleMessage"].get().replace("%1", version)).grid()
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (dialog.destroy())).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    x = ttk.Scrollbar(message)
    x.pack(side=RIGHT, fill="y")
    li = Listbox(message, width=50, height = 10, yscrollcommand=x.set)
    ttk.Label(message, text=lang["mod.select"].get()).pack()
    writeLog("optifine downloader", "allOpti: " + str(allOpti) + "; optifine: " + str(optifine))
    for i in optifine:
        li.insert(END, i[1])
    li.pack(side=LEFT, fill=BOTH)
    x.config(command=li.yview)
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (setOptifine(optifine, li.index(ACTIVE)), dialog.destroy())).grid(column=0, row=0)
    if (downloadConfig["optifine"] != ""):
        myButton(check, text=lang["mod.clear"].get(), command=lambda: (exec("downloadConfig[\"optifine\"] = \"\""), pageDownloads(), dialog.destroy())).grid(column=1, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=dialog.destroy).grid(column=2, row=0)
    message.grid()
    check.grid()

def editDownload(index):
    if (index == 0):
        editMinecraft()
    if (index == 1):
        editFabric(downloadConfig["minecraft"])
    if (index == 2):
        editOptifine(downloadConfig["minecraft"])

def startDownload(customName):
    try:
        pageDownloads()
        flag = 1
    except:
        flag = 0
    if (downloadConfig["minecraft"] == ""):
        dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
        dialog.iconbitmap("icon.ico")
        dialog.focus_force()
        dialog.resizable(0, 0)
        message = ttk.Frame(dialog, padding=30)
        check = ttk.Frame(dialog, padding=30)
        ttk.Label(message, text=lang["mod.instead"].get()).grid()
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
        message.grid()
        check.grid()
        dialog.mainloop()
        return 0
    global per
    global downloadButtonLocked
    downloadButtonLocked = 1
    selectedDownload = downloadConfig["minecraft.id"]
    downloads = eval(get("https://launchermeta.mojang.com/mc/game/version_manifest.json"))["versions"]
    originName = downloadConfig["minecraft"]
    if (customName == ""):
        customName = originName
    makeDir(".minecraft\\versions\\" + customName)
    versionInfo = eval(get(downloads[selectedDownload]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".json")))
    versionInfo["id"] = customName
    versionInfo["river_origin"] = originName
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
            pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.assets"].get()) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        writeLog("downloader", "assets " + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
    while 1:
        if (flag == 1):
            pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.assets"].get()) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        writeLog("downloader", "assets " + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())))
        if (per == len(assetsInfo["objects"].keys())):
            break
    if (flag == 1):
        pageDownloadsButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.assets"].get()))
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
            pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.libraries"].get()) + str(per).zfill(len(str(x))) + "/" + str(x))
    while 1:
        if (flag == 1):
            pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.libraries"].get()) + str(per).zfill(len(str(x))) + "/" + str(x))
        if (per == x):
            break
    if (flag == 1):
        pageDownloadsButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.libraries"].get()))
    writeLog("downloader", "finish libraries")
    # Client
    if (flag == 1):
        pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.client"].get()))
    if ("sha1" in versionInfo["downloads"]["client"]): 
        get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"), hashHex = versionInfo["downloads"]["client"]["sha1"])
    else:
        get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"))
    if (flag == 1):
        pageDownloadsButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.client"].get()))
    writeLog("downloader", "finish client")
    # Logging
    try:
        if (flag == 1):
            pageDownloadsButton.config(text=lang["downloads.downloading"].get().replace("%1", lang["downloads.logging"].get()))
        logging = versionInfo["logging"]["client"]
        get(logging["file"]["url"], saveIn = (".minecraft\\versions\\" + customName))
        if (flag == 1):
            pageDownloadsButton.config(text=lang["downloads.finish"].get().replace("%1", lang["downloads.logging"].get()))
        writeLog("downloader", "finish logging file")
    except:
        writeLog("downloader", "no logging file")
    if (flag == 1):
        pageDownloadsButton.config(text=lang["do.downloads"].get())
    downloadButtonLocked = 0
    if (flag == 1):
        pageDownloads()

if (len(sys.argv) != 1):
    arg = sys.argv[1:]
    for i in range(len(arg)):
        arg[i] = arg[i].replace("\"", "")
    for i in range(3):
        arg.append("")
    writeLog("pre-parse", "arg: " + str(arg))
    if ( (arg[0] == "help") or
         (arg[0] == "h")
         ):
        print(lang["main.usage"].get())
    if (arg[0] == "launch"): 
        root.destroy()
        launchVersion(arg[1])
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
    dynamic = ttk.Frame(root, padding=30)

    message = ttk.Frame(dynamic)
    listArea = ttk.Frame(dynamic)
    buttonArea = ttk.Frame(dynamic)
    entry = ttk.Entry(message)
    liK = Listbox(listArea, width=20, height = 10)
    liV = Listbox(listArea, width=30, height = 10, disabledforeground="black")
    if (downloadConfig["minecraft"] != ""): 
        fabric = eval(get("https://meta.fabricmc.net/v2/versions/loader/" + downloadConfig["minecraft"]))
    else:
        fabric = []
    # Minecraft
    i = "minecraft"
    liK.insert(END, lang["mod."+i].get())
    if (downloadConfig[i] == ""): 
        liV.insert(END, lang["mod.none"].get())
    else: 
        liV.insert(END, downloadConfig[i])
    # Fabric
    i = "fabric"
    liK.insert(END, lang["mod."+i].get())
    if (downloadConfig["minecraft"] == ""): 
        liV.insert(END, lang["mod.none"].get())
    elif (fabric == []):
        liV.insert(END, lang["mod.noAvalible"].get())
    elif (downloadConfig[i] == ""): 
        liV.insert(END, lang["mod.none"].get())
    else:
        liV.insert(END, downloadConfig[i])
    # Optifine
    i = "optifine"
    liK.insert(END, lang["mod."+i].get())
    if (downloadConfig["minecraft"] == ""): 
        liV.insert(END, lang["mod.none"].get())
    #elif (downloadConfig["fabric"] != ""):
        #liV.insert(END, lang["mod.notCompatible"].get().replace("%1", lang["mod.fabric"].get()))
    elif (downloadConfig[i] == ""): 
        liV.insert(END, lang["mod.none"].get())
    else:
        liV.insert(END, downloadConfig[i][0])

    liK.grid(column=0, row=0)
    liV.config(state=DISABLED)
    liV.grid(column=1, row=0)
    ttk.Label(message, text=lang["downloads.custom"].get()).grid()
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
        buttonArea.grid_columnconfigure(col, pad=30)

    listArea.grid()
    message.grid()
    buttonArea.grid()
    downloadsPage.pack()
    dynamic.pack()
    pageCur = downloadsPage
    dynamicCur = dynamic

def changeMod(name, index):
    if (name.endswith(lang["mods.disabled"].get())):
        disabled = 1
        oldName = name.replace(lang["mods.disabled"].get(), ".jar.disabled")
        name = name.replace(lang["mods.disabled"].get(), ".jar")
    else:
        disabled = 0
        oldName = name + ".jar"
        name = name + ".jar.disabled"
    os.rename(".minecraft\\mods\\"+oldName, ".minecraft\\mods\\"+name)
    pageMods(index)

def changeModAll(mode, index):
    mods = os.listdir(".minecraft\\mods")
    for i in mods:
        name = i
        disabled = 0
        if (name.endswith(".disabled")):
            disabled = 1
        name = ".".join(name.replace(".disabled", "").split(".")[:-1])
        if (disabled):
            name += lang["mods.disabled"].get()
            
        if (name.endswith(lang["mods.disabled"].get())):
            disabled = 1
        else:
            disabled = 0
        if (mode == 0):
            if (disabled == 1):
                changeMod(name, index)
        if (mode == 1):
            if (disabled == 0):
                changeMod(name, index)

def processRemoveMod(name):
    if (name.endswith(lang["mods.disabled"].get())):
        disabled = 1
        oldName = name.replace(lang["mods.disabled"].get(), ".jar.disabled")
    else:
        disabled = 0
        oldName = name + ".jar"
    os.remove(".minecraft\\mods\\"+oldName)
    pageDownloads()

def removeMod(name):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["mods.removePrompt"].get()).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        processRemoveMod(name), 
        dialog.destroy(),
        pageMods()
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageMods()

def modsPopup(click, mod):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["mods.remove"].get(), command=lambda: removeMod(mod))
    popup.add_command(label=lang["mods.directory"].get(), command=lambda: subprocess.getstatusoutput("explorer .minecraft\\mods"))
    popup.tk_popup(click.x_root, click.y_root) 

def pageMods(sel=None): 
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=30)
    
    message = ttk.Frame(dynamic)
    check = ttk.Frame(dynamic)
    li = Listbox(message, width=50, height=10)
    li.bind("<Button-3>", lambda x: modsPopup(x, li.get("active")))
    if ( ("mods" in os.listdir(".minecraft\\")) and (os.listdir(".minecraft\\mods") != []) ): 
        for i in os.listdir(".minecraft\\mods"):
            name = i
            disabled = 0
            if (name.endswith(".disabled")):
                disabled = 1
            name = ".".join(name.replace(".disabled", "").split(".")[:-1])
            if (disabled):
                name += lang["mods.disabled"].get()
            li.insert(END, name)
        if not (sel is None):
            li.activate(sel)
            li.select_set(sel)
        li.grid()
    else:
        ttk.Label(message, text=lang["mods.instead"].get()).grid()
    myButton(check, text=lang["do.mods"].get(), command=lambda: changeMod(li.get(ACTIVE), li.index(ACTIVE))).grid(column=1, row=0)
    myButton(check, text=lang["do.mods.all.on"].get(), command=lambda: changeModAll(0, li.index(ACTIVE))).grid(column=0, row=0)
    myButton(check, text=lang["do.mods.all.off"].get(), command=lambda: changeModAll(1, li.index(ACTIVE))).grid(column=2, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    modsPage.pack()
    dynamic.pack()
    pageCur = modsPage
    dynamicCur = dynamic

def removeAccount(account):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["accounts.removePrompt"].get()).grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (
        accounts.pop(account),
        exec("global cfg;cfg[\"accounts\"] = accounts"), 
        exec("global cfg;cfg[\"selectedAccount\"] = selectedAccount"), 
        exec("global config;config = open(\".river_cfg.json\", \"w\")"), 
        config.write(str(cfg)), 
        config.close(), 
        dialog.destroy(),
        pageAccounts()
    )).grid(column=0, row=0)
    myButton(check, text=lang["sel.no"].get(), command=dialog.destroy).grid(column=1, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageAccounts()
    
def accountsPopup(click, account):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["accounts.remove"].get(), command=lambda: removeAccount(account))
    popup.tk_popup(click.x_root, click.y_root) 

def processMojang(code, dialog):
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["accounts.loading"].get()).grid()
    message.grid()
    t = eval(requests.get("https://login.live.com/oauth20_token.srf?client_id=00000000402b5328&client_secret=client_secret&code=<CODE>&grant_type=authorization_code&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf".replace("<CODE>", code)).content)
    refreshToken = t["refresh_token"]
    t = eval(requests.post("https://user.auth.xboxlive.com/user/authenticate", json={"Properties":{"AuthMethod":"RPS", "SiteName":"user.auth.xboxlive.com", "RpsTicket":("d="+t["access_token"])}, "RelyingParty":"http://auth.xboxlive.com", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json={"Properties":{"SandboxId":"RETAIL", "UserTokens":[t["Token"]]}, "RelyingParty":"rp://api.minecraftservices.com/", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json={"identityToken":("XBL3.0 x="+t["DisplayClaims"]["xui"][0]["uhs"]+";"+t["Token"])}).content)
    x = requests.get("https://api.minecraftservices.com/entitlements/mcstore", headers={"Authorization":"Bearer "+t["access_token"]}).content
    if (x != b""):
        x = x.json()
        flag = 0
        for i in x["items"]:
            if (i["name"] == "game_minecraft"):
                flag = 1
        if (flag == 0): 
            message.grid_forget()
            message = ttk.Frame(dialog, padding=30)
            check = ttk.Frame(dialog, padding=30)
            ttk.Label(message, text=lang["accounts.noMinecraft"].get()).grid()
            dialog.mainloop()
            return 0
    profile = eval(requests.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization":"Bearer "+t["access_token"]}).content)
    usrName = profile["name"]
    usrId = profile["id"]
    usrSkin = profile["skins"][0]["url"]
    usrSkinId = profile["skins"][0]["id"].replace("-", "")
    usrCapes = profile["capes"]
    accessToken = t["access_token"]
    accounts[usrName] = {"usrType": "mojang", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken, "refreshToken": refreshToken}
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.json", "w") 
    config.write(str(cfg))
    config.close()
        
def createMojangAccount(dialog):
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["accounts.prompt"].get()).grid()
    global entry
    entry = ttk.Entry(message)
    entry.grid()
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (exec("global code;code = entry.get().replace(\"https://login.live.com/oauth20_desktop.srf?code=\", \"\").replace(\"&lc=\", \"\")[:-4]"), message.grid_forget(), check.grid_forget(), processMojang(code, dialog), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
    subprocess.getstatusoutput("explorer \"https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=XboxLive.signin%20offline_access&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf\"")
    message.grid()
    check.grid()

def processLegacy(usrName):
    usrId = "4d696e6563726166744d696e65637261"
    usrSkin = ""
    usrSkinId = ""
    accessToken = "${auth_access_token}"
    usrCapes = []
    accounts[usrName] = {"usrType": "legacy", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken}
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.json", "w") 
    config.write(str(cfg))
    config.close()
    
def createLegacyAccount(dialog):
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["accounts.name"].get()).grid()
    global entry
    entry = ttk.Entry(message)
    entry.grid()
    myButton(check, text=lang["sel.yes"].get(), command=lambda: (processLegacy(entry.get()), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()

def createAccount():
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["accounts.type"].get()).grid()
    sel = -1
    myButton(check, text=lang["accounts.type.mojang"].get(), command=lambda: (exec("global sel;sel=0"), message.grid_remove(), check.grid_remove(), createMojangAccount(dialog))).grid(column=1, row=0)
    myButton(check, text=lang["accounts.type.legacy"].get(), command=lambda: (exec("global sel;sel=1"), message.grid_remove(), check.grid_remove(), createLegacyAccount(dialog))).grid(column=2, row=0)
    myButton(check, text=lang["sel.cancel"].get(), command=lambda: (exec("global sel;sel=2"), dialog.destroy())).grid(column=3, row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageAccounts()

def pageAccounts():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root)
    buttonArea = ttk.Frame(dynamic)
    if (accounts == {}): ttk.Label(dynamic, textvariable=lang["accounts.instead"]).grid()
    else:
        li = Listbox(dynamic, width=50, height = 10)
        li.bind("<Button-3>", lambda x: accountsPopup(x, li.get("active").split(" (")[0]))
        for i in range(len(accounts.keys())):
            j = accounts[list(accounts)[i]]
            name = j["usrName"]
            info = lang["accounts.info"].get().replace("%1", lang["accounts.type."+j["usrType"]].get()).replace("%2", j["usrId"])
            li.insert(END, name + " (" + info + ") ")
        li.grid()
        ttk.Label(dynamic, text=lang["accounts.current"].get().replace("%1", list(accounts)[selectedAccount])).grid()
        myButton(buttonArea, textvariable=lang["do.accounts"], command=lambda: (exec("global selectedAccount; selectedAccount = "+str(li.index("active"))), pageAccounts())).grid(column=0)
    myButton(buttonArea, textvariable=lang["do.accounts.new"], command=lambda: (createAccount(), pageAccounts())).grid(column=1, row=0)
    col_count, row_count = buttonArea.grid_size()
    for col in range(col_count):
        buttonArea.grid_columnconfigure(col, pad=30)
    accountsPage.pack()
    buttonArea.grid()
    dynamic.pack()
    pageCur = accountsPage
    dynamicCur = dynamic

def editSettings(index):
    global key
    key = list(settings)[index]
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    if (settings[key]["type"] == "static"):
        ttk.Label(message, text=lang["settings.static"].get().replace("%1", lang["sets."+key].get())).grid()  
        myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid(column=0, row=0)
        message.grid()
        check.grid()
        dialog.mainloop()
    ttk.Label(message, text=lang["settings.edit"].get().replace("%1", lang["sets."+key].get())).grid()
    if (settings[key]["type"] == "int"):
        global entry
        global vals
        global editSettingsDialog
        global editSettingsMessage
        editSettingsDialog = dialog
        editSettingsMessage = message
        entry = ttk.Entry(message)
        entry.grid()
        global hasTo
        hasTo = 0
        myButton(check, text=lang["sel.yes"].get(), command=lambda: (
            exec("try: int(entry.get())\nexcept: \n    global editSettingsLabel\n    editSettingsLabel = ttk.Label(editSettingsDialog)\n    editSettingsLabel.grid_remove()\n    editSettingsLabel = ttk.Label(editSettingsMessage, text=lang[\"settings.type\"].get().replace(\"%1\", lang[\"settings.type.int\"].get()))\n    editSettingsLabel.grid()\n    hasTo = 1"), 
            exec("if (hasTo == 0): \n    global settings\n    settings[key][\"value\"] = int(entry.get())\n    editSettingsDialog.destroy()\n    pageSettings()\n    global cfg\n    global settings\n    cfg[\"settings\"]=settings\n    config = open(\".river_cfg.json\", \"w\")\n    config.write(str(cfg))\n    config.close()")
        )).grid(column=0, row=0)
    if (settings[key]["type"] == "page"):
        pages = ["launch", "downloads", "mods", "accounts", "settings", "language"]
        for i in range(len(pages)): 
            myButton(check, text=lang["title."+pages[i]].get(), command=lambda x=pages[i]: (
                exec("global settings\nsettings[key][\"value\"]=\""+x+"\"\nglobal cfg\ncfg[\"settings\"] = settings\nglobal config\nconfig = open(\".river_cfg.json\", \"w\")"),
                config.write(str(cfg)), 
                config.close(), 
                dialog.destroy(),
                pageSettings()
            )).grid(column=i, row=0)
    myButton(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy(), pageSettings())).grid(column=len(pages), row=0)
    col_count, row_count = check.grid_size()
    for col in range(col_count):
        check.grid_columnconfigure(col, pad=30)
    message.grid()
    check.grid()
    pageSettings()

def pageSettings():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=30)
    listArea = ttk.Frame(dynamic)
    buttonArea = ttk.Frame(dynamic)
    liK = Listbox(listArea, width=30, height = 10)
    liV = Listbox(listArea, width=20, height = 10, disabledforeground="black")
    for i in settings:
        if (settings[i]["type"] == "static"): 
            content = settings[i]["value"]
        if (settings[i]["type"] == "int"): 
            content = str(settings[i]["value"])
        if (settings[i]["type"] == "page"): 
            content = lang["title." + settings[i]["value"]].get()
        liK.insert(END, lang["sets."+i].get())
        liV.insert(END, content)
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

def pageLanguage():
    global lang
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=30)
    langs = os.listdir("assets\\lang")
    for i in langs:
        if (i.startswith("_")):
            langs.remove(i)
    li = Listbox(dynamic, width=50, height = 10)
    for x in range(len(langs)):
        i = langs[x]
        tmp = open("assets\\lang\\"+i, encoding = "utf-8")
        content = eval(tmp.read())
        li.insert(END, content["lang.name"] + " (" + content["lang.region"] + ") ")
        tmp.close()
    languagePage.pack()
    li.grid()
    myButton(dynamic, textvariable=lang["do.language"], command=lambda: switchLang(langs[li.index("active")].replace(".py", ""))).grid()
    dynamic.pack()
    pageCur = languagePage
    dynamicCur = dynamic

titleImage = PhotoImage(master=root, file=os.getcwd()+"\\assets\\title\\main.png")
tabTitle = ttk.Label(tabs, textvariable=lang["title.main"], padding=30, image=titleImage, compound=TOP)
tabTitle.config(font=("微软雅黑", 13, "bold"))
tabTitle.grid()
myTab(tabs, textvariable=lang["title.launch"], command=lambda: pageLaunch()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.downloads"], command=lambda: pageDownloads()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.mods"], command=lambda: pageMods()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.accounts"], command=lambda: pageAccounts()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.settings"], command=lambda: pageSettings()).grid(sticky=W)
myTab(tabs, textvariable=lang["title.language"], command=lambda: pageLanguage()).grid(sticky=W)
ttk.Label(launchPage, textvariable=lang["title.launch"]).grid(column=1, row=0)
ttk.Label(downloadsPage, textvariable=lang["title.downloads"]).grid(column=1, row=0)
ttk.Label(modsPage, textvariable=lang["title.mods"]).grid(column=1, row=0)
ttk.Label(accountsPage, textvariable=lang["title.accounts"]).grid(column=1, row=0)
ttk.Label(settingsPage, textvariable=lang["title.settings"]).grid(column=1, row=0)
ttk.Label(languagePage, textvariable=lang["title.language"]).grid(column=1, row=0)


tabs.pack(side=LEFT, anchor=N)
ttk.Separator(orient=VERTICAL).pack(side=LEFT, fill=Y)
for x in [tabs, launchPage, downloadsPage, modsPage, accountsPage, settingsPage, languagePage, fabricPage, optifinePage]:
    col_count, row_count = x.grid_size()
    for col in range(col_count):
        x.grid_columnconfigure(col, pad=20)
    for row in range(row_count):
        x.grid_rowconfigure(row, pad=20)
if (settings["startupPage"]["value"] == "launch"): pageLaunch()
if (settings["startupPage"]["value"] == "downloads"): pageDownloads()
if (settings["startupPage"]["value"] == "mods"): pageMods()
if (settings["startupPage"]["value"] == "accounts"): pageAccounts()
if (settings["startupPage"]["value"] == "settings"): pageSettings()
if (settings["startupPage"]["value"] == "language"): pageLanguage()
checkNew()
if (helpToProtect == 1):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.warn"].get())
    dialog.iconbitmap("icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=30)
    check = ttk.Frame(dialog, padding=30)
    ttk.Label(message, text=lang["main.warnContent"].get()).grid()
    myButton(check, text=lang["sel.yes"].get(), command=dialog.destroy).grid()
    message.grid()
    check.grid()
root.mainloop()
