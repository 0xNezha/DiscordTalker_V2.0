import sys
import threading
import tkinter as tk

import requests
import json
import random
import time
import traceback
import configparser
 

config = configparser.ConfigParser()
config.read('botConfig.ini', encoding="utf-8-sig")

authorization_list = [config.get('bots', 'bots_1'),config.get('bots', 'bots_2')]
guild_id   = config.get('channel', 'guild_id')
channel_id = config.get('channel', 'channel_id')
bot_delay = config.getint('time', 'bot_delay')

useProxy = config.getboolean('proxy', 'use_proxy')
proxies={
'http': config.get('proxy', 'http'),
'https':config.get('proxy', 'https')
}

message_id = 0
talk_counter = 0 
talk_pause = 0 
talk_list = []

with open("talk_list_1.txt", "r",encoding='utf-8') as f:
    for line in f.readlines():
        line = line.strip('\n') 
        talk_list.append(line)
    print("语料读取完毕,共" + str(len(talk_list)) + "条")

def chat():

    global message_id
    global talk_counter

    for authorization in authorization_list:
        header = {
            "Authorization":authorization,
            "Content-Type":"application/json",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
        }

        msg_say = {
            "content": talk_list[talk_counter],
            "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
            "tts": False
        }
        msg_respone = {
            "content": talk_list[talk_counter],
            "nonce": "82329451214{}33232234".format(random.randrange(0, 1000)),
            "tts": False,
            "message_reference":{"guild_id":guild_id,"channel_id":channel_id,"message_id":message_id}
        }

        if message_id == 0:
            msg = msg_say
        else:
            msg = msg_respone

        talk_counter += 1
        if talk_counter >= len(talk_list) -1 :
            talk_counter  = 0


        url = 'https://discord.com/api/v9/channels/{}/messages'.format(channel_id)
        try:
            if useProxy:
                res = requests.post(url=url, headers=header, data=json.dumps(msg),proxies=proxies)
            else:
                res = requests.post(url=url, headers=header, data=json.dumps(msg))         
            result= res.json()
            print('已发送第'+str(talk_counter)+'句话，内容:',result['content'])
            message_id = result['id']
            time.sleep(random.randrange(1,3))
        except:
            print(traceback.format_exc())
            break
        time.sleep(random.randrange(bot_delay,bot_delay+3))


def exit():
        global talk_pause
        talk_pause = 1
        root.destroy
        sys.exit() 






class App:
 def __init__(self, root):

    root.title("Dsicord Talker V2.0")
    root.iconbitmap("favicon.ico")
    root.geometry("300x260")
    root.resizable(0,0)#
    frame = tk.Frame(root)
    frame.pack()

    label_2 = tk.Label(root, text="2 Bots talk edition || 两人互答版 ", bg="Orange", font=("微软雅黑", 12), )
    label_2.pack(side=tk.TOP)
    
    label_channel = tk.Label(root, text="灌水频道ID:" + str(channel_id), bg="yellow", font=("微软雅黑", 12), )#width=5, height=2
    label_channel.pack(side=tk.TOP)

    label_1 = tk.Label(root, text="语料读取完毕,共" + str(len(talk_list)) + "条 || bot回复延时" + str(bot_delay) + "秒", bg="CornflowerBlue", font=("微软雅黑", 12), )
    label_1.pack(side=tk.TOP)



    label_3 = tk.Label(root, text="如需退出，请直接点击命令行窗口右上[X]", bg="Orange", font=("微软雅黑", 12), )
    label_3.pack(side=tk.TOP)

    if len(talk_list) < 2:
        label_3 = tk.Label(root, text="语料太少，请及时添加！", bg="red", font=("微软雅黑", 12), )
        label_3.pack(side=tk.TOP)


    self.Button_run = tk.Button(frame, text="启动", fg="blue", width = 20,command=self.run)
    self.Button_run.pack(side=tk.LEFT)

    self.Button_pause = tk.Button(frame, text="暂停", fg="blue",width = 20, command=self.pause)
    self.Button_pause.pack(side=tk.LEFT)
    self.Button_pause.configure(state='disable')




 def run(self):
        self.Button_run.configure(state='disable')
        self.Button_pause.configure(state='normal')

        insert_data = threading.Thread(target=self.talk_loop)
        insert_data.start()

 def talk_loop(self):
     global talk_pause 
     talk_pause = 0 
     print("RUN!")
     while talk_pause == 0:
        try:
            chat()
        except:
            print(traceback.format_exc())
            break


 def pause(self):
        self.Button_run.configure(state='normal')
        self.Button_pause.configure(state='disable')
        print("PAUSE...")
        global talk_pause
        talk_pause = 1



root = tk.Tk()
app = App(root)
logo = tk.PhotoImage(file="logo.png")
explanation = """

discord.gg/                           
cryptochasers                          
                               
@0xNalakuvara                         

"""
tk.Label(root,compound=tk.CENTER,text=explanation, fg="Blue",font=("微软雅黑", 15,"bold"),image=logo).pack(side="right")

root.protocol('WM_DELETE_WINDOW', exit)
root.mainloop()