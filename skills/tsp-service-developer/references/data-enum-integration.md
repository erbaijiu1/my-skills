# Data, enum, and integration rules

## Database access

- Identify the mapper/DAO data source before designing SQL. Do not join tables that are not guaranteed to exist in the same configured data source.
- Prefer focused single-table batch queries and merge independent datasets in Java when a wide join is fragile.
- Guard empty collections before invoking SQL containing `IN (...)`.
- Select only required columns and align aliases, result maps, and DO properties exactly.
- For latest N records per business key, use deterministic ordering such as timestamp descending plus unique ID descending. A window function with an outer `rn <= N` filter is acceptable when supported.
- Keep SQL and Java ordering consistent before accessing the current and previous record.
- Build lookup maps once; do not repeatedly scan full query results inside a per-item loop.
- Define duplicate resolution explicitly.

## Mapper XML conventions

Follow the established MyBatis mapper style when writing or reviewing mapper XML:

1. Declare an explicit `<resultMap>` mapping snake_case columns to camelCase properties, one `<result column="..." property="..." />` per field:
   ```xml
   <resultMap id="BaseResultMap" type="com.ciccwm.tsp.coupon.domain.CouponRecord">
       <result column="coupon_status" property="couponStatus" />
       <result column="discount_value" property="discountValue" />
   </resultMap>
   ```
2. Extract the selected column list into a reusable `<sql id="Base_Column_List">` fragment and reference it with `<include refid="Base_Column_List"/>`.
3. Use `resultMap="BaseResultMap"` on `<select>` rather than `resultType`, so aliases and property mapping stay explicit and reviewable.
4. When a column name needs an alias (e.g. `uc.id AS coupon_id`), put the alias inside `Base_Column_List` and keep the `<result column="coupon_id" property="couponId" />` matching the aliased name.
5. For enum-typed properties, write a plain `<result column="..." property="..." />` without an explicit `typeHandler`. TSP dynamic enums are auto-registered by the shared `TypeHandlerConfiguration`, which scans `AbstractDynamicEnum` subclasses and registers the default `EnumTypeHandler`.
6. Keep dynamic `<if>` / `<where>` conditions in the `<select>` body, not inside the column list fragment.

## Response assembly

Organize service code by the response values it fills:

1. base identity fields;
2. current business values;
3. comparison/change fields;
4. derived counts or classifications;
5. restriction and placeholder fields;
6. final sort and pagination.

Prefer one canonical identity map containing raw code, normalized market, and display name over several parallel maps. Include market in the key where source codes are not globally unique.

Apply display placeholders such as `--` in response assembly, not SQL. Ensure restriction flags, placeholders, sort placement, change flags, and counts remain mutually consistent.

## JSON fields

- Keep a database JSON column as a string in the DO when only one use case parses it.
- Parse it in a focused helper using the project's JSON library.
- Match typed JSON elements exactly; do not substring-search serialized JSON.
- Handle null, blank, malformed JSON, missing keys, wrong types, empty arrays, and exact matches deliberately.
- Avoid logging sensitive or excessively large payloads.

## External systems

- Prefer batch endpoints; never issue one remote request per item when a list call exists or can safely be added.
- A successful dependency call with no records maps to an empty collection.
- Null envelopes and explicit non-success business statuses are dependency failures.
- Timeout, connection, HTTP 5xx, and decoding exceptions may propagate to the global handler when its response is acceptable; otherwise translate them consistently at the integration boundary.
- Confirm Feign registration and configuration after adding a client.

## Dynamic enums

TSP dynamic enums normally extend `AbstractDynamicEnum` and expose constants plus `valueOf`, `valueOfOrNull`, `valueOfOrDefault`, and `values` through `EnumUtil`.

- Put each source system's enum in its own namespace.
- Convert source enum -> TSP enum at the integration boundary, then use the TSP enum in business logic.
- Never use another source's market enum because numeric values currently coincide.
- Add a `TspDictionaryTypeEnum` category when onboarding a new dictionary source.
- Runtime conversion may depend on dictionary data. Java enum code is incomplete without required category, enum-value, and conversion-mapping DML.
- Use the `tsp-emun-sql-generator` skill whenever dictionary or bidirectional conversion SQL is required.
- Treat missing release DML as a release risk or explicitly deferred task even when compilation passes.
