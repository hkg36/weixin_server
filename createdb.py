import importlib
import os

from dbconfig import *

for filename in os.listdir(r'datamodel'):
    if filename.endswith('.py') and filename!='__init__.py':
        print filename
        importlib.import_module('datamodel.'+filename[:-3])
DBBase.metadata.create_all(db)