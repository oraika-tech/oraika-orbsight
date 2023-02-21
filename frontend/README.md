# Oraika Web Mono Repo


## Developer Guide

### Creating common packages

You need to have a index.ts or index.js file in the root of every package (even if they just have an empty export), in order for the next-transpile-modules to work, but you can organize your code in folders, you don't need to export everything in the main index file.

### Naming convensions

1. Component name: PascalCase
2. File name same as Component name in PascalCase
3. Always have only one component in a file
4. No index.js for components
5. Write test, css, component all in same folder
6. Prefix higher order component with "with"

E.g.

```
- src/
--- components/
----- App/
------- index.js
------- component.js
------- test.js
------- style.css
----- List/
------- index.js
------- component.js
------- test.js
------- style.css
--- hooks/
----- useClickOutside.js
----- useScrollDetect/
------- index.js
------- hook.js
------- test.js
--- context/
----- Session.js
```

# Mantine Next Template

Get started with Mantine + Next with just a few button clicks.
Click `Use this template` button at the header of repository or [follow this link](https://github.com/mantinedev/mantine-next-template/generate) and
create new repository with `@mantine` packages. Note that you have to be logged in to GitHub to generate template.

## Features

This template comes with several essential features:

- Server side rendering setup for Mantine
- Color scheme is stored in cookie to avoid color scheme mismatch after hydration
- Storybook with color scheme toggle
- Jest with react testing library
- ESLint setup with [eslint-config-mantine](https://github.com/mantinedev/eslint-config-mantine)

## npm scripts

### Build and dev scripts

- `dev` – start dev server
- `build` – bundle application for production
- `export` – exports static website to `out` folder
- `analyze` – analyzes application bundle with [@next/bundle-analyzer](https://www.npmjs.com/package/@next/bundle-analyzer)

### Testing scripts

- `typecheck` – checks TypeScript types
- `lint` – runs ESLint
- `prettier:check` – checks files with Prettier
- `jest` – runs jest tests
- `jest:watch` – starts jest watch
- `test` – runs `jest`, `prettier:check`, `lint` and `typecheck` scripts

### Other scripts

- `storybook` – starts storybook dev server
- `storybook:build` – build production storybook bundle to `storybook-static`
- `prettier:write` – formats all files with Prettier
