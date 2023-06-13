import { getLastPartOfUrl } from '../utils/common';

describe('getLastPartOfUrl', () => {
    test('should return the last part of the URL', () => {
        const url = 'https://www.example.com/path/to/page';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('page');
    });

    test('should return an empty string when no path after domain with slash', () => {
        const url = 'https://www.example.com/';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('');
    });

    test('should return an empty string when no path after domain even without slash', () => {
        const url = 'https://www.example.com';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('');
    });

    test('should return last part of path string when URL ends with a trailing slash', () => {
        const url = 'https://www.example.com/path/to/';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('to');
    });

    test('should return the last part of the URL when it starts with a slash', () => {
        const url = '/path/to/page';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('page');
    });

    test('should return the URL itself when it does not contain slashes', () => {
        const url = 'page';
        const result = getLastPartOfUrl(url);
        expect(result).toBe('page');
    });
});
