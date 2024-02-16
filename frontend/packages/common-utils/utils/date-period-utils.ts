export interface DatePeriod {
    start?: Date
    end?: Date
}

export function getStartOfDay(day: Date) {
    const dayDate = new Date(day);
    dayDate.setHours(0);
    dayDate.setMinutes(0);
    dayDate.setSeconds(0);
    dayDate.setMilliseconds(0);
    return dayDate;
}

export function getEndOfDay(day: Date) {
    const dayDate = new Date(day);
    dayDate.setHours(23);
    dayDate.setMinutes(59);
    dayDate.setSeconds(59);
    dayDate.setMilliseconds(0);
    return dayDate;
}

export function rangeInRange(insideRange: DatePeriod, outsideRange: DatePeriod): boolean {
    // ouside start is bounded but inside start is unbounded
    if (outsideRange.start && !insideRange.start) {
        return false;
    }

    // ouside end is bounded but inside end is unbounded
    if (outsideRange.end && !insideRange.end) {
        return false;
    }

    // inside starts before outside
    if (insideRange.start && outsideRange.start && insideRange.start < outsideRange.start) {
        return false;
    }

    // inside ends after outside
    if (insideRange.end && outsideRange.end && outsideRange.end < insideRange.end) {
        return false;
    }

    return true;
}

export function getRangeDateForPeriod(value: string, today: Date = new Date()): DatePeriod {
    // E.g  'last-7-days' => [Date('2024-03-05 00:00:00'), Date('2024-03-11 23:59:59')]
    if (!today) {
        today = new Date();
    }

    switch (value) {
        case 'today':
            return {
                start: getStartOfDay(today),
                end: getEndOfDay(today)
            };

        case 'yesterday': {
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            return {
                start: getStartOfDay(yesterday),
                end: getEndOfDay(yesterday)
            };
        }
        case 'this-week': {
            const startOfWeek = new Date(today);
            startOfWeek.setDate(startOfWeek.getDate() - startOfWeek.getDay());
            return {
                start: getStartOfDay(startOfWeek),
                end: getEndOfDay(today)
            };
        }
        case 'this-month': {
            const thisMonth = new Date(today.getFullYear(), today.getMonth(), 1);
            return {
                start: getStartOfDay(thisMonth),
                end: getEndOfDay(today)
            };
        }
        case 'last-7-days': {
            const sevenDaysAgo = new Date(today);
            sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7);
            return {
                start: getStartOfDay(sevenDaysAgo),
                end: getEndOfDay(today)
            };
        }
        case 'last-30-days': {
            const thirtyDaysAgo = new Date(today);
            thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);
            return {
                start: getStartOfDay(thirtyDaysAgo),
                end: getEndOfDay(today)
            };
        }
        case 'last-week': {
            const lastWeekStart = new Date(today);
            lastWeekStart.setDate(lastWeekStart.getDate() - (lastWeekStart.getDay() + 7));
            const lastWeekEnd = new Date(lastWeekStart);
            lastWeekEnd.setDate(lastWeekEnd.getDate() + 6);
            return {
                start: getStartOfDay(lastWeekStart),
                end: getEndOfDay(lastWeekEnd)
            };
        }
        case 'last-month': {
            const lastMonthStart = new Date(today.getFullYear(), today.getMonth() - 1, 1);
            const lastMonthEnd = new Date(today.getFullYear(), today.getMonth(), 0); // '0' date - prev month last day
            return {
                start: getStartOfDay(lastMonthStart),
                end: getEndOfDay(lastMonthEnd)
            };
        }
        case 'this-year': {
            const thisYearStart = new Date(today.getFullYear(), 0, 1);
            return {
                start: getStartOfDay(thisYearStart),
                end: getEndOfDay(today)
            };
        }
        case 'last-year': {
            const lastYearStart = new Date(today.getFullYear() - 1, 0, 1);
            const lastYearEnd = new Date(today.getFullYear(), 0, 0);
            return {
                start: getStartOfDay(lastYearStart),
                end: getEndOfDay(lastYearEnd)
            };
        }
        default:
            throw new Error(`Invalid period value: ${value}`);
    }
}

export function monthStringToDate(input: string): Date | null {
    // convert following pattern to date: MMM-yyyy, yyyy-MMM
    // E.g  '2024-Jan' => Date(2024, 0, 1)

    // Sanity test
    if (!/^[A-Za-z]{3}-[1-2][09][0-9][0-9]$/.test(input) &&
        !/^[1-2][09][0-9][0-9]-[A-Za-z]{3}$/.test(input)) {
        return null;
    }

    const parts = input.split(/-|\s/);
    const yearIndex = parts[0].length === 4 ? 0 : 1;
    const monthIndex = parts[0].length === 3 ? 0 : 1;

    const dateString = [parts[yearIndex], parts[monthIndex], '01'].join('-');

    const dateObj = new Date(dateString);
    return Number.isNaN(dateObj.getTime()) ? null : dateObj;
}

export function dateToMonthRange(anyDate: Date): [Date, Date] {
    const firstDateOfMonth = new Date(anyDate.getFullYear(), anyDate.getMonth(), 1);
    const lastDateOfMonth = new Date(anyDate.getFullYear(), anyDate.getMonth() + 1, 0);
    return [firstDateOfMonth, lastDateOfMonth];
}

export function dateToString(date: Date): string {
    const year = date.getFullYear().toString();
    const month = (date.getMonth() + 1).toString().padStart(2, '0'); // Ensure two-digit month
    const day = date.getDate().toString().padStart(2, '0'); // Ensure two-digit day

    return `${year}-${month}-${day}`;
}

export function dateRangeToStringRange(range: [Date, Date]): string[] {
    return range.map(dateToString);
}
