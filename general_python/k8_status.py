#!/usr/bin/env python3
"""Check the status of Kubernetes control-plane and worker nodes.

The script shells out to ``kubectl`` to obtain node information in JSON format and
summarises the Ready condition for master/control-plane nodes as well as worker
nodes.  The command output is meant to be human-readable so the script can be
used as part of operational runbooks.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from typing import Iterable, List


def ensure_kubectl_exists() -> None:
    """Ensure that ``kubectl`` is available in the user's PATH.

    Raises:
        FileNotFoundError: if kubectl cannot be located.
    """

    if shutil.which("kubectl") is None:
        raise FileNotFoundError(
            "kubectl command not found. Please install kubectl and ensure it is in your PATH."
        )


@dataclass
class NodeStatus:
    """Represents the Ready status of a Kubernetes node."""

    name: str
    role: str
    ready: bool
    reason: str

    @classmethod
    def from_node(cls, node: dict) -> "NodeStatus":
        metadata = node.get("metadata", {})
        name = metadata.get("name", "<unknown>")
        labels = metadata.get("labels", {})
        role = infer_role(labels)
        conditions = node.get("status", {}).get("conditions", [])
        ready_condition = next(
            (condition for condition in conditions if condition.get("type") == "Ready"),
            None,
        )
        ready = bool(ready_condition and ready_condition.get("status") == "True")
        reason = ready_condition.get("reason", "Unknown") if ready_condition else "Unknown"
        return cls(name=name, role=role, ready=ready, reason=reason)


MASTER_LABELS = {
    "node-role.kubernetes.io/master",
    "node-role.kubernetes.io/control-plane",
    "node-role.kubernetes.io/controlplane",
}


def infer_role(labels: dict) -> str:
    """Infer the role of a node from its labels."""

    if any(label in labels for label in MASTER_LABELS):
        return "master"
    if "node-role.kubernetes.io/worker" in labels:
        return "worker"
    # Default classification: treat nodes without explicit role labels as workers.
    return "worker"


def fetch_nodes() -> List[dict]:
    """Fetch node information via ``kubectl`` and return the JSON payload."""

    ensure_kubectl_exists()
    try:
        completed = subprocess.run(
            ["kubectl", "get", "nodes", "-o", "json"],
            check=True,
            capture_output=True,
            text=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
            "Failed to execute 'kubectl get nodes'. Ensure your kubeconfig is valid and you have access to the cluster."
        ) from exc

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("kubectl returned invalid JSON output") from exc

    return payload.get("items", [])


def group_statuses(statuses: Iterable[NodeStatus]) -> tuple[list[NodeStatus], list[NodeStatus]]:
    masters: list[NodeStatus] = []
    workers: list[NodeStatus] = []
    for status in statuses:
        if status.role == "master":
            masters.append(status)
        else:
            workers.append(status)
    return masters, workers


def format_status_table(title: str, statuses: Iterable[NodeStatus]) -> str:
    rows = [
        f"{title}",
        "=" * len(title),
    ]
    empty = True
    for status in statuses:
        empty = False
        state = "Ready" if status.ready else f"NotReady ({status.reason})"
        rows.append(f"- {status.name}: {state}")
    if empty:
        rows.append("No nodes found.")
    return "\n".join(rows)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(argv)

    try:
        nodes = fetch_nodes()
    except (FileNotFoundError, RuntimeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    statuses = [NodeStatus.from_node(node) for node in nodes]
    masters, workers = group_statuses(statuses)

    print(format_status_table("Control-plane nodes", masters))
    print()
    print(format_status_table("Worker nodes", workers))

    if all(status.ready for status in statuses):
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
