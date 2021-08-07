import os
from ruamel import yaml


def ReadConfig():
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    return config['mcrcon']['server'], config['mcrcon']['port'], config['mcrcon']['password']


def checkOnline():
    server, port, password = ReadConfig()
    return os.system(f'./mcrcon/mcrcon -H {server} -P {port} -c -p {password} tps') == 0


def runshell(command):
    print(f'[RCON]{command}')
    server, port, password = ReadConfig()
    re = str(os.popen(
        f"./mcrcon/mcrcon -H {server} -P {port} -c -p {password} '{command}'").read())
    return re.split('\n')[0]


def status(text, chat, senderid, sendmsg):
    if checkOnline() == False:
        sendmsg(chat, '服务器未在运行')
        return
    tps = f'近 1min,5mins,10mins 的TPS平均值(最高20)：{runshell("tps").split(":")[-1]}'
    lcr = runshell("list")
    playercnt = int(lcr.split(" ")[2])
    list = ''
    if playercnt == 0:
        list = '服务器没有人在线'
    else:
        list = f'服务器有{lcr.split(" ")[2]}人在线：{lcr.split(":")[-1]}'
    sendmsg(chat, list+'\n'+tps)


def backup(text, chat, senderid, sendmsg):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    server_path = config['backup']['server_path']
    adminlist = None
    with open('config/admin.yml', 'r', encoding='utf-8') as f:
        adminlist = yaml.load(f.read(), Loader=yaml.Loader)
        print(adminlist)
    if senderid not in adminlist:
        sendmsg(chat, '你没有使用该命令的权限')
        return
    sendmsg(chat, '正在备份服务器存档，请勿滥用此功能，此项操作将被记录')
    # ret=0
    ret = os.system(f'cd {server_path} && python3 backup.py')
    if ret == 0:
        file_stats = os.stat(f"{server_path}/backup.zip")
        size = file_stats.st_size/(1024*1024)
        sendmsg(
            chat, f'成功备份存档到COS。存档大小{round(size, 2)}M')
    else:
        sendmsg(chat, '备份失败')


def GetPlayerName(qq: int):
    with open('config/config.yml', 'r', encoding='utf-8') as f:
        config = yaml.load(f.read(), Loader=yaml.Loader)
    data_path = config['ohayo']['Easybot_data']
    with open(data_path, 'r', encoding='utf-8') as f:
        bound = yaml.load(f.read(), Loader=yaml.Loader)
    if str(qq) in bound['QQ_Bound'].keys():
        return bound['QQ_Bound'][str(qq)]
    runshell("bot reload")
    with open(data_path, 'r', encoding='utf-8') as f:
        bound = yaml.load(f.read(), Loader=yaml.Loader)
    if str(qq) in bound['QQ_Bound'].keys():
        return bound['QQ_Bound'][str(qq)]
    return None


def backpack(text, chat, senderid, sendmsg):
    with open('data/backpack.yml', 'r', encoding='utf-8') as f:
        backpack = yaml.load(f.read(), Loader=yaml.Loader)
    playerName = GetPlayerName(senderid)
    if backpack == None or senderid not in backpack.keys():
        sendmsg(chat, "你还未进行过抽卡，尝试发送 #ohayo 签到抽卡")
    elif len(backpack[senderid]) == 0:
        sendmsg(chat, "你邮件中没有任何物品")
    elif playerName == None:
        sendmsg(chat, f'你还没有绑定mc账号，在游戏内使用指令 /bot bind {senderid} 并根据提示完成绑定')
    else:
        for obj in backpack[senderid]:
            ret = runshell(obj['command'].replace(str(senderid), playerName))
            sendmsg(chat, ret)
        backpack[senderid] = list()
        with open("data/backpack.yml", "w", encoding="utf-8") as f:
            yaml.dump(backpack, f, Dumper=yaml.RoundTripDumper)
