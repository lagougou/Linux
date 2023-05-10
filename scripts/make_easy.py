import hmac, hashlib, datetime
import requests, json

def create_header():
    api_key = '9c723852-f2b3-4832-bd38-677da2aa6451'
    secret_key = 'f1bf32cd-9e38-436b-81f1-710b37ac71c9'

    request_date = datetime.datetime.strftime(datetime.datetime.utcnow(), '%a, %d %b %Y %H:%M:%S GMT')

    # print(request_date)
    hmac_text = hmac.new(bytes(secret_key, "UTF-8"), bytes(request_date, "UTF-8"), hashlib.sha1).hexdigest()

    headers = {
                "Content-Type": "application/json",
                "x-dnsme-hmac": hmac_text,
                "x-dnsme-apiKey": api_key,
                "x-dnsme-requestDate": request_date,
            }
    return headers





response = requests.get("https://api.dnsmadeeasy.com/V2.0/dns/managed", headers=create_header())
domains = response.json()['data']
data = []
for d in domains:
    # ids.append(d['id'])
    resp = requests.get("https://api.dnsmadeeasy.com/V2.0/dns/managed/{}/records".format(d['id']), headers=create_header())
    records = resp.json()['data']
    for r in records:
        if r['value'] == "a83e737bc4e9f4b7db7bfc638fdaff8f-a8841a2f00884bf4.elb.ap-southeast-1.amazonaws.com.":
            # print(r['ttl'])
            # r["ttl"] = 86400
            r['value'] = "a2e62b5e18c124b76b32c96d4ef2c05c-6a02383ca379d450.elb.ap-southeast-1.amazonaws.com."
            res = requests.put("https://api.dnsmadeeasy.com/V2.0/dns/managed/{}/records/{}".format(d['id'], r['id']),headers=create_header(), data=json.dumps(r))
            if res.status_code == 200:
                print("{}.{} 更新成功".format(r['name'], d['name']))
