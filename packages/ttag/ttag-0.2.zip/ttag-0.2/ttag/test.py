# -*- coding: UTF-8 -*-

import socket, struct
import sys
import copy
import json

def tprint():
    print "睿智的你早已看穿一切"

def ttrans():
    try:
        fr = open(sys.argv[1],'r')
        fa = open(sys.argv[2],'r')
        i = 0
        j = 0
        for line in fr:
            i += 1
            if not line:
                break
            dict1 = {}
            # try:
            content = json.loads(line)
            dict1 = copy.deepcopy(content)
            if dict1["location"]["city"] != "Fuyang":
                dict1["location"]["city"] = "Fuyang"
                dict1["location"]["longitude"] = 115.816703796386
                dict1["location"]["latitude"] = 32.900001525878906
            if dict1["location"]["province"] != "Anhui":
                dict1["location"]["province"] = "Anhui"
            autonomous_system ={
                "routed_prefix":"",
                "country_code":"",
                "path": "",
                "organization":"",
                "name":"",
                "description":"",
                "asn":""
            }
            dict1["autonomous_system"] = autonomous_system
            line_content = json.dumps(dict1,ensure_ascii=False)+"\n"
            fa.write(line_content)
            j += 1
            # except:
            #     print i
            #     continue
        fr.close()
        fa.close()
        return [i,j]
    except:
        print "格式错误，ttrans 待转换文件 目标文件"


class jsoner:
    def __init__(self):
        print "++init++"

    def translate1(self,fr,fa):
        i = 0
        j = 0
        for line in fr:
            i += 1
            if not line:
                break
            dict1 = {}
            # try:
            content = json.loads(line)
            dict1 = copy.deepcopy(content)
            if dict1["location"]["city"] != "Fuyang":
                dict1["location"]["city"] = "Fuyang"
                dict1["location"]["longitude"] = 115.816703796386
                dict1["location"]["latitude"] = 32.900001525878906
            if dict1["location"]["province"] != "Anhui":
                dict1["location"]["province"] = "Anhui"
            autonomous_system ={
                "routed_prefix":"",
                "country_code":"",
                "path": "",
                "organization":"",
                "name":"",
                "description":"",
                "asn":""
            }
            dict1["autonomous_system"] = autonomous_system
            line_content = json.dumps(dict1,ensure_ascii=False)+"\n"
            fa.write(line_content)
            j += 1
            # except:
            #     print i
            #     continue
        fr.close()
        fa.close()
        return [i,j]

    # def ip2long(self,ip):
    #         """
    #         Convert an IP string to long
    #         """
    #     packedIP = socket.inet_aton(ip)
    #     return struct.unpack("!L", packedIP)[0]