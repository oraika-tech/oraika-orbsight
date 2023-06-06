export function getLoginUrl(): string {
    return process.env.NEXT_PUBLIC_DEMO_MODE === 'true'
        ? process.env.NEXT_PUBLIC_DEMO_LOGIN_URL
        : process.env.NEXT_PUBLIC_LOGIN_URL;
}
