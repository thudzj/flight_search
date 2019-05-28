#-*- coding: utf-8 -*-
# python 3.5.0
 
import json
import time
import random
import datetime
import sqlalchemy
import urllib.request
import pandas as pd
from operator import itemgetter
from dateutil.parser import parse
import requests
from urllib.parse import urlencode
import hashlib
 
def crawl_ctrip(fromcity, fromcode, tocity, tocode, fromdate, returndate, useragent):
  fromdate = datetime.datetime.strptime(fromdate,'%Y-%m-%d').date()
  returndate = datetime.datetime.strptime(returndate,'%Y-%m-%d') if returndate else None
  url = 'https://flights.ctrip.com/itinerary/oneway/%s-%s?date=%s' % (fromcode,tocode,fromdate)
  headers = {
    "Host": "flights.ctrip.com",
    "User-Agent": useragent,
    "Referer": "https://flights.ctrip.com/booking/%s-%s-day-1.html?DDate1=%s" % (fromcode,tocode,fromdate),
    "Connection": "keep-alive",
  }
  req = urllib.request.Request(url,headers=headers)
  body = urllib.request.urlopen(req,timeout=30).read()
  
  #parse(body)
  
  return []
  
def crawl_qunar(fromcity, fromcode, tocity, tocode, fromdate, returndate, useragent):
  fromdate = datetime.datetime.strptime(fromdate,'%Y-%m-%d').date()
  returndate = datetime.datetime.strptime(returndate,'%Y-%m-%d') if returndate else None
  url = 'https://flight.qunar.com/site/oneway_list.htm'
  
  headers = {
    "User-Agent": useragent,
    "Referer": "https://flight.qunar.com/",
    "Connection": "keep-alive",
  }
  data = {
      'searchDepartureAirport': fromcity,
      'searchArrivalAirport': tocity,
      'searchDepartureTime': fromdate,
      'searchArrivalTime': fromdate,
      'nextNDays': '0',
      'startSearch': 'true',
      'fromCode': fromcode,
      'tocode': tocode,
      'from': 'home',
      'lowestPrice': 'null'
  }
  r = requests.get(url, params=data, headers=headers)
  # soup = BS(r.text, 'html')
  # for item in soup.findAll('strong'):
    # ...
  return []
 
def crawl_tripsky(fromcity, fromcode, tocity, tocode, fromdate, returndate, useragent):
  fromdate = str(datetime.datetime.strptime(fromdate,'%Y-%m-%d').date())
  returndate = str(datetime.datetime.strptime(returndate,'%Y-%m-%d')) if returndate else fromdate
  url = 'http://api.tripsky.com.cn/ctrip/API/ctripPolicy.php'
  data = {
      'username': "KKKKKKK",
      'password': "XXXXXXX",
      'startDate': fromdate,
      'endDate': returndate,
      'depcity': fromcity,
      'arrcity': tocity,
      'code2': "MF",
  }

  # 获取sign
  sign = ''
  for i in data.values():
      sign += i

  # 使用md5加密
  sign = hashlib.md5(sign.encode('utf-8')).hexdigest()
  print(sign)

  # 将sign添加到data字典
  data['sign'] = sign
  print(data)

  # 发送post请求
  response = requests.post(url, data=data).content
  print(response)
  return response

 
class FLIGHT(object):
  def __init__(self):
    self.Airline = {} #航空公司代码
    #self.engine = sqlalchemy.create_engine("mssql+pymssql://kk:kk@HZC/Myspider")
    self.url = ''
    self.headers = {}
    self.city={"AAT":"阿勒泰","ACX":"兴义","AEB":"百色","AKU":"阿克苏","AOG":"鞍山","AQG":"安庆","AVA":"安顺","AXF":"阿拉善左旗","BAV":"包头","BFJ":"毕节","BHY":"北海"
    ,"BJS":"北京","BPE":"秦皇岛","BPL":"博乐","BPX":"昌都","BSD":"保山","CAN":"广州","CDE":"承德","CGD":"常德","CGO":"郑州","CGQ":"长春","CHG":"朝阳","CIF":"赤峰"
    ,"CIH":"长治","CKG":"重庆","CSX":"长沙","CTU":"成都","CWJ":"沧源","CYI":"嘉义","CZX":"常州","DAT":"大同","DAX":"达县","DBC":"白城","DCY":"稻城","DDG":"丹东"
    ,"DIG":"香格里拉(迪庆)","DLC":"大连","DLU":"大理","DNH":"敦煌","DOY":"东营","DQA":"大庆","DSN":"鄂尔多斯","DYG":"张家界","EJN":"额济纳旗","ENH":"恩施"
    ,"ENY":"延安","ERL":"二连浩特","FOC":"福州","FUG":"阜阳","FUO":"佛山","FYJ":"抚远","GOQ":"格尔木","GYS":"广元","GYU":"固原","HAK":"海口","HDG":"邯郸"
    ,"HEK":"黑河","HET":"呼和浩特","HFE":"合肥","HGH":"杭州","HIA":"淮安","HJJ":"怀化","HKG":"香港","HLD":"海拉尔","HLH":"乌兰浩特","HMI":"哈密","HPG":"神农架"
    ,"HRB":"哈尔滨","HSN":"舟山","HTN":"和田","HUZ":"惠州","HYN":"台州","HZG":"汉中","HZH":"黎平","INC":"银川","IQM":"且末","IQN":"庆阳","JDZ":"景德镇"
    ,"JGD":"加格达奇","JGN":"嘉峪关","JGS":"井冈山","JHG":"西双版纳","JIC":"金昌","JIQ":"黔江","JIU":"九江","JJN":"晋江","JMJ":"澜沧","JMU":"佳木斯","JNG":"济宁"
    ,"JNZ":"锦州","JSJ":"建三江","JUH":"池州","JUZ":"衢州","JXA":"鸡西","JZH":"九寨沟","KCA":"库车","KGT":"康定","KHG":"喀什","KHN":"南昌","KJH":"凯里","KMG":"昆明"
    ,"KNH":"金门","KOW":"赣州","KRL":"库尔勒","KRY":"克拉玛依","KWE":"贵阳","KWL":"桂林","LCX":"龙岩","LDS":"伊春","LFQ":"临汾","LHW":"兰州","LJG":"丽江","LLB":"荔波"
    ,"LLF":"永州","LLV":"吕梁","LNJ":"临沧","LPF":"六盘水","LUM":"芒市","LXA":"拉萨","LYA":"洛阳","LYG":"连云港","LYI":"临沂","LZH":"柳州","LZO":"泸州"
    ,"LZY":"林芝","MDG":"牡丹江","MFK":"马祖","MFM":"澳门","MIG":"绵阳","MXZ":"梅州","NAO":"南充","NBS":"白山","NDG":"齐齐哈尔","NGB":"宁波","NGQ":"阿里"
    ,"NKG":"南京","NLH":"宁蒗","NNG":"南宁","NNY":"南阳","NTG":"南通","NZH":"满洲里","OHE":"漠河","PZI":"攀枝花","RHT":"阿拉善右旗","RIZ":"日照","RKZ":"日喀则"
    ,"RLK":"巴彦淖尔","SHA":"上海","SHE":"沈阳","SIA":"西安","SJW":"石家庄","SWA":"揭阳","SYM":"普洱","SYX":"三亚","SZX":"深圳","TAO":"青岛","TCG":"塔城","TCZ":"腾冲"
    ,"TEN":"铜仁","TGO":"通辽","THQ":"天水","TLQ":"吐鲁番","TNA":"济南","TSN":"天津","TVS":"唐山","TXN":"黄山","TYN":"太原","URC":"乌鲁木齐","UYN":"榆林","WEF":"潍坊"
    ,"WEH":"威海","WMT":"遵义(茅台)","WNH":"文山","WNZ":"温州","WUA":"乌海","WUH":"武汉","WUS":"武夷山","WUX":"无锡","WUZ":"梧州","WXN":"万州","XFN":"襄阳","XIC":"西昌"
    ,"XIL":"锡林浩特","XMN":"厦门","XNN":"西宁","XUZ":"徐州","YBP":"宜宾","YCU":"运城","YIC":"宜春","YIE":"阿尔山","YIH":"宜昌","YIN":"伊宁","YIW":"义乌","YNJ":"延吉"
    ,"YNT":"烟台","YNZ":"盐城","YTY":"扬州","YUS":"玉树","YZY":"张掖","ZAT":"昭通","ZHA":"湛江","ZHY":"中卫","ZQZ":"张家口","ZUH":"珠海","ZYI":"遵义(新舟)"}
    """{"KJI":"布尔津"}"""
    self.UserAgent = [
      "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
      "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0) Gecko/16.0 Firefox/16.0",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
      "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
      "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
      "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1500.55 Safari/537.36",
      "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
      "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
      "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
      "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    ]
    self.crawl_funcs = [crawl_ctrip, crawl_qunar, crawl_tripsky]
  
  def respond_to_query(self, fromcity, tocity, fromdate, returndate=None):
    fromcode = list(self.city.keys())[list(self.city.values()).index(fromcity)]
    tocode = list(self.city.keys())[list(self.city.values()).index(tocity)]
    if fromcode == tocode:
      return
      
    outputs = []
    for func in self.crawl_funcs:
      outputs += func(fromcity, fromcode, tocity, tocode, fromdate, returndate, random.choice(self.UserAgent))

    
if __name__ == "__main__":
  fly = FLIGHT()
  fly.respond_to_query("北京", "上海", '2019-06-16')