The goal in **pure FP terms**:

- no `interface`, no nominal contracts
- no classes
- no framework magic
- everything is **values + functions**
- routing is **derived data**

Below is a routing model that fits our constraints _exactly_.

---

## 1. Pages are just functions

A page is **nothing but a function**.

```ts
export default function Page (ctx: PageCtx) {
  return (
	  <html>
	    <body>
	      <h1>About</h1>
	    </body>
	  </html>
  )
}
```

No interface. No default export requirement. No special typing.

### Context is a value

```ts
export default function makePageCtx(url: URL) {
	return function makePageCtxWithUrl(params: Record<string, string>) {
		return function makePageCtxWithParams(mode: "dom" | "string") {
			return {
				url,
				params,
				mode,
			};
		};
	};
}
```

Types are **structural**, not nominal.

---

## 2. Route = pure data

A route is a _record_, not a concept.

```ts
export default function Route(path: string) {
	return function RouteWithPath(
		load: () => Promise<(ctx: PageCtx) => JSX.Element | string>,
	) {
		return { path, load };
	};
}
```

No interface. No class.

This is key: **routes are values**.

---

## 3. Filesystem → routes (pure transformation)

The router is just a function:

```ts
export default async function discoverRoutes(root: string) {
	const files = await collectIndexFiles(root);

	return files.map(function toRoute(file) {
		return Route(fileToPath(root)(file))(function load() {
			return import(file).then(function getPage(m) {
				return m.page;
			});
		});
	});
}
```

All side effects are:

- reading the filesystem
- dynamic import

Everything else is pure mapping.

---

## 4. Hidden folders: a filter, not a rule

```ts
function isHidden(path: string) {
	return path.split("/").some((seg) => seg.startsWith("_"));
}
```

Used as a filter:

```ts
files
  .filter(f => !isHidden(relative(root, f)))
  .map(...)
```

No special router logic.

---

## 5. Index-based routing only (simple, correct)

```ts
function fileToPath(root: string) {
	return function fileToPathFromRoot(file: string) {
		const rel = relative(root, dirname(file));

		return rel === "" ? "/" : `/${rel}`;
	};
}
```

No ambiguity.
No edge cases.
No magic filenames.

---

## 6. Matching = function composition

Routing is **just lookup**.

```ts
export default function matchRoute(routes) {
	return function matchRouteIn(path) {
		return routes.find(function hasPath(r) {
			return r.path === path;
		});
	};
}
```

Later, if you want dynamic segments, you _replace this function_, not the system.

---

## 7. Rendering = apply function to value

```ts
export default function renderRoute(route) {
	return async function renderRouteWithRoute(ctx) {
		const page = await route.load();

		return page(ctx);
	};
}
```

That’s it.

No lifecycle.
No hooks.
No mutable state.

---

## 8. Layouts as higher-order functions (very FP)

Layouts are just:

```ts
export default function layout(child) {
	return function layoutWithChild(ctx) {
		return (
			<html>
				<body>
					{child(ctx)}
				</body>
			</html>
		);
	};
}
```

Folder `_layout.tsx` exports a function.

Composition:

```ts
export default function compose(layouts) {
	return function composeWithLayouts(page) {
		return layouts.reduceRight(function wrap(acc, l) {
			return l(acc);
		}, page);
	};
}
```

Again:

- values
- functions
- no interfaces

---

## 9. Assets stay dumb (important FP decision)

Assets are **not routed**.

They’re static files served separately.

This avoids:

- impurity in the router
- coupling render logic to IO

FP win.

---

## 10. What you’ve actually built

Conceptually, you now have:

```
Filesystem
  ↓
[ Route data ]
  ↓
match : Path → Route
  ↓
load : () → Page
  ↓
apply : PageCtx → View
```

That is a **pure pipeline**.

---

## 11. Why this scales without regret

- You can cache routes
- You can precompute them for SSG
- You can serialize them
- You can test them without a browser
- You can replace matching logic later
- You never have to break users

This is _exactly_ how an FP-first web framework should feel.

---

## 12. Next

Natural next steps that **don’t violate FP**:

1. Dynamic routes as _parsers_
2. Typed params via combinators
3. Route trees as zippers
4. Static extraction for SSG
5. Effect isolation (IO layer)
