import requests
from requests.auth import HTTPBasicAuth
import json


header = {
        'Content-Type': 'application/json'
}

auth = HTTPBasicAuth('admin', 'Harbor12345')


def get_image_name(baseUrl):
    data = {}
    page = 1
    page_size = 20
    while True:
        resp = requests.get(baseUrl, params={'page_size': page_size, 'page': page}, headers=header, auth=auth)
        # print(resp)
        result = resp.content.decode("utf-8")
        content = json.loads(result)
        # print(content)
        if content:
            for item in content:
                count = item["artifact_count"]
                if count > 10:
                    data['name'] = item['name'].split('/')[1]
                    data["artifact_count"] = count
                    yield data
            page += 1
        else:
            break  


def get_each_image_info(baseUrl):
    storage = {}
    finish = False
    for item in get_image_name(baseUrl):
        page = 1
        page_size = 20
        # arr = []
        if item:
            storage[item['name']] = [] 
            while True:
                resp = requests.get(baseUrl + item['name'] + '/artifacts', params={'page_size': page_size, 'page': page}, headers=header, auth=auth)
                content = json.loads(resp.content.decode("utf-8"))
                if content:
                    for data in content:
                        storage[item['name']].append({"digest": data["digest"], "id": data["id"], "tags": data['tags'][0]['name']})
                    page = page + 1
                else:
                    break
    for k, v in storage.items():
        finish = delete_over_image(k, v[10:], baseUrl)
    return finish

def delete_over_image(name, images, baseUrl):
    if images:
        for image in images:
            resp = requests.delete(baseUrl+name + "/artifacts/" + image['digest'], headers=header, auth=auth)
            if resp.status_code == 200:
                pass
            else:
                print("{}:{}删除失败".format(name, image['digest']))
        print("{}镜像删除完毕".format(name))
        return True
    return False


def clearUpBuckets(url):
    data = {"schedule": {"type": "Manual"}, "parameters": {"delete_untagged": "true", "dry_run": "false"}}
    resp = requests.post(url, headers=header, auth=auth, data=json.dumps(data))
    if resp.status_code == 201:
        print("清除完成")


if __name__ == "__main__":
    urls = ["http://172.16.102.78/api/v2.0/projects/anxin/repositories/", "http://172.16.102.78/api/v2.0/projects/h5/repositories/"]
    clearUpurl = 'http://172.16.102.78/api/v2.0/system/gc/schedule'
    result = False
    for url in urls:
        result = get_each_image_info(url)
        if result:
            clearUpBuckets(clearUpurl)
