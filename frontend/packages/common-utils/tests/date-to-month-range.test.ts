import { dateToMonthRange } from '../utils/date-period-utils';

describe('monthStringToDate', () => {
    it('should return the correct month range for a date in January', () => {
        const anyDate = new Date(2024, 0, 15); // January 15, 2024
        const expectedRange = [new Date(2024, 0, 1), new Date(2024, 1, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for a date in February', () => {
        const anyDate = new Date(2024, 1, 20); // February 20, 2024
        const expectedRange = [new Date(2024, 1, 1), new Date(2024, 2, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for the first day of a month', () => {
        const anyDate = new Date(2024, 5, 1); // June 1, 2024
        const expectedRange = [new Date(2024, 5, 1), new Date(2024, 6, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for the last day of a month', () => {
        const anyDate = new Date(2024, 4, 30); // May 30, 2024
        const expectedRange = [new Date(2024, 4, 1), new Date(2024, 5, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for the last day of December', () => {
        const anyDate = new Date(2024, 11, 31); // December 31, 2024
        const expectedRange = [new Date(2024, 11, 1), new Date(2025, 0, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for a date with time', () => {
        const anyDate = new Date(2024, 5, 15, 4); // June 15, 2024, 4 AM
        const expectedRange = [new Date(2024, 5, 1), new Date(2024, 6, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for the first day of the year', () => {
        const anyDate = new Date(2024, 0, 1); // January 1, 2024
        const expectedRange = [new Date(2024, 0, 1), new Date(2024, 1, 0)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });

    it('should return the correct month range for the last day of the year', () => {
        const anyDate = new Date(2024, 11, 31); // December 31, 2024
        const expectedRange = [new Date(2024, 11, 1), new Date(2024, 11, 31)];
        expect(dateToMonthRange(anyDate)).toEqual(expectedRange);
    });
});
