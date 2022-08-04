from multiprocessing import Pool
from os import path as Path
from os import remove
from turtle import down
from utility.make_dir import makedirs
from get_data import download_mp3, get_links, get_media_links, download_media, get_mp3, get_mp3_links


# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = Path.dirname(Path.abspath(__file__))
# 상위 디렉토리 주소 /fds
PARENT_DIR = Path.dirname((CUR_DIR))


if __name__ == '__main__':

    siteUrl = 'https://www.fss.or.kr'
    pageUrl = ['/fss/bbs/B0000207/list.do?menuNo=200691&bbsId=&cl1Cd=&pageIndex=',
               '&sdate=&edate=&searchCnd=1&searchWrd=']
    makedirs(PARENT_DIR+'/data')
    makedirs(PARENT_DIR+'/data/imposter')
    pageIndex = 20
    total = 375
    pageList = []
    mediaList = []

    while True:
        try:
            pageList = get_mp3_links(siteUrl, pageUrl[0]+str(pageIndex)+pageUrl[1])
            mediaList = get_mp3(pageList, siteUrl, total)

            if len(pageList) < 1:
                break

            print('{}page: {} media files'.format(pageIndex, len(mediaList)))

            pool = Pool(processes=min(5, len(mediaList)))
            pool.map(download_mp3, mediaList)
            pool.close()
            pool.join()

            pageIndex += 1
            total += (len(mediaList))
            pageList.clear()
            mediaList.clear()
        except Exception:
            print('Exception in {} page, Re-try crawling this page...'.format(pageIndex))

            for f in mediaList:
                file_path = PARENT_DIR+'/data/fraud/'+f[0]
                if Path.exists(file_path):
                    remove(file_path)
