import { MantineTheme, MantineThemeOverride } from '@mantine/core';

export function getGrayBgShade(theme: MantineTheme) {
    return theme.colors.gray[theme.colorScheme === 'dark' ? 9 : 1];
}

export function getPrimaryFontShade(theme: MantineTheme) {
    return theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 3 : 7];
}

export function getSecondaryFontShade(theme: MantineTheme) {
    return theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 2 : 4];
}

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
                fontWeight: 800,
                fontSize: '3rem'
            },
            h2: {
                fontWeight: 600,
                fontSize: '2.25rem'
            },
            h3: {
                fontWeight: 500,
                fontSize: '1.5rem'
            }
        }
    },

    components: {
        Title: {
            styles: (theme) => ({
                root: {
                    // '&:is(h1)': {
                    //     color: getPrimaryFontShade(theme),
                    //     [`@media (max-width: ${theme.breakpoints.xs})`]: {
                    //         fontSize: 32
                    //     }
                    // },
                    '&:is(h2)': {
                        color: getPrimaryFontShade(theme),
                        [`@media (max-width: ${theme.breakpoints.xs})`]: {
                            fontSize: 24
                        }
                    },
                    '&:is(h3)': {
                        color: getSecondaryFontShade(theme),
                        [`@media (max-width: ${theme.breakpoints.xs})`]: {
                            fontSize: 20
                        }
                    }
                }
            })
        },
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
        Link: {
            styles: (theme) => ({
                root: {
                    textDecoration: 'none',
                    color: theme.colorScheme === 'dark' ? theme.colors.dark[1] : theme.colors.gray[7],
                    '&:hover': {
                        backgroundColor:
                            theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0]
                    }
                }
            })
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
