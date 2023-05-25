import * as Sentry from '@sentry/react';
import { BrowserTracing } from '@sentry/tracing';

export function sentrySetup() {
    const enabled = process.env.NEXT_PUBLIC_SENTRY_ENABLED === 'true';
    const dsn = process.env.NEXT_PUBLIC_SENTRY_DSN;

    if (enabled) {
        Sentry.init({
            dsn,
            integrations: [new BrowserTracing()],

            // Set tracesSampleRate to 1.0 to capture 100%
            // of transactions for performance monitoring.
            // We recommend adjusting this value in production
            tracesSampleRate: 1.0
        });
    }
}

export function setSentryUser(email: string) {
    Sentry.setUser({ email });
}
