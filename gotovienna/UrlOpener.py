import mechanize
import defaults

class MechanizeOpener:
    cookies = mechanize.CookieJar()
    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebkit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13')]

def loadCookie():
    MechanizeOpener.opener.open('http://www.wienerlinien.at/itip/')
    
def urlopen_check(*args, **kwargs):
    #if not filter(lambda c: c.name=='PHPSESSID', MechanizeOpener.cookies):
    #    print 'load cookie'
    #    loadCookie()
    return MechanizeOpener.opener.open(*args, **kwargs)

urlopen = urlopen_check


#version = 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebkit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
#version = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

#urlopen = NokiaN9Opener().open
#urlretrieve = NokiaN9Opener().retrieve
