# AWX ixpeer starter (Junos)

This repository contains a minimal, safe-by-default IX peer automation for Junos using Ansible.

## Contents
- `requirements.yml` – Ansible collections
- `inventory/hosts.yml` – example inventory (for local testing)
- `group_vars/routers.yml` – defaults (policies, confirm window, Telegram)
- `templates/junos_ixpeer_set.j2` – renders Junos `set` commands
- `playbooks/ixpeer_add.yml` – add peer, verify, confirm
- `playbooks/ixpeer_remove.yml` – remove peer safely
- `playbooks/ixpeer_verify.yml` – verify neighbor state

## Run locally (optional)
```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i inventory/hosts.yml playbooks/ixpeer_add.yml \
  -e group_name=IX-HKG -e peer_ip=198.51.100.1 -e peer_asn=65001 \
  -e description="HKGIX Example" -e prefix_limit=100000 \
  -e local_address_v4=192.0.2.2