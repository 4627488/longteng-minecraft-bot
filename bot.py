from miraicle.message import At
from server import backpack, status, backup
from ohayo import ohayo
import miraicle
from ruamel import yaml


def sendfmsg(aim, msg):
    if isinstance(msg, list):
        msg2 = list(filter(lambda item: not isinstance(item, At), msg))
        print(len(msg2))
        bot.send_friend_msg(qq=aim, msg=msg2)
    else:
        bot.send_friend_msg(qq=aim, msg=msg)


def sendgmsg(aim, msg):
    bot.send_group_msg(group=aim, msg=msg)


@miraicle.Mirai.receiver('GroupMessage')
def gm(bot: miraicle.Mirai, msg: miraicle.GroupMessage):
    if msg.text == "status" or msg.text == "#status":
        status(msg.text, msg.group, msg.sender, sendgmsg)
        return
    if msg.text == 'backup' or msg.text == "#backup":
        backup(msg.text, msg.group, msg.sender, sendgmsg)
        return
    if msg.text == 'ohayo' or msg.text == "#ohayo":
        ohayo(msg.text, msg.group, msg.sender, sendgmsg)
        return
    if msg.text == 'backpack' or msg.text == "#backpack":
        backpack(msg.text, msg.group, msg.sender, sendgmsg)
        return


@miraicle.Mirai.receiver('FriendMessage')
def fm(bot: miraicle.Mirai, msg: miraicle.FriendMessage):
    if msg.text == "status" or msg.text == "#status":
        status(msg.text, msg.sender, msg.sender, sendfmsg)
        return
    if msg.text == 'backup' or msg.text == "#backup":
        backup(msg.text, msg.sender, msg.sender, sendfmsg)
        return
    if msg.text == 'ohayo' or msg.text == "#ohayo":
        ohayo(msg.text, msg.sender, msg.sender, sendfmsg)
        return
    if msg.text == 'backpack' or msg.text == "#backpack":
        backpack(msg.text, msg.sender, msg.sender, sendfmsg)
        return


with open('config/config.yml', 'r', encoding='utf-8') as f:
    config = yaml.load(f.read(), Loader=yaml.Loader)
bot = miraicle.Mirai(qq=int(config['mirai']['qq']), verify_key=config['mirai']
                     ['verify_key'], port=int(config['mirai']['port']))
bot.run()
