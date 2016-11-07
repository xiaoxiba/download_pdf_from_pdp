import requests
import base64
from lxml import html
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urlparse, parse_qs

class SSOSite(requests.Session):
    def __init__(self, baseurl, login_page='/'):
        super(SSOSite, self).__init__()
        self.baseurl = baseurl
        fd = open("secret.txt", "rb")
        encoded = fd.read()
        self.password = str(base64.b64decode(encoded), 'utf-8')
    def login(self, username):
        self.auth = HttpNtlmAuth('nvidia.com\\' + username, self.password, self)
        result = self.get(
        'https://ssoauth.nvidia.com/siteminderagent/ntlm/creds.ntc?CHALLENGE=&SMAGENTNAME=-SM-g29Lry3kCzPVuHmEXFRjSLOUUbtBVpl%2f7ptElB5BWROOZLaZSFXKsVGcly19D3p0&TARGET=-SM-http%3a%2f%2fnvplm%2envidia%2ecom%2fWindchill',
        auth=self.auth)
        if (result.status_code == 401):
            print(result)
            print('Login Failed')
        else:
            print('Login Successful')
    def download(self, url):
        # open in binary mode
        parsed = urlparse(url)
        print("File is stored as ", parse_qs(parsed.query)['originalFileName'])
        file_name = (parse_qs(parsed.query)['originalFileName'])[0]
        with open(file_name, "wb") as file:
            # get request
            response = s.get(url)
            # write to file
            file.write(response.content)

if __name__ == '__main__':
    username = input("Enter your username: ")
    s = SSOSite(
            'https://ssoauth.nvidia.com/siteminderagent/ntlm/creds.ntc?CHALLENGE=&SMAGENTNAME=-SM-g29Lry3kCzPVuHmEXFRjSLOUUbtBVpl%2f7ptElB5BWROOZLaZSFXKsVGcly19D3p0&TARGET=-SM-http%3a%2f%2fnvplm%2envidia%2ecom%2fWindchill')
    # AD username
    s.login(username)   
    r = s.get('https://nvplm.nvidia.com/mfgspec/131-0542-000')  ###url of the file u want to download
    tree = html.fromstring(r.content)
    location = tree.xpath('//table/tr/td[1]/text()')
    print (location[0])
    s.download(location[0])
    print('Done.')

