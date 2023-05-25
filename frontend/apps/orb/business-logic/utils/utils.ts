export function emToPx(em: string) {
    return parseInt(em, 10) * 16;
}

export function toPascalCase(str: string) {
    return str.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

export function getUndefForAll(str: string) {
    return str === 'all' ? undefined : str;
}
