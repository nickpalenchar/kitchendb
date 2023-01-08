# Components

This directory contains independent [solid][https://www.solidjs.com/] components, which can be required into a
hugo page via a partial or shortcode.

Every component with that is capitalized will considered a build input, and will be built into its own file. 
Lowercased files are not exported by themselves (they should be required into another component).

```
Form.tsx // built
utils.tsx // not built
Login.tsx // built
```

## Creating a Component.

Declare a solid component, but instead of exporting it, attach it to the window object as `window._components<Name>`

```ts
import type { Component } from 'solid-js';

const Foo: Component = () => {
  return (
    <div>Hello!</div> 
  );
};

window._componentFoo = Foo;
```

Run `npm build` from `scripts/compononts`

## Using a component in Hugo

### Within a shortcode/layout (as a partial)

Pass a `Component` variable in the context

```hugo
// example.html
{{ partial render-component dict "Component" "Foo" }}
```

### Within content (as a shortcode)

Pass the name in the shortcode.

```md
// content/example.md

{{< render-component "Foo" >}}
```