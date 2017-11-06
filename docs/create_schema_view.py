import codecs
import sadisplay
from pyhgnc.manager.database import models
import os

base_folder = './source/_static/models/'


def create_uml_files(list_of_models, file_prefix):
    desc = sadisplay.describe(list_of_models)
    path_prefix = os.path.join(base_folder, file_prefix)
    with codecs.open(path_prefix+'.dot', 'w', encoding='utf-8') as f:
        f.write(sadisplay.dot(desc))
    os.system(''.join(['dot -Tpng ', path_prefix, '.dot > ', path_prefix, '.png']))

# for all models one UML
list_of_all_models = [getattr(models, attr) for attr in dir(models)]
create_uml_files(list_of_all_models, 'all')

