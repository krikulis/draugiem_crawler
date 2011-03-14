import MySQLdb 
import settings
conn = MySQLdb.connect(host = settings.MYSQL_HOST,
                       user = settings.MYSQL_USERNAME,
                       db = settings.MYSQL_DATABASE,
                       passwd = settings.MYSQL_PASSWORD,
                       use_unicode = True)

conn.cursor().execute("set names utf8;");
conn.cursor().execute("""CREATE TABLE IF NOT EXISTS `draugiem` (
  `adult` varchar(255) DEFAULT NULL,
  `age` varchar(255) DEFAULT NULL,
  `img` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `nick` varchar(255) DEFAULT NULL,
  `place` varchar(255) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `surname` varchar(255) DEFAULT NULL,
  `uid` varchar(255) DEFAULT NULL,
  UNIQUE KEY `uid` (`uid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 """);
import api 
import sys
from random import randrange
handle = api.UserCrawler(settings.DRAUGIEM_EMAIL, settings.DRAUGIEM_PASSWORD)

def crawl(id):
    try:
        friends = handle.friends(id)
    except:
        return None 
    if len(friends) == 0:
        return None 
    friends = friends['users']
    uids = []
    for user in friends:
        d = friends[user]
        cursor = conn.cursor()
        cursor.execute(u""" INSERT DELAYED IGNORE INTO 
                            draugiem (adult, age, img, name, nick, place, sex, surname, uid) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""", (d['adult'], d['age'], d['img'], d['name'].encode("utf-8"), d['nick'].encode("utf-8"), d['place'].encode("utf-8"), d['sex'], d['surname'].encode("utf-8"), d['uid']))
        uids.append(user)
    return set(uids)
def main():
    rand = randrange(1000, 3000000)

    results = None
    while not results:
        results = crawl(rand)
        print results
        rand = randrange(1000, 3000000)
    for uid in results:
        print "Crawling %s " % (uid)
        res = crawl(uid)
        
        new = results.difference(res)
        results = results.union(res)
    while len(new):
        new = set()
        for uid in new:
            res = crawl(new)
            if res is None:
                continue
            new_t = results.difference(res)
            new = new.union(new_t)
            results = results.union(res)
        
if __name__ == "__main__":
    main()
