
import os

from pyd2s.itemdata import ItemData
from pyd2s.savebuffer import SaveBuffer

import pytest


def item_source():
    for file in os.listdir('tests/itemdata'):
        if file.endswith('.data'):
            data = f'tests/itemdata/{file}'
            desc = f'tests/itemdata/{file.removesuffix(".data")}.desc'
            yield {'data': data, 'desc': desc}

@pytest.mark.parametrize('item', item_source())
def test_item(item):
    with open(item['desc'], 'r', encoding='ascii') as descfile:
        desc = descfile.read().strip()

    data = SaveBuffer(item['data'])
    item = ItemData.Item.from_data(data, 0)
    assert str(item) == desc
    assert str(item) == desc
    assert str(item) == desc

