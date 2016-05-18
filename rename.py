import shutil
import os

for filename in os.listdir('data/pairwise/'):
    items = filename.split('_')
    if items[0].isdigit():
        del items[0]
    newname = items[0]
    for item in items[1:]:
        newname += '_' + item
    shutil.move('data/pairwise/' + filename, 'data/pairwise/' + newname)
