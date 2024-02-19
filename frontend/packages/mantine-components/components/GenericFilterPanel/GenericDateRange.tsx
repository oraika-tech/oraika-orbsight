import { ActionIcon, Flex, Menu, Select, Stack, Text, Tooltip } from '@mantine/core';
import { DatePickerInput, DateValue, DatesRangeValue, MonthPickerInput } from '@mantine/dates';
import '@mantine/dates/styles.css';
import { IconArrowAutofitContent, IconArrowAutofitLeft, IconCalendarMonth } from '@tabler/icons-react';
import { getRangeDateForPeriod, rangeInRange } from 'common-utils/utils/date-period-utils';
import { useState } from 'react';
import classes from './GenericDateRange.module.css';

export type DateRangeValue = Date | [Date, Date] | string | null;

export enum DateRangeType {
    PERIOD = 'PERIOD',
    MONTH = 'MONTH',
    CUSTOM = 'CUSTOM'
}

// function toDateRangeType(value: string) {
//     return DateRangeType[value as keyof typeof DateRangeType];
// }

export interface GenericDateRangeValue {
    rangeType: DateRangeType | undefined
    rangeValue: DateRangeValue
}

interface DateRangePeriod {
    start?: Date
    end?: Date
    period?: string
}

interface GenericDateRangeProps {
    label: string
    dateValue: GenericDateRangeValue
    allowedPeriod?: DateRangePeriod
    onChange: (v: GenericDateRangeValue) => void
}

function periodParsing(allowedPeriod: DateRangePeriod) {
    if (!allowedPeriod.start && allowedPeriod.period) {
        const todayDate = new Date();
        todayDate.setHours(0);
        todayDate.setMinutes(0);
        todayDate.setSeconds(0);
        if (allowedPeriod.period.endsWith('d')) {
            const days = parseInt(allowedPeriod.period.replace('d', ''), 10);
            todayDate.setDate(todayDate.getDate() - days);
        } else if (allowedPeriod.period.endsWith('M')) {
            const months = parseInt(allowedPeriod.period.replace('m', ''), 10);
            todayDate.setMonth(todayDate.getMonth() - months);
        } else if (allowedPeriod.period.endsWith('y')) {
            const years = parseInt(allowedPeriod.period.replace('y', ''), 10);
            todayDate.setFullYear(todayDate.getFullYear() - years);
        }
        allowedPeriod.start = todayDate;
    }

    if (!allowedPeriod.end) {
        allowedPeriod.end = new Date();
        allowedPeriod.end.setHours(23);
        allowedPeriod.end.setMinutes(59);
        allowedPeriod.end.setSeconds(59);
    }
}

export default function GenericDateRange({ label, dateValue, allowedPeriod, onChange }: GenericDateRangeProps) {
    const [rangeTypeState, setRangeTypeState] =
        useState<DateRangeType | null>(dateValue.rangeType || DateRangeType.PERIOD);
    const [rangeValueState, setRangeValueState] = useState<DateRangeValue>(dateValue.rangeValue);

    if (allowedPeriod) {
        periodParsing(allowedPeriod);
    }

    function periodSelectChange(value: string | null) {
        setRangeValueState(value);
        onChange({ rangeType: DateRangeType.PERIOD, rangeValue: value });
    }

    function monthPickerChange(value: DateValue) {
        setRangeValueState(value as Date);
        onChange({ rangeType: DateRangeType.MONTH, rangeValue: value });
    }

    function customDatePickerChange(value: DatesRangeValue) {
        setRangeValueState(value as [Date, Date]);
        if (value[0] && value[1]) {
            onChange({ rangeType: DateRangeType.CUSTOM, rangeValue: value as [Date, Date] });
        }
    }

    function getPeriodValue(): string | undefined {
        if (rangeValueState && typeof rangeValueState === 'string') {
            return rangeValueState;
        }
        return undefined;
    }

    function getMonthValue(): DateValue | undefined {
        if (rangeValueState && rangeValueState instanceof Date) {
            return new Date(rangeValueState.getFullYear(), rangeValueState.getMonth(), 1);
        }
        return undefined;
    }

    function getCustomDatePickerValue(): DatesRangeValue | undefined {
        if (rangeValueState && Array.isArray(rangeValueState) && rangeValueState.length === 2) {
            return rangeValueState as [Date, Date];
        }
        return undefined;
    }

    const rangeTypeIcons = {
        [DateRangeType.PERIOD]: <IconArrowAutofitLeft />,
        [DateRangeType.MONTH]: <IconCalendarMonth />,
        [DateRangeType.CUSTOM]: <IconArrowAutofitContent />
    };

    const periodValues = [
        {
            value: 'today',
            label: 'Today'
        },
        {
            value: 'yesterday',
            label: 'Yesterday'
        },
        {
            value: 'this-week',
            label: 'This Week'
        },
        {
            value: 'this-month',
            label: 'This Month'
        },
        {
            value: 'last-7-days',
            label: 'Last 7 Days'
        },
        {
            value: 'last-30-days',
            label: 'Last 30 Days'
        },
        {
            value: 'last-week',
            label: 'Last Week'
        },
        {
            value: 'last-month',
            label: 'Last Month'
        },
        {
            value: 'this-year',
            label: 'This Year'
        },
        {
            value: 'last-year',
            label: 'Last Year'
        }
    ];

    // limit choices based on provided range
    const allowedPeriodValues = allowedPeriod
        ? periodValues.filter((period) => {
            const periodRange = getRangeDateForPeriod(period.value);
            return rangeInRange(periodRange, allowedPeriod);
        })
        : periodValues;

    const minWidth = 220;

    let datePicker;
    switch (rangeTypeState) {
        case DateRangeType.PERIOD:
            datePicker = (
                <Select
                    id="RangeDate"
                    miw={minWidth}
                    data={allowedPeriodValues}
                    classNames={{ input: classes.rightElement }}
                    label=" "
                    placeholder="Select Period"
                    maxDropdownHeight={350}
                    value={getPeriodValue()}
                    onChange={periodSelectChange}
                />
            );
            break;
        case DateRangeType.MONTH:
            datePicker = (
                <MonthPickerInput
                    id="RangeMonth"
                    miw={minWidth}
                    classNames={{ input: classes.rightElement }}
                    label=" "
                    placeholder="Pick Month"
                    value={getMonthValue()}
                    onChange={monthPickerChange}
                    minDate={allowedPeriod?.start}
                    maxDate={allowedPeriod?.end}
                />
            );
            break;
        default: // CUSTOM
            datePicker = (
                <DatePickerInput
                    id="RangeCustom"
                    type="range"
                    miw={minWidth}
                    valueFormat="MMM DD, YYYY"
                    classNames={{ input: classes.rightElement }}
                    label=" "
                    placeholder="Pick Date Range"
                    allowSingleDateInRange
                    popoverProps={{ zIndex: 10000, withinPortal: true }}
                    value={getCustomDatePickerValue()}
                    onChange={customDatePickerChange}
                    minDate={allowedPeriod?.start}
                    maxDate={allowedPeriod?.end}
                />
            );
    }

    return (
        <Stack justify="flex-end">
            <Text size="sm" fw={500} h={8}> {label} </Text>
            <Flex
                h={36}
                align="flex-end"
                wrap="nowrap"
            >
                <Menu>
                    <Menu.Target>
                        <Tooltip label="Select Period Type">
                            <ActionIcon
                                size={36}
                                variant="default"
                                className={classes.leftElement}
                            >
                                {rangeTypeIcons[rangeTypeState || DateRangeType.PERIOD]}
                            </ActionIcon>
                        </Tooltip>
                    </Menu.Target>

                    <Menu.Dropdown>
                        {Object.values(DateRangeType).map((rangeType) =>
                            <Menu.Item
                                key={rangeType}
                                leftSection={rangeTypeIcons[rangeType]}
                                onClick={() => setRangeTypeState(rangeType)}
                            />
                        )}
                    </Menu.Dropdown>
                </Menu>
                {datePicker}
            </Flex>
        </Stack>
    );
}
