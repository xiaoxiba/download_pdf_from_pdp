import requests
import base64
from lxml import html
from requests_ntlm import HttpNtlmAuth
from urllib.parse import urlparse, parse_qs

from html.parser import HTMLParser

import os
import getpass
import csv
import string
import pdb


class SSOSite(requests.Session):
    def __init__(self, baseurl, login_page='/'):
        super(SSOSite, self).__init__()
        self.baseurl = baseurl
        """
        with open("secret.txt", "rb") as fd:
            encoded = fd.read()
            self.password = str(base64.b64decode(encoded), 'utf-8')
        """
    def login(self, username, password):
        self.auth = HttpNtlmAuth('nvidia.com\\' + username, password, self)
        result = self.get(
        'https://ssoauth.nvidia.com/siteminderagent/ntlm/creds.ntc?CHALLENGE=&SMAGENTNAME=-SM-g29Lry3kCzPVuHmEXFRjSLOUUbtBVpl%2f7ptElB5BWROOZLaZSFXKsVGcly19D3p0&TARGET=-SM-http%3a%2f%2fnvplm%2envidia%2ecom%2fWindchill',
        auth=self.auth)
        if (result.status_code == 401):
            print(result)
            print('Login Failed')
        else:
            print('Login Successful')
    def download(self, url, name_prefix='Dummy'):
        # open in binary mode
        parsed = urlparse(url)
        
        file_name = (parse_qs(parsed.query)['originalFileName'])[0]
        
        file_name = name_prefix + '_' + file_name # put name_suffix into file name for easy search, and save to \download folder
        print("File is stored as ", file_name)
        
        with open(file_name, "wb") as file:
            # get request
            response = s.get(url)
            # write to file
            file.write(response.content)

def file2nvpn(file_name):
    """ input file is .txt file with NVPN on each line
    """   
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file)
        dict_nvpn = {}
        # make {nvpn : mfgpn} dictionary from csv file
        for row in reader:
            nvpn = row['Number']
            mfgpn = row['Manufacturer Part Number']
            dict_nvpn[nvpn] = mfgpn

    #remove invalid file name char from mfgpn to avoid download issue
    invalid_list = ['\\','/',':','*','?','\"','<','>','|']
    for nvpn in dict_nvpn:
        mfgpn = dict_nvpn[nvpn]
        for invalid_char in invalid_list:
            mfgpn = mfgpn.replace(invalid_char,'-')
        dict_nvpn[nvpn] = mfgpn
            
    print('will download PDF for below nvpn:')
    for nvpn in dict_nvpn:
        print(nvpn,':',dict_nvpn[nvpn])
    return dict_nvpn

            
if __name__ == '__main__':

    #print information for user reference
    print('=============usage notice==================================================')
    print('The NVPN list is in nvpn.csv file, with "Name" colum for NVPN and "Manufacturer Part Number" colum for mfg PN')
    print('Files will be downloaded to "download" folder')
    print('Check log file in "log" folder for those failed to download')
    print('===========================================================================')

    # get username
    username = input("Enter your username: ")
    password = getpass.getpass('Enter your password: ')

    
    s = SSOSite(
            'https://ssoauth.nvidia.com/siteminderagent/ntlm/creds.ntc?CHALLENGE=&SMAGENTNAME=-SM-g29Lry3kCzPVuHmEXFRjSLOUUbtBVpl%2f7ptElB5BWROOZLaZSFXKsVGcly19D3p0&TARGET=-SM-http%3a%2f%2fnvplm%2envidia%2ecom%2fWindchill')
    # AD username
    s.login(username,password)

    # get NVPN list
    #convert csv file into nvpn dictionary with {nvpn: mfgpn}
    file_name = 'nvpn.csv'
    dict_nvpn = file2nvpn(file_name)

    #prepare download folder
    if not(os.path.exists('download') and os.path.isdir('download')):
        os.mkdir('download')
    if not(os.path.exists('log') and os.path.isdir('log')):
        os.mkdir('log')

    #start download
    log = {}
    for nvpn in sorted(dict_nvpn):
        
        mfgpn = dict_nvpn[nvpn]
        name_prefix = '.\\download\\' + nvpn + '_' + mfgpn  # use folder+nvpn+mfgpn as file name prefix
        
        url_link =  'https://nvplm.nvidia.com/mfgspec/' + nvpn           ###url of the file u want to download

        # the download may have exception
        try:
            r = s.get(url_link)  ###url of the file u want to download
            tree = html.fromstring(r.content)
            location = tree.xpath('//table/tr/td[1]/text()')
            #print (location[0])
            s.download(location[0],name_prefix)
        except:
            warning = str(tree.xpath('//*[@id="mainform"]/p[1]/b/text()'))  # get warning message if download fail
            print(nvpn, 'can not be downloaded. Please check again')
            log[nvpn] = warning      #record warning to log dictionary

    #record failed items into log file
    with open('.\\log\\failed_nvpn_log.txt','w') as fail_log:
        for nvpn in log:
            fail_log.write(nvpn + log[nvpn] + '\n')       
        print('failed NVPN is recorded in .\\log\\failed_nvpn_log.txt, please check')
    
    print('Failed to download below NVPN: ')
    for nvpn in log:
        print(nvpn)
                 
    print('Done.')




