#
# This salt state attempts to download and install the correct Splunk
# client-agent for the host's architecture. Further, the state will attempt
# to locate and install appropriate client configuration files. Th salt state
# will also add the requisite iptables exceptions to the OUTPUT filter to
# allow communications between the local Splunk agent and the remote Splunk
# Enterprise collector.
#
#################################################################

{%- from tpldir ~ '/map.jinja' import splunkforwarder with context %}

{%- set comment = "Connectivity for splunkforwarder" %}

{%- for port in splunkforwarder.client_out_ports %}
  {%- if salt.grains.get('osmajorrelease') == '7' %}
Allow Splunk Mgmt Outbound Port {{ port }}:
  cmd.run:
    - name: |
        firewall-cmd --direct --add-rule ipv4 filter OUTPUT_direct 50 -p tcp -m tcp --dport={{ port }} -m comment --comment "{{ comment }}" -j ACCEPT
        firewall-cmd --permanent --direct --add-rule ipv4 filter OUTPUT_direct 50 -p tcp -m tcp --dport={{ port }} -m comment --comment "{{ comment }}" -j ACCEPT
  {%- elif salt.grains.get('osmajorrelease') == '6' %}
Allow Splunk Mgmt Outbound Port {{ port }}:
  iptables.append:
    - table: filter
    - chain: OUTPUT
    - jump: ACCEPT
    - match:
        - state
        - comment
    - comment: "{{ comment }}"
    - connstate: NEW
    - dport: {{ port }}
    - proto: tcp
    - save: True
    - require_in:
      - file: Install Splunk Package
  {%- else %}
  {%- endif %}
{%- endfor %}

Install Splunk Package:
  pkg.installed:
    - sources:
      - {{ splunkforwarder.package }}: {{ splunkforwarder.package_url }}

Install Client Log Config File:
  file.managed:
    - name: {{ splunkforwarder.log_local.conf }}
    - user: root
    - group: root
    - mode: 0600
    - contents: |
        {{ splunkforwarder.log_local.contents | indent(8) }}
    - require:
      - pkg: Install Splunk Package

Install Client Agent Config File:
  file.managed:
    - name: {{ splunkforwarder.deploymentclient.conf }}
    - user: root
    - group: root
    - mode: 0600
    - contents: |
        [deployment-client]
        disabled = false
        clientName = {{ splunkforwarder.deploymentclient.client_name }}

        [target-broker:deploymentServer]
        targetUri = {{ splunkforwarder.deploymentclient.target_uri }}
    - require:
      - pkg: Install Splunk Package

{%- if splunkforwarder.inputs.get('sections') %}
Create Inputs Conf:
  file.managed:
    - name: {{ splunkforwarder.inputs.conf }}
    - user: root
    - group: root
    - mode: 0600
    - makedirs: True
    - replace: False
    - require_in:
      - ini: Configure Local Log Sources

Configure Local Log Sources:
  ini.options_present:
    - name: {{ splunkforwarder.inputs.conf }}
    - sections: {{ splunkforwarder.inputs.sections }}
    - require_in:
      - cmd: Accept Splunk License
    - watch_in:
      - service: Ensure Splunk Service is Running
{%- endif %}

Accept Splunk License:
  cmd.run:
    - name: {{ splunkforwarder.bin_file }} start --accept-license
    - require:
      - file: Install Client Log Config File
      - file: Install Client Agent Config File
    - unless: test -f {{ splunkforwarder.cert_file }}

Configure Splunk Agent Boot-scripts:
  cmd.run:
    - name: {{ splunkforwarder.bin_file }} enable boot-start
    - require:
      - cmd: Accept Splunk License
    - unless: test -f {{ splunkforwarder.service_file }}

Enable Splunk Service:
  service.enabled:
    - name: {{ splunkforwarder.service }}
    - require:
      - cmd: Configure Splunk Agent Boot-scripts

Ensure Splunk Service is Running:
  service.running:
    - name: {{ splunkforwarder.service }}
    - require:
      - service: Enable Splunk Service
    - watch:
      - file: Install Client Log Config File
      - file: Install Client Agent Config File
