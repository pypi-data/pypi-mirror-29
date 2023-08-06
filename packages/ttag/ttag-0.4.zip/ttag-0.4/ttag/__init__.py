# -*- coding: UTF-8 -*-
import copy
import json
import sys
def tprint():
    print "test123"

def ttrans():
    print "come here"
    try:
        print sys.argv
        fr = open(sys.argv[1],'r')
        fa = open(sys.argv[2],'wb')
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
            fa.write(line_content.encode("utf-8"))
            j += 1
            # except:
            #     print i
            #     continue
        fr.close()
        fa.close()
        print [i,j]
    except Exception as e:
        print "format_cmd:ttrans source_ipv4_file target_file"