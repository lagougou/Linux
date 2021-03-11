
import requests
from requests.auth import HTTPBasicAuth
# from MySQLdb import _mysql
import MySQLdb, re
from jenkins import Jenkins

auth = HTTPBasicAuth('jiangrui', 'jiangrui')

# server = Jenkins("http://172.16.101.96:8080/", username='jiangrui', password='jiangrui')
# # server.get
# jobs = server.get_jobs()
# sets = set()
# for j in jobs:
#     # print(j)
    
#     index = j[0].find('/')
#     fullname = j[0][:index]
#     sets.add(fullname)
#     # # print(fullname)
#     # config = j.get_config()
#     # print(config)


db = MySQLdb.connect(host="172.16.101.87", user="jiangrui", passwd="pi3hxxthD8mYoqny", db="devops")
# db.query("SELECT project FROM deployconfig WHERE deploy_type='vm'")
c = db.cursor()
c.execute("SELECT project FROM deployconfig WHERE deploy_type='vm'")

results = c.fetchall()
names = set()
print(results)
for item in results:
    # if item == "saas-factoring":
    names.add(item[0])

server = Jenkins('http://172.16.101.96:8080/', username='jiangrui', password='jiangrui')
jobs = server.get_jobs()
for i in jobs:
    # print(i['fullname'])
    tag = "Jenkinsfile-bak"
    full_name = i['fullname']
    if full_name in names:
        config = server.get_job_config(full_name)
        # if full_name == "check-account":
        #     print(config)
        result = re.search(r'<scriptId>(.*?)</scriptId>', config, re.M)
        if result:
            find = result.groups()[0]
            if find == "Jenkinsfile-Java-Business-Docker" or find == "Jenkinsfile-Java-Business":
                print(full_name, find)
        # if find == 'Jenkinsfile-bak':
                cc = config.replace(find, tag)
                server.reconfig_job(full_name, cc)
            # print(cc)
# for item in names:
#     tag = 'Jenkinsfile-Java-Business'
#     resp = requests.get("http://172.16.101.96:8080/job/{}/config.xml".format(item), auth=auth)
#     if resp.status_code == 200:
#         content = resp.content.decode("utf-8")
#         # print(content)
#         regex = re.compile('<scriptId>(.*?)</scriptId>')
#         result = re.search(r'<scriptId>(.*?)</scriptId>', content, re.M)
#         if result:
#             find = result.groups()[0]
#             if find == 'Jenkinsfile-bak':
#                 cc = content.replace(find, tag)
#                 with open('config.xml', 'wb') as f:
#                     f.write(cc.encode("utf-8"))
#                     f.close()
#                 config = open('config.xml', 'rb')
#                 respons = requests.post("http://172.16.101.96:8080/job/{}/config.xml".format(item),headers= {'content-type': 'application/xml'},data=config, auth=('jiangrui', 'jiangrui'))
#             # print(find)
#                 print(respons.status_code)
        # break