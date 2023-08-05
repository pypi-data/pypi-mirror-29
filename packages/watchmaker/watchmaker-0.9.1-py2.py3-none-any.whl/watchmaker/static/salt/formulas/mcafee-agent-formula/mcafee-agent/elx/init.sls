#
# This salt state installs McAfee Agent dependencies, configures iptables, and
# runs a downloaded copy of ePO server's exported install.sh. The `install.sh`
# file is a pre-configured, self-installing SHell ARchive. The SHAR installs
# the MFEcma and MFErt RPMs, service configuration (XML) files and SSL keys
# necessary to secure communications between the local McAfee agent software
# and the ePO server.
#
#################################################################
{%- from tpldir ~ '/map.jinja' import mcafee with context %}

Install McAfee Agent Dependencies:
  pkg.installed:
    - pkgs:
      - unzip
      - ed

{%- for port in mcafee.client_in_ports %}
  {%- if salt.grains.get('osmajorrelease') == '7'%}
    {%- for zone in salt.firewalld.get_zones() %}
Allow ePO Mgmt Inbound Port {{ port }}-{{ zone }}:
  module.run:
    - name: 'firewalld.add_port'
    - zone: '{{ zone }}'
    - port: '{{ port }}/tcp'
    - permanent: True
    - require_in:
      - module: Reload firewalld for McAfee Inbound Port {{ port }}
    {%- endfor %}
Reload firewalld for McAfee Inbound Port {{ port }}:
  module.run:
    - name: firewalld.reload_rules
  {%- elif salt.grains.get('osmajorrelease') == '6'%}
Allow ePO Mgmt Inbound Port {{ port }}:
  iptables.append:
    - table: filter
    - chain: INPUT
    - jump: ACCEPT
    - match:
        - state
        - comment
    - comment: "ePO management of McAfee Agent"
    - connstate: NEW
    - dport: {{ port }}
    - proto: tcp
    - save: True
    - require_in:
      - file: Stage McAfee Install Archive
  {%- endif %}
{%- endfor %}

Stage McAfee Install Archive:
  file.managed:
  - name: /root/install.sh
  - source: {{ mcafee.source }}
  - source_hash: {{ mcafee.source_hash }}
  - user: root
  - group: root
  - mode: 0700
  - show_changes: False
  - require:
    - pkg: Install McAfee Agent Dependencies

Install McAfee Agent:
  cmd.run:
    - name: 'sh /root/install.sh -i'
    - cwd: '/root'
    - require:
      - file: Stage McAfee Install Archive
    - unless:
{%- for rpm in mcafee.rpms %}
      - 'rpm --quiet -q {{ rpm }}'
{%- endfor %}
{%- for key_file in mcafee.key_files %}
      - 'test -s {{ mcafee.keystore_directory }}/{{ key_file }}'
{%- endfor %}
