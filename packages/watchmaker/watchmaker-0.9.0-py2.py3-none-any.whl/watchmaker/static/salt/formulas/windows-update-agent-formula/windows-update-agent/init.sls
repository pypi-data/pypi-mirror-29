{%- from "windows-update-agent/map.jinja" import wua with context %}

# Loop through the data model, creating `reg.present` states for any key with
# a defined value. If `remove-undefined-keys` is `True`, also create
# `reg.absent` states for any key that is missing or that has an empty value.
{%- set remove_undefined_keys = salt['pillar.get'](
    'windows-update-agent:remove-undefined-keys',
    False) %}

{%- for subkey,keys in wua.items() %}
    {%- for key,settings in keys.items() %}
{%- if settings.get('value', '') %}
wua_reg_{{ subkey }}_{{ key }}:
  reg.present:
    - name: {{ settings.name }}
    - value: {{ settings.value }}
    - vtype: {{ settings.vtype }}
    - reflection: False
    - watch_in:
      - service: wua_service
{%- elif remove_undefined_keys %}
wua_reg_{{ subkey }}_{{ key }}:
  reg.absent:
    - name: {{ settings.name }}
    - watch_in:
      - service: wua_service
{%- endif %}
    {%- endfor %}
{%- endfor %}

wua_service:
  service.running:
    - name: wuauserv
    - onchanches_in:
      - cmd: wua_reset
      
wua_reset:
  cmd.run:
    - name: 'wuauclt.exe /resetauthorization /detectnow'
