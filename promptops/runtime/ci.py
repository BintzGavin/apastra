"""Enforcement only: execute or admit revision-bound trusted evidence."""

import subprocess

from promptops.runtime.evidence import EvidenceError
from promptops.runtime.gate import admit_run, regression
from promptops.runtime.suite import evaluate_suite


def ci_gate(suite, adapter, revision, mode, run_dir, baseline=None, policy=None):
    if mode not in ("execute", "evidence"):
        raise EvidenceError("CI mode must be execute or evidence; advisory output is not a required check")
    if bool(baseline) != bool(policy):
        raise EvidenceError("Regression enforcement needs both baseline and policy")
    head = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
    if head.returncode or head.stdout.strip() != revision:
        raise EvidenceError("CI checkout does not match the expected revision")
    if mode == "execute":
        executed = evaluate_suite(suite, adapter, run_dir)
        if executed["status"] not in ("pass", "fail", "not_evaluated"):
            return executed
    if baseline:
        return regression(run_dir, baseline, policy, adapter, revision, suite, check_workspace=True)
    return admit_run(run_dir, adapter, revision, suite, check_workspace=True)["decision"]
