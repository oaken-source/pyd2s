
import os
import logging

from pyd2s import SaveFile

import pytest

logging.basicConfig(level=10)


def item_source():
    for file in os.listdir('tests/itemdata'):
        if file.endswith('.d2i'):
            data = f'tests/itemdata/{file}'
            desc = f'tests/itemdata/{file.removesuffix(".d2i")}.desc'
            yield pytest.param({'data': data, 'desc': desc}, id=os.path.basename(file))


@pytest.mark.parametrize('item', item_source())
def test_item(item):
    with open(item['desc'], 'r', encoding='ascii') as descfile:
        desc = descfile.read().strip()

    item = SaveFile.open(item['data']).item

    assert str(item) == desc
    assert str(item) == desc
    assert str(item) == desc

