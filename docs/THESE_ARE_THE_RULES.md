# These Are The Rules

## Constitutional Rules (MANDATORY)

1. **No classes** - Pure functions only
2. **No mutations** - `ReadonlyArray<T>` everywhere
3. **No loops** - Use native methods internally
4. **No exceptions** - NEVER throw. Return monadic helpss. Use try/catch ONLY to wrap user-provided callbacks and convert their exceptions to Help/Helps
5. **Never null** - Use `undefined` for absent values
6. **One function per file** - `index.ts` + `index.test.ts`
7. **Pure functions** - Same input → same output
8. **No arrow functions** - Use `function` keyword in implementations
9. **Fully curried** - EXACTLY one parameter per function level. Curried does **NOT** mean _returns a function_. That is higher-order. A curried function has exactly ONE parameter, no more, no fewer, no optional parameters, no default values and can return ANYTHING except void.
10. **100% test coverage** - All tests must pass, no unreachable code
11. **Happy path pattern** - Nest positive conditionals; usable case innermost, return help as you exit each level
12. **No negation operators** - NEVER use `!` in conditionals; use positive predicates (e.g., `isNonEmptyArray` not `!isEmpty`)
13. **Accumulate helps** - Validation path MUST check ALL validatable params even when one fails, to collect all helps
14. **Private naming** - Functions in `_folder/` MUST have underscore prefix: `_functionName`
15. **Helper functions are private** — Use the prepended underscore on the folder and the function. Do not rename on import. Underscore everywhere. Example: `_functionName/index.ts`.
16. **Utility functions, constants, and types folders at LOWEST COMMON ANCESTOR** — If used in only one function, then the folder goes in that function's folder. If used by multiple functions, then the folder is promoted to the LOWEST COMMON ANCESTOR folder.
17. **No interfaces** — union types only.

## Additional Rules

From `strict-implementation.md` lines 106-116:

- No OOP array/string methods
- No arrow functions (except type signatures)
- No raw operators
- Correct file naming

## Comments

- Every function MUST have an `//++` Envoy comment

## The Three Monads

| Monad          | Usable      | Helps                         | Purpose                    |
| -------------- | ------------ | ------------------------------- | -------------------------- |
| **Maybe**      | `Just<T>`    | `Nothing`                       | Optional values, no errors |
| **Result**     | `Ok<T>`      | `Help<E>`                       | Fail-fast with rich errors |
| **Validation** | `Usable<T>` | `Helps<readonly [H, ...H[]]>` | Accumulates ALL errors     |

### Critical Difference

- **Result** + `chain`: Fail-fast (stops at first error). USE FOR SEQUENTIAL OPERATIONS WHERE ONE FAILURE ENDS THE OPERATION.
- **Validation** + `combineValidations`: Accumulates ALL errors. USE FOR TREE/PARALLEL OPERATIONS WHERE THE OPERATION CAN CONTINUE IN ANOTHER BRANCH AFTER A FAILURE.
- Never use `chain` in Validation for accumulation; use `combineValidations`

## File Structure

```
operation/
├── index.ts                    # Main function
├── index.test.ts               # Tests with fast-check, 100% coverage
├── constants/index.ts          # Shared HELP definitions
├── types/index.ts              # Type definitions
├── _privateHelper/             # Private functions start with underscore
│   ├── index.ts
│   └── index.test.ts
```

## File Requirements Checklist

Before moving to the next file, ALL of these must be complete:

1. **Algorithm Correctness** - Function does what it is supposed to do
2. **Envoy Comments** - File has `//++` comments
3. **Linter** - Zero issues (`deno task lint`)
4. **Type Check** - Zero issues (`deno check <file>`)
5. **Tests** - 100% code coverage, using `Deno.test`, `t.step`, and `fast-check`
6. **Plan Updates** - Keep plan document current
7. **All rules followed, no exceptions** - No lying, cheating, guessing, assuming, shortcuts, agent. One file and line at a time. Take your time and get it right. DO NOT REPORT "FACTS" THAT YOU HAVE NOT CONFIRMED.

## Unreachable Code Policy

From `CLAUDE.md`:

- There is NO such thing as "defensive" unreachable code
- Unreachable code is tech debt
- Eliminate all unreachable code
- Do NOT write fallback branches that can never execute
- 100% coverage means 100% - no exceptions
