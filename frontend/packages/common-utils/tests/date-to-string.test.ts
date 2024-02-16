import { dateToString } from '../utils/date-period-utils';

describe('dateToString function', () => {
    it('should format date in yyyy-MM-dd format for current date', () => {
        const currentDate = new Date();
        const formattedDate = dateToString(currentDate);

        const expected = currentDate.toISOString().slice(0, 10); // Extract yyyy-MM-dd

        expect(formattedDate).toEqual(expected);
    });

    it('should handle single-digit month and day', () => {
        const date = new Date(2024, 0, 5); // January 5th, 2024
        const formattedDate = dateToString(date);

        expect(formattedDate).toEqual('2024-01-05');
    });

    it('should handle double-digit month and day', () => {
        const date = new Date(2024, 10, 23); // November 23rd, 2024
        const formattedDate = dateToString(date);

        expect(formattedDate).toEqual('2024-11-23');
    });

    it('should handle leap year', () => {
        const date = new Date(2024, 1, 29); // February 29th, 2024 (leap year)
        const formattedDate = dateToString(date);

        expect(formattedDate).toEqual('2024-02-29');
    });

    it('should handle non-leap year', () => {
        const date = new Date(2023, 1, 28); // February 28th, 2023 (non-leap year)
        const formattedDate = dateToString(date);

        expect(formattedDate).toEqual('2023-02-28');
    });
});
