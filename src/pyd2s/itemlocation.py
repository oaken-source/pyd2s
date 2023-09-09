'''
this module contains classes for managing item storage locations
'''

from enum import Enum


class ItemLocation:
    '''
    where an item is located
    '''
    class LocationType(Enum):
        '''
        roughly where the item is located
        '''
        STORED = 0
        EQUIPPED = 1
        TUCKED = 2
        POINTER = 4
        SOCKET = 6

        def __lt__(self, other):
            '''
            comparator for sorting
            '''
            if self.__class__ is other.__class__:
                return self.value < other.value
            return NotImplemented

    class EquipmentSlot(Enum):
        '''
        where the item is equipped
        '''
        HELMET = 1
        AMULET = 2
        ARMOR = 3
        RIGHT_HAND = 4
        LEFT_HAND = 5
        RIGHT_RING = 6
        LEFT_RING = 7
        BELT = 8
        BOOTS = 9
        GLOVES = 10
        ALT_RIGHT_HAND = 11
        ALT_LEFT_HAND = 12

        def __lt__(self, other):
            '''
            comparator for sorting
            '''
            if self.__class__ is other.__class__:
                return self.value < other.value
            return NotImplemented

    class StoredType(Enum):
        '''
        if LocationType is STORED, distinguish where
        '''
        INVENTORY = 1
        CUBE = 4
        STASH = 5

        def __lt__(self, other):
            '''
            comparator for sorting
            '''
            if self.__class__ is other.__class__:
                return self.value < other.value
            return NotImplemented

    def __init__(self, location, equipped=None, position=None, stored=None):
        '''
        constructor
        '''
        self._location = self.LocationType(location)

        self._equipped = None
        if self._location == self.LocationType.EQUIPPED:
            self._equipped = self.EquipmentSlot(equipped)

        self._stored = None
        if self._location == self.LocationType.STORED:
            self._stored = self.StoredType(stored)

        self._pos = None
        if self._location in [self.LocationType.STORED, self.LocationType.TUCKED]:
            self._pos = position

    @classmethod
    def stored(cls, where, position):
        '''
        produce an ItemLocation instance for the given storage type and position
        '''
        return cls(cls.LocationType.STORED, stored=where, position=position)

    @classmethod
    def inventory(cls, position):
        '''
        produce an ItemLocation instance for the inventory
        '''
        return cls.stored(cls.StoredType.INVENTORY, position=position)

    @classmethod
    def cube(cls, position):
        '''
        produce an ItemLocation instance for the cube
        '''
        return cls.stored(cls.StoredType.CUBE, position=position)

    @classmethod
    def stashed(cls, position):
        '''
        produce an ItemLocation instance for the stash
        '''
        return cls.stored(cls.StoredType.STASH, position=position)

    @classmethod
    def equipped(cls, slot):
        '''
        produce an ItemLocation instance for the given equipment slot
        '''
        return cls(cls.LocationType.EQUIPPED, equipped=slot)

    @classmethod
    def tucked(cls, position):
        '''
        produce an ItemLocation instance for the given belt slot
        '''
        return cls(cls.LocationType.TUCKED, position=(position, 0))

    def get_location(self):
        '''
        the location part of the ItemLocation
        '''
        return self._location

    def get_equipped(self):
        '''
        the equipped part of the ItemLocation
        '''
        return self._equipped

    def get_stored(self):
        '''
        the stored part of the ItemLocation
        '''
        return self._stored

    def get_pos(self):
        '''
        the position part of the ItemLocation
        '''
        return self._pos

    def raw_data(self):
        '''
        the raw data fields of this location info
        '''
        return (
            self._location.value,
            self._equipped.value if self._equipped else 0,
            self._pos[0] if self._pos else 0,
            self._pos[1] if self._pos else 0,
            self._stored.value if self._stored else 0)

    def __str__(self):
        '''
        string representation
        '''
        if self._location == self.LocationType.STORED:
            return f'Stored in {self._stored} at {self._pos}'
        if self._location == self.LocationType.EQUIPPED:
            return f'Equipped in {self._equipped} slot'
        if self._location == self.LocationType.TUCKED:
            return f'Tucked in belt slot {self._pos[0]}'
        if self._location == self.LocationType.POINTER:
            return 'Attached to cursor'
        if self._location == self.LocationType.SOCKET:
            return 'Placed in socket'
        return NotImplemented

    def __lt__(self, other):
        '''
        comparator for sorting
        '''
        if self.__class__ is not other.__class__:
            return NotImplemented

        return (
            self.get_location(),
            self.get_equipped() if self.get_location() == self.LocationType.EQUIPPED else 0,
            self.get_stored() if self.get_location() == self.LocationType.STORED else 0,
            self.get_pos()
        ) < (
            other.get_location(),
            other.get_equipped() if other.get_location() == self.LocationType.EQUIPPED else 0,
            other.get_stored() if other.get_location() == self.LocationType.STORED else 0,
            other.get_pos()
        )
