# import re
# import time
# import subprocess
# from datetime import datetime
# from io import StringIO

# def main(domain):
#     f = StringIO()
#     comm = f"curl -Ivs https://{domain} --connect-timeout 10"

#     result = subprocess.getstatusoutput(comm)
#     f.write(result[1])
#     print(result)
#     m = re.search('start date: (.*?)\n.*?expire date: (.*?)\n.*?common name: (.*?)\n.*?issuer: CN=(.*?)\n', f.getvalue(), re.S)
#     start_date = m.group(1)
#     expire_date = m.group(2)
#     common_name = m.group(3)
#     issuer = m.group(4)

#     # time 字符串转时间数组
#     start_date = time.strptime(start_date, "%b %d %H:%M:%S %Y GMT")
#     start_date_st = time.strftime("%Y-%m-%d %H:%M:%S", start_date)
#     # datetime 字符串转时间数组
#     expire_date = datetime.strptime(expire_date, "%b %d %H:%M:%S %Y GMT")
#     expire_date_st = datetime.strftime(expire_date,"%Y-%m-%d %H:%M:%S")

#     # 剩余天数
#     remaining = (expire_date-datetime.now()).days

#     print ('域名:', domain)
#     print ('通用名:', common_name)
#     print ('开始时间:', start_date_st)
#     print ('到期时间:', expire_date_st)
#     print (f'剩余时间: {remaining}天')
#     print ('颁发机构:', issuer)
#     print ('*'*30)

#     time.sleep(0.5)

# if __name__ == "__main__":
#     domains = ['www.e-pex.com'] 
#     for domain in domains:
#         main(domain)
from OpenSSL import SSL
from cryptography import x509
from cryptography.x509.oid import NameOID
import idna

from socket import socket
from collections import namedtuple
# import datetime
from datetime import datetime
import yagmail

HostInfo = namedtuple(field_names='cert hostname peername', typename='HostInfo')

HOSTS = [
    ('www.e-pex.com', 443),
]

def verify_cert(cert, hostname):
    # verify notAfter/notBefore, CA trusted, servername/sni/hostname
    cert.has_expired()
    # service_identity.pyopenssl.verify_hostname(client_ssl, hostname)
    # issuer

def get_certificate(hostname, port):
    hostname_idna = idna.encode(hostname)
    sock = socket()

    sock.connect((hostname, port))
    peername = sock.getpeername()
    ctx = SSL.Context(SSL.SSLv23_METHOD) # most compatible
    ctx.check_hostname = False
    ctx.verify_mode = SSL.VERIFY_NONE

    sock_ssl = SSL.Connection(ctx, sock)
    sock_ssl.set_connect_state()
    sock_ssl.set_tlsext_host_name(hostname_idna)
    sock_ssl.do_handshake()
    cert = sock_ssl.get_peer_certificate()
    crypto_cert = cert.to_cryptography()
    sock_ssl.close()
    sock.close()

    return HostInfo(cert=crypto_cert, peername=peername, hostname=hostname)

def get_alt_names(cert):
    try:
        ext = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName)
        return ext.value.get_values_for_type(x509.DNSName)
    except x509.ExtensionNotFound:
        return None

def get_common_name(cert):
    try:
        names = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None

def get_issuer(cert):
    try:
        names = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
        return names[0].value
    except x509.ExtensionNotFound:
        return None


def print_basic_info(hostinfo):
    s = '''» {hostname} « … {peername}
    \tcommonName: {commonname}
    \tSAN: {SAN}
    \tissuer: {issuer}
    \tnotBefore: {notbefore}
    \tnotAfter:  {notafter}
    '''.format(
            hostname=hostinfo.hostname,
            peername=hostinfo.peername,
            commonname=get_common_name(hostinfo.cert),
            SAN=get_alt_names(hostinfo.cert),
            issuer=get_issuer(hostinfo.cert),
            notbefore=hostinfo.cert.not_valid_before,
            notafter=hostinfo.cert.not_valid_after
    )
    
    # ca_date = datetime.strptime(str(hostinfo.cert.not_valid_after), '%Y%m%d%H%M%S')
    # ca_date = time.mktime(hostinfo.cert.not_valid_after)
    # print(type(hostinfo.cert.not_valid_after))
    time_delta = (hostinfo.cert.not_valid_after - datetime.now()).days
    if time_delta < 350:
        send_mail(hostinfo.hostname, time_delta)
    print(s)

def check_it_out(hostname, port):
    hostinfo = get_certificate(hostname, port)
    print_basic_info(hostinfo)

def send_mail(domain, remainDays):
    user = 'jiangrui@greenlandfinancial.com'
    password = 'Jr992716'
    host = 'smtp.mxhichina.com'
    to = 'jiangrui@greenlandfinancial.com'
    subject = 'ssl 证书过期告警'
    html = '''
            <h1> 证书过期通知 </h1>
            <p>域名: {0} 证书有效期还剩 {1} 天 
            '''.format(domain, remainDays)
    yag = yagmail.SMTP(user=user, password=password, host=host)
    yag.send(to=to, subject=subject, contents=html)

    
import concurrent.futures
if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        for hostinfo in e.map(lambda x: get_certificate(x[0], x[1]), HOSTS):
            print_basic_info(hostinfo)

