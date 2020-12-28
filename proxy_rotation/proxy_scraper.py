from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException


# 'SSL': 'https://www.sslproxies.org/',
# 'GOOGLE': 'https://www.google-proxy.net/',
# 'ANANY': 'https://free-proxy-list.net/anonymous-proxy.html',
# 'UK': 'https://free-proxy-list.net/uk-proxy.html',
# 'US': 'https://www.us-proxy.org/',
# 'NEW': 'https://free-proxy-list.net/',
# 'SPYS.ME': 'http://spys.me/proxy.txt',
# 'proxyscrape': 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all',
# 'ALL': 'ALL'


def create_proxy_list():
    scrapper = Scrapper(category='SPYS.ME', print_err_trace=False)
    data = scrapper.getProxies()

    with open('proxy_rotation/proxies.txt', 'w') as f:
        for item in data.proxies:
            f.write('https://{}:{}\n'.format(item.ip, item.port, item))
