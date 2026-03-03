# 🤖 Automation Toolkit

> Cross-cutting automation for lab validation, operational tasks, and configuration management.

---

## Directory Structure

```
automation/
├── ansible/              # Ansible playbooks for fabric operations
│   ├── ansible.cfg
│   ├── inventory/        # Lab device inventory
│   ├── playbooks/        # Operational playbooks
│   └── roles/            # Reusable roles
├── python/               # Python scripts for validation and state management
│   ├── requirements.txt
│   └── *.py              # Utility scripts
└── ai-prompts/           # AI prompt templates (see separate README)
```

## Setup

```bash
# Install Python dependencies
pip install -r python/requirements.txt

# Install Ansible
pip install ansible ansible-pylibssh

# Verify
ansible --version
python -c "import netmiko; print(netmiko.__version__)"
```

## Ansible Playbooks

| Playbook              | Purpose                            | Usage                                            |
| --------------------- | ---------------------------------- | ------------------------------------------------ |
| `deploy-underlay.yml` | Deploy OSPF underlay across fabric | `ansible-playbook playbooks/deploy-underlay.yml` |
| `deploy-overlay.yml`  | Deploy BGP EVPN overlay            | `ansible-playbook playbooks/deploy-overlay.yml`  |
| `pre-check.yml`       | Capture pre-change state           | `ansible-playbook playbooks/pre-check.yml`       |
| `post-check.yml`      | Capture post-change state + diff   | `ansible-playbook playbooks/post-check.yml`      |
| `health-check.yml`    | Full fabric health report          | `ansible-playbook playbooks/health-check.yml`    |
| `rollback.yml`        | Emergency rollback                 | `ansible-playbook playbooks/rollback.yml`        |

## Python Scripts

| Script                | Purpose                                  | Usage                                                         |
| --------------------- | ---------------------------------------- | ------------------------------------------------------------- |
| `state_capture.py`    | Snapshot routing/switching state to JSON | `python state_capture.py --hosts inventory.yml`               |
| `state_diff.py`       | Compare two state snapshots              | `python state_diff.py --before snap1.json --after snap2.json` |
| `convergence_test.py` | Measure failover convergence time        | `python convergence_test.py --target 10.1.0.1 --duration 60`  |
| `config_lint.py`      | Lint configs for common errors           | `python config_lint.py --config router.cfg`                   |
