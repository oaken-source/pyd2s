
'''
this module provides classes to manage item of a d2s save
'''

class Item(object):
    '''
    save data related to item
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._count = 0
        self._pcountondata = 0
        self._mcountondata = 0
        self._pdata = []
        self._mdata = []

        loc = 848
        first = True
        player = True
        onedata = []
        while loc < len(self._buffer):
             if self._buffer[loc] == ord("J") and self._buffer[loc + 1] == ord("M"):
                 if len(onedata) != 0:
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
                         if onedata[0] != 0x00 or onedata[1] != 0x00:
                             self._count += 1
                     if player and len(onedata) > 2:
                         if onedata[0] == 0x00 and onedata[1] == 0x00:
                             first = True
                             player = False
                     onedata = []
                 loc += 2
             else:
                 onedata.append(self._buffer[loc])
                 loc += 1
        if len(onedata):
             if player:
                 self._pdata.append(onedata)
             else:
                 self._mdata.append(onedata)
             if onedata[0] != 0x00 or onedata[1] != 0x00:
                 self._count += 1

    @property
    def count(self):
        '''
        item count
        '''
        return self._count

    @property
    def pcountondata(self):
        '''
        player item count
        '''
        return self._pcountondata

    def getpdata(self, index):
        '''
        Get player item data
        '''
        if(index >= len(self._pdata)):
            return []
        else:
            return self._pdata[index]

    @property
    def mcountondata(self):
        '''
        mercenary item count
        '''
        return self._mcountondata

    def getmdata(self, index):
        '''
        Get mercenary item data
        '''
        if(index >= len(self._mdata)):
            return []
        else:
            return self._mdata[index]

