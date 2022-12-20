import os
import time
import json
import sys
import zipfile
import subprocess
try: 
    import requests
except:
    import sys
    print("Downloading necessary libraries! 正在下载必要的库! ")
    subprocess.getstatusoutput(sys.executable + " -m pip install requests -i https://pypi.doubanio.com/simple/")
    import requests
import msvcrt
import threading as thread
import hashlib
import copy
from tkinter import *
from tkinter import ttk


root = Tk("river", "river", " River L... 这是一个彩蛋! 在这的文字会因长度不够被折叠掉而隐藏! ")
root.iconbitmap("G:\\RiverLauncher\\icon.ico")
root.geometry("539x333+100+100")
true = True
false = False
curBuild = 10
builds = {1: "v0.1", 2: "v0.2", 3: "v0.3", 4: "v0.4", 5: "v0.5", 6: "v0.6", 7: "v0.7", 8: "v0.8.0", 9: "v0.8.1", 10: "v0.9"}


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
    targetLang = eval(open("langs\\" + langName + ".py", encoding="utf-8").read())
    for i in targetLang:
        if (type(targetLang[i]) == str): 
            lang[i].set(targetLang[i])
        else:
            lang[i] = targetLang[i]
    root.title(lang["title.main"].get())


def writeLog(obj, end = "\n"):
    log.write(str(obj) + end)
    log.flush()


def get(url, saveIn = None, saveAs = None, hashHex = None):
    if (not saveIn is None):
        if (not saveAs is None):
            filePath = saveIn + "\\" + saveAs
        else:
            filePath = saveIn + "\\" + os.path.split(url)[1]
        if (os.path.exists(filePath)): 
            file = open(filePath, "rb")
            if (hashHex != None):
                if (hashlib.sha1(file.read()).hexdigest() == hashHex):
                    return file.read()
        file = open(filePath, "wb")
        got = requests.get(url).content
        file.write(got)
        file.close()
        return got
    got = requests.get(url).content
    return got


per = 0
def getPer(url, saveIn = None, saveAs = None, hashHex = None):
    global per
    per += 1
    return get(url, saveIn, saveAs, hashHex)


def printEnd(tup):
    for i in tup:
        print(i, end = " ")


helpToProtect = 1
makeDir(".minecraft")
makeDir(".minecraft\\versions")
makeDir(".minecraft\\assets")
makeDir(".minecraft\\libraries")
makeDir(".minecraft\\assets\\indexes")
makeDir(".minecraft\\assets\\objects")
subprocess.getstatusoutput("rmdir .river_tmp /S /Q")
makeDir(".river_tmp")
versions = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
lang = {}
defaultLang = "zh_cn"
targetLang = eval(open("langs\\"+defaultLang+".py", encoding="utf-8").read())
for i in targetLang:
    if (type(targetLang[i]) == str): 
        lang[i] = StringVar(value=targetLang[i])
    else:
        lang[i] = targetLang[i]
defaultCfg = {"lang": defaultLang, "version": curBuild, "latest": eval(versions)["versions"][0]["id"], "accounts": {}, "selectedAccount": 0, "settings": {"downloadRenderDistance": {"value": 7, "type": "int"}, "resolutionWidth": {"value": 1618, "type": "int"}, "resolutionHeight": {"value": 1000, "type": "int"}, "startupPage": {"value": "launch", "type": "page"}, "info": {"value": lang["sets.info.value"].get().replace("%1", builds[curBuild]), "type": "static"}}, "THANKS_FOR": {"Python": "source support", "Tkinter & Ttk": "GUI support", "Minecraft":"game to launch", "PCL & HMCL":"launch bat refrence", "HlHill":"write source code"}}
if (not os.path.isfile(".river_cfg.json")):
    config = open(".river_cfg.json", "w")
    config.write(str(defaultCfg))
    config.close()
    helpToProtect = 1
config = open(".river_cfg.json", "r")
cfg = eval(config.read())
config.close()
log = open(".river_log.txt", "w")
cfg["THANKS_FOR"] = defaultCfg["THANKS_FOR"]
cfg["settings"]["info"]["value"] = lang["sets.info.value"].get().replace("%1", builds[curBuild])
for i in defaultCfg:
    if not (i in cfg):
        cfg[i] = defaultCfg[i]
        helpToProtect = 1
for i in defaultCfg["settings"].keys():
    if not (i in cfg["settings"]):
        cfg["settings"][i] = defaultCfg["settings"][i]
        helpToProtect = 1
try: 
    switchLang(cfg["lang"])
except FileNotFoundError:
    switchLang(defaultLang)
selectedAccount = cfg["selectedAccount"]
settings = cfg["settings"]
accounts = cfg["accounts"]

def launchVersion(versionId):
    if (accounts == {}):
        print(lang["launch.instead"])
        return 1
    cwd = os.getcwd().replace("\\", "\\\\")+"\\"
    versionInfo = json.load(open(".minecraft\\versions\\"+versionId+"\\"+versionId+".json"))
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
                    if (j["os"]["name"] == "windows"):
                        x = 1
                if (j["action"] == "disallow"):
                    if (j["os"]["name"] == "windows"):
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
        except:
            pass
        avalible[theVersion] = libName
    writeLog(avalible)
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
    if (file["complianceLevel"] == 0): 
        gameArg = file["minecraftArguments"]
        jvmArg = ["-cp", "\""+tmp.replace("\\\\", "\\").replace("/", "\\")+"\""]
    if (file["complianceLevel"] == 1): 
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
    if (versionInfo["javaVersion"]["majorVersion"] < 12):output.write("java\\A\\bin\\javaw.exe ")
    if (versionInfo["javaVersion"]["majorVersion"] > 12):output.write("java\\B\\bin\\javaw.exe ")
    output.write("-Dminecraft.client.jar=")
    output.write(cwd+".minecraft\\versions\\"+versionId+"\\"+versionId+".jar")
    if not ("-Djava.library.path" in jvmArg):
        output.write(" -Djava.library.path="+cwd+".minecraft\\versions\\"+versionId+"\\river_natives\\")
    try:
        logging = file["logging"]["client"]
        output.write(" " + logging["argument"].replace("${path}", cwd+".minecraft\\versions\\"+versionId + logging["file"]["id"]))
    except:
        pass
    output.write(" ")
    output.write(jvmArg.replace("-Dos.name=Windows 10", "-Dos.name=\"Windows 10\"").replace("-DFabricMcEmu= net.minecraft.client.main.Main", "-DFabricMcEmu=net.minecraft.client.main.Main"))
    output.write(" "+versionInfo["mainClass"]+" ")
    output.write(gameArg)
    if not ("--width" in gameArg):
        output.write(" --width " + str(settings["resolutionWidth"]["value"]) + " --height " + str(settings["resolutionHeight"]["value"]))
    output.close()
    subprocess.getstatusoutput(".minecraft\\versions\\" + versionId + "\\river_launch.bat")
    print(lang["launch.end"].get())
    return 0


tabs = ttk.Frame(root, padding = 10, width = 40)
launchPage = ttk.Frame(root, padding = 10)
downloadsPage = ttk.Frame(root, padding = 10)
accountsPage = ttk.Frame(root, padding = 10)
settingsPage = ttk.Frame(root, padding = 10)
languagePage = ttk.Frame(root, padding = 10)
fabricPage = ttk.Frame(root, padding = 10)
optifinePage = ttk.Frame(root, padding = 10)
dynamicCur = ttk.Frame(root, padding = 10)
pageCur = launchPage


def checkNew():
    global helpToProtect
    has = 0
    tmp = []
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
        tmp.append(lang["main.update"].get().replace("%1", updateFromVer).replace("%2", builds[curBuild]))
        for i in range(updateFrom, curBuild+1):
            if (updateFrom < i):
                if ((curBuild - updateFrom) > 1):
                    tmp.append(builds[i] + ": ")
                for j,updateContent in enumerate(up[i-1]):
                    tmp.append(str(j+1) + ". " + updateContent + "! ")
    if (cfg["latest"] != eval(versions)["versions"][0]["id"]):
        has = 1
        if (cfg["latest"] != ""): 
            tmp.append(lang["main.new"].get().replace("%1", eval(versions)["versions"][0]["id"]))
            cfg["latest"] = eval(versions)["versions"][0]["id"]
    config = open(".river_cfg.json", "w")
    config.write(str(cfg))
    config.close()
    if (has == 1):
        ttk.Label(x, text=("\n".join(tmp))).grid(column=0, row=0)
        ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (dialog.destroy())).grid(column=1, row=0)
    
def renameVersion(version):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("G:\\RiverLauncher\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["launch.renamePrompt"].get().replace("%1", version)).grid()
    entry = ttk.Entry(message)
    entry.grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (
        os.rename(".minecraft\\versions\\" + version + "\\" + version + ".jar", ".minecraft\\versions\\" + version + "\\" + entry.get() + ".jar"), 
        os.rename(".minecraft\\versions\\" + version + "\\" + version + ".json", ".minecraft\\versions\\" + version + "\\" + entry.get() + ".json"), 
        os.rename(".minecraft\\versions\\" + version, ".minecraft\\versions\\" + entry.get()), 
        dialog.destroy(),
        pageLaunch()
    )).grid(column=0, row=0)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy())).grid(column=1, row=0)
    message.grid()
    check.grid()
    pageLaunch()

def removeVersion(version):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("G:\\RiverLauncher\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["launch.removePrompt"].get()).grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (subprocess.getstatusoutput("rmdir .minecraft\\versions\\" + version + " /S /Q"), dialog.destroy(), pageLaunch())).grid(column=0, row=0)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy())).grid(column=1, row=0)
    message.grid()
    check.grid()
    pageLaunch()

def launchPopup(click, version):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["launch.rename"].get().replace("%1", version), command=lambda: renameVersion(version))
    popup.add_command(label=lang["launch.remove"].get(), command=lambda: removeVersion(version))
    popup.add_command(label=lang["launch.directory"].get(), command=lambda: subprocess.getstatusoutput("explorer .minecraft\\versions\\" + version))
    popup.tk_popup(click.x_root, click.y_root)

def pageLaunch():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=10)
    launch = []
    tmp = os.listdir(".minecraft\\versions")
    for i in tmp:
        if (os.path.isfile(".minecraft\\versions\\"+i+"\\"+i+".json")):
            launch.append(i)
    i = 0
    if (launch == []):
        ttk.Label(dynamic, textvariable=lang["launch.instead"]).grid(column=1, row=2)
    else: 
        li = Listbox(dynamic, width=40, height = 10)
        li.bind("<Button-3>", lambda x: launchPopup(x, li.get("active").split(" (")[0]))
        for i in range(len(launch)):
            versionName = launch[i]
            infoFile = open(".minecraft\\versions\\" + launch[i] + "\\" + launch[i] + ".json")
            info = eval(infoFile.read())
            infoFile.close()
            infos = []
            if ("river_origin" in info): 
                origin = info["river_origin"]
            else:
                origin = versionName
            try: 
                if ("net.fabricmc" in info["libraries"][-1]["name"]):
                    if ("net.fabricmc:intermediary" in info["libraries"][-2]["name"]):
                        origin = info["libraries"][-2]["name"].split(":")[-1]
                    else:
                        origin = "Unknown"
                    infos.append(lang["mod.fabric"].get() + " " + info["libraries"][-1]["name"].split(":")[-1])
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
        ttk.Button(dynamic, textvariable=lang["do.launch"], command=lambda: thread._start_new_thread(launchVersion, (li.get("active").split(" (")[0], ))).grid()
    launchPage.pack()
    dynamic.pack()
    pageCur = launchPage
    dynamicCur = dynamic

def pageDownloads():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=10)
    tmp = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    downloads = eval(tmp)["versions"]
    downloadLatest = eval(tmp)["latest"]
    li = Listbox(dynamic, width=40, height = 10)

    li.pack()
    downloadsPage.pack()
    dynamic.pack()
    pageCur = downloadsPage
    dynamicCur = dynamic

def removeAccount(account):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("G:\\RiverLauncher\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["accounts.removePrompt"].get()).grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (
        accounts.pop(account),
        exec("global cfg;cfg[\"accounts\"] = accounts"), 
        exec("global cfg;cfg[\"selectedAccount\"] = selectedAccount"), 
        exec("global config;config = open(\".river_cfg.json\", \"w\")"), 
        config.write(str(cfg)), 
        config.close(), 
        dialog.destroy(),
        pageAccounts()
    )).grid(column=0, row=0)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy())).grid(column=1, row=0)
    message.grid()
    check.grid()
    pageAccounts()
    
def accountsPopup(click, account):
    popup = Menu(root, tearoff=0)
    popup.add_command(label=lang["accounts.remove"].get().replace("%1", account), command=lambda: removeAccount(account))
    popup.tk_popup(click.x_root, click.y_root) 

def processMojang(code):
    token = eval(requests.get("https://login.live.com/oauth20_token.srf?client_id=00000000402b5328&client_secret=client_secret&code=<CODE>&grant_type=authorization_code&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf".replace("<CODE>", code)).content)
    t = eval(requests.post("https://user.auth.xboxlive.com/user/authenticate", json={"Properties":{"AuthMethod":"RPS", "SiteName":"user.auth.xboxlive.com", "RpsTicket":("d="+token["access_token"])}, "RelyingParty":"http://auth.xboxlive.com", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://xsts.auth.xboxlive.com/xsts/authorize", json={"Properties":{"SandboxId":"RETAIL", "UserTokens":[t["Token"]]}, "RelyingParty":"rp://api.minecraftservices.com/", "TokenType":"JWT"}).content)
    t = eval(requests.post("https://api.minecraftservices.com/authentication/login_with_xbox", json={"identityToken":("XBL3.0 x="+t["DisplayClaims"]["xui"][0]["uhs"]+";"+t["Token"])}).content)
    profile = eval(requests.get("https://api.minecraftservices.com/minecraft/profile", headers={"Authorization":"Bearer "+t["access_token"]}).content)
    usrName = profile["name"]
    usrId = profile["id"]
    usrSkin = profile["skins"][0]["url"]
    usrSkinId = profile["skins"][0]["id"].replace("-", "")
    usrCapes = profile["capes"]
    accessToken = t["access_token"]
    accounts[usrName] = {"usrType": "mojang", "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken}
    cfg["accounts"] = accounts
    cfg["selectedAccount"] = selectedAccount
    config = open(".river_cfg.json", "w") 
    config.write(str(cfg))
    config.close()
        
def createMojangAccount(dialog):
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["accounts.prompt"].get()).grid()
    global entry
    entry = ttk.Entry(message)
    entry.grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (exec("global code;code = entry.get().replace(\"https://login.live.com/oauth20_desktop.srf?code=\", \"\").replace(\"&lc=\", \"\")[:-4]"), processMojang(code), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
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
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["accounts.name"].get()).grid()
    global entry
    entry = ttk.Entry(message)
    entry.grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=lambda: (processLegacy(entry.get()), dialog.destroy(), pageAccounts())).grid(column=0, row=1)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (dialog.destroy(), pageAccounts())).grid(column=1, row=1)
    message.grid()
    check.grid()

def createAccount():
    dialog = Tk("river_dia", "river_dia", " " + lang["main.dialog"].get())
    dialog.iconbitmap("G:\\RiverLauncher\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["accounts.type"].get()).grid()
    sel = -1
    ttk.Button(check, text=lang["accounts.type.mojang"].get(), command=lambda: (exec("global sel;sel=0"), message.grid_remove(), check.grid_remove(), createMojangAccount(dialog))).grid(column=1, row=0)
    ttk.Button(check, text=lang["accounts.type.legacy"].get(), command=lambda: (exec("global sel;sel=1"), message.grid_remove(), check.grid_remove(), createLegacyAccount(dialog))).grid(column=2, row=0)
    ttk.Button(check, text=lang["sel.no"].get(), command=lambda: (exec("global sel;sel=2"), dialog.destroy())).grid(column=3, row=0)
    message.grid()
    check.grid()
    pageAccounts()
    
def pageAccounts():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=10)
    buttonArea = ttk.Frame(dynamic, padding=10)
    if (accounts == {}): ttk.Label(dynamic, textvariable=lang["accounts.instead"]).grid()
    else:
        li = Listbox(dynamic, width=40, height = 10)
        li.bind("<Button-3>", lambda x: accountsPopup(x, li.get("active").split(" (")[0]))
        for i in range(len(accounts.keys())):
            j = accounts[list(accounts)[i]]
            name = j["usrName"]
            info = lang["accounts.info"].get().replace("%1", lang["accounts.type."+j["usrType"]].get()).replace("%2", j["usrId"])
            li.insert(END, name + " (" + info + ") ")
        li.grid()
        ttk.Label(dynamic, text=lang["accounts.current"].get().replace("%1", list(accounts)[selectedAccount])).grid()
        ttk.Button(buttonArea, textvariable=lang["do.accounts"], command=lambda: (exec("global selectedAccount; selectedAccount = "+str(li.index("active"))), pageAccounts())).grid(column=0)
    ttk.Button(buttonArea, textvariable=lang["do.accounts.new"], command=lambda: (createAccount(), pageAccounts())).grid(column=1, row=0)
    accountsPage.pack()
    buttonArea.grid()
    dynamic.pack()
    pageCur = accountsPage
    dynamicCur = dynamic

def pageSettings():
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=10)
    settingsPage.pack()
    pageCur = settingsPage
    dynamicCur = dynamic

def pageLanguage():
    global lang
    global pageCur
    global dynamicCur
    pageCur.pack_forget()
    dynamicCur.pack_forget()
    dynamic = ttk.Frame(root, padding=10)
    langs = os.listdir("langs")
    for i in langs:
        if (i.startswith("_")):
            langs.remove(i)
    li = Listbox(dynamic, width=40, height = 10)
    for x in range(len(langs)):
        i = langs[x]
        tmp = open("langs\\"+i, encoding = "utf-8")
        content = eval(tmp.read())
        li.insert(END, content["lang.name"] + " (" + content["lang.region"] + ") ")
        tmp.close()
    languagePage.pack()
    li.grid()
    ttk.Button(dynamic, textvariable=lang["do.language"], command=lambda: switchLang(langs[li.index("active")].replace(".py", ""))).grid()
    dynamic.pack()
    pageCur = languagePage
    dynamicCur = dynamic

tabTitle = ttk.Label(tabs, textvariable=lang["title.main"], padding=10)
tabTitle.config(font=("微软雅黑", 13, "bold"))
tabTitle.grid()
ttk.Button(tabs, textvariable=lang["title.launch"], command=lambda: pageLaunch()).grid()
ttk.Button(tabs, textvariable=lang["title.downloads"], command=lambda: pageDownloads()).grid()
ttk.Button(tabs, textvariable=lang["title.accounts"], command=lambda: pageAccounts()).grid()
ttk.Button(tabs, textvariable=lang["title.settings"], command=lambda: pageSettings()).grid()
ttk.Button(tabs, textvariable=lang["title.language"], command=lambda: pageLanguage()).grid()
ttk.Label(launchPage, textvariable=lang["title.launch"]).grid(column=1, row=0)
ttk.Label(downloadsPage, textvariable=lang["title.downloads"]).grid(column=1, row=0)
ttk.Label(accountsPage, textvariable=lang["title.accounts"]).grid(column=1, row=0)
ttk.Label(settingsPage, textvariable=lang["title.settings"]).grid(column=1, row=0)
ttk.Label(languagePage, textvariable=lang["title.language"]).grid(column=1, row=0)


tabs.pack(side=LEFT, anchor=N)
ttk.Separator(orient=VERTICAL).pack(side=LEFT, fill=Y)
if (settings["startupPage"]["value"] == "launch"): pageLaunch()
if (settings["startupPage"]["value"] == "downloads"): pageDownloads()
if (settings["startupPage"]["value"] == "accounts"): pageAccounts()
if (settings["startupPage"]["value"] == "settings"): pageSettings()
if (settings["startupPage"]["value"] == "language"): pageLanguage()
checkNew()
if (helpToProtect == 1):
    dialog = Tk("river_dia", "river_dia", " " + lang["main.warn"].get())
    dialog.iconbitmap("G:\\RiverLauncher\\icon.ico")
    dialog.focus_force()
    dialog.resizable(0, 0)
    message = ttk.Frame(dialog, padding=10)
    check = ttk.Frame(dialog, padding=10)
    ttk.Label(message, text=lang["main.warnContent"].get()).grid()
    ttk.Button(check, text=lang["sel.yes"].get(), command=dialog.destroy)
    message.grid()
    check.grid()
root.mainloop()
