# Repository discovery and layering

## Repository boundaries

TSP workspaces commonly contain multiple sibling Git repositories. A feature may change a service repository and `tsp-service-common`, but each has its own branch, dirty state, base comparison, build, and commit history. Never run repository-wide Git assumptions from their non-Git parent directory.

## Discover rather than assume

TSP services share Spring Boot, Dubbo, Maven, MyBatis, OpenFeign, validation, and common contracts, but their internal layouts vary:

- newer services often use `provider`, `service`, `manager`, `mapper`, and BO/DO packages;
- some adapter-style services use `controller`, `adapter`, `dao`, and factories;
- specialized services may add strategies, handlers, actions, tasks, and listeners.

Follow the closest current implementation in the target service. Do not impose another service's package layout solely for uniformity.

## Common ownership

Within `tsp-service-common`, verify the current module structure, typically:

- `tsp-service-biz-api`: public business RPC interfaces and request/response contracts;
- `tsp-service-adapter-api`: external service interfaces, Feign clients, and source-specific DTOs;
- `tsp-service-enum`: TSP and source-system dynamic enums;
- `tsp-service-cmn-api`: common-service contracts when local precedent assigns them here;
- `tsp-service-util`: genuinely reusable utilities;
- BOM/parent modules: dependency and build policy, not ordinary feature placement.

## Layer decisions

- Public wire types belong in common, not in a service implementation repository.
- RPC providers/controllers adapt public contracts and should remain thin.
- Services own use-case orchestration and business-derived response fields.
- Managers/adapters own reusable external or cross-use-case access and normalize vendor protocols.
- Mappers/DAOs own database access, not presentation rules.
- Query-specific DOs must not leak into public responses.
- Use a top-level BO when it crosses class boundaries or has reusable meaning; retain a private helper type only when truly local.
- Before moving existing logic, search all consumers and ensure the new abstraction serves more than cosmetic method shortening.

## Runtime registration

- Follow the target's existing `@RpcImpl` form and service interface binding.
- Follow the target's Spring stereotype and injection convention.
- Keep mapper scan, mapper annotation, namespace, XML location, and `@DS` consistent.
- Inspect whether `@EnableFeignClients` registers explicit client classes or package names and update it accordingly.
