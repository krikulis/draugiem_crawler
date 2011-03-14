import urllib
import urllib2
import json 

DRAUGIEM_URL = 'http://api.draugiem.lv/json/' 
APP_KEY = '55c08536218323ec842e8863feb86834'

class DraugiemException(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description
    def __unicode__(self):
        return u"draugiem.lv API error (%s, %s)" % (self.code, self.description)
class UserCrawler(object):
    def __init__(self, username, password):
        self.api_key = None
        self.login(username, password)
        self.inbox = []
        self.outbox = []
        self.users = {}
    def login(self, username, password):
        response = self.call(action = 'login',
                  email = username,
                  password = password)
        self.user_info = response['login']
        self.api_key = response['login']['apikey']

    def call(self, **kwargs):
        kwargs['app'] = APP_KEY
        if self.api_key:
            kwargs['apikey'] = self.api_key
        url = "%s?%s" % (DRAUGIEM_URL, urllib.urlencode(kwargs))
        response = urllib.urlopen(url).read()
        response = json.loads(response)
        if 'error' in response:
            raise DraugiemException(response['error']['code'], response['error']['description'])
        return response

    def friends(self, uid = None):
        args = {'action' : 'iphone/users',
                'type' : 'friends'}
        if uid:
            args['uid'] = uid
        return self.call(**args)
