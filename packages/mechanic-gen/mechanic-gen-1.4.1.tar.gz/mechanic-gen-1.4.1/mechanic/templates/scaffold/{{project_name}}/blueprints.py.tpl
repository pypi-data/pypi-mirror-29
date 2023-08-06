# mechanic save - safe to modify below #

import re
import os
import importlib
import glob

from flask import Blueprint
from flask_restplus import Api

script_path = os.path.dirname(os.path.abspath(__file__))
with open(script_path + '/VERSION', 'r') as f:
    VERSION = re.search(r'([0-9].[0-9].[0-9])', f.read()).group(0)

{{project_name}}_blueprint = Blueprint('{{project_name}}', __name__)
api = Api({{project_name}}_blueprint,
          title='{{project_name}}',
          version=VERSION,
          description='{{project_name}} blueprint',
          doc='/swagger')

ns_list = glob.glob('{{project_name}}/namespaces/ns_*.py')

for ns in ns_list:
    module = importlib.import_module('{{project_name}}.namespaces.%s' % ns.split('/')[-1].replace('.py', ''))
    if hasattr(module, 'ns'):
        api.add_namespace(getattr(module, 'ns'))
# END mechanic save #
