import builtwith
import whois
import urllib2
import itertools
import re
import urlparse
import robotparser

#识别网站所用技术
def parsebuilt(url):
    return builtwith.parse(url)

#寻找网站所有者
def parsewhois(url):
    return  whois.whois(url)

#支持捕获异常重试下载设置用户代理的下载网页函数
def download(url,user_agent = 'wswp',num_retries=2l):
    print 'Downloading:',url
    headers = {'User-agent':user_agent}
    request = urllib2.Request(url,headers=headers)
    try:
        html = urllib2.urlopen(request).read()
    except urllib2.URLError as e:
        print 'Download error:',e.reason
        html = None
        if num_retries > 0:
            if hasattr(e,'code') and 500 <= e.code <600:
                #recursively retry 5xx HTTP errors
                return download(url,num_retries=1)
    return html

#根据站点地图爬取
def crawl_sitemap(url) :
    # download the sitemap file
    sitemap = download(url)
    # extract the s i t emap l i n k s
    links = re.findall('<loc>(. * ? ) < / l o c >' , sitemap)
    # download each l i n k
    for link in links :
        html = download (link)

#遍历ID爬取
def crawl_ID(url_base):
    for page in itertools.count(1):
        url = url_base + page
        html = download(url)
        if html is None:
           break
        else:
            pass


#爬取符合正则表达式的网页
def link_crawler(seed_url,link_regex):
    crawl_queue = {seed_url}
    #keep track which URL'S have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links(html):
            #check if link matches expected regex
            if re.match(link_regex,link):
                #form absolute link
                link = urlparse.urljoin(seed_url,link)
                #check if have already seen this link
                if link not in seen:
                    seen.add(link)
                    crawl_queue.append(link)

def get_links(html):
    """return a list of links from html
    """
    #a regular expression to extract all links from the webpage
    webpage_regex = re.compile('<a [^>] +href＝["\'](.*?)["\']',re.IGNORECASE)
    return webpage_regex.findall(html)

#添加解析robots.txt协议,下载限速的link_crawler
def link_crawler(seed_url,link_regex,user_agent = 'wswp'):
    rp = robotparser.RobotFileParser()
    crawl_queue = {seed_url}
    #keep track which URL'S have seen before
    seen = set(crawl_queue)
    while crawl_queue:
        url = crawl_queue.pop()
        #check url passes robots.txt restrictions
        if rp.can_fetch(user_agent,url):
            html = download(url)
            for link in get_links(html):
                #check if link matches expected regex
                if re.match(link_regex,link):
                    #form absolute link
                    link = urlparse.urljoin(seed_url,link)
                    #check if have already seen this link
                    if link not in seen:
                        seen.add(link)
                        crawl_queue.append(link)
        else:
            print 'Blocked by robots.txt',url
