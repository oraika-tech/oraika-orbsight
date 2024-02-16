import { getStartOfDay } from '../utils/date-period-utils';

describe('getStartOfDay', () => {
    it('should return the start of the day for a given date', () => {
        const testDate = new Date('2024-02-15T12:34:56');
        const expectedResult = new Date('2024-02-15T00:00:00');
        const result = getStartOfDay(testDate);

        expect(result).toEqual(expectedResult);
    });

    it('should handle the end of a day', () => {
        const testDate = new Date('2024-02-15T23:59:59');
        const expectedResult = new Date('2024-02-15T00:00:00');
        const result = getStartOfDay(testDate);

        expect(result).toEqual(expectedResult);
    });
});
