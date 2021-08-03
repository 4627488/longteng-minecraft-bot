import random
import time
from server import backpack

from ruamel import yaml

from server import runshell

lv = {"I": 1,
      "II": 2,
      "III": 3,
      "IV": 4,
      "V": 5}

# 最高八个附魔钻石 oqi 1-30
# oqi = abs((A?1:0)*100-50) P(A)=1/2

# /give @p minecraft:diamond_sword{display:{Name:"[{\"text\":\"7.29抽卡 h4627488 获得\",\"color\":\"white\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}]",Lore:["{\"text\":\"\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}"]},Enchantments:[{id:"minecraft:looting",lvl:230},{id:"minecraft:respiration",lvl:30},{id:"minecraft:sharpness",lvl:5555555}]} 1
# /give @p minecraft:diamond_sword{AttributeModifiers:[{Operation:1,Amount:0.5,UUIDLeast:-1165299638744679141L,UUIDMost:2741597136358241217L,AttributeName:"generic.attackSpeed",Name:"generic.attackSpeed"}],display:{Name:"[{\"text\":\"[限定]\",\"color\":\"white\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false},{\"text\":\"钻石剑\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}]",Lore:["{\"text\":\"8.1日签到 获得\",\"color\":\"dark_purple\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}","{\"text\":\"攻击速度提升50%\",\"color\":\"gray\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}","{\"text\":\"无限耐久\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}","{\"text\":\"愿我的弹雨能熄灭你的苦痛\",\"color\":\"aqua\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}"]},Unbreakable:1} 1
# give @p minecraft:diamond_sword{display:{Name:"[{\"text\":\"【SR】钻石剑\",\"color\":\"gold\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}]",Lore:["{\"text\":\"2021-08-01签到获得\",\"color\":\"blue\",\"bold\":false,\"italic\":false,\"underlined\":false,\"strikethrough\":false,\"obfuscated\":false}"]}} 1


def GetCommand(obj: str, magic: list, player: str):
    # 里面有{}不能fstring,没关系可以先转义
    # TODO 没有处理附魔，因为附魔id改成minecraft:xxx这种了,我不会
    # TODO 没有颜色，我不会
    give = 'give PLAYER minecraft:OBJECT{display:{Name:"[{\\"text\\":\\"DIFF CNNAME\\",\\"color\\":\\"gold\\",\\"bold\\":false,\\"italic\\":false,\\"underlined\\":false,\\"strikethrough\\":false,\\"obfuscated\\":false}]",Lore:["{\\"text\\":\\"DATE签到获得\\",\\"color\\":\\"blue\\",\\"bold\\":false,\\"italic\\":false,\\"underlined\\":false,\\"strikethrough\\":false,\\"obfuscated\\":false}"]}} 1'
    give = give.replace("PLAYER", str(player))
    give = give.replace("OBJECT", str(obj))
    give = give.replace("CNNAME", GetText(obj, magic))
    give = give.replace("DIFF", "[N]")
    give = give.replace("DATE", str(
        time.strftime("%Y-%m-%d", time.localtime())))
    return give


def GetText(obj: str, magic: list):
    with open('zh-cn.yml', 'r', encoding='utf-8') as f:
        zh_cn = yaml.load(f.read(), Loader=yaml.Loader)
    if obj in zh_cn.keys():
        return zh_cn[obj]
    print(obj)
    sp = obj.split('_')
    m = zh_cn[sp[0]]
    e = zh_cn[sp[1]]
    return m+e


def record(qq: int, command: str, cnname: str):
    # 加入邮件
    with open('backpack.yml', 'r', encoding='utf-8') as f:
        backpack = yaml.load(f.read(), Loader=yaml.Loader)
    if backpack == None:
        backpack = dict()
    if qq not in backpack.keys():
        backpack[qq] = list()
    backpack[qq].append(
        {'command': command, "name": cnname, 'timestamp': str(time.time())})
    # print(backpack)
    with open("backpack.yml", "w", encoding="utf-8") as f:
        yaml.dump(backpack, f, Dumper=yaml.RoundTripDumper)

    # 记录历史
    with open('history.yml', 'r', encoding='utf-8') as f:
        history = yaml.load(f.read(), Loader=yaml.Loader)
    if history == None:
        history = list()
    history.append({'qq': qq, 'command': command,
                   "name": cnname, 'timestamp': str(time.time())})
    with open("history.yml", "w", encoding="utf-8") as f:
        yaml.dump(history, f, Dumper=yaml.RoundTripDumper)


def gacha(text, chat, senderid, sendmsg):
    #runshell("bot reload")
    with open('magic.yml', 'r', encoding='utf-8') as f:
        magics = yaml.load(f.read(), Loader=yaml.Loader)
    with open('cards.yml', 'r', encoding='utf-8') as f:
        cards = yaml.load(f.read(), Loader=yaml.Loader)
    with open('diff.yml', 'r', encoding='utf-8') as f:
        diffs = yaml.load(f.read(), Loader=yaml.Loader)

    # 抽取物品
    total_diff = 0
    for diff in diffs['object'].values():
        total_diff += int(diff)
    c = random.randint(1, total_diff)
    selected_object = ""
    selected_diff = 0
    for obj in diffs['object'].keys():
        if c <= int(diffs['object'][obj]):
            selected_object = obj
            selected_diff = int(diffs['object'][obj])
            break
        else:
            c -= int(diffs['object'][obj])
    # print(selected_object)
    selected_magics = []

    # 可以被附魔，计算附魔等级
    if selected_object in cards['magic'].keys():
        # TODO 这个地方本来应该按magic的稀有度抽取，但我不想写，那就等概率吧
        while True:
            if(random.randint(1, 2) == 1):
                break
            if(random.randint(1, 3) != 1 and len(selected_magics) != 0):
                selected_magics.append(selected_magics[-1])
                continue
            selected_magics.append(random.choice(
                cards['magic'][selected_object]))
    # print(selected_magics)

    # 有无材质，计算材质
    if selected_object in cards['equipment'].keys():
        dic = {}
        for diff in diffs['material'].keys():
            if diff in cards['equipment'][selected_object]:
                dic[diff] = diffs['material'][diff]
        total_diff = 0
        for diff in dic.values():
            total_diff += int(diff)
        c = random.randint(1, total_diff)
        for obj in dic.keys():
            if c <= int(dic[obj]):
                selected_object = f'{obj}_{selected_object}'
                selected_diff += int(dic[obj])
                break
            else:
                c -= int(dic[obj])
    print(f"抽卡成功！\n {selected_object} {selected_diff}")
    sendmsg(
        chat, f"抽卡成功！\n {GetText(selected_object, selected_magics)} {selected_diff}")
    record(senderid, GetCommand(selected_object, selected_magics, str(
        senderid)), GetText(selected_object, selected_magics))


def ohayo(text, chat, senderid, sendmsg):
    with open('ohayo.yml', 'r', encoding='utf-8') as f:
        checkin = yaml.load(f.read(), Loader=yaml.Loader)
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    if checkin == None:
        checkin = dict()
    if today not in checkin.keys():
        checkin[today] = list()
    if senderid not in checkin[today]:
        checkin[today].append(senderid)
        sendmsg(chat, f'签到成功，你是今天第{len(checkin[today])}个签到的人！')
        gacha(text, chat, senderid, sendmsg)
        with open("ohayo.yml", "w", encoding="utf-8") as f:
            yaml.dump(checkin, f, Dumper=yaml.RoundTripDumper)
    else:
        sendmsg(chat, f'你已经签到过了')


if __name__ == '__main__':
    gacha('ohayo', 12345678, 12345678, 233)
