# Protocol and common-library rules

## Function contracts

For a TSP function-number endpoint:

1. Locate the correct common service interface by function-number range and business ownership.
2. Add request/response types in that interface's established package.
3. Match method capitalization and naming used by nearby functions.
4. Use the established request and response envelopes, normally `ReqVo<R...>` and `RespVo<...>`.
5. For a paged design, normally let the request extend `RPageVo` and return `RespVo<APageVo<A...>>`; do not flatten or add wrappers without explicit contract evidence.
6. Add bean-validation annotations and business comments for required values, formats, display placeholders, enum meanings, and special ordering.
7. Keep contract fields that are specified for compatibility even when initial logic is customer-level and does not yet consume an account-level field.
8. Name request classes with the `R` prefix and response classes with the `A` prefix, matching the function number: `R<functionNo>` for requests and `A<functionNo>` for responses. Every endpoint gets its own `A` response class even when the result is a single scalar (a success flag or an ID); do not return a bare `Boolean`/`Long`/`String` as the response body type.
9. Use a dynamic enum (e.g. `TspYesNoEnum`) rather than a raw `boolean`/`Boolean` for yes/no and success/failure result fields.

Rules 8 and 9 apply only to the public RPC contract surface: the function-number endpoint methods and their request/response contract types (the `ReqVo`/`RespVo` generics and the `R`/`A` classes). Internal layers (services, managers, DAOs, BOs, and helper methods) may freely use primitive and standard types (`boolean`, `Long`, `String`, etc.) and are not bound by these two rules.

An internal service return type does not dictate the public shape. The provider/controller owns BO-to-public mapping and the outer `RespVo`.

## Comment and formatting conventions

For request/response contract classes, follow these conventions so generated protocol code stays uniform:

1. Use a multi-line Javadoc comment for each field, placed directly above its annotations:
   ```java
   /**
    * 客户号
    */
   @NotBlank(message = "custCode不能为空")
   private String custCode;
   ```
2. Put each bean-validation annotation on its own line; keep the field declaration on a separate line. Do not write `@Annotation private Type field;` on one line.
3. Separate fields with a blank line.
4. Comment each RPC method in the service interface with a short `//` line describing its business name (e.g. `// 卡券预占冻结(Freeze)`).
5. Keep the class-level Javadoc concise: function number plus business name.

Comment content should cover required values, formats, display placeholders, enum meanings, and special ordering as required by the contract.

## RPC entry responsibilities

- Guard a null envelope and null request in addition to bean validation.
- Perform endpoint-level permission checks following existing behavior.
- Copy every request field into the internal BO.
- Invoke a focused service entry point.
- Map every response field and copy all page metadata.
- Return the exact success envelope or throw the project's established exception.

Do not place database queries, multi-source aggregation, vendor status handling, JSON parsing, or rating/count calculations in the RPC entry.

## Pagination

- Respect `RPageVo.MAX_PAGE_SIZE` from the actual dependency version rather than duplicating a number.
- Normalize page size to at least 1 and no more than the maximum unless validation is explicitly required to reject it.
- Normalize numeric page number/page sequence according to the actual `RPageVo` API in use.
- Calculate `(pageNum - 1) * pageSize` as `long`.
- Populate `list`, `pageSeq`, `pageSize`, `size`, `total`, `pages`, `firstPage`, and `lastPage`.
- Make empty-page semantics explicit and consistent with neighboring endpoints.

## External adapter contracts

- Put an external endpoint's true wire contract in a source-specific request/response type.
- Do not reuse a DTO when doing so exposes an unrelated flag or changes JSON shape.
- Match path, verb, envelope, generics, JSON names, nullable fields, and source status-code semantics.
- Search all usages before changing or deleting any public common type.

## Compatibility discipline

- Preserve generic nesting and serialization names unless the requirement explicitly changes them.
- Distinguish a stale example from an established compatibility constraint by checking current callers.
- If design, legacy code, and current implementation differ, use the latest explicit user clarification and report any compatibility consequence.
