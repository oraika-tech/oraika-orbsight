export function getUrlRoot() {
    return `${process.env.NEXT_PUBLIC_BE_API_URL}/api/v1`;
}

const logoPath = 'https://cdn.jsdelivr.net/gh/obsei/obsei-resources/logos/';
const observerTypeIcons: Record<string, string> = {
    Twitter: 'twitter.png',
    Android: 'playstore.png',
    iOS: 'appstore.png',
    GoogleMaps: 'google_maps.png',
    Facebook: 'facebook.png',
    Reddit: 'reddit.png',
    GoogleNews: 'googlenews.png'
};
const placeholderPath = 'https://cdn.jsdelivr.net/gh/obsei/Banks-in-India/Icons/bi-Placeholder.png';
export function getLogoFromObserverType(observerType: string) {
    const iconFile = observerTypeIcons[observerType];
    return iconFile ? logoPath + iconFile : placeholderPath;
}

export function getLastPartOfUrl(rawUrl: string): string {
    const url = rawUrl.endsWith('/') ? rawUrl.slice(0, -1) : rawUrl;
    const parts = url.split('/');
    return parts[parts.length - 1];
}
