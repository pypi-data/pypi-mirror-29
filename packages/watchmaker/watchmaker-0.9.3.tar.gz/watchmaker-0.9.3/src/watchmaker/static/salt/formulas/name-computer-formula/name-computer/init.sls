{%- from tpldir + "/map.jinja" import name_computer with context %}

{%- if name_computer %}
Set Computer Name:
  {{ name_computer.state_name }}:
    {{ name_computer.state_opts }}
{%- else %}
Print name-computer help:
  test.show_notification:
    - text: |
        The name-computer formula reads the computername from these keys:

          grain: `name-computer:computername`
          pillar: `name-computer:lookup:computername`

        The grain overrides the pillar key. However, neither of these keys
        are set, or they otherwise evaluate to False, so the formula did not
        attempt to set the computername.
{%- endif %}
