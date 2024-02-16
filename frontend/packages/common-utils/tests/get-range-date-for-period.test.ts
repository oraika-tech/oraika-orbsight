import { DatePeriod, getRangeDateForPeriod } from '../utils/date-period-utils';

describe('getRangeDateForPeriod', () => {
    const today = new Date(2024, 0, 15); // Choose a specific date for consistency
    /**
     * today
     * yesterday
     * this-week
     * this-month
     * last-7-days
     * last-30-days
     * last-week
     * last-month
     * this-year
     * last-year
     */
    it('returns today\'s range for `today`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 15, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('today', today)).toEqual(expected);
    });
    it('returns yesterday\'s range for `yesterday`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 14, 0, 0, 0),
            end: new Date(2024, 0, 14, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('yesterday', today)).toEqual(expected);
    });
    it('returns this week\'s range for `this-week`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 14, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('this-week', today)).toEqual(expected);
    });
    it('returns this month\'s range for `this-month`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 1, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('this-month', today)).toEqual(expected);
    });
    it('returns last 7 day\'s range for `last-7-days`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 8, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('last-7-days', today)).toEqual(expected);
    });
    it('returns last 30 day\'s range for `last-30-days`', () => {
        const expected: DatePeriod = {
            start: new Date(2023, 11, 16, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('last-30-days', today)).toEqual(expected);
    });
    it('returns last week\'s range for `last-week`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 7, 0, 0, 0),
            end: new Date(2024, 0, 13, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('last-week', today)).toEqual(expected);
    });
    it('returns last month\'s range for `last-month`', () => {
        const expected: DatePeriod = {
            start: new Date(2023, 11, 1, 0, 0, 0),
            end: new Date(2023, 11, 31, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('last-month', today)).toEqual(expected);
    });
    it('returns this year range for `this-year`', () => {
        const expected: DatePeriod = {
            start: new Date(2024, 0, 1, 0, 0, 0),
            end: new Date(2024, 0, 15, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('this-year', today)).toEqual(expected);
    });
    it('returns last year range for `last-year`', () => {
        const expected: DatePeriod = {
            start: new Date(2023, 0, 1, 0, 0, 0),
            end: new Date(2023, 11, 31, 23, 59, 59)
        };
        expect(getRangeDateForPeriod('last-year', today)).toEqual(expected);
    });
    it('throws an error for invalid `value`', () => {
        expect(() => getRangeDateForPeriod('invalid-period', today)).toThrow(
            'Invalid period value: invalid-period'
        );
    });
});
