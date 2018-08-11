#coding:utf-8
import codecs
import requests
from urllib.parse import urlencode
from lxml import etree
import time
import sys
import io
import os

def query_files(formfilenames,fo=sys.stdout):
    web_data = requests.post('http://nvsm.cnki.net/kns/ViewPage/viewsave.aspx?displayMode=elearning', 
        data={
            'formfilenames':",".join(formfilenames)})
    ftext=etree.HTML(web_data.text)
    for elm in ftext.xpath('//table[@class="mainTable"]//td'):
        for d in elm.xpath('.//text()'):
            print(d, file=fo)
    fo.flush()

def search(key,fo=sys.stdout,page=1):
    # 不带cookie的请求头，从chrome复制的
    headers={
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, sdch",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "Connection":"keep-alive",
        "Host":"nvsm.cnki.net",
        "Referer":"http://nvsm.cnki.net/kns/brief/default_result.aspx",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    }
    # searchHandler的post参数
    formdata_searchHandler={
        "action":"",
        "NaviCode":"*",
        "ua":"1.11",
        "isinEn":"1",
        "PageName":"ASP.brief_default_result_aspx",
        "DbPrefix":"SCDB",
        "DbCatalog":"中国学术文献网络出版总库",
        "ConfigFile":"SCDBINDEX.xml",
        "db_opt":"CJFQ,CJRF,CDFD,CMFD,CPFD,IPFD,CCND,CCJD",
        "txt_1_sel":"SU$%=|",
        "txt_1_value1":key,
        "txt_1_special1":"%",
        "his":"0",
        "parentdb":"SCDB",
    }
    # Session可以保持请求的状态，保持不同请求之间cookie沿用相同的cookie
    s=requests.Session()
    # post请求之后服务器才有用户的记录，否则无法获得搜索结果列表，说用户不存在
    s.post('http://nvsm.cnki.net/kns/request/SearchHandler.ashx',data=formdata_searchHandler,headers=headers)
    # brief里是搜索结果
    url='http://nvsm.cnki.net/kns/brief/brief.aspx?'
    parameter={
        "pagename":"ASP.brief_default_result_aspx",
        "dbPrefix":"SCDB",
        "keyValue":key,
        "S":"1",
        "sorttype":"(FFD,'RANK') desc",
    }
    response=s.get(url+urlencode(parameter),headers=headers)
    selector=etree.HTML(text=response.text)
    lst=selector.xpath('//input[@type="checkbox"]/@value')
    QueryID = ",".join(lst).split('!')[-1]
    print('QueryID=' + QueryID)
    i=page
    while(True):
        print('page=' + str(i))
        param = parameter.copy()
        param.update({
                "curpage":str(i),
                "RecordsPerPage":"20",
                "QueryID":QueryID,
                "turnpage":"1",
                "tpagemode":"L"
            })
        try:
            # 用urlencode构建网址
            response=s.get(url+urlencode(param),headers=headers)
            selector=etree.HTML(text=response.text)
            lst=selector.xpath('//input[@type="checkbox"]/@value')
            if len(lst) > 0:
                i=i+1
                print(lst)
                QueryID = ",".join(lst).split('!')[-1]
                query_files(lst,fo)
            else:
                raise RuntimeError('err')
        except Exception as e:
            if(str(e)!='err'):
                print(e)
                os.system("pause")
            else:
                return i
    


if __name__ == '__main__':
    key='人工智能'
    fo = codecs.open("out/"+key+".txt", "w", encoding='utf-8')
    i = 1
    while(True):
        newi = search(key,fo, i)
        if(newi==i):
            os.system("pause")
        i=newi
