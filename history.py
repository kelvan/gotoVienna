import os

class History(list):

    def __init__(self, hist_file, *args, **kwargs):
        if os.path.isfile(hist_file):
            f = open(hist_file, 'r')
            h = map(lambda x: x.strip(), f.readlines())
            f.close()
            self._file = open(hist_file, 'a')
        else:
            self._file = open(hist_file, 'w')
            h = []

        list.__init__(self, h, *args, **kwargs)

    def __add__(self, item):
        if not item in self:
            super(History, self).__add__(item)
            self._file.writelines(map(lambda x: x + '\n', self))
            self._file.flush()

    def insert(self, index, item):
        if not item in self:
            super(History, self).insert(index, item)
            self._file.writelines(map(lambda x: x + '\n', self))
            self._file.flush()

    def __delitem__(self, item):
        super(History, self).__deltitem(item)
        self._file.writelines(map(lambda x: x + '\n', self))
        self._file.flush()
        self._file.close()

    def close(self):
        self._file.close()
