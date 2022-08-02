from multiprocessing import Pool
from os import path as Path
from os import remove
from utility.make_dir import makedirs
from get_data import get_links, get_media_links, download_media


# 현재 디렉토리 주소 /fds/crawler
CUR_DIR = Path.dirname(Path.abspath(__file__))
# 상위 디렉토리 주소 /fds
PARENT_DIR = Path.dirname((CUR_DIR))


if __name__ == '__main__':

    siteUrl = 'https://www.fss.or.kr'
    pageUrl = ['/fss/bbs/B0000203/list.do?menuNo=200686&bbsId=&cl1Cd=&pageIndex=',
               '&sdate=&edate=&searchCnd=1&searchWrd=']
    makedirs(PARENT_DIR+'/data')
    makedirs(PARENT_DIR+'/data/this_voice')

    pageIndex = 1
    pageList = []
    mediaList = []
    while True:
        try:
            pageList = get_links(siteUrl, pageUrl[0]+str(pageIndex)+pageUrl[1])
            mediaList = get_media_links(pageList, siteUrl)

            if len(pageList) < 1:
                break

            print('{}page : {} media files'.format(pageIndex, len(mediaList)))

            pool = Pool(processes=len(mediaList))
            pool.map(download_media, mediaList)
            pool.close()
            pool.join()

            pageIndex += 1
            pageList.clear()
            mediaList.clear()

        except Exception:
            print('Exception in {} page, Re-try crawling this page...'.format(pageIndex))

            for f in mediaList:
                file_path = PARENT_DIR+'/data/this_voice/'+f[0]
                if Path.exists(file_path):
                    remove(file_path)
