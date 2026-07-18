# Agent-Native Infrastructure Review Checklist

## Contract

- Public API, OpenAPI/CRD schema, CLI, SDK, generated clients
- Defaults, validation, compatibility, version skew, deprecation
- Cross-language or cross-provider semantic parity

## Lifecycle And State

- Create, ready, execute, suspend, resume, expire, delete
- Pool fill, acquire, release, shrink, destroy, tombstone
- Source of truth versus cache, informer, reflected status, Redis, lease
- Idempotency, retries, backoff, cancellation, partial cleanup, restart recovery

## Runtime And Isolation

- Container, Pod, VM, process, or inner-session boundary
- Namespace, cgroup, seccomp, capability, user namespace, filesystem mount
- Image pull, snapshot/commit, volume ownership, resource requests and limits
- Host prerequisites: architecture, kernel, KVM, privileged mode, cgroup mode

## Trust And Multi-Tenancy

- Authentication and authorization subject
- Tenant-to-namespace/provider mapping
- Service account tokens and workload identity
- Credential custody and injection point
- Egress allowlist, DNS/IP binding, proxy trust, path normalization
- Ingress exposure, token scope, SSRF, traversal, confused-deputy risks

## Operations

- Health, readiness, metrics, logs, traces, alert compatibility
- Bounded labels and cardinality
- Helm/operator/controller upgrade and rollback
- Release train versus main-only behavior
- Failure-domain cleanup and operator diagnostics

## Validation Matrix

| Tier | Typical proof | Environment |
| --- | --- | --- |
| Static | format, lint, schema, generated diff | local |
| Unit | pure behavior and error paths | local |
| Component | server/runtime/provider integration | local or Docker |
| Cluster | controller, RBAC, scheduling, network policy | Kind or Kubernetes |
| Privileged | KVM, bwrap, gVisor, mount, kernel behavior | capable Linux host |
| Cloud | managed identity, registry, load balancer, provider API | controlled account |

State every tier not run and why. After a smoke test, verify cleanup and record the final host/cluster state.
