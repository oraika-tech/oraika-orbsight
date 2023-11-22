import { MantineThemeOverride } from '@mantine/core';

export const globalTheme: MantineThemeOverride = {
    colors: {
        purple: [
            '#f0e4ff',
            '#ccb2ff',
            '#aa80ff',
            '#884dff',
            '#661bfe',
            '#4d02e5',
            '#3c00b3',
            '#2b0081',
            '#19004f',
            '#0a001f'
        ],
        bluex: [
            '#e7f5ff',
            '#d0ebff',
            '#a5d8ff',
            '#23baff', // light shade
            '#4dabf7',
            '#339af0',
            '#228be6',
            '#004aad', // dark shade
            '#1971c2',
            '#1864ab'
        ]
    },
    primaryColor: 'bluex',
    primaryShade: { light: 7, dark: 3 },

    headings: {
        sizes: {
            h1: {
                fontWeight: '800px',
                fontSize: '3rem'
            },
            h2: {
                fontWeight: '600px',
                fontSize: '2.25rem'
            },
            h3: {
                fontWeight: '500px',
                fontSize: '1.5rem'
            }
        }
    },

    components: {
        Button: {
            defaultProps: {
                radius: 'xl'
            }
        },
        Image: {
            defaultProps: {
                width: '100%'
            }
        },
        ActionIcon: {
            defaultProps: {
                variant: 'transparent'
            }
        },
        ThemeIcon: {
            defaultProps: {
                variant: 'transparent'
            }
        },
        Paper: {
            defaultProps: {
                shadow: 'xs',
                radius: 'md',
                p: 'sm'
            }
        },
        Card: {
            defaultProps: {
                shadow: 'xs',
                radius: 'md',
                padding: 'sm'
            }
        }
    }
};
