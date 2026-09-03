{% macro grant_select_on_schemas(schema_name, role_name='PUBLIC') %}

  grant usage on schema {{ schema_name }} to role {{ role_name }};
  grant select on all tables in schema {{ schema_name }} to role {{ role_name }};
  grant select on all views in schema {{ schema_name }} to role {{ role_name }};

{% endmacro %}
