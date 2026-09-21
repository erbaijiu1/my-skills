# Verification and review checklist

## Establish the baseline

For every involved repository:

- run `git branch --show-current`;
- run `git status --short`;
- identify the requested comparison base and verify that ref exists;
- inspect both committed branch changes and working-tree changes;
- do not claim or alter unrelated dirty files.

## Contract audit

- Function number, interface, method name, and owning module are correct.
- Request envelope, class, inheritance, required fields, validation, and comments match.
- Response envelope and generic nesting match exactly.
- Every specified response field is present and mapped; unrequested fields are absent.
- Enum types, dates, display placeholders, ordering, and pagination match.
- Permissions, empty behavior, and failures match the requirement.

## Data and runtime audit

- Mapper/DAO method, XML statement, parameter names, aliases, result map, and DO agree.
- Empty input cannot create invalid dynamic SQL.
- Data-source annotations match table ownership.
- Queries and remote calls are batch-oriented where feasible.
- Latest/current/previous selection is deterministic.
- Source enum conversion uses the correct source namespace.
- New Feign clients are registered by the application.
- Dependency failures cannot become successful empty results.
- Sorting happens after flags and derived fields are populated and before paging.
- Page limits, overflow-safe offsets, and all `APageVo` metadata are correct.
- Dynamic-enum DML and release configuration are accounted for.

## Static and build checks

Run in each changed Git repository:

```text
git diff --check
git status --short
git diff --stat
```

Read the POM before choosing commands. For common, compile affected modules plus dependencies, for example:

```text
mvn -pl tsp-service-enum,tsp-service-adapter-api,tsp-service-biz-api -am -DskipTests compile
```

Compile the target service after common. Install changed common artifacts locally only if required for normal dependency resolution and safe within the request.

Run focused tests when present. Treat `no tests found` as missing behavioral coverage, not proof of correctness. Validate mapper XML with an XML parser or build tooling and manually inspect dynamic SQL; Java compilation does not prove runtime SQL, data-source presence, Feign registration, enum DML, or business semantics.

## Final code review

Review the final diff for:

- protocol compatibility;
- null and empty handling;
- exception semantics;
- N+1 calls and oversized joins;
- deterministic comparison, sorting, and pagination;
- thread safety and state leakage;
- source/TSP enum confusion;
- missing registration, SQL, configuration, or release scripts;
- missing tests;
- business-stage grouping: one blank line between distinct stages/substages, comments adjacent to their code, and stage-specific preparation grouped with its consumer (see the proximity rules in `SKILL.md`).

Report findings by severity with file and line evidence. If no material finding remains, say so and list residual runtime or coverage risks.
