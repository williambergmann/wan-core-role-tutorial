#!/usr/bin/env python3
"""
State Diff Script — Compare two state snapshots and highlight changes.

Compares two JSON snapshots produced by state_capture.py and generates
a diff report showing added, removed, and changed state.

Usage:
    python state_diff.py --before snap_before.json --after snap_after.json
"""

import json
import argparse
import sys

try:
    from deepdiff import DeepDiff
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
except ImportError:
    print("Required packages not installed. Run: pip install -r requirements.txt")
    exit(1)

console = Console()


def load_snapshot(filepath: str) -> dict:
    """Load a state snapshot from JSON."""
    with open(filepath) as f:
        return json.load(f)


def compare_snapshots(before: dict, after: dict) -> dict:
    """Compare two snapshots and return structured diff."""
    results = {
        "summary": {
            "before_timestamp": before.get("capture_timestamp"),
            "after_timestamp": after.get("capture_timestamp"),
            "devices_before": before.get("device_count"),
            "devices_after": after.get("device_count"),
        },
        "device_diffs": [],
    }

    before_devices = {d["hostname"]: d for d in before.get("devices", [])}
    after_devices = {d["hostname"]: d for d in after.get("devices", [])}

    all_hostnames = set(before_devices.keys()) | set(after_devices.keys())

    for hostname in sorted(all_hostnames):
        device_diff = {"hostname": hostname, "changes": []}

        if hostname not in before_devices:
            device_diff["status"] = "NEW DEVICE"
            results["device_diffs"].append(device_diff)
            continue

        if hostname not in after_devices:
            device_diff["status"] = "MISSING DEVICE"
            results["device_diffs"].append(device_diff)
            continue

        device_diff["status"] = "PRESENT"
        before_cmds = before_devices[hostname].get("commands", {})
        after_cmds = after_devices[hostname].get("commands", {})

        for cmd in set(before_cmds.keys()) | set(after_cmds.keys()):
            before_out = before_cmds.get(cmd, "")
            after_out = after_cmds.get(cmd, "")

            if before_out != after_out:
                # Find specific line-level differences
                before_lines = set(before_out.splitlines())
                after_lines = set(after_out.splitlines())

                added = after_lines - before_lines
                removed = before_lines - after_lines

                device_diff["changes"].append({
                    "command": cmd,
                    "lines_added": len(added),
                    "lines_removed": len(removed),
                    "added": sorted(list(added))[:20],  # cap at 20 lines
                    "removed": sorted(list(removed))[:20],
                })

        results["device_diffs"].append(device_diff)

    return results


def print_report(diff: dict):
    """Print a formatted diff report."""
    console.print(Panel(
        f"Before: {diff['summary']['before_timestamp']}\n"
        f"After:  {diff['summary']['after_timestamp']}\n"
        f"Devices: {diff['summary']['devices_before']} → {diff['summary']['devices_after']}",
        title="📊 State Comparison Report",
    ))

    changes_found = False

    for device in diff["device_diffs"]:
        hostname = device["hostname"]
        status = device["status"]

        if status == "NEW DEVICE":
            console.print(f"\n[bold green]🆕 {hostname} — NEW DEVICE[/]")
            changes_found = True
            continue

        if status == "MISSING DEVICE":
            console.print(f"\n[bold red]❌ {hostname} — MISSING DEVICE[/]")
            changes_found = True
            continue

        if not device["changes"]:
            continue

        changes_found = True
        console.print(f"\n[bold yellow]🔄 {hostname}[/]")

        for change in device["changes"]:
            console.print(f"  Command: [cyan]{change['command']}[/]")
            console.print(f"    Lines added: [green]+{change['lines_added']}[/]  "
                         f"Lines removed: [red]-{change['lines_removed']}[/]")

            for line in change.get("removed", [])[:5]:
                console.print(f"    [red]- {line.strip()}[/]")
            for line in change.get("added", [])[:5]:
                console.print(f"    [green]+ {line.strip()}[/]")

    if not changes_found:
        console.print("\n[bold green]✅ No differences found — state is identical.[/]")


def main():
    parser = argparse.ArgumentParser(description="Compare two state snapshots")
    parser.add_argument("--before", "-b", required=True, help="Before snapshot JSON")
    parser.add_argument("--after", "-a", required=True, help="After snapshot JSON")
    parser.add_argument("--output", "-o", help="Save diff report to JSON")
    args = parser.parse_args()

    before = load_snapshot(args.before)
    after = load_snapshot(args.after)

    diff = compare_snapshots(before, after)
    print_report(diff)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(diff, f, indent=2)
        console.print(f"\n[dim]Report saved to {args.output}[/]")


if __name__ == "__main__":
    main()
