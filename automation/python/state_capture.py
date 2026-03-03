#!/usr/bin/env python3
"""
State Capture Script — Snapshot network device state to JSON.

Connects to all devices in inventory and captures:
- Routing tables (all VRFs)
- BGP neighbor state
- OSPF neighbor state
- EVPN MAC/IP table
- VXLAN tunnel peers
- ARP table
- Interface status & counters
- NVE VNI status

Usage:
    python state_capture.py --inventory hosts.yml --output snapshot_20260309.json
"""

import json
import argparse
from datetime import datetime
from pathlib import Path

try:
    from netmiko import ConnectHandler
    from rich.console import Console
    from rich.progress import track
except ImportError:
    print("Required packages not installed. Run: pip install -r requirements.txt")
    exit(1)

console = Console()

# Show commands to capture state (NX-OS)
STATE_COMMANDS_NXOS = [
    "show ip route vrf all",
    "show bgp l2vpn evpn summary",
    "show ip ospf neighbor",
    "show l2route evpn mac all",
    "show nve peers",
    "show ip arp vrf all",
    "show interface brief",
    "show interface counters errors",
    "show nve vni",
    "show bfd neighbors",
    "show mac address-table",
    "show ip route summary vrf all",
]

# Show commands for Junos
STATE_COMMANDS_JUNOS = [
    "show route summary",
    "show bgp summary",
    "show ospf neighbor",
    "show evpn database",
    "show ethernet-switching vxlan-tunnel-end-point remote",
    "show arp no-resolve",
    "show interfaces terse",
    "show bfd session",
    "show ethernet-switching table summary",
]


def capture_device_state(device_params: dict, commands: list) -> dict:
    """Connect to a device and capture all state commands."""
    state = {
        "hostname": device_params.get("host", "unknown"),
        "timestamp": datetime.now().isoformat(),
        "commands": {},
    }

    try:
        with ConnectHandler(**device_params) as conn:
            hostname = conn.find_prompt().strip("#>")
            state["hostname"] = hostname

            for cmd in commands:
                try:
                    output = conn.send_command(cmd, read_timeout=30)
                    state["commands"][cmd] = output
                except Exception as e:
                    state["commands"][cmd] = f"ERROR: {str(e)}"

    except Exception as e:
        state["error"] = str(e)

    return state


def load_inventory(inventory_file: str) -> list:
    """Load device inventory from YAML file."""
    import yaml

    with open(inventory_file) as f:
        inv = yaml.safe_load(f)

    devices = []
    for group_name, group in inv.get("groups", {}).items():
        for host in group.get("hosts", []):
            devices.append(host)

    return devices


def main():
    parser = argparse.ArgumentParser(description="Capture network device state")
    parser.add_argument("--inventory", "-i", required=True, help="Inventory YAML file")
    parser.add_argument("--output", "-o", help="Output JSON file (default: auto-named)")
    parser.add_argument("--platform", "-p", default="nxos", choices=["nxos", "junos"],
                       help="Device platform")
    args = parser.parse_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = args.output or f"state_snapshot_{timestamp}.json"

    commands = STATE_COMMANDS_NXOS if args.platform == "nxos" else STATE_COMMANDS_JUNOS

    devices = load_inventory(args.inventory)
    console.print(f"[bold green]Capturing state from {len(devices)} devices...[/]")

    all_states = []
    for device in track(devices, description="Capturing..."):
        state = capture_device_state(device, commands)
        all_states.append(state)
        status = "✅" if "error" not in state else "❌"
        console.print(f"  {status} {state['hostname']}")

    snapshot = {
        "capture_timestamp": datetime.now().isoformat(),
        "device_count": len(all_states),
        "platform": args.platform,
        "devices": all_states,
    }

    with open(output_file, "w") as f:
        json.dump(snapshot, f, indent=2)

    console.print(f"\n[bold green]State captured → {output_file}[/]")
    console.print(f"  Devices: {len(all_states)}")
    console.print(f"  Commands per device: {len(commands)}")


if __name__ == "__main__":
    main()
