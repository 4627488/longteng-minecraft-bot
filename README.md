# longteng-minecraft-bot

minecraft服务器的qq群机器人

- 支持qq群签到抽卡
- 查询服务器tps及在线人数
- 备份服务器存档

## 快速开始

### 必要条件

- Python 3.7以上
- mirai - 参见 [miria项目](https://github.com/mamoe/mirai/)
- Easybot - 一个用于互通服务器消息的插件，机器人需要读取其中的绑定信息，参见 [MCBBS](https://www.mcbbs.net/forum.php?mod=viewthread&tid=1175227&extra=page%3D1%26filter%3Dsortid%26sortid%3D7)

使用 pip 安装 miraicle 和 ruamel.yaml

```pip install miraicle```

```pip install ruamel.yaml```

### 配置

1.在config/config.yml中配置mirai的http端口和地址

```yaml
mirai:
  qq: 12345678 #机器人的qq号
  verify_key: 12345678 # mirai-http 设置的 verify_key
  port: 8080 # mirai-http 的端口
```

2.下载 mcrcon 到 `mcrcon/` 中，在 main 分支已经附带了Linux的二进制文件

3.服务器的配置文件`server.properties`中

```properties
rcon.port=25575 #这是服务器rcon的端口
rcon.password=password #在这里设置你的rcon密码
enable-rcon=true #确保此项为true
```

然后在 `config/config.yml` 中

```yaml
mcrcon:
  server: 127.0.0.1 #服务器的地址
  port: 25575 #rcon的端口
  password: "12345678" #rcon的密码
```

安装好Easybot插件后 在服务器文件夹下 `plugins/EasyBot_Reloaded/boundData.yml` 应自动生成

把这个文件的完整路径添加到 `config/config.yml` 中

```yaml
ohayo:
  #读取Easybot的数据获得游戏名和qq的对照表
  Easybot_data: "/home/h4627488/minecraft/midsummer/plugins/EasyBot_Reloaded/boundData.yml"
```

### 运行

```bash
python3 bot.py
```

完成了，在群里发送 `#status` 试试吧

机器人对所有会话的指令都会应答

## 机器人指令

`#ohayo` : 签到并完成一次抽卡

`#status` : 查询服务器状态

`#backpack` : 玩家在线时使用，提取自己的抽到的物品

`#backup` : 备份服务器存档并上传到cos