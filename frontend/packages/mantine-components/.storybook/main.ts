/** @type { import('@storybook/nextjs').StorybookConfig } */
const config = {
    stories: ['../stories/**/*.mdx', '../**/*.stories.@(js|jsx|ts|tsx)'],
    addons: [
        '@storybook/addon-links',
        '@storybook/addon-essentials',
        '@storybook/addon-interactions',
        '@storybook/addon-styling-webpack',
        'storybook-dark-mode'
    ],
    framework: {
        name: '@storybook/nextjs',
        options: {}
    },
    docs: {
        autodocs: 'tag'
    }
};
export default config;
