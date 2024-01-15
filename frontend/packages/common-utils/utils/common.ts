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
    GoogleNews: 'googlenews.png',
    GoogleSearch: 'google.png'
};
const placeholderPath = 'https://cdn.jsdelivr.net/gh/obsei/Banks-in-India/Icons/bi-Placeholder.png';
export function getLogoFromObserverType(observerType: string) {
    const iconFile = observerTypeIcons[observerType];
    return iconFile ? logoPath + iconFile : placeholderPath;
}

export function getLastPartOfUrl(rawUrl: string): string {
    if (!rawUrl.includes('/')) {
        return rawUrl;
    }
    const url = new URL(rawUrl.includes('://') ? rawUrl : `http://${rawUrl}`);
    const path = url.pathname.endsWith('/') ? url.pathname.slice(0, -1) : url.pathname;
    const parts = path.split('/');
    return parts[parts.length - 1];
}

export function getCurrentDateTimeFormatted() {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export function capitalizeFirstLetter(word: string) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export function wrapSentence(sentence: string, lineCharacterCount: number): string[] {
    if (lineCharacterCount < 1) {
        throw new Error('lineCharacterCount must be at least 1');
    }

    const words = sentence.split(/\s+/);
    const lines: string[] = [];
    let currentLine = words[0];

    for (let i = 1; i < words.length; i += 1) {
        if (currentLine.length + words[i].length + 1 <= lineCharacterCount) {
            currentLine += ` ${words[i]}`;
        } else {
            lines.push(currentLine);
            currentLine = words[i];
        }
    }

    lines.push(currentLine);
    return lines;
}
