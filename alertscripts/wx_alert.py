#!/usr/local/bin/python3

import requests,sys,json

def GetTokenFromServer(Corpid,Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid":Corpid,
        "corpsecret":Secret
    }
    r = requests.get(url=Url,params=Data,verify=False).json()
    if r['errcode'] == 0:
        return r['access_token'] 
    return False   

def SendMessage(User, Subject, Content, Corpid, Secret):
    token = GetTokenFromServer(Corpid, Secret)
    if token:
        Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
        data = {
		    "touser": User,
			"toparty": 2,
			"msgtype": "text",
			"agentid": 1000002,
			"text": {
				"content": Subject + "\n" + Content
			},
			"safe": "0"
		}
        r = requests.post(url=Url,data=json.dumps(data, ensure_ascii=False),verify=False)
        return r.json()
    raise "Get the auth token  error"
	
if __name__ == '__main__':
    User = str(sys.argv[1])
    Subject = str(sys.argv[2])                                                       
    Content = str(sys.argv[3])
    corpid = "ww24ed28d********"
    secret = "MnyzNQCxJpEsVQvLuda5mXSiRZTfS**************"
    status = SendMessage(User, Subject, Content, corpid, secret)
    print(status)
