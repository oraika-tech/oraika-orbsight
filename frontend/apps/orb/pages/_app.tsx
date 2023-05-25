import { Box, ColorScheme, ColorSchemeProvider, createStyles, MantineProvider, Text, Title } from '@mantine/core';
import { MDXProvider } from '@mdx-js/react';
import { Components } from '@mdx-js/react/lib';
import { googleAnalyticsScript } from 'common-utils/scripts/google-analytics';
import { mixPanelSetup } from 'common-utils/scripts/mixpanel';
import { clarityScript } from 'common-utils/scripts/ms-clarity';
import { sentrySetup } from 'common-utils/scripts/sentry';
import { getCookie, setCookie } from 'cookies-next';
import { TawkMessenger } from 'headless-components/comm/TawkMessenger';
import NextApp, { AppContext, AppProps } from 'next/app';
import Head from 'next/head';
import Script from 'next/script';
import { useState } from 'react';
import { globalTheme } from '../business-logic/theme/theme';
import UserInfoProvider from '../business-logic/user-info/UserInfoProvider';


const useStyles = createStyles((theme) => ({
    heading1: {
        alignItems: 'center',
        color: theme.colors[theme.primaryColor][theme.colorScheme === 'dark' ? 4 : 6],
        paddingBottom: 30
    },
    heading2: {
        paddingTop: '1rem',
        paddingBottom: '0.3rem'
    },
    heading3: {
        paddingTop: '1rem',
        paddingBottom: '0.1rem'
    },
    text: {
        hyphens: 'auto'
    },
    list: {
        marginTop: '0.2rem'
    }
}));

export default function App(props: AppProps & { colorScheme: ColorScheme }) {
    const { classes } = useStyles();
    const { Component, pageProps } = props;
    const [colorScheme, setColorScheme] = useState<ColorScheme>(props.colorScheme);

    const toggleColorScheme = (value?: ColorScheme) => {
        const nextColorScheme = value || (colorScheme === 'dark' ? 'light' : 'dark');
        setColorScheme(nextColorScheme);
        setCookie('mantine-color-scheme', nextColorScheme, { maxAge: 60 * 60 * 24 * 30 });
    };

    const components: Components = {
        h1: ({ children }) => <Title align="center" className={classes.heading1} order={1}>{children}</Title>,
        h2: ({ children }) => <Title className={classes.heading2} order={2}>{children}</Title>,
        h3: ({ children }) => <Title className={classes.heading3} order={3}>{children}</Title>,
        p: ({ children }) => <Text className={classes.text} fz="md" align="justify">{children}</Text>,
        ul: ({ children }) => <ul className={classes.list}>{children}</ul>
    };

    sentrySetup();
    mixPanelSetup();

    return (
        <Box>
            <Head>
                <title>Orbsight</title>
                <meta
                    name="viewport"
                    content="minimum-scale=1, initial-scale=1, width=device-width"
                />
                <link rel="shortcut icon" href="/favicon.png" />

                <meta name="twitter:title" content="Orbsight" />
                <meta
                    name="google-site-verification"
                    content="JQGIVVDWGeihwo5GRrGZkhx3DUc8rMy9FaV0_qQecGM"
                />
                <meta
                    name="description"
                    // eslint-disable-next-line max-len
                    content="Unlock the potential of your technical infrastructure with our expert team
                    Optimize performance, reduce costs, and achieve success"
                />
            </Head>

            {process.env.NEXT_PUBLIC_GA_ID &&
                <Script async src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`} />
            }
            {process.env.NEXT_PUBLIC_GA_ID &&
                <Script id="google-analytics"> {googleAnalyticsScript} </Script>
            }

            {process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID &&
                <Script id="clarity-tracking"> {clarityScript} </Script>
            }

            <ColorSchemeProvider colorScheme={colorScheme} toggleColorScheme={toggleColorScheme}>
                <MantineProvider
                    theme={{ ...globalTheme, colorScheme }}
                    withGlobalStyles
                    withNormalizeCSS
                >
                    <UserInfoProvider>
                        <MDXProvider components={components}>
                            <Component {...pageProps} />
                        </MDXProvider>
                    </UserInfoProvider>
                </MantineProvider>
            </ColorSchemeProvider>

            {process.env.NEXT_PUBLIC_TAWK_WIDGET_ID &&
                <TawkMessenger
                    propertyId={process.env.NEXT_PUBLIC_TAWK_PROPERTY_ID}
                    widgetId={process.env.NEXT_PUBLIC_TAWK_WIDGET_ID}
                />
            }

        </Box>
    );
}

App.getInitialProps = async (appContext: AppContext) => {
    const appProps = await NextApp.getInitialProps(appContext);
    return {
        ...appProps,
        colorScheme: getCookie('mantine-color-scheme', appContext.ctx) || 'light'
    };
};
