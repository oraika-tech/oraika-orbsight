export function emToPx(em: string) {
    return parseInt(em, 10) * 16;
}

export function toPascalCase(str: string) {
    return str.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

export function getUndefForAll(str: string) {
    return str === 'all' ? undefined : str;
}

export function cleanObject(obj: object) {
    return Object.fromEntries(Object.entries(obj).filter(([_, v]) => v !== undefined && v !== null));
}

export function removeNulls(obj: object) {
    Object.keys(obj).forEach(key => obj[key] == null && delete obj[key]);
}
