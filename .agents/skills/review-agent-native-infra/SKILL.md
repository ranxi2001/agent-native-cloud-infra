---
name: review-agent-native-infra
description: Review agent-native cloud infrastructure across sandbox runtimes, Kubernetes controllers, multi-cluster control planes, SDK and API contracts, lifecycle pools, isolation, networking, credentials, multi-tenancy, observability, and release boundaries. Use for architecture reviews, source tracing, design proposals, PR reviews, runtime comparisons, failure analysis, security-sensitive sandbox changes, or cross-project analysis involving Karmada, AgentCube, OpenSandbox, or similar infrastructure.
---

# Review Agent-Native Infra

Review system behavior across contracts, state, lifecycle, trust, and operations rather than treating a sandbox or controller change as an isolated function diff.

## Establish The Review Surface

1. Route every repository and load its nearest instructions.
2. Read `references/review-checklist.md`.
3. Pin source, docs, releases, and CI evidence to exact refs and observation dates.
4. State whether each capability is released, merged on main, proposed, locally measured, or inferred.
5. Map the user entry point through API/SDK, control plane, provider/controller, runtime, persistence, networking, and cleanup.
6. Identify authoritative state, caches, reflected status, queues, leases, and recovery events.

## Trace Behavior

For each changed or compared flow, cover:

- creation, readiness, use, timeout, cancellation, deletion, retry, and recovery;
- identity, tenant, authorization, credential, ingress, and egress boundaries;
- cold start, warm pool, acquire/release, expiry, tombstone, and orphan cleanup;
- schema-to-server-to-provider-to-SDK propagation;
- concurrency, idempotency, stale state, partial failure, and restart behavior;
- metrics, logs, traces, health/readiness, and bounded cardinality;
- version skew, generated clients, upgrades, rollback, and component release trains.

Use a sequence diagram for actor order, a state diagram for lifecycle, and a flowchart for branching causes. Keep claims linked to code, logs, tests, or official contracts.

## Apply Safety Gates

- Prove production reachability before calling a synthetic failure a bug.
- Require a complete causal chain before proposing a flake or retry fix.
- Treat credential injection, proxy trust, path normalization, bind mounts, privileged execution, tenant isolation, and secret handling as security boundaries.
- Separate host/bootstrap failures from product behavior in runtime smoke tests.
- Verify cleanup of containers, clusters, ports, worktrees, and temporary credentials.
- Do not equate a monorepo main commit with all components being released.

## Produce Findings

Lead with confirmed behavior, concrete failure scenario, impact, and smallest credible correction or test. Separate findings from questions and hypotheses. For cross-project comparisons, compare equivalent contract layers and runtime modes; do not compare a released Docker path in one project with an unshipped Kubernetes proposal in another without labeling the mismatch.

Store task-specific analysis and evidence in the selected lane. Promote only reusable cross-project review checks into this skill.

## Finalize The Review

Before delivering the result:

- name the loaded repository instructions, exact refs, `observed_at`, and evidence status;
- include a small Mermaid diagram when the trace crosses three or more actors, branches, or lifecycle states;
- separate confirmed findings from questions, hypotheses, and unverified release reachability;
- list every validation tier run or skipped and confirm the final repository, host, and cluster cleanup state.
