import { Button, Flex, Group, Select } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconFilter } from '@tabler/icons-react';
import { getDateFromString, getTitleSentance } from 'common-utils/utils';
import { dateRangeToStringRange, dateToMonthRange, monthStringToDate } from 'common-utils/utils/date-period-utils';
import GenericDateRange, { DateRangeType, GenericDateRangeValue } from './GenericDateRange';

export enum FilterFieldType {
    DATE = 'DATE',
    DATE_RANGE = 'DATE_RANGE',
    AUTO_COMPLETE = 'AUTO_COMPLETE'
}

export interface AutocompleteOption {
    id?: string
    code: string
    label?: string
}

export interface AutocompleteData {
    id: string
    label: string
    options: Array<AutocompleteOption>
}

// todo: make field mandatory
export interface FilterChangeEvent {
    name?: string
    oldValues?: string[]
    newValues?: string[]
}

export interface FilterData {
    id: string
    label: string
    minWidth?: number
    maxWidth?: number
    type: FilterFieldType
    selectedValue: AutocompleteOption | Date | string
    defaultValue: AutocompleteOption | Date | string | [string, string]
    options?: Array<AutocompleteOption>
    validations?: Record<string, any>
}

const LANG_CODE_TO_NAME: Record<string, string> = {
    all: 'All',
    en: 'English',
    hi: 'Hindi',
    ta: 'Tamil',
    te: 'Telugu',
    gu: 'Gujarati',
    kn: 'Kannada',
    bn: 'Bengali',
    mr: 'Marathi',
    ml: 'Malayalam',
    pa: 'Punjabi',
    ur: 'Urdu'
};

interface FilterPanelProps {
    filtersData: FilterData[]
    filterHandler: (filterChangeEvent: FilterChangeEvent) => boolean
    showFilterButton?: boolean
}

function updateOptionsLabel(filters: FilterData[]) {
    for (const filter of filters) {
        if (filter.type === FilterFieldType.AUTO_COMPLETE) {
            let options = filter.options
                ? filter.options.filter(o => o && o.code &&
                    (typeof o.code === 'number' || o.code.trim().length > 0)
                )
                : [];
            if (options && options.length > 0) {
                for (const option of options) {
                    option.code = option.code.toString();
                }
                if (!options[0].label) {
                    if (filter.id === 'lang') {
                        options = options.filter(o => LANG_CODE_TO_NAME[o.code || '']);
                        for (const option of options) {
                            if (option && option.code && LANG_CODE_TO_NAME[option.code]) {
                                option.label = LANG_CODE_TO_NAME[option.code];
                            }
                        }
                    } else {
                        for (const option of options) {
                            if (option && option.code) {
                                option.label = getTitleSentance(option.code);
                            }
                        }
                    }
                }
            }
            filter.options = options;
        }
    }
}

// function recalculateWidth(filters: FilterData[], showFilterButton: boolean) {
//     const totalWidth = filters.reduce((acc, filter) => acc + filter.width, 0);
//     const widthFactor = showFilterButton ? 11.2 : 11.9;
//     for (const filter of filters) {
//         filter.width = (widthFactor * filter.width) / totalWidth;
//     }
// }

function handleDateField(
    filter: FilterData,
    filterHandler: (filterChangeEvent: FilterChangeEvent) => boolean) {
    const filterDateChangeHandler = (dateValue: Date | null) => {
        if (!dateValue) {
            return;
        }
        const filterChangeEvents: FilterChangeEvent = {
            newValues: [dateValue.toUTCString()]
        };
        filterHandler(filterChangeEvents);
    };

    const dateSelectedValue = getDateFromString(String(filter.selectedValue));
    return (
        <DateInput
            label={filter.label}
            value={dateSelectedValue}
            minDate={filter.validations && filter.validations.minDate}
            maxDate={filter.validations && filter.validations.maxDate}
            onChange={filterDateChangeHandler}
        />
    );
}

function getValueByCode(optionList: Array<AutocompleteOption> | undefined, code: string) {
    if (optionList) {
        const value = optionList.filter(o => o.code === code);
        if (value && value.length && value[0].code) {
            return value[0].label;
        }
    }
    return null;
}

function handleDateRangeField(
    filter: FilterData,
    filterHandler: (filterChangeEvent: FilterChangeEvent) => boolean
) {
    /**
     * Value can be:
     *  1. Month: MMM-yyyy, yyyy-MMM
     *  2. Date Range: ['yyyy-MM-dd', 'yyyy-MM-dd']
     *  3. Period: string
     */

    let value: GenericDateRangeValue = { rangeType: DateRangeType.PERIOD, rangeValue: 'last-7-days' };

    if (filter.defaultValue) {
        const dv = filter.defaultValue instanceof Object && 'code' in filter.defaultValue
            ? filter.defaultValue.code : filter.defaultValue;
        if (dv instanceof Array && dv.length === 2) {
            value = { rangeType: DateRangeType.CUSTOM, rangeValue: [new Date(dv[0]), new Date(dv[1])] };
        } else if (dv instanceof Date) {
            value = { rangeType: DateRangeType.CUSTOM, rangeValue: [dv, dv] };
        } else {
            const monthDate = monthStringToDate(dv as string);
            if (monthDate) {
                value = { rangeType: DateRangeType.MONTH, rangeValue: monthDate };
            } else {
                value = { rangeType: DateRangeType.PERIOD, rangeValue: dv as string };
            }
        }
    }

    const dateRangeChangeHandler = (dateValue: GenericDateRangeValue) => {
        if (!dateValue) {
            return;
        }

        const newValues: string[] = [];

        switch (dateValue.rangeType) {
            case DateRangeType.PERIOD:
                newValues.push(dateValue.rangeValue as string);
                break;
            case DateRangeType.MONTH:
                {
                    const monthRange = dateToMonthRange(dateValue.rangeValue as Date);
                    const rangeString = dateRangeToStringRange(monthRange);
                    newValues.push(...rangeString);
                }
                break;
            case DateRangeType.CUSTOM:
                {
                    const rangeString = dateRangeToStringRange(dateValue.rangeValue as [Date, Date]);
                    newValues.push(...rangeString);
                }
                break;
        }

        filterHandler({ name: filter.id, newValues });
    };

    const allowedDateRange = {
        start: filter?.validations?.minDate,
        end: filter?.validations?.maxDate
    };

    return (
        <GenericDateRange
            label={filter.label}
            dateValue={value}
            allowedPeriod={allowedDateRange}
            onChange={dateRangeChangeHandler}
        />
    );
}

function handleAutoCompleteField(
    filter: FilterData,
    filterHandler: (filterChangeEvent: FilterChangeEvent) => boolean
) {
    const filterChangeHandler = (value: string | null, defaultValue: any, filterName: string) => {
        if (!value) {
            return;
        }
        const newValue = value ?? defaultValue;
        const filterChangeEvent: FilterChangeEvent = {
            name: filterName,
            newValues: [newValue]
        };
        filterHandler(filterChangeEvent);
        // if (cancelEvent) {
        //     event.preventDefault();
        // }
    };

    if (filter.selectedValue) {
        const acSelectedValue: AutocompleteOption = filter.selectedValue as AutocompleteOption;
        if (!acSelectedValue.label && acSelectedValue.code) {
            const labelForCode: string | null | undefined = getValueByCode(filter.options, acSelectedValue.code);
            if (labelForCode) {
                acSelectedValue.label = labelForCode;
            } else if (filter.id === 'lang') {
                acSelectedValue.label = LANG_CODE_TO_NAME[acSelectedValue.code];
            } else {
                acSelectedValue.label = getTitleSentance(acSelectedValue.code);
            }
        }
    }

    const selectedValueToString = (selectedValue: AutocompleteOption | Date | string | string[]) => {
        if (typeof selectedValue === 'string') {
            return selectedValue;
        } else if (selectedValue instanceof Date) {
            return selectedValue.toUTCString();
        } else if (selectedValue instanceof Array) {
            return selectedValue.join('-');
        } else { // AutocompleteOption
            return selectedValue.code;
        }
    };

    // if local variable not used, then it show last value on all filters
    const filterId = filter.id;
    // const filterLabel = filter.label;
    const { defaultValue } = filter;
    const options: { label: string, value: string }[] = filter
        .options?.map(o => ({ label: o.label || '', value: o.code })) || [];
    const selectedValue: string = selectedValueToString(filter.selectedValue || defaultValue);
    const defaultValueString = selectedValueToString(defaultValue);

    // const optionCodes = options.map(o => o.value);
    // if (!optionCodes.includes(selectedValue)) {
    //     options.push(selectedValue);
    // }

    return (
        // <Grid.Col key={filter.id} md={filter.width} lg={filter.width} style={{ minWidth: '6rem' }}>
        // </Grid.Col>
        <Select
            id={filter.id}
            key={filter.id}
            label={filter.label}
            style={{ flex: 'auto' }}
            miw={filter.minWidth}
            maw={filter.maxWidth}
            data={options}
            value={selectedValue}
            maxDropdownHeight={350}
            onChange={(value: string | null) => filterChangeHandler(value, defaultValueString, filterId)}
        />
    );
}

function getRemovedSingleValuedFilters(filters: FilterData[]) {
    return filters.filter(filter =>
        filter.type === FilterFieldType.DATE_RANGE ||
        (filter.options && filter.options.filter(o => o.code !== 'all').length > 1)
    );
}

export default function GenericFilterPanel({ filtersData, filterHandler, showFilterButton = false }: FilterPanelProps) {
    const filterButtonClickHandler = () => {
        const filterChangeEvent: FilterChangeEvent = {};
        filterHandler(filterChangeEvent);
    };

    updateOptionsLabel(filtersData);
    const visibleFiltersData = getRemovedSingleValuedFilters(filtersData);
    // recalculateWidth(visibleFiltersData, showFilterButton || false);
    // const ordinaryFiltersData = visibleFiltersData.filter(filter => filter.type !== FilterFieldType.DATE_RANGE);
    // const dateRangeFiltersData = visibleFiltersData.filter(filter => filter.type === FilterFieldType.DATE_RANGE);

    const filterComponents: React.ReactNode[] = [];
    for (const filter of visibleFiltersData) {
        switch (filter.type) {
            case FilterFieldType.DATE:
                filterComponents.push(handleDateField(filter, filterHandler));
                break;

            case FilterFieldType.AUTO_COMPLETE:
                filterComponents.push(handleAutoCompleteField(filter, filterHandler));
                break;

            case FilterFieldType.DATE_RANGE:
                filterComponents.push(handleDateRangeField(filter, filterHandler));
                break;

            // default:
            // console.error(`Wrong component type: ${filter.type}`);
            // todo: send error to sentry
        }
    }
    // const dateComponents: React.ReactNode[] = dateRangeFiltersData.map(
    //     filter => handleDateRangeField(filter, filterHandler)
    // );

    return (
        <Flex
            wrap={{ base: 'wrap', lg: 'nowrap' }}
            direction="row"
            gap={{ base: 'sm', sm: 'lg' }}
            justify={{ base: 'center', xs: 'flex-end' }}
        >
            {filterComponents}
            {showFilterButton &&
                <Group w={50} align="flex-end">
                    <Button variant="contained" onClick={filterButtonClickHandler}>
                        <IconFilter />
                    </Button>
                </Group>
            }
        </Flex>
    );
}
