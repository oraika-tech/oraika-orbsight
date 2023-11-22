const fs = require('fs');
const path = require('path');
const _ = require('lodash'); // Import lodash

module.exports = function (fileInfo, api, options) {
    const j = api.jscodeshift;
    const root = j(fileInfo.source);
    console.log("Transforming: ", fileInfo.path)

    // Find createStyles import and remove it
    root.find(j.ImportDeclaration, {
        source: { value: '@mantine/core' },
    }).forEach(pathx => {
        pathx.node.specifiers = pathx.node.specifiers.filter(
            specifier => specifier.imported.name !== 'createStyles'
        );
        if (pathx.node.specifiers.length === 0) {
            j(pathx).remove();
        }
    });

    // Find createStyles usage
    root.find(j.CallExpression, {
        callee: { name: 'createStyles' },
    }).forEach(pathx => {
        const stylesObject = pathx.node.arguments[0];
        let cssContent = '';

        // Convert the JS object to CSS string
        function convertKeysToKebabCase(obj) {
            if (obj.type === 'ObjectExpression') {
                obj.properties.forEach(prop => {
                    if (prop && prop.key) {
                        const key = _.kebabCase(prop.key.name || prop.key.value);
                        prop.key.name = key;
                        convertKeysToKebabCase(prop.value);
                    }
                });
            } else if (obj.type === 'ArrayExpression') {
                obj.elements.forEach(element => {
                    convertKeysToKebabCase(element);
                });
            }
        }

        function tranformSource(sourceStr) {
            // console.log("Start:" + sourceStr)
            const output = sourceStr
                .replace(/[`']/g, '')
                .replace(/,/g, ';')
                .replace(/\${([^}]+)}/g, '$1')
                .replace(/\[theme\.fn\.smallerThan\((\w+)\)\]:/g, '@media (max-width: var(--mantine-spacing-$1))')
                .replace(/\[theme\.fn\.largerThan\((\w+)\)\]:/g, '@media (min-width: var(--mantine-spacing-$1))')
                .replace(/\.\.\.theme\.fn\.hover\(/g, '@mixin hover')
                .replace(/}\),?/g, '}')
                .replace(/}\s*;/g, '}')
                .replace(/theme\.([a-zA-Z0-9.]+)\[(\d+)\]/g, (_, properties, index) => {
                    const propsArray = properties.split('.').join('-');
                    return `var(--mantine-${propsArray}-${index})`;
                })
                .replace(/theme\.([a-zA-Z0-9.]+)/g, (_, properties) => {
                    const propsArray = properties.split('.').join('-');
                    return `var(--mantine-${propsArray})`;
                })
                .replace(/var\(--mantine-colorScheme\) === dark \? (\S+) : ([^\s;]+)/g, 'light-dark($2, $1)')
            // console.log("end:" + output);
            return output;
        }

        j(stylesObject).find(j.ObjectExpression).forEach(stylePath => {
            if (stylePath.parentPath.value.type === 'ArrowFunctionExpression') {
                // console.log("Obj: ", stylePath)
                const styleObject = stylePath.node;
                convertKeysToKebabCase(styleObject);
                styleObject.properties.forEach(prop => {
                    if (prop && prop.key) {
                        const key = _.kebabCase(prop.key.name || prop.key.value);
                        const value = tranformSource(j(prop.value).toSource())
                        // console.log("Prop: ", key, value)
                        cssContent += `.${key} ${value} \n`;
                    }
                });
            }
        });

        // Generate CSS Module file
        const cssFileName = `${fileInfo.path.replace(/\.(js|jsx|ts|tsx)$/, '')}.module.css`;
        fs.writeFileSync(cssFileName, cssContent, 'utf-8');

        // Replace createStyles call with import of CSS Module
        const importDeclaration = j.importDeclaration(
            [j.importDefaultSpecifier(j.identifier('classes'))],
            j.literal('./' + path.basename(cssFileName))
        );

        // Find position to insert import after React import
        let insertPosition = 0;
        root.find(j.ImportDeclaration).forEach((path, index) => {
            if (path.node.source.value === 'react') {
                insertPosition = index + 1;
            }
        });

        // Insert the import at the beginning of the file
        root.find(j.Program).get('body', insertPosition).insertBefore(importDeclaration);

        // Remove the createStyles call
        // j(path).remove();

        // Remove useStyles and its usage
        root.find(j.VariableDeclaration).forEach(pathx => {
            const declarations = pathx.node.declarations;
            if (declarations.length === 1 && declarations[0].id.name === 'useStyles') {
                j(pathx).remove();
            }
        });

        root.find(j.VariableDeclarator, {
            id: { type: 'ObjectPattern' },
        }).forEach(path => {
            if (path.node.id.properties.some(prop => prop.key.name === 'classes' || prop.key.name === 'cx')) {
                j(path.parent).remove();
            }
        });

    });

    return root.toSource({ 'quote': 'single' });
};
