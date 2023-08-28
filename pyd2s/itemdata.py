
'''
this module provides classes to manage item of a d2s save
'''

class ItemData:
    '''
    save data related to item
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._pcount = 0
        self._pcountondata = 0
        self._mcount = 0
        self._mcountondata = 0
        self._pdata = []
        self._mdata = []

        loc = 840    # about
        start = True
        first = True
        player = True
        onedata = []
        while loc < len(self._buffer):
            if self._buffer[loc] == ord("J") and self._buffer[loc + 1] == ord("M"):
                if start:
                    start = False
                else:
                    if len(onedata) >= 2:
                        if first:
                            if player:
                                self._pcountondata = (onedata[1] << 8) + onedata[0]
                            else:
                                self._mcountondata = (onedata[1] << 8) + onedata[0]
                            first = False
                        else:
                            if player:
                                self._pdata.append(onedata)
                            else:
                                self._mdata.append(onedata)
                            if onedata[0] != 0x00 or onedata[1] != 0x00 or onedata[2] != 0x6A:
                                if player:
                                    self._pcount += 1
                                else:
                                    self._mcount += 1
                        if player and len(onedata) > 2:
                            if onedata[0] == 0x00 and onedata[1] == 0x00 and onedata[2] == 0x6A:
                                first = True
                                player = False
                onedata = []
                loc += 2
            else:
                if not start:
                    onedata.append(self._buffer[loc])
                loc += 1
        if onedata:
            if player:
                self._pdata.append(onedata)
            else:
                self._mdata.append(onedata)
            if onedata[0] != 0x00 or onedata[1] != 0x00 or onedata[2] != 0x6A:
                if player:
                    self._pcount += 1
                else:
                    self._mcount += 1

    @property
    def pcount(self):
        '''
        player item count
        '''
        return self._pcount

    @property
    def pcountondata(self):
        '''
        player item count (on data)
        '''
        return self._pcountondata

    def getpdata(self, index):
        '''
        Get player item data
        '''
        return self._pdata[index]

    @property
    def mcount(self):
        '''
        mercenary item count
        '''
        return self._mcount

    @property
    def mcountondata(self):
        '''
        mercenary item count (on data)
        '''
        return self._mcountondata

    def getmdata(self, index):
        '''
        Get mercenary item data
        '''
        return self._mdata[index]
