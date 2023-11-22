import { Box, MantineProvider, Text, Title } from '@mantine/core';
import '@mantine/core/styles.css';
import { MDXProvider } from '@mdx-js/react';
import { MDXComponents } from '@mdx-js/react/lib';
import { googleAnalyticsScript } from 'common-utils/scripts/google-analytics';
import { mixPanelSetup } from 'common-utils/scripts/mixpanel';
import { clarityScript } from 'common-utils/scripts/ms-clarity';
import { sentrySetup } from 'common-utils/scripts/sentry';
import { getCookie } from 'cookies-next';
import { TawkMessenger } from 'headless-components/comm/TawkMessenger';
import AuthProvider from 'mantine-components/components/Auth/AuthProvider';
import NextApp, { AppContext, AppProps } from 'next/app';
import Head from 'next/head';
import Script from 'next/script';
import { getLoginUrl } from '../business-logic/login/loginUtility';
import { globalTheme } from '../business-logic/theme/theme';
import '../global.css';
import classes from './_app.module.css';

export default function App(props: AppProps) {
    const { Component, pageProps } = props;

    const components: MDXComponents = {
        h1: ({ children }) => <Title ta="center" className={classes.heading1} order={1}>{children}</Title>,
        h2: ({ children }) => <Title className={classes.heading2} order={2}>{children}</Title>,
        h3: ({ children }) => <Title className={classes.heading3} order={3}>{children}</Title>,
        p: ({ children }) => <Text className={classes.text} fz="md" ta="justify">{children}</Text>,
        ul: ({ children }) => <ul className={classes.list}>{children}</ul>
    };

    sentrySetup();
    mixPanelSetup();

    return (
        <MantineProvider theme={{ ...globalTheme }}>
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
                    <Script
                        async
                        src={`https://www.googletagmanager.com/gtag/js?id=${process.env.NEXT_PUBLIC_GA_ID}`}
                    />
                }
                {process.env.NEXT_PUBLIC_GA_ID &&
                    <Script id="google-analytics"> {googleAnalyticsScript} </Script>
                }

                {process.env.NEXT_PUBLIC_CLARITY_PROJECT_ID &&
                    <Script id="clarity-tracking"> {clarityScript} </Script>
                }

                <MDXProvider components={components}>
                    <AuthProvider loginUrl={getLoginUrl()}>
                        <Component {...pageProps} />
                    </AuthProvider>
                </MDXProvider>

                {
                    process.env.NEXT_PUBLIC_TAWK_WIDGET_ID &&
                    <TawkMessenger
                        propertyId={process.env.NEXT_PUBLIC_TAWK_PROPERTY_ID}
                        widgetId={process.env.NEXT_PUBLIC_TAWK_WIDGET_ID}
                    />
                }

            </Box>
        </MantineProvider>
    );
}

App.getInitialProps = async (appContext: AppContext) => {
    const appProps = await NextApp.getInitialProps(appContext);
    return {
        ...appProps,
        colorScheme: getCookie('mantine-color-scheme', appContext.ctx) || 'light'
    };
};
