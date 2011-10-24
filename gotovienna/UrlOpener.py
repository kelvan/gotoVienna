from urllib import FancyURLopener


class NokiaN9Opener (FancyURLopener):
    """ Sends NokiaN9 browser useragent
    """
    version = 'Mozilla/5.0 (MeeGo; NokiaN9) AppleWebkit/534.13 (KHTML, like Gecko) NokiaBrowser/8.5.0 Mobile Safari/534.13'

urlopen = NokiaN9Opener().open
urlretrieve = NokiaN9Opener().retrieve
