# mechanic save - safe to modify below #
# This is where you can place imports and code that you don't want overwritten by mechanic
from mechanic.fields import MechanicEmbeddable
# END mechanic save #


# avoid modifying below - generated code at UTC {{ timestamp }} #
{%- for cb in codeblocks %}
    {%- if cb.type == 'table' %}
{{ cb.table_name }} = db.Table('{{ cb.table_name }}',
                                {%- for col_name, col_obj in cb.oapi.columns.items() %}
                        db.Column('{{ col_name }}', db.{{ col_obj.type.title() }}({%- if col_obj.maxLength %}{{ col_obj.maxLength }}{% endif %}),
                                                            {%- if col_obj.foreign_key %} db.ForeignKey('{{ col_obj.foreign_key.key }}',
                                                                {%- if col_obj.foreign_key.ondelete %} ondelete='{{ col_obj.foreign_key.ondelete }}',{%- endif %}
                                                                {%- if col_obj.foreign_key.onupdate %} onupdate='{{ col_obj.foreign_key.onupdate }}',{%- endif %})
                                                            {%- endif %}),
                                {%- endfor %}
                        {% if cb.oapi.schema %}schema='{{ cb.oapi.schema }}',{%- endif %})
    {%- elif cb.type == 'schema' %}
class {{ cb.class_name }}({{ cb.base_class_name }}):
        {%- if cb.oapi.description %}
    """
    {{ cb.oapi.description }}
    """
        {%- endif %}
        {%- for prop_name, prop_val in cb.oapi.get('x-mechanic-schema', {}).get('class_properties', {}).items() %}
    {{ prop_name }} = {{ prop_val }}
        {%- endfor %}
        {%- for prop_name, prop_obj in cb.oapi.properties.items() %}
            {%- if not prop_obj['x-mechanic-db'] or not prop_obj['x-mechanic-db'].model_only %}
                {%- if prop_obj['x-mechanic-embeddable'] %}
    {{ prop_name }} = MechanicEmbeddable('{{ prop_obj['x-mechanic-embeddable'] }}', deserialize_key='identifier', column=['uri', 'identifier', 'name']{%- if prop_name in cb.oapi.required %}, required=True,{% endif %})
                {%- else %}
    {{ prop_name }} = fields.{{ prop_obj.type.title() }}({%- if prop_name in cb.oapi.required %}required=True, {% else %}allow_none=True, {% endif %}
                                                 {%- if prop_obj.maxLength %}maxLength={{ prop_obj.maxLength }}, {% endif %}
                                                 {%- if prop_obj.readOnly %}dump_only={{ prop_obj.readOnly }}, {% endif %}
                                                 {%- if prop_obj.writeOnly %}load_only={{ prop_obj.writeOnly }}, {% endif %}
                                                 {%- if prop_obj.enum %}validate=OneOf({{ prop_obj.enum }}), {% endif %}
                                                 {%- if prop_obj.pattern %}validate=Regexp(r'{{ prop_obj.pattern}}'), {% endif %})
                {%- endif %}
            {%- endif %}
        {%- endfor %}
{# #}
    class Meta:
        fields = ({%- for prop_name, prop_obj in cb.oapi.properties.items() %}{%- if not prop_obj['x-mechanic-db'] or not prop_obj['x-mechanic-db'].model_only %}'{{ prop_name }}', {% endif %}{%- endfor %})
        strict = True
        {% if cb.oapi['x-mechanic-model'] -%}
        model = {{ cb.oapi['x-mechanic-model'].class_name }}
        sqla_session = db.session
        {%- endif %}
    {%- elif cb.type == 'model' %}
class {{ cb.class_name }}({{ cb.base_class_name }}):
        {%- if cb.oapi.description %}
    """
    {{ cb.oapi.description }}
    """
        {%- endif %}
    __tablename__ = '{%- if cb.oapi['x-mechanic-db'] -%}
                        {{ cb.oapi['x-mechanic-db'].__tablename__ }}
                     {%- endif -%}'
    __table_args__ = ({%- if cb.oapi['x-mechanic-db'] and cb.oapi['x-mechanic-db'].__table_args__.uniqueConstraints -%}
                                    {%- for key, value in cb.oapi['x-mechanic-db'].__table_args__.uniqueConstraints.items() -%}
                                    db.UniqueConstraint({%- for item in value %}'{{ item }}', {%- endfor %} name='{{ key }}'),
                                    {%- endfor %}
                      {% endif -%}
                                    {'schema': '{%- if cb.oapi['x-mechanic-db'] -%}{{ cb.oapi['x-mechanic-db'].__table_args__.schema }}{%- endif -%}'})
    {# #}
    controller = db.Column(db.String, default='{{ cb.oapi['x-mechanic-controller'] }}')
        {%- for prop_name, prop_obj in cb.oapi.properties.items() %}
            {%- if prop_obj['x-mechanic-db'] %}
                {%- if prop_obj['x-mechanic-db'].column %}
    {{ prop_name }} = db.Column({%- if prop_obj['x-mechanic-db'].column.type %}{{ prop_obj['x-mechanic-db'].column.type }}{%- else %}db.{{ prop_obj.type.title() }}({%- if prop_obj.maxLength %}{{ prop_obj.maxLength }}{% endif %}){%- endif %},
                                {%- if prop_obj['x-mechanic-db'].column.primary_key %} primary_key={{ prop_obj['x-mechanic-db'].column.primary_key }},{%- endif %}
                                {%- if prop_obj['x-mechanic-db'].column.unique %} unique={{ prop_obj['x-mechanic-db'].column.unique }},{%- endif %}
                                {%- if prop_obj['x-mechanic-db'].column.nullable %} nullable={{ prop_obj['x-mechanic-db'].column.nullable }},{%- endif %}
                                {%- if prop_obj['x-mechanic-db'].column.default %} default={{ prop_obj['x-mechanic-db'].column.default }},{%- endif %}
                                {%- if prop_obj['x-mechanic-db'].column.onupdate %} onupdate={{ prop_obj['x-mechanic-db'].column.onupdate }},{%- endif %}
                                {%- if prop_obj['x-mechanic-db'].column.server_default %} server_default={{ prop_obj['x-mechanic-db'].column.server_default }},{%- endif %})
                {%- elif prop_obj['x-mechanic-db'].synonym %}
    {{ prop_name }} = synonym('{{ prop_obj['x-mechanic-db'].synonym }}')
                {%- elif prop_obj['x-mechanic-db'].foreign_key %}
    {{ prop_name }} = db.Column(db.String(36), db.ForeignKey('{{ prop_obj['x-mechanic-db'].foreign_key.key }}',
                                                                {%- if prop_obj['x-mechanic-db'].foreign_key.ondelete %} ondelete='{{ prop_obj['x-mechanic-db'].foreign_key.ondelete }}',{%- endif %}
                                                                {%- if prop_obj['x-mechanic-db'].foreign_key.onupdate %} onupdate='{{ prop_obj['x-mechanic-db'].foreign_key.onupdate }}',{%- endif %}),
                                                                {%- if prop_obj['x-mechanic-db'].foreign_key.primary_key %} primary_key={{ prop_obj['x-mechanic-db'].foreign_key.primary_key }}{% endif %})
                {%- elif prop_obj['x-mechanic-db'].relationship %}
    {{ prop_name }} = db.relationship('{{ prop_obj['x-mechanic-db'].relationship.model }}',
                                        {%- if prop_obj['x-mechanic-db'].relationship.backref %} backref='{{ prop_obj['x-mechanic-db'].relationship.backref }}',{%- endif %}
                                        {%- if prop_obj['x-mechanic-db'].relationship.back_populates %} back_populates='{{ prop_obj['x-mechanic-db'].relationship.back_populates }}',{%- endif %}
                                        {%- if prop_obj['x-mechanic-db'].relationship.cascade %} cascade='{{ prop_obj['x-mechanic-db'].relationship.cascade }}',{%- endif %}
                                        {%- if prop_obj['x-mechanic-db'].relationship.uselist != None %} uselist={{ prop_obj['x-mechanic-db'].relationship.uselist }},{% endif %}
                                        {%- if prop_obj['x-mechanic-db'].relationship.foreign_keys %} foreign_keys={{ prop_obj['x-mechanic-db'].relationship.foreign_keys }},{%- endif -%}
                                        {%- if prop_obj['x-mechanic-db'].relationship.secondary %} secondary={{ prop_obj['x-mechanic-db'].relationship.secondary }},{% endif -%})
                {%- endif %}
            {%- endif %}
        {%- endfor %}
    {%- elif cb.type == 'blueprint' %}
@ns.route('{{ cb.route }}')
class {{ cb.class_name }}({{ cb.base_class_name }}):
        {%- if cb.oapi.description %}
    """
    {{ cb.oapi.description }}
    """
        {%- endif %}
    {%- for method_attr_name, method_attr in cb.oapi['x-mechanic-controller']['methods'].items() %}
    {# #}
    @staticmethod
    @utils.api_enforce(response={{ method_attr.response_schema }}, request={{ method_attr.request_schema}}, many={{ method_attr.many }}, code={{ method_attr.code }})
    def {{ method_attr_name }}({%- for item in method_attr.parameters %}{{ item }}{%- if not loop.last %}, {% endif %}{% endfor %}):
        return {{ method_attr.operationId }}({%- for item in method_attr.parameters %}{{ item }}{%- if not loop.last %}, {% endif %}{% endfor %})
    {%- endfor %}
    {%- elif cb.type == 'versions' %}
VERSIONS = {
    {%- for controller in cb.controllers %}
    '{{ controller.class_name }}': {
        {%- if controller.versions %}
            {%- for version_num, version in controller.versions.items() %}
        '{{ version_num }}': {
            'schema': {{ version.schema }}
        },
            {%- endfor %}
        {%- else %}
        '{{ cb.version }}': {
            'schema': {{ controller.schema }}
        },
        {%- endif %}
    },
    {%- endfor %}
}
    {%- endif %}
{# #}
{% endfor %}