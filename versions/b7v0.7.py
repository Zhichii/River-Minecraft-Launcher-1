import os
import time
import json
import sys
import zipfile
import requests
import msvcrt
import threading as thread
import hashlib


true = True
false = False
curBuild = 7
builds = {1: "v0.1", 2: "v0.2", 3: "v0.3", 4: "v0.4", 5: "v0.5", 6: "v0.6", 7: "v0.7"}


def makeDir(dirName):
    if (not os.path.isdir(dirName)):
        os.makedirs(dirName, mode = 755)


def testHash(byte, sha1):
    return hashlib.sha1(byte).hexdigest() == sha1


def sp(string, a, b):
    return string[string.find(a)+len(a):string.find(b)]
    

#prepare
makeDir(".minecraft")
makeDir(".minecraft\\versions")
makeDir(".minecraft\\assets")
makeDir(".minecraft\\libraries")
makeDir(".minecraft\\assets\\indexes")
makeDir(".minecraft\\assets\\objects")
lang = eval(open("langs\\en.json", encoding="utf-8").read())
defaultCfg = {"lang": "en", "version": curBuild, "latest": "", "accounts": {}, "selectedAccount": 0, "selectedLaunch": 0, "settings": {"downloadRenderDistance": {"value": 7, "type": "int"}, "resolutionWidth": {"value": 1618, "type": "int"}, "resolutionHeight": {"value": 1000, "type": "int"}, "info": {"value": lang["sets.info.value"].replace("%1", builds[curBuild]), "type": "static"}}, "THANKS_FOR": {"Python": "source support", "Minecraft":"game to launch", "PCL & HMCL":"launch bat refrence", "HlHill":"write source code"}}
if (not os.path.isfile(".river_cfg.json")):
    config = open(".river_cfg.json", "w")
    config.write(str(defaultCfg))
    config.close()
config = open(".river_cfg.json", "r")
cfg = eval(config.read())
config.close()
log = open(".river_log.txt", "w")
for i in defaultCfg:
    if not (i in cfg):
        cfg[i] = defaultCfg[i]
lang = eval(open("langs\\" + cfg["lang"] + ".json", encoding="utf-8").read())
    

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


def getTerminalSize():
    return os.get_terminal_size()


def showTitle(title):
    size = (getTerminalSize().columns-len(title))//2
    os.system("cls")
    os.system("title " + lang["title.main"])
    print(" "*size + title, end = "\n\n")


def makeLaunch(versionId):
    if (accounts == {}):
        print(lang["launch.instead"])
        return 1
    cwd = os.getcwd().replace("\\", "\\\\")+"\\"
    versionInfo = json.load(open(".minecraft\\versions\\"+versionId+"\\"+versionId+".json"))
    libraries = versionInfo['libraries']
    libs = []
    launch = []
    tmp = []
    for i in libraries:
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
                    tmp.append(cwd + ".minecraft\\\\libraries\\\\" + libDir.replace("/", "\\\\") + "\\\\" + libSFName)
                continue
        if ("rules" in i):
            try:
                flag = 0
                for j in i["rules"]:
                    if ("os" in j):
                        if ((j["os"]["name"] == "osx") and (j["action"] == "allow")):
                            flag = 1
                            break
                if (flag): continue
            except:
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
        tmp.append(libName)
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
                .replace("${launcher_name}", "River")
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
                            jvmArg.append(j)
    jvmArg = " ".join(jvmArg)
    output = open(".minecraft\\versions\\"+versionId+"\\river_launch.bat", "w")
    output.write("@echo off\n")
    output.write("cd /d " + cwd + "\n")
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
    return 0


def pageFabric(version):
    sel = 0
    loaders = eval(requests.get("https://meta.fabricmc.net/v2/versions/loader/" + version).content)
    if (loaders == []):
        return 0
    while 1:
        if (sel == 0): print(lang["fabric.prompt"].replace("%1", lang["sel.yes"]), end = "")
        if (sel == 1): print(lang["fabric.prompt"].replace("%1", lang["sel.no"]), end = "")
        tmp = msvcrt.getch()
        if (tmp == b'x'):
            return 0
        if (tmp == b'a'):
            if (sel != 0):
                sel -= 1
        if (tmp == b'd'):
            if (sel != 1):
                sel += 1
        if (tmp == b' '):
            if (sel == 0):
                break
            else:
                return 0
    selectedLoader = 0
    while 1:
        showTitle(lang["title.modify"].replace("%1", lang["mod.fabric"]))
        for i in range(selectedLoader, selectedLoader + settings["downloadRenderDistance"]["value"]):
            if (i >= len(loaders)):
                break
            if (i == selectedLoader):
                print(" [", end = "")
            else:
                print("  ", end = "")
            print(loaders[i]["loader"]["version"], end = "")
            if (i == selectedLoader):
                print("] ")
            else:
                print("  ")
        press = msvcrt.getch()
        if (press == b'w'):
            if (selectedLoader != 0):
                selectedLoader -= 1
        if (press == b's'):
            if (selectedLoader != len(loaders)-1):
                selectedLoader += 1
        if (press == b' '):
            loader = loaders[selectedLoader]["loader"]["version"]
            break
        if (press == b'x'):
            return 0
    return eval(requests.get("https://meta.fabricmc.net/v2/versions/loader/" + version + "/" + loader + "/profile/json").content)


def pageOptifine(version):
    return 0
"""
    x = requests.get("https://optifine.net/downloads").content.decode("utf-8").splitlines()
    optifine = []
    wrappers = []
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
            curTmp[3] = sp(x[i], "<td class='colForge'>Forge ", "</td>")
            optifine.append(curTmp)
            curTmp = ["", 0, 0, 0]
    for i in optifine:
        if (i[0] == version):
            wrappers.append(i)
    if (wrappers == []):
        return 0
    sel = 0
    while 1:
        if (sel == 0): print(lang["optifine.prompt"].replace("%1", lang["sel.yes"]), end = "")
        if (sel == 1): print(lang["optifine.prompt"].replace("%1", lang["sel.no"]), end = "")
        tmp = msvcrt.getch()
        if (tmp == b'x'):
            return 0
        if (tmp == b'a'):
            if (sel != 0):
                sel -= 1
        if (tmp == b'd'):
            if (sel != 1):
                sel += 1
        if (tmp == b' '):
            if (sel == 0):
                break
            else:
                return 0
    selectedWrapper = 0
    while 1:
        showTitle(lang["title.modify"].replace("%1", lang["mod.optifine"]))
        for i in range(selectedWrapper, selectedWrapper + settings["downloadRenderDistance"]["value"]):
            if (i >= len(wrappers)):
                break
            if (i == selectedWrapper):
                print(" [", end = "")
            else:
                print("  ", end = "")
            print(wrappers[i][0], end = "")
            if (i == selectedWrapper):
                print("] ")
            else:
                print("  ")
        press = msvcrt.getch()
        if (press == b'w'):
            if (selectedWrapper != 0):
                selectedWrapper -= 1
        if (press == b's'):
            if (selectedWrapper != len(wrappers)-1):
                selectedWrapper += 1
        if (press == b' '):
            wrapper = wrappers[selectedWrapper]
            get(wrapper[2], saveIn = ".minecaft\\libraries\\optifine\\Optifine")
            break
        if (press == b'x'):
            return 0
    if (wrapper[2].startswith("http://optifine.net/adloadx?f=preview_OptiFine_")):
        wrapperName = sp(wrapper[2], "http://optifine.net/adloadx?f=preview_OptiFine_", ".jar")
    elif (wrapper[2].startswith("http://optifine.net/adloadx?f=OptiFine_")):
        wrapperName = sp(wrapper[2], "http://optifine.net/adloadx?f=OptiFine_", ".jar")
    else:
        writeLog("Unable to split optifine " + str(wrapper))
        raise ValueError("Unable to split optifine" + str(wrapper))
    zipFile = zipfile.ZipFile(".minecraft\\libraries\\optifine\\Optifine\\" + wrapperName + ".jar")
    x = zipFile.filelist
    flag = 0
    for i in x:
        y = i.filename
        if ("launchewraooer" in y):
            if (".jar" in y):
                wrapperLaunch = y.filename
                wrapperLaunch = wrapperLaunch.split("-")
                wrapperLaunch
                zipFile.extract(wrapperLaunch, ".minecraft\\libraries\\optifine\\")
                flag = 1
                break
    if (flag == 0): 
        return (wrapperName, )
    if (flag == 1):
        return (wrapperName, wrapperLaunch)
"""


downloads = []
downloadLatest = None
selectedDownload = 0
def pageDownloads():
    global per
    global downloads
    global downloadLatest
    global selectedDownload
    tmp = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
    downloads = eval(tmp)["versions"]
    downloadLatest = eval(tmp)["latest"]
    while 1:
        showTitle(lang["title.downloads"])
        if (downloadLatest["release"] == downloadLatest["snapshot"]):
            print(lang["downloads.latest"].replace("%1", downloadLatest["release"]))
        else: 
            print(lang["downloads.latests"].replace("%1", downloadLatest["release"]).replace("%2", downloadLatest["snapshot"]))
        for i in range(selectedDownload, selectedDownload + settings["downloadRenderDistance"]["value"]):
            if (i >= len(downloads)): break
            theTime = downloads[i]["releaseTime"].replace("T", ".").replace("+00:00", "").replace("-", ".").replace(":", ".").split(".")
            tl = []
            for j in range(6):
                tl.append(int(theTime[j]))
            if (i == selectedDownload): print("[ ", end = "")
            else: print("  ", end = "")
            print(str(i).zfill(2), end = "   ")
            releaseTime = time.mktime((tl[0], tl[1], tl[2], tl[3], tl[4], tl[5], 0, 0, 0)) - time.timezone
            writeLog(downloads[i])
            writeLog(releaseTime)
            RT = time.localtime(releaseTime)
            print(lang["downloads.date"].replace("%1", str(RT.tm_year)).replace("%2", str(RT.tm_mon).zfill(2)).replace("%3", str(RT.tm_mday).zfill(2)).replace("%4", str(RT.tm_hour).zfill(2)).replace("%5", str(RT.tm_min).zfill(2)).replace("%6", str(RT.tm_sec).zfill(2)), end = "   ")
            print(lang["downloads.type."+downloads[i]["type"]] + downloads[i]["id"], end = "   ")
            if (i == selectedDownload): print(" ]", end = "")
            else: print("  ", end = "")
            print()
        print(lang["help.downloads"])
        press = msvcrt.getch()
        if (press == b'x'):
            return 0
        if (press == b'w'):
            if ((selectedDownload - 1) >= 0):
                selectedDownload -= 1
        if (press == b's'):
            if ((selectedDownload + 1) < len(downloads)):
                selectedDownload += 1
        if (press == b'i'):
            versionId = downloads[selectedDownload]["id"]
            versionId = versionId.replace("-pre", "_Pre-release_").replace("-rc", "_Release_Candidate_")
            if (versionId.startswith("rd-")):
                versionId = "_pre-Classic_rd-" + versionId[3:]
            if (versionId.startswith("a")):
                versionId = "Alpha_" + versionId[1:]
            if (versionId.startswith("b")):
                versionId = "Beta_" + versionId[1:]
            os.system("explorer \"https://minecraft.fandom.com/Java_Edition_" + versionId + "\"")
        if (press == b'g'):
            goto = input(lang["downloads.goto"])
            simillar = []
            done = 0
            for i in range(len(downloads)):
                if (downloads[i]["id"].startswith(goto)): simillar.append(downloads[i]["id"])
                if (downloads[i]["id"] == goto):
                    done = 1
                    selectedDownload = i
            if (done == 0):
                print(lang["downloads.unable"].replace("%1", goto) + (lang["downloads.another"].replace("%2", ", ".join(simillar))) * (simillar != []))
                msvcrt.getch()
        if (press == b' '):
            sel = 0
            yes = 0
            while 1:
                if (sel == 0): print(lang["downloads.prompt"].replace("%1", downloads[selectedDownload]["id"]).replace("%2", lang["sel.yes"]), end = "")
                if (sel == 1): print(lang["downloads.prompt"].replace("%1", downloads[selectedDownload]["id"]).replace("%2", lang["sel.no"]), end = "")
                tmp = msvcrt.getch()
                if (tmp == b'a'):
                    if (sel != 0):
                        sel -= 1
                if (tmp == b'd'):
                    if (sel != 1):
                        sel += 1
                if (tmp == b' '):
                    print()
                    if (sel == 1):
                        break
                    else:
                        yes = 1
                        break
                if (tmp == b'x'):
                    break
            if (yes == 1):
                customName = input(lang["downloads.custom"])
                originName = downloads[selectedDownload]["id"]
                fabric = pageFabric(originName)
                makeDir(".minecraft\\versions\\" + customName)
                versionInfo = eval(get(downloads[selectedDownload]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".json")))
                versionInfo["id"] = customName
                if (fabric != 0): 
                    versionInfo["releaseTime"] = fabric["releaseTime"]
                    versionInfo["time"] = fabric["time"]
                    versionInfo["type"] = fabric["type"]
                    versionInfo["mainClass"] = fabric["mainClass"]
                    versionInfo["arguments"]["game"] += fabric["arguments"]["game"]
                    versionInfo["arguments"]["jvm"] += fabric["arguments"]["jvm"]
                    versionInfo["libraries"] += fabric["libraries"]
                if (fabric == 0):
                    optifine = pageOptifine(originName)
                    if (optifine != 0):
                        if (len(optifine) == 2): 
                            versionInfo["libraries"] += [{"name": "optifine:OptiFine:" + optifine[0]}, {"name": "optifine:" + optifine[1]}]
                        elif (len(optifine) == 1):
                            versionInfo["libraries"].append({"name": "optfiine.OptiFine:" + optifine[0]})
                json.dump(versionInfo, open(".minecraft\\versions\\"+versionInfo["id"]+"\\" + customName + ".json", "w"), indent=2, sort_keys=True, ensure_ascii=False)
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
                    print(lang["downloads.downloading"].replace("%1", lang["downloads.assets"]) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())) + " %" + str(per/len(assetsInfo["objects"].keys())*100), end = "")
                while 1:
                    print(lang["downloads.downloading"].replace("%1", lang["downloads.assets"]) + str(per).zfill(len(str(len(assetsInfo["objects"].keys())))) + "/" + str(len(assetsInfo["objects"].keys())) + " %" + str(per/len(assetsInfo["objects"].keys())*100), end = "")
                    if (per == len(assetsInfo["objects"].keys())):
                        break
                print(lang["downloads.finish"].replace("%1", lang["downloads.assets"]))
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
                    print(lang["downloads.downloading"].replace("%1", lang["downloads.libraries"]) + str(per).zfill(len(str(x))) + "/" + str(x) + " %" + str(per/x*100), end = "")
                while 1:
                    print(lang["downloads.downloading"].replace("%1", lang["downloads.libraries"]) + str(per).zfill(len(str(x))) + "/" + str(x) + " %" + str(per/x*100), end = "")
                    if (per == x):
                        break
                print(lang["downloads.finish"].replace("%1", lang["downloads.libraries"]))
                # Client
                print(lang["downloads.downloading"].replace("%1", lang["downloads.client"]), end = "")
                if ("sha1" in versionInfo["downloads"]["client"]): 
                    get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"), hashHex = versionInfo["downloads"]["client"]["sha1"])
                else:
                    get(versionInfo["downloads"]["client"]["url"], saveIn = (".minecraft\\versions\\" + customName), saveAs = (customName + ".jar"))
                print(lang["downloads.finish"].replace("%1", lang["downloads.client"]))
                # Logging
                try:
                    print(lang["downloads.downloading"].replace("%1", lang["downloads.logging"]), end = "")
                    logging = versionInfo["logging"]["client"]
                    get(logging["file"]["url"], saveIn = (".minecraft\\versions\\" + customName))
                    print(lang["downloads.finish"].replace("%1", lang["downloads.logging"]))
                except:
                    pass
                # End
                print(lang["downloads.finish"].replace("%1", customName))
                msvcrt.getch()

                
launch = []
selectedLaunch = cfg["selectedLaunch"]
def pageLaunch():
    global launch
    global selectedLaunch
    while 1:
        showTitle(lang["title.launch"])
        launch = []
        tmp = os.listdir(".minecraft\\versions")
        for i in tmp:
            if (os.path.isfile(".minecraft\\versions\\"+i+"\\"+i+".json")):
                launch.append(i)
        i = 0
        if (launch == []):
            print(lang["launch.instead"])
        for i in range(len(launch)):
            if (i == selectedLaunch): print("[ ", end = "")
            else: print("  ", end = "")
            print(launch[i], end = "")
            if (i == selectedLaunch): print(" ]", end = "")
            else: print("  ", end = "")
            infoFile = open(".minecraft\\versions\\" + launch[i] + "\\" + launch[i] + ".json")
            info = eval(infoFile.read())
            infoFile.close()
            infos = []
            try: 
                if ("net.fabricmc" in info["libraries"][-1]["name"]):
                    infos.append(lang["mod.fabric"] + " " + info["libraries"][-1]["name"].split(":")[-1])
            except KeyError:
                pass
            try: 
                if ("net.minecraftforge" in info["libraries"][-1]["name"]):
                    infos.append(lang["mod.forge"] + " " + info["libraries"][-1]["name"].split("-")[-1])
            except KeyError:
                pass
            try:
                if ("optifine.OptiFineTweaker" in info["arguments"]["game"]):
                    tmp = ""
                    for i in info["libraries"]:
                        if ("optifine:OptiFine" in i["name"]):
                            tmp = "_".join(i["name"].split(":")[-1].split("_")[1:])
                    infos.append(lang["mod.optifine"] + " " + tmp)
            except KeyError:
                pass
            if (infos != []): 
                print(" (" + ", ".join(infos) + ") ", end = "")
            print()
        print(lang["help.launch"])
        cfg["selectedLaunch"] = selectedLaunch
        config = open(".river_cfg.json", "w")
        config.write(str(cfg))
        config.close()
        press = msvcrt.getch()
        if (press == b'x'):
            return 0
        if (press == b'w'):
            if ((selectedLaunch-1) >= 0):
                selectedLaunch -= 1
        if (press == b's'):
            if ((selectedLaunch+1) < (i+1)):
                selectedLaunch += 1
        if (press == b'd'):
            if (launch == []):
                print(lang["launch.instead"])
                msvcrt.getch()
                continue
            sel = 0
            while 1:
                if (sel == 0): print(lang["launch.remove"].replace("%1", lang["sel.yes"]), end = "")
                if (sel == 1): print(lang["launch.remove"].replace("%1", lang["sel.no"]), end = "")
                tmp = msvcrt.getch()
                if (tmp == b'a'):
                    if (sel != 0):
                        sel -= 1
                if (tmp == b'd'):
                    if (sel != 1):
                        sel += 1
                if (tmp == b'x'):
                    break
                if (tmp == b' '):
                    if (sel == 0):
                        versionName = launch.pop(selectedLaunch)
                        os.removedirs(".minecraft\\versions\\"+versionName)
                        break
        if (press == b'f'):
            if (launch == []):
                print(lang["launch.instead"])
                msvcrt.getch()
                continue
            os.system("explorer .minecraft\\versions\\" + launch[selectedLaunch])
        if (press == b' '):
            if (launch == []):
                print(lang["launch.instead"])
                msvcrt.getch()
                continue
            tmp = launch[selectedLaunch]
            if (accounts == {}):
                print(lang["accounts.instead"])
                msvcrt.getch()
                continue
            makeLaunch(tmp)
            os.system(".minecraft\\versions\\" + tmp + "\\river_launch.bat")
            msvcrt.getch()


settings = cfg["settings"]
selectedSetting = 0
def pageSettings():
    global settings
    global selectedSetting
    while 1:
        showTitle(lang["title.settings"])
        k = 0
        j = 0
        while (k < len(settings.keys())):
            i = list(settings)[k]
            k += 1
            if (i.startswith("_")): continue
            if (j == selectedSetting): print("[ ", end = "")
            else: print("  ", end = "")
            print(lang["sets."+i] + ": " + str(settings[i]["value"]), end = "")
            if (j == selectedSetting): print(" ]")
            else: print("  ")
            j += 1
        print(lang["help.settings"])
        cfg["settings"] = settings
        config = open(".river_cfg.json", "w")
        config.write(str(cfg))
        config.close()
        press = msvcrt.getch()
        if (press == b'x'):
            return 0
        if (press == b' '):
            if (settings[list(settings)[selectedSetting]]["type"] == "static"):
                print(lang["settings.static"])
                msvcrt.getch()
                continue
            while 1:
                inValue = input(lang["settings.edit"].replace("%1", lang["sets."+list(settings)[selectedSetting]]))
                try:
                    if (settings[list(settings)[selectedSetting]]["type"] == "int"): 
                        settings[list(settings)[selectedSetting]]["value"] = int(inValue)
                        break
                except:
                    print(lang["settings.type"].replace("%1", lang["settings.type."+settings[list(settings)[selectedSetting]]["type"]]))
            
        if (press == b'w'):
            if ((selectedSetting-1) >= 0):selectedSetting -= 1
        if (press == b's'):
            if ((selectedSetting+1) < len(settings.keys())):selectedSetting += 1


langs = []
def pageLanguage():
    global lang
    while 1:
        langs = os.listdir("langs")
        for i in langs:
            if (i.startswith("_")):
                langs.remove(i)
        showTitle(lang["title.language"])
        for i in langs:
            tmp = open("langs\\"+i, encoding = "utf-8")
            content = eval(tmp.read())
            tmp.close()
            if (lang == content): print("[ ", end = "")
            else: print("  ", end = "")
            print(content["lang.name"], end = "")
            if (lang == content): print(" ]")
            else: print("  ")
        print(lang["help.language"])
        press = msvcrt.getch()
        if (press == b'w'):
            index = langs.index(cfg["lang"] + ".json")
            if (index != 0):
                index -= 1
            cfg["lang"] = langs[index][:-5]
            tmp = open("langs\\"+langs[index], encoding = "utf-8")
            lang = eval(tmp.read())
            tmp.close()
        if (press == b's'):
            index = langs.index(cfg["lang"] + ".json")
            if (index != len(langs)-1):
                index += 1
            cfg["lang"] = langs[index][:-5]
            tmp = open("langs\\"+langs[index], encoding = "utf-8")
            lang = eval(tmp.read())
            tmp.close()
        if (press == b'x'):
            return 0


accounts = cfg["accounts"]
selectedAccount = cfg["selectedAccount"]
def pageAccounts():
    global accounts
    global selectedAccount
    while 1:
        showTitle(lang["title.accounts"])
        if (accounts == {}): print(lang["accounts.instead"])
        else:
            for i in range(len(accounts.keys())):
                j = accounts[list(accounts)[i]]
                if (i == selectedAccount): print("[ ", end = "")
                else: print("  ", end = "")
                print(j["usrName"], end = "")
                if (i == selectedAccount): print(" ]")
                else: print("  ")
                print(lang["accounts.info"].replace("%1", lang["accounts."+j["usrType"]]).replace("%2", j["usrId"]))
        print(lang["help.accounts"])
        cfg["accounts"] = accounts
        cfg["selectedAccount"] = selectedAccount
        config = open(".river_cfg.json", "w")
        config.write(str(cfg))
        config.close()
        press = msvcrt.getch()
        if (press == b'x'):
            return 0
        if (press == b'w'):
            if ((selectedAccount-1) >= 0): selectedAccount -= 1
        if (press == b's'):
            if ((selectedAccount+1) < len(accounts.keys())): selectedAccount += 1
        if (press == b'c'):
            sel = 0
            while 1:
                if (sel == 0): print(lang["accounts.type"].replace("%1", lang["accounts.sel.mojang"]), end = "")
                if (sel == 1): print(lang["accounts.type"].replace("%1", lang["accounts.sel.legacy"]), end = "")
                tmp = msvcrt.getch()
                if (tmp == b'a'):
                    if (sel != 0):
                        sel -= 1
                if (tmp == b'd'):
                    if (sel != 1):
                        sel += 1
                if (tmp == b'x'):
                    break
                if (tmp == b' '):
                    print()
                    if (sel == 0):
                        usrType = "mojang"
                        input(lang["accounts.prompt"])
                        os.system("explorer \"https://login.live.com/oauth20_authorize.srf?client_id=00000000402b5328&response_type=code&scope=XboxLive.signin%20offline_access&redirect_uri=https%3a%2f%2flogin.live.com%2foauth20_desktop.srf\"")
                        code = input("").replace("https://login.live.com/oauth20_desktop.srf?code=", "").replace("&lc=", "")[:-4]
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
                    if (sel == 1):
                        usrType = "legacy"
                        usrName = input(lang["accounts.name"])
                        usrId = "4d696e6563726166744d696e65637261"
                        usrSkin = ""
                        usrSkinId = ""
                        accessToken = "${auth_access_token}"
                        usrCapes = []
                    accounts[usrName] = {"usrType": usrType, "usrName": usrName, "usrId": usrId, "usrSkin": usrSkin, "usrSkinId": usrSkinId, "usrCapes": usrCapes, "accessToken": accessToken}
                    break
        if (press == b'd'):
            sel = 0
            while 1:
                if (sel == 0): print(lang["accounts.remove"].replace("%1", lang["sel.yes"]), end = "")
                if (sel == 1): print(lang["accounts.remove"].replace("%1", lang["sel.no"]), end = "")
                tmp = msvcrt.getch()
                if (tmp == b'a'):
                    if (sel != 0):
                        sel -= 1
                if (tmp == b'd'):
                    if (sel != 1):
                        sel += 1
                if (tmp == b'x'):
                    break
                if (tmp == b' '):
                    if (sel == 0):
                        accounts.pop(list(accounts)[selectedAccount])
                    break
            
sel = 0
tmp = get("https://launchermeta.mojang.com/mc/game/version_manifest.json")
while 1:
    showTitle(lang["title.main"])
    if (sel == 0): print(lang["main.sel.launch"])
    if (sel == 1): print(lang["main.sel.downloads"])
    if (sel == 2): print(lang["main.sel.accounts"])
    if (sel == 3): print(lang["main.sel.settings"])
    if (sel == 4): print(lang["main.sel.language"])
    if (cfg["version"] != curBuild):
        updateFrom = cfg["version"]
        updateFromVer = builds[updateFrom]
        cfg["version"] = curBuild
        config = open(".river_cfg.json", "w")
        config.write(str(cfg))
        config.close()
        up = []
        up.append(("Fixed bugs", ))
        up.append(("Could now launch 1.7.x and 1.8.x", ))
        up.append(("Added Help", ))
        up.append(("Could now remove versions and accounts",
                   "Modified update log showing"))
        up.append(("Could now open location directories of versions",
                   "Would now downloads logging xml file",
                   "Modified update log showing"))
        up.append(("When downloading Minecraft, would now ask to install Fabric",
                   "Could now see the info of Minecraft",
                   "Modified update log showing",
                   "Fixed legacy versions' ${auth_session} bug",
                   "Would now check Minecraft's sha1 hash value"))
        up.append(("Now support multi-language", ))
        print(lang["main.update"].replace("%1", updateFromVer).replace("%2", builds[curBuild]))
        for i in range(updateFrom, curBuild+1):
            if (updateFrom < i):
                if ((curBuild - updateFrom) > 1):
                    print(builds[i] + ": ")
                for j,updateContent in enumerate(up[i-1]):
                    print(str(j+1) + ". " + updateContent + "! ")
    if (cfg["latest"] != eval(tmp)["versions"][0]["id"]):
        if (cfg["latest"] != ""): 
            print(lang["main.new"].replace("%1",eval(tmp)["versions"][0]["id"]), end = "")
            print()
            cfg["latest"] = eval(tmp)["versions"][0]["id"]
    print(lang["help.main"])
    cfg["settings"]["info"]["value"] = lang["sets.info.value"].replace("%1", builds[curBuild])
    config = open(".river_cfg.json", "w")
    config.write(str(cfg))
    config.close()
    press = msvcrt.getch()
    if (press == b'a'):
        if (sel != 0):
            sel -= 1
    if (press == b'd'):
        if (sel != 4):
            sel += 1
    if (press == b' '):
        if (sel == 0): pageLaunch()
        if (sel == 1): pageDownloads()
        if (sel == 2): pageAccounts()
        if (sel == 3): pageSettings()
        if (sel == 4): pageLanguage()
    if (press == b'x'):
        break
   
