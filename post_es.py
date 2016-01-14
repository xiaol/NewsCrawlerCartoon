import requests
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
POSTGRES = "postgresql://postgres:ly@postgres&2015@120.27.163.25/BDP"
Base = automap_base()
engine = create_engine(POSTGRES)
Base.prepare(engine, reflect=True)
Comic = Base.classes.comiclist
session = Session(engine)
COUNT = 50


def post_comics_to_es():
    q = session.query(Comic)
    count = q.count()
    pages, remainder = divmod(count, COUNT)
    for page in range(0, pages):
        start = page * COUNT
        end = (page+1) * COUNT
        comics = q[start:end]
        map(_process_comic, comics)
    start = pages * COUNT
    end = count
    comics = q[start:end]
    map(_process_comic, comics)


def _process_comic(comic):
    item = dict()
    item["areaLocation"] = comic.area_location
    item["author"] = comic.author
    item["category"] = comic.category
    item["chapterNum"] = comic.chapter_num
    item["comicId"] = comic.comic_id
    item["comicUrl"] = comic.comic_url
    item["downloadUrl"] = comic.download_url
    item["lastUpdateDate"] = comic.last_update_date
    item["name"] = comic.name
    item["originName"] = comic.origin_name
    item["popularity"] = comic.popularity
    item["pubStatus"] = comic.pub_status
    item["summary"] = comic.summary
    item["tags"] = comic.tags
    item["titleImage"] = comic.title_image
    url = "http://120.27.162.230:9200/cartoon/fulltext/"
    r = requests.post(url, json=item)
    if r.status_code != 200:
        print("status: %s, error: %s" % (r.status_code, item["comicUrl"]))
    else:
        print("success: %s" % item["comicUrl"])

if __name__ == '__main__':
    post_comics_to_es()




