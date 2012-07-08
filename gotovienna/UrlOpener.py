import mechanize

class MechanizeOpener:
    cookies = mechanize.CookieJar()
    opener = mechanize.build_opener(mechanize.HTTPCookieProcessor(cookies))
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebkit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13')]

urlopen = MechanizeOpener.opener.open

def loadCookie():
    urlopen('http://www.wienerlinien.at')

#version = 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebkit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'
#version = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'

#urlopen = NokiaN9Opener().open
#urlretrieve = NokiaN9Opener().retrieve
