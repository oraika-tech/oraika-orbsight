import { Button, Grid, Select, SimpleGrid } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { IconFilter } from '@tabler/icons-react';
import { getDateFromString, getTitleSentance } from 'common-utils/utils';

export interface AutocompleteOption {
    id?: string
    code: string
    label: string
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
    width: number
    type: string
    selectedValue: AutocompleteOption | Date | string
    defaultValue: AutocompleteOption | Date | string
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
        if (filter.type === 'AUTO_COMPLETE') {
            let options = filter.options
                ? filter.options.filter(o => o && o.code && o.code.trim().length > 0)
                : [];
            if (options && options.length > 0) {
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

function recalculateWidth(filters: FilterData[], showFilterButton: boolean) {
    const totalWidth = filters.reduce((acc, filter) => acc + filter.width, 0);
    const widthFactor = showFilterButton ? 11.2 : 11.9;
    for (const filter of filters) {
        filter.width = (widthFactor * filter.width) / totalWidth;
    }
}

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
            const labelForCode: string | null = getValueByCode(filter.options, acSelectedValue.code);
            if (labelForCode) {
                acSelectedValue.label = labelForCode;
            } else if (filter.id === 'lang') {
                acSelectedValue.label = LANG_CODE_TO_NAME[acSelectedValue.code];
            } else {
                acSelectedValue.label = getTitleSentance(acSelectedValue.code);
            }
        }
    }

    const selectedValueToString = (selectedValue: AutocompleteOption | Date | string) => {
        if (typeof selectedValue === 'string') {
            return selectedValue;
        } else if (selectedValue instanceof Date) {
            return selectedValue.toUTCString();
        } else {
            return selectedValue.code;
        }
    };

    // if local variable not used, then it show last value on all filters
    const filterId = filter.id;
    // const filterLabel = filter.label;
    const { defaultValue } = filter;
    const options: { label: string, value: string }[] = filter
        .options?.map(o => ({ label: o.label, value: o.code })) || [];
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
            data={options}
            value={selectedValue}
            maxDropdownHeight={350}
            onChange={(value: string | null) => filterChangeHandler(value, defaultValueString, filterId)}
        />
    );
}

function getRemovedSingleValuedFilters(filters: FilterData[]) {
    return filters.filter(filter => filter.options && filter.options.filter(o => o.code !== 'all').length > 1);
}

export default function GenericFilterPanel({ filtersData, filterHandler, showFilterButton }: FilterPanelProps) {
    const filterButtonClickHandler = () => {
        const filterChangeEvent: FilterChangeEvent = {};
        filterHandler(filterChangeEvent);
    };

    updateOptionsLabel(filtersData);
    const visibleFiltersData = getRemovedSingleValuedFilters(filtersData);
    recalculateWidth(visibleFiltersData, showFilterButton || false);

    const filterComponents: React.ReactNode[] = [];
    for (const filter of visibleFiltersData) {
        switch (filter.type) {
            case 'DATE':
                filterComponents.push(handleDateField(filter, filterHandler));
                break;

            case 'AUTO_COMPLETE':
                filterComponents.push(handleAutoCompleteField(filter, filterHandler));
                break;

            default:
            // console.error(`Wrong component type: ${filter.type}`);
            // todo: send error to sentry
        }
    }

    const filterCount = filterComponents.length + (showFilterButton ? 1 : 0);

    return (
        <SimpleGrid
            cols={{ base: 2, xs: filterCount / 2, lg: filterCount }}
            spacing={{ base: 'sm', xs: 'md' }}
            verticalSpacing="xs"
        >
            {filterComponents}

            {showFilterButton &&
                <Grid.Col>
                    <Button variant="contained" onClick={filterButtonClickHandler}>
                        <IconFilter />
                    </Button>
                </Grid.Col>
            }
        </SimpleGrid>
    );
}

GenericFilterPanel.defaultProps = {
    showFilterButton: false
};
