import re
import hashlib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart,MIMEBase
import smtplib
import json
import requests
from  pyquery import PyQuery as pq
from requests.exceptions import RequestException
from selenium import webdriver


class SendMail:

    def __init__(self):
        self.from_addr = '1214251739@qq.com'
        self.password = 'erkezuuzeesgiagb'  # qq授权码
        #349176813@qq.com
        haixin = '349176813@qq.com'
        ws1 = '476301176@qq.com'
        ws2 = 'wangsheng9297@163.com'
        self.to_addr = [haixin,ws2]
        self.smtp_server = 'smtp.qq.com'
        self.msg = ''
        self.server = smtplib.SMTP_SSL()
        self.__configServer()

    def __format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    def __configServer(self):
        self.server = smtplib.SMTP_SSL(self.smtp_server, 465)  # 使用SSL加密传输
        # self.server.set_debuglevel(1)
        self.server.login(self.from_addr, self.password)


    def sendPlainEmail(self, text):
        msg = MIMEText(text, 'plain', 'utf-8')
        msg['From'] = self.__format_addr('我是勤劳的小爬虫 <%s>' % self.from_addr)
        # s1 = ','.join(self.to_addr)

        msg['To'] = ','.join(self.to_addr)
        msg['Subject'] = Header('小主，您的新闻又更新啦', 'utf-8').encode()
        self.msg = msg
        self.__sendEamil()

    def sendAttachEmail(self,picPath):
        self.msg = MIMEMultipart()
        self.msg['From'] = self.__format_addr('Python爱好者 <%s>' % self.from_addr)
        self.msg['To'] = self.__format_addr('管理员 <%s>' % self.to_addr)
        self.msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()

        # 邮件正文是MIMEText:
        self.msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
        #添加图片附件
        with open(picPath, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('image', 'png', filename='test.png')
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename='test.png')
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            self.msg.attach(mime)

        # 添加附件2，传送当前目录下的 1.txt 文件
        att1 = MIMEText(open('1.txt', 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename="test.txt"'
        self.msg.attach(att1)
        self.__sendEamil()


    def __sendEamil(self):
        self.server.sendmail(self.from_addr, self.to_addr, self.msg.as_string())
        self.server.quit()



foshan = 'http://bendi.news.163.com/guangdong/special/04178D7C/foshanjbc.js'
dongguan = 'http://bendi.news.163.com/guangdong/special/04178D75/dongduanxinxiliu.js'
zhanjiang = 'http://bendi.news.163.com/guangdong/special/04178DAL/zhanjiangxinxiliu.js'
shantou = 'http://bendi.news.163.com/guangdong/special/04178D9D/xinxiliu.js'
chaozhou = 'http://bendi.news.163.com/guangdong/special/04178D6T/czxinxiliu.js'
jieyang = 'http://bendi.news.163.com/guangdong/special/04178D8D/jyxinxiliu.js'
zhuhai = 'http://bendi.news.163.com/guangdong/special/04178SVQ/web_index2016_centernews1.js'
huizhou = 'http://bendi.news.163.com/guangdong/special/04178KC4/hzxinxiliu.js'
shaoguan = 'http://bendi.news.163.com/guangdong/special/04178D9T/sgxinxiliu.js'
CSLJL = 'http://www.zsbtv.com.cn/a/spyp/dslm/cityzero/two_zerolist.shtml'
XQRX = 'http://www.fstv.com.cn/news/xqrx'
ZHYW = 'http://www.hizh.cn/localnews/index.jhtml'
MMXW = 'http://www.mm111.net/news/mmxw/'
#38：广州，39：深圳，85：珠海，87：汕头，韶关：90，惠州：76，东莞：41，湛江：75
SouthPlus = 'https://api.nfapp.southcn.com/nanfang_if/getArticles?columnId=14&lastFileId=0&count=20&rowNumber=0&version=0'
ChinaWeather = 'http://www.weather.com.cn/alarm/newalarmlist.shtml?areaId=10128'

#各大城市最后一次爬取的新闻内容
CSLJLLastparsedString =''
XQRXLastparsedString =''
ZHYWLastparsedString =''
MMXWLastparsedString = ''
SouthPlusLastparsedString =''
ChinaWeatherLastparsedString =''
WANGYINewsDic = {
    'foshan_KEY': '',
    'dongguan_KEY':'',
    'zhanjiang_KEY':'',
    'shantou_KEY':'',
    'chaozhou_KEY':'',
    'jieyang_KEY':'',
    'zhuhai_KEY':'',
    'shaoguan_KEY':'',
    'huizhou_KEY':''
}



SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']



class parseHtml:
    def  getStaticHtmlConten(self, url):
        header = \
            {
                "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
            }

        header1={
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
            "qn-sig": "C2FF49006F008FF8F5E143E6DB0B3B10",
            "idfa":"00000000-0000-0000-0000-000000000000",
            "appver": "10.3.2_qqnews_5.3.9",
            "Accept-Language": "zh-Hans-CN;q=1, zh-Hant-CN;q=0.9",
            "qn-rid": "1f468c0c232f",
            "qqnetwork": "wifi",
            "deviceToken": "<eb7c0e06 36eecbda 871c9b7a 0c51af62 416f9029 9f5c94f5 3c1cc87e 8f97848c>",
            "devid": "f2ba7649-c5e0-467f-b31e-23d9ae8eab7b",
            "User-Agent" :"QQNews/5.3.9 (iPhone; iOS 10.3.2; Scale/2.00)",
            "Referer": "http://inews.qq.com/inews/iphone/",
            "Content-Length" :68,
            "Accept-Encoding" :"gzip, deflate",
            "Connection" :"keep-alive",
            "Cookie" :"openid=oI6CFjhAqmKDJ-KEfync6k3C1xNQ;%20appid=wx073f4a4daff0abe8;%20access_token=ge7PSrSzQfUlQGjmY-fPDLlfx--K4VuU1EUNhAFJ7N2eNAFFWR4OJczqKnKEpixEMcX5DMG20AgWR78px-3bTg;%20refresh_token=ge7PSrSzQfUlQGjmY-fPDEVhmXzw2JkcJDy8nncyck8RuSM6Dyaj2e8EUZq9qZPEh08aHPV43oxol_evhuQfkg;%20unionid=onCs1uIomD4WW3eutmrgZHVuCsSk;%20logintype=1",
            "store": 1
        }

        datas ={
            'uid':'05DCC486-E375-40A5-9354-3D929F1C790E',
            'child':'5317581',
            'media_openid':''

        }

        cookies = {'openid':'oI6CFjhAqmKDJ-KEfync6k3C1xNQ', 'appid':'wx073f4a4daff0abe8', 'access_token':'ge7PSrSzQfUlQGjmY-fPDLlfx--K4VuU1EUNhAFJ7N2eNAFFWR4OJczqKnKEpixEMcX5DMG20AgWR78px-3bTg', 'refresh_token':'ge7PSrSzQfUlQGjmY-fPDEVhmXzw2JkcJDy8nncyck8RuSM6Dyaj2e8EUZq9qZPEh08aHPV43oxol_evhuQfkg','unionid':'onCs1uIomD4WW3eutmrgZHVuCsSk','logintype':1}

        try:
            r = requests.post(url, headers=header1,data=datas)
            if r.status_code == 200:
                r.encoding = r.apparent_encoding
                text = r.text
                return text
            return None
        except RequestException:
            return None



    def getCSLJLNews(self):
        global CSLJLLastparsedString
        htmlContent = self.getStaticHtmlConten(CSLJL)
        doc = pq(htmlContent)
        # .zsbtv-cont:first-child-----》父元素里面class=.zsbtv-cont的第一个标签
        # .zsbtv-cont :first-child-----》class = .zsbtv-cont元素的后代元素里面，每个元素的第一个标签
        # .zsbtv-cont>:first-child-----》父元素为.zsbtv-cont的子元素里面的第一个子元素，注意和上面的作对比，此处是直接的父子关系，上面是后代关系，不是直接的父子关系

        generator1 = list(doc('#left_list .zsbtv-cont:first-child .video_img a:first-child').items())
        generator2 = list(doc('#left_list .zsbtv-cont:first-child .video_img .video_time').items())

        list1 = []
        list2 = []
        list3 = []

        for item in generator2:
            string = item.text()+'\n'
            list1.append(string)

        for item in generator1:
            s =  'http://www.zsbtv.com.cn/' + item.attr('href')+'\n'
            list3.append(s)

        for item in generator1:
            s = item.attr('title') +'\n'
            list2.append(s)

        list4 = [str(str1) + str(str2) + str(str3) for str1, str2,str3 in zip(list1[:5], list2[:5], list3[:5])]
        parsedString = '分类：城市零距离'+'\n \n'
        parsedString += ' \n'.join(list4)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        if CSLJLLastparsedString != '':
            if self.md5(CSLJLLastparsedString) == self.md5(parsedString):
                return ''
            else:
                CSLJLLastparsedString = parsedString;
                return parsedString
        else:
            CSLJLLastparsedString = parsedString;
            return parsedString;



    def getXQRXNews(self):
        global XQRXLastparsedString
        htmlContent = self.getStaticHtmlConten(XQRX)
        doc = pq(htmlContent)

        generator1 = list(doc('#content div:nth-child(2) ul li ').items())
        generator2 = list(doc('#content div:nth-child(2) ul li .date').items())

        l1 = []
        l2 = []
        l3 = []

        for item in generator1:
            news = {
                'title':item.find('h2 a').attr('title'),
                'href': item.find('h2 a').attr('href'),
                'time': item.find('.date').text()

            }

            print(news)

            # for item in generator2:
        #     l1.append(item.text()+'\n')
        #
        # for item1 in generator1:
        #     string = item1.attr('href') + '\n'
        #     l3.append(string)
        #
        # for item in generator1:
        #     string =  item.attr('title') +'\n'
        #     l2.append(string)
        #
        #
        # l4 = [str(str1) + str(str2) + str(str3) for str1, str2,str3 in zip(l1[:5], l2[:5], l3[:5])]
        # parsedString = '分类：小强热线' + '\n \n'
        # parsedString += ' \n'.join(l4)
        # parsedString += '\n \n ===================================================================================================================================== \n \n'
        # if XQRXLastparsedString != '':
        #     if self.md5(XQRXLastparsedString) == self.md5(parsedString):
        #         return ''
        #     else:
        #         XQRXLastparsedString = parsedString;
        #         return parsedString
        # else:
        #     XQRXLastparsedString = parsedString;
        #     return parsedString;


    def getZHYWNews(self):
        global ZHYWLastparsedString
        htmlContent = self.getStaticHtmlConten(ZHYW)
        doc = pq(htmlContent)

        generator1 = list(doc('#newsList  .t_news .txt_t .news_tit02 p a').items())
        generator2 = list(doc('#newsList  .t_news .txt_t .news_info span').items())

        l1 = []
        l2 = []
        l3 = []

        for item in generator2:
            l1.append(item.text()+'\n')

        for item in generator1:
            string =  item.text() + '\n'
            l2.append(string)

        for item in generator1:
            string =  item.attr('href')+'\n'
            l3.append(string)

        l4 = [str(str1) + str(str2) + str(str3) for str1, str2, str3 in zip(l1[:5], l2[:5], l3[:5])]
        parsedString = '分类：珠海新闻网·珠海要闻' + '\n \n'
        parsedString += ' \n'.join(l4)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        if ZHYWLastparsedString != '':
            if self.md5(ZHYWLastparsedString) == self.md5(parsedString):
                return ''
            else:
                ZHYWLastparsedString = parsedString;
                return parsedString
        else:
            ZHYWLastparsedString = parsedString;
            return parsedString;



    def getMMXWNews(self):
        global MMXWLastparsedString
        htmlContent = self.getStaticHtmlConten(MMXW)
        doc = pq(htmlContent)
        generator1 = list(doc('#list  ul li h3 a ').items())
        generator2 = list(doc('#list ul li .m-imagetext div a span').items())

        l1 = []
        l2 = []
        l3 = []

        for item in generator2:
            l1.append( item.text()+'\n')

        for item in generator1:
            string =  item.text() + '\n'
            l2.append(string)

        for item in generator1:
            string =  item.attr('href')+'\n'
            l3.append(string)


        l4 = [str(str1) + str(str2) + str(str3) for str1, str2, str3 in zip(l1[:5], l2[:5], l3[:5])]
        parsedString = '分类：茂名新闻网' + '\n \n'
        parsedString += ' \n'.join(l4)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        if MMXWLastparsedString != '':
            if self.md5(MMXWLastparsedString) == self.md5(parsedString):
                return ''
            else:
                MMXWLastparsedString = parsedString;
                return parsedString
        else:
            MMXWLastparsedString = parsedString;
            return parsedString;



    def getWangYiNews(self,url):
        jsonStr = self.getStaticHtmlConten(url)
        jsonStr = re.sub('data_callback\(', '', jsonStr)
        jsonStr = re.sub('\)', '', jsonStr)

        datas = json.loads(jsonStr, strict=False)
        l1 = []
        if datas:
            for data in datas:
                string= data.get('time')+'\n' + data.get('title') +'\n' +data.get('docurl')+'\n'
                l1.append(string)
        l1 = l1[:5]
        return  self.HandleWangYiNewsUpdate(l1,url)



    def HandleWangYiNewsUpdate(self, news, url):
        global WANGYINewsDic
        if url == foshan:
            category = '网易佛山'
            key = 'foshan_KEY'
        if url == dongguan:
            category = '网易东莞'
            key = 'dongguan_KEY'
        if url == zhanjiang:
            category = '网易湛江'
            key = 'zhanjiang_KEY'
        if url == shantou:
            category = '网易汕头'
            key = 'shantou_KEY'
        if url == chaozhou:
            category = '网易潮州'
            key = 'chaozhou_KEY'
        if url == jieyang:
            category = '网易揭阳'
            key = 'jieyang_KEY'
        if url == zhuhai:
            category = '网易珠海'
            key = 'zhuhai_KEY'
        if url == huizhou:
            category = '网易惠州'
            key = 'huizhou_KEY'
        if url == shaoguan:
            category = '网易韶关'
            key = 'shaoguan_KEY'

        parsedString = '分类：%s' % category + '\n \n'
        parsedString += ' \n'.join(news)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        LastparsedString = WANGYINewsDic.get(key)
        if LastparsedString != '':
            if self.md5(LastparsedString) == self.md5(parsedString):
                return ''
            else:
                WANGYINewsDic[key] = parsedString;
                return parsedString
        else:
            WANGYINewsDic[key] = parsedString;
            return parsedString;


    def getSouthPlusNews(self):
        global SouthPlusLastparsedString
        jsonStr = self.getStaticHtmlConten(SouthPlus)

        datas = json.loads(jsonStr, strict=False)
        l1 = []
        if datas:
            for data in datas:
                string = data.get('publishtime') + '\n' + data.get('title') + '\n' + data.get('shareUrl') + '\n'
                l1.append(string)
        l1 = l1[:10]

        parsedString = '分类：南方Plus' + '\n \n'
        parsedString += ' \n'.join(l1)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        if SouthPlusLastparsedString != '':
            if self.md5(SouthPlusLastparsedString) == self.md5(parsedString):
                return ''
            else:
                SouthPlusLastparsedString = parsedString;
                return parsedString
        else:
            SouthPlusLastparsedString = parsedString;
            return parsedString;



    def getChinaWeatherNews(self):
        global  ChinaWeatherLastparsedString
        browser = webdriver.PhantomJS(service_args=SERVICE_ARGS,executable_path = '/Users/Chan/phantomjs-2.1.1-macosx/bin/phantomjs')
        browser.set_window_size(1400, 900)
        browser.get(ChinaWeather)
        htmlContent = browser.page_source

        doc = pq(htmlContent)
        generator1 = list(doc('.dDUl li a:nth-of-type(2)').items())
        generator2 = list(doc('.dDUl li span:nth-of-type(2)').items())

        l1 = []
        l2 = []

        for item1 in generator1:
            string = item1.text() + '\n' + item1.attr('href') +'\n'
            l2.append(string)


        for item2 in generator2:
            string = item2.text()+'\n'
            l1.append(string)

        l4 = [str(str1) + str(str2)  for str1, str2 in zip(l1[:10], l2[:10])]
        parsedString = '分类：中国天气网' + '\n \n'
        parsedString += ' \n'.join(l4)
        parsedString += '\n \n ===================================================================================================================================== \n \n'
        if ChinaWeatherLastparsedString != '':
            if self.md5(ChinaWeatherLastparsedString) == self.md5(parsedString):
                return ''
            else:
                ChinaWeatherLastparsedString = parsedString;
                return parsedString
        else:
            ChinaWeatherLastparsedString = parsedString;
            return parsedString;


    def sendAllNewsToEmail(self):
        news = self.getMMXWNews()+self.getZHYWNews()+self.getCSLJLNews()+self.getXQRXNews()+self.getSouthPlusNews()+self.getChinaWeatherNews()
        city_list = [foshan,dongguan,zhanjiang,shantou,chaozhou,jieyang,zhuhai,huizhou,shaoguan]
        for city in city_list:
            news += self.getWangYiNews(city)
        if news != '':
            sender = SendMail()
            sender.sendPlainEmail(news);
        return  news;


    def md5(self,text):
        m = hashlib.md5()
        m.update(text.encode('utf-8'))
        md5Str = m.hexdigest()
        return md5Str