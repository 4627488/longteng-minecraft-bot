import random
import time
from miraicle.message import At, Plain

from ruamel import yaml

lv = {"I": 1,
      "II": 2,
      "III": 3,
      "IV": 4,
      "V": 5}


def RandomLevel():
    with open('config/cards.yml', 'r', encoding='utf-8') as f:
        cards = yaml.load(f.read(), Loader=yaml.Loader)
    total_pro = 0
    selected_pro_name = ''
    for pro in cards['probability'].values():
        total_pro += pro
    selected_pro = random.randint(1, total_pro)
    for pro_name, pro in cards['probability'].items():
        if selected_pro <= int(pro):
            selected_pro_name = pro_name
            break
        else:
            selected_pro -= int(pro)
    return selected_pro_name


def GetCommand(obj: str, magic: list, player: str, probability: str):
    # 里面有{}不能fstring,没关系可以先转义
    # TODO 没有处理附魔，因为附魔id改成minecraft:xxx这种了,我不会
    with open('config/cardpool.yml', 'r', encoding='utf-8') as f:
        cardpool = yaml.load(f.read(), Loader=yaml.Loader)
    if str(obj) in cardpool['command'].keys():
        give = cardpool['command'][obj]
    else:
        give = cardpool['command']['default']
    print(give)
    give = give.replace("PLAYER", str(player))
    give = give.replace("OBJECT", str(obj))
    give = give.replace("CNNAME", GetText(obj, magic))
    give = give.replace("DIFF", f'[{probability}]')
    give = give.replace("DATE", str(
        time.strftime("%Y-%m-%d", time.localtime())))
    return give


def GetText(obj: str, magic: list):
    with open('config/zh-cn.yml', 'r', encoding='utf-8') as f:
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
    with open('data/backpack.yml', 'r', encoding='utf-8') as f:
        backpack = yaml.load(f.read(), Loader=yaml.Loader)
    if backpack == None:
        backpack = dict()
    if qq not in backpack.keys():
        backpack[qq] = list()
    backpack[qq].append(
        {'command': command, "name": cnname, 'timestamp': str(time.time())})
    # print(backpack)
    with open("data/backpack.yml", "w", encoding="utf-8") as f:
        yaml.dump(backpack, f, Dumper=yaml.RoundTripDumper)

    # 记录历史
    with open('data/history.yml', 'r', encoding='utf-8') as f:
        history = yaml.load(f.read(), Loader=yaml.Loader)
    if history == None:
        history = list()
    history.append({'qq': qq, 'command': command,
                   "name": cnname, 'timestamp': str(time.time())})
    with open("data/history.yml", "w", encoding="utf-8") as f:
        yaml.dump(history, f, Dumper=yaml.RoundTripDumper)


def gacha(text, chat, senderid, sendmsg, isFree=False):
    with open('config/cards.yml', 'r', encoding='utf-8') as f:
        cards = yaml.load(f.read(), Loader=yaml.Loader)
    with open('config/cardpool.yml', 'r', encoding='utf-8') as f:
        cardpool = yaml.load(f.read(), Loader=yaml.Loader)

    # 抽取物品
    object_level = RandomLevel()  # 随机一个稀有度
    selected_object = random.choice(cardpool['object'][object_level])

    material_level = None
    selected_magics = list()
    selected_material = None
    # 有无材质，计算材质
    if selected_object in cards['equipment'].keys():
        # 材料的概率
        material_level = RandomLevel()  # 随机一个稀有度
        material_list = list()
        for material in cards['equipment'][selected_object]:
            if material in cardpool['material'][material_level]:
                material_list.append(material)
        selected_material = random.choice(material_list)
        selected_object = f'{selected_material}_{selected_object}'
    if isFree:
        sendmsg(chat, f"正在进行模拟抽卡，抽卡记录不会生效，但会计入个人欧气统计")
    if material_level == None:
        sendmsg(
            chat, f"抽卡成功！\n 获得：{GetText(selected_object, selected_magics)} *1\n 物品稀有度：[{object_level}]")
        if not isFree:
            record(senderid, GetCommand(selected_object, selected_magics, str(
                senderid), object_level), GetText(selected_object, selected_magics))
    else:
        sendmsg(
            chat, f"抽卡成功！\n 获得：{GetText(selected_object, selected_magics)} *1\n 物品稀有度：[{object_level}]，材质稀有度：[{material_level}]")
        if not isFree:
            record(senderid, GetCommand(selected_object, selected_magics, str(
                senderid), material_level), GetText(selected_object, selected_magics))


def ohayo(text, chat, senderid, sendmsg):
    with open('data/ohayo.yml', 'r', encoding='utf-8') as f:
        checkin = yaml.load(f.read(), Loader=yaml.Loader)
    today = str(time.strftime("%Y-%m-%d", time.localtime()))
    if checkin == None:
        checkin = dict()
    if today not in checkin.keys():
        checkin[today] = list()
    if senderid not in checkin[today]:
        checkin[today].append(senderid)
        sendmsg(chat, [At(senderid), Plain(
            f'\n签到成功，你是今天第{len(checkin[today])}个签到的人！')])
        gacha(text, chat, senderid, sendmsg)
        with open("data/ohayo.yml", "w", encoding="utf-8") as f:
            yaml.dump(checkin, f, Dumper=yaml.RoundTripDumper)
    else:
        sendmsg(chat, [At(senderid), Plain(f'\n你已经签到过了')])


if __name__ == '__main__':
    def fakesend(to, text):
        print(to)
        print(text)
    gacha('ohayo', 12345678, 12345678, fakesend)
