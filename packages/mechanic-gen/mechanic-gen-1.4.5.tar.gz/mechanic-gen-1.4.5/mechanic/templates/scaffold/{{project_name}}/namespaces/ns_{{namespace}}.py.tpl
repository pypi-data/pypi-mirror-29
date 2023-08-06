# mechanic save - safe to modify below #
import os

import yaml
import flask
import flask_restplus
from mechanic import utils

{% if imported %}
from {{ project_name }}.models import ({%- for s in imported %}{{s}},{%- endfor %})
{% endif %}

ns = flask_restplus.Namespace('{{namespace}}', path='/', description='{{description}}')

script_path = os.path.dirname(os.path.abspath(__file__))
with open(script_path + '/../../openapi.yaml') as f:
    oapi_schemas = yaml.load(f.read())['components']['schemas']

{%- for cb in codeblocks %}
    {%- if cb.type == 'namespace' %}
        {%- for method_attr_name, method_attr in cb.oapi['x-mechanic-controller']['methods'].items() %}
{# #}
{# #}
def {{ method_attr.operationId.split('.')[-1] }}({%- for item in method_attr.parameters %}{% if item.required %}{{ item.name }}{% else %}{{item.name}}=None{% endif %}{%- if not loop.last %}, {% endif %}{% endfor %}):
    return {
        '{{ method_attr.operationId.split('.')[-1] }}': 'check'
    }
        {%- endfor %}
    {%- endif %}
{%- endfor %}
# END mechanic save #


# avoid modifying below - generated code at UTC {{ timestamp }} #
{%- for cb in codeblocks %}
    {%- if cb.type == 'namespace' %}
@ns.route('{{ cb.route }}')
class {{ cb.class_name }}({{ cb.base_class_name }}):
        {%- if cb.oapi.description %}
    """
    {{ cb.oapi.description }}
    """
        {%- endif %}
        {%- for method_attr_name, method_attr in cb.oapi['x-mechanic-controller']['methods'].items() %}
    {# #}
    @staticmethod{% if method_attr.auth_header %}
    @ns.header('Authorization', 'Bearer', required=True)
    {%- endif %}
    @ns.doc(body={% if method_attr.ns_body %}ns.schema_model('{{ method_attr.ns_body }}', oapi_schemas['{{ method_attr.ns_body }}']){% else %}None{% endif %}, model={% if method_attr.ns_model %}ns.schema_model('{{ method_attr.ns_model }}', oapi_schemas['{{ method_attr.ns_model }}']){% else %}None{% endif %})
    @utils.api_enforce(auth_bearer={{ method_attr.auth_header }}, response={{ method_attr.response_schema }}, request={{ method_attr.request_schema}}, many={{ method_attr.many }}, code={{ method_attr.code }})
    def {{ method_attr_name }}({%- for item in method_attr.parameters %}{% if item.required %}{{ item.name }}{% else %}{{item.name}}=None{% endif %}{%- if not loop.last %}, {% endif %}{% endfor %}):
        return {{ method_attr.operationId }}({%- for item in method_attr.parameters %}{{item.name}}{%- if not loop.last %}, {% endif %}{% endfor %})
        {%- endfor %}
    {%- endif %}
{# #}
{% endfor %}