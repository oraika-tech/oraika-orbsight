import { monthStringToDate } from '../utils/date-period-utils';

describe('monthStringToDate', () => {
    // Test for valid input patterns
    it('converts "MMM-yyyy" format correctly', () => {
        expect(monthStringToDate('Jan-2024')).toEqual(new Date(2024, 0, 1));
    });

    it('converts "yyyy-MMM" format correctly', () => {
        expect(monthStringToDate('2024-Jan')).toEqual(new Date(2024, 0, 1));
    });

    // Test for leap year
    it('handles leap year correctly', () => {
        expect(monthStringToDate('Feb-2024')).toEqual(new Date(2024, 1, 1));
    });

    // Test for case insensitivity (optional, if your function is case-insensitive)
    it('is case-insensitive', () => {
        expect(monthStringToDate('feb-2024')).toEqual(new Date(2024, 1, 1));
    });

    // Test for invalid month
    it('returns null for invalid month', () => {
        expect(monthStringToDate('Abc-2024')).toBeNull();
    });

    // Test for invalid year
    it('returns null for invalid year', () => {
        expect(monthStringToDate('Jan-20AB')).toBeNull();
    });

    // Test for incorrect format
    it('returns null for incorrect format', () => {
        expect(monthStringToDate('2024/Jan')).toBeNull();
    });

    // Test for edge cases - beginning and end of year
    it('handles beginning of year', () => {
        expect(monthStringToDate('Jan-2024')).toEqual(new Date(2024, 0, 1));
    });

    it('handles end of year', () => {
        expect(monthStringToDate('Dec-2024')).toEqual(new Date(2024, 11, 1));
    });
});
