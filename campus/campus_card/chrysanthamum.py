import requests


def Nx():
    try:
        proxy = {
            'http': 'http://baidu.com',
            'https': 'http://baidu.com'
        }
        '''head 信息'''
        head = {'User-Agent': 'User-Agent": "NCP/5.3.1 (iPhone; iOS 13.5; Scale/2.00)', 'Connection': 'keep-alive'}
        # http://icanhazip.com
        k = requests.get('http://icanhazip.com', headers=head, proxies=proxy)
        print(k.text)
    except Exception as err:
        print(err)