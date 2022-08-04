from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from os import path as Path
import re


# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = Path.dirname(Path.abspath(__file__))
# 상위 디렉토리 주소 /fds
PARENT_DIR = Path.dirname((CUR_DIR))


def get_links(siteUrl, pageUrl):
    pageList = []
    html = urlopen(siteUrl+pageUrl)
    bsObject = BeautifulSoup(html, "lxml", from_encoding='utf-8')

    crawlHref = bsObject.select('div .bd-list-thumb-a > ul > li > a')

    for tag in crawlHref:
        pageList.append(siteUrl+tag['href'])

    return pageList


def get_mp3_links(siteUrl, pageUrl):
    pageList = []
    html = urlopen(siteUrl+pageUrl)
    bsObject = BeautifulSoup(html, 'lxml', from_encoding='utf-8')

    crawlHref = bsObject.select('div.bd-list > table td.title > a')

    for tag in crawlHref:
        pageList.append(siteUrl+tag['href'])

    return pageList


def get_media_links(pageList, siteUrl):
    media_list = []
    for pageUrl in pageList:
        html = urlopen(pageUrl)
        bsObject = BeautifulSoup(html, "lxml", from_encoding='utf-8')
        mediaUrl = (bsObject.select('div .bd-view > dl > dd > a'))[0]['href']
        mediaName = re.sub(r'\(파일크기: [^)]*\)', '', (bsObject.select(
            'div .bd-view > dl > dd > a > span .name'))[0].get_text()).strip()
        media_list.append([mediaName, siteUrl+mediaUrl])
    return media_list


def get_mp3(pageList, siteUrl, total):
    media_list = []
    idx = 1
    for pageUrl in pageList:
        html = urlopen(pageUrl)
        bsObject = BeautifulSoup(html, 'lxml', from_encoding='utf-8')
        mediaUrl = (bsObject.select('div.dbdata > video'))[0]['src']
        mediaName = str(total+idx)+'.mp3'
        idx += 1

        media_list.append([mediaName, siteUrl+mediaUrl])
    return media_list


def download_media(media):
    urlretrieve(media[1], PARENT_DIR+'/data/this_voice/'+media[0])
    print(media[0], ' download completed')


def download_mp3(media):
    urlretrieve(media[1], PARENT_DIR+'/data/fraud/'+media[0])
    print(media[0], ' download completed')
