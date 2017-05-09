import builtwith
import whois
import urllib2
import itertools
import re

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
        html = download (link )

#遍历ID爬取
def crawl_ID(url_base):
    for page in itertools.count(1):
        url = url_base + page
        html = download(url)
        if html is None:
           break
        else:
            pass

#爬取符合正则表达式的
def link_crawler(seed_url,link_regex):
    crawl_queue = {seed_url}
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url)
        for link in get_links()