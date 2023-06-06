import Router from 'next/router';
import { getLoginUrl } from '../../../apps/orb/business-logic/login/loginUtility';

export function sleep(ms: number) {
    return new Promise(resolve => {
        setTimeout(resolve, ms);
    });
}

const defaultHeaders: Record<string, string> = {
    accept: 'application/json',
    'Content-Type': 'application/json'
};

function addHeaderIfMissing(request: RequestInit, field: string, value: string): RequestInit {
    if (request.headers instanceof Headers) {
        if (!request.headers.has(field)) {
            request.headers.set(field, value);
        }
    } else if (request.headers && typeof request.headers === 'object') {
        if (!(request.headers as Record<string, string>)[field]) {
            // Convert headers from object literal to Headers
            const headers = new Headers(request.headers);
            headers.set(field, value);
            request.headers = headers;
        }
    }
    return request;
}

function setDefaultHeaders(request: RequestInit) {
    request.headers = request.headers || {};
    Object.entries(defaultHeaders).forEach(([field, value]) => {
        addHeaderIfMissing(request, field, value);
    });
}

export async function restApi(url: string, request?: RequestInit) {
    const requestObj = request || {};
    requestObj.credentials = 'include';
    setDefaultHeaders(requestObj);
    // console.log('requestObj:', JSON.stringify(requestObj));
    return fetch(url, requestObj)
        .then(response => {
            if (response.status === 401 || response.status === 403) {
                Router.push(getLoginUrl() || '/login');
                throw new Error('Unauthorized');
            } else if (!response.ok) {
                response.json()
                    .then((rj: any) => {
                        console.log('Response: ', JSON.stringify(rj));
                    });
                throw new Error('API failed');
            }
            return (response.status === 204) ? null : response.json();
        });
}

export function getCurrentDate() {
    return new Date();
}

export function getCurrentEpochMs() {
    return getCurrentDate().getTime();
}

export function getCurrentNDays(nDays: number) {
    const date = getCurrentDate();
    date.setDate(date.getDate() + nDays);
    return date;
}

export function getCurrentMinusNDays(nDays: number) {
    return getCurrentNDays(-1 * nDays);
}
export function getDateFromString(data_string: string) {
    if (data_string.endsWith('d')) {
        return getCurrentNDays(parseInt(data_string.replace('d$', ''), 10));
    }
    return new Date(data_string);
}

export function getTitleWord(word: string) {
    if (word && word.length > 0) {
        return word.charAt(0).toUpperCase() + word.slice(1);
    }
    return word;
}

export function getTitleSentance(sentance: string) {
    return sentance.split(' ').map(word => getTitleWord(word)).join(' ');
}

export function arrayEquals<T>(a: T[], b: T[]) {
    return Array.isArray(a) &&
        Array.isArray(b) &&
        a.length === b.length &&
        a.every((val, index) => val === b[index]);
}

export function shallowEqual(object1: any, object2: any): boolean {
    if (object1 instanceof Date) {
        return object1.getTime() === object2.getTime();
    }
    const keys1 = Object.keys(object1);
    const keys2 = Object.keys(object2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    for (let i = 0; i < keys1.length; i += 1) {
        const key = keys1[i];
        if (!keys2.includes(key) || object1[key] !== object2[key]) {
            return false;
        }
    }

    return true;
}

function isObject(object: any): boolean {
    return object != null && typeof object === 'object';
}

export function deepEqual(object1: any, object2: any): boolean {
    const keys1 = Object.keys(object1);
    const keys2 = Object.keys(object2);

    if (keys1.length !== keys2.length) {
        return false;
    }

    let isEqual = true;

    keys1.forEach((key) => {
        const val1 = object1[key];
        const val2 = object2[key];
        const areObjects = isObject(val1) && isObject(val2);

        if (
            (areObjects && !deepEqual(val1, val2)) ||
            (!areObjects && val1 !== val2)
        ) {
            isEqual = false;
        }
    });

    return isEqual;
}

export function capitalizeFirstLetter(word: string) {
    return word.charAt(0).toUpperCase() + word.slice(1);
}

export function roundDecimal(num: number, places: number) {
    const placeValue = 10 ** places;
    return Math.round(num * placeValue + Number.EPSILON) / placeValue;
}

export function emailValidation(email: string) {
    if (!email || email.length === 0) {
        return true;
    }
    const emailParts = email.split('@');
    if (emailParts.length !== 2) {
        return false;
    }
    const domainParts = emailParts[1].split('.');
    if (domainParts.length < 2) {
        return false;
    }
    const superDomainLength = domainParts[domainParts.length - 1].length;
    return superDomainLength >= 2 && superDomainLength <= 3;
}

export function getRandomNumber(digits: number) {
    let rum = Math.random();
    let digitsLeft = digits;
    while (digitsLeft > 0) {
        const initialNum = rum;
        rum *= 10;
        if (Math.trunc(initialNum) !== Math.trunc(rum)) {
            digitsLeft -= 1;
        }
    }
    return Math.trunc(rum);
}
