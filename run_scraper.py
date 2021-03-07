from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scraper.spiders.auma import AumaSpider
import requests
import json

cookies = {
    'ASP.NET_SessionId': 'jnf33gk1i14vgschnvnrd3di',
    'BT_sdc': 'eyJldF9jb2lkIjoiTkEiLCJyZnIiOiIiLCJ0aW1lIjoxNjE0NjkyOTQ1NTcwLCJwaSI6MCwiZXVybCI6Imh0dHBzOi8vd3d3LmF1bWEuZGUvZW4vZXhoaWJpdC9maW5kLXlvdXItZXhoaWJpdGlvbnMiLCJyZXR1cm5pbmciOjAsImV0Y2NfY21wIjoiTkEiLCJzbXMiOm51bGwsIm5vV1MiOiI5WDlTVG0ifQ%3D%3D',
    'isSdEnabled': 'false',
    '_et_coid': 'c9313f6bc20d32bb8a9a89b431a3e51c',
    'WSS_FullScreenMode': 'false',
    'BT_pdc': 'eyJ2aWQiOiJOQSIsImV0Y2NfY3VzdCI6MCwiZWNfb3JkZXIiOjAsImV0Y2NfbmV3c2xldHRlciI6MCwic21zIjpudWxsLCJub19zaWduYWxpemUiOmZhbHNlfQ%3D%3D',
    'AUMA_cookieAccept': 'cookieAccept',
    'BT_ctst': '101',
}

headers = {
    'Connection': 'keep-alive',
    'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
    'Content-Type': 'application/json',
    'Origin': 'https://www.auma.de',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://www.auma.de/en/exhibit/find-your-exhibitions',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8',
}

data = '{"searchTitle":"","searchCity":"","searchFedstate":"","searchCountry":"","searchContinent":"","searchOrganizer":"","searchBranch":"","searchBranchKeyword":"","searchYearFrom":"","searchMonthFrom":"","searchYearTo":"","searchMonthTo":"","filterAMP":false,"filterLPAFedstate":"","filterLPA":false,"filterEE":false,"filterJIU":false,"filterHD":false,"filterHN":false,"filterHR":false,"filterNV":false,"filterFKM":false,"filterGTQ":false,"filterCity":"","filterFedState":"","filterCountry":"","filterContinent":"","filterBranch":"","filterBranchKeyword":"","filterYear":"","filterMonth":"","exhibitorsPromo":"false","currentFilterSection":"","showallFairs":"true","nextTradeFairs":"false","strLanguage":"ENG","strSort":"","strUpdate":""}'

response = requests.post('https://www.auma.de/_layouts/15/aumatradefairdata/sharepointservice.asmx/getTradefairList',
                         headers=headers, cookies=cookies, data=data)

content = json.loads(response.text)

content_json = json.loads(content['d'])

trade_fairs = content_json['SimpleTradeFairs']

exhibitions_urls = ['https://www.auma.de' + t['TFDetailsURL'] for t in trade_fairs]

s = get_project_settings()

proc = CrawlerProcess(s)

proc.crawl(AumaSpider, exhibitions_urls, headers)
proc.start()
