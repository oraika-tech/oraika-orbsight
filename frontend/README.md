# Oraika Web Mono Repo


## Developer Guide

### Creating common packages

You need to have a index.ts or index.js file in the root of every package (even if they just have an empty export), in order for the next-transpile-modules to work, but you can organize your code in folders, you don't need to export everything in the main index file.
