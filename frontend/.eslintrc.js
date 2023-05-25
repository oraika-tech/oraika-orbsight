module.exports = {
    extends: [
        'mantine',
        'plugin:@next/next/recommended',
        'plugin:jest/recommended',
        'plugin:storybook/recommended',
    ],
    plugins: ['testing-library', 'jest'],
    overrides: [
        {
            files: ['**/?(*.)+(spec|test).[jt]s?(x)'],
            extends: ['plugin:testing-library/react'],
        },
    ],
    parserOptions: {
        project: './tsconfig.json',
    },
    rules: {
        'no-restricted-syntax': 'off',
        'no-else-return': 'off',
        'react/jsx-indent-props': ['error', 4],
        'react/react-in-jsx-scope': 'off',
        'comma-dangle': ['error', 'never'],
        'max-len': ['error', 120]
    }
};
