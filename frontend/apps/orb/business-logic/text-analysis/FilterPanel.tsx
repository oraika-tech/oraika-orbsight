import { Button, Grid, Paper, Select } from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
// import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { IconFilter } from '@tabler/icons-react';
import { trackFilter } from 'common-utils/scripts/mixpanel';
import { getCurrentMinusNDays, shallowEqual } from 'common-utils/utils';
import { useRouter } from 'next/router';
import { useEffect, useRef, useState } from 'react';
import { DataRequest, getData } from '../../lib/service/data-service';
import { getUndefForAll, toPascalCase } from '../utils/utils';
// import { DataRequest, getData } from 'service/data-service';
// import { trackFilter } from 'tracking/mixpanel';
// import { getCurrentMinusNDays, shallowEqual } from 'utils';

export interface DataEntity {
    id: string
    name: string
}

export interface DataSourceType {
    name: string
}

export interface DataTerm {
    name: string
}

export interface DataLanguage {
    code: string
    name: string
}

interface DateRange {
    start: Date
    end: Date
}

export interface SelectOption {
    value: string;
    label: string;
}

export interface SelectData {
    id: string;
    label: string;
    options: Array<SelectOption>;
}

export interface FilterPanelData {
    lang: string;
    entity: string;
    source: string;
    term: string;
    startDate: Date
    endDate: Date
}

interface FilterPanelProps {
    showFilterButton?: boolean
    defaultValue: FilterPanelData
    filterHandler: (filterPanelData: FilterPanelData) => void
}

const LANG_CODE_TO_NAME = {
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

export default function FilterPanel({ defaultValue, filterHandler, showFilterButton }: FilterPanelProps) {
    const location = useRouter();

    const [filterPanelData, setFilterPanelData] = useState(defaultValue);
    const [dateRange, setDateRange] = useState<DateRange>({ start: defaultValue.startDate, end: defaultValue.endDate });
    const [languages, setLanguages] = useState<DataLanguage[]>([]);
    const [entities, setEntities] = useState<DataEntity[]>([]);
    const [sourceTypes, setSourceTypes] = useState<DataSourceType[]>([]);
    const [terms, setTerms] = useState<DataTerm[]>([]);

    const syncFilterFields = (filterData: FilterPanelData) => {
        filterData.startDate.setHours(0, 0, 0, 0);
        filterData.endDate.setHours(23, 59, 59, 999);

        const filters: DataRequest = {
            start_date: filterData.startDate,
            end_date: filterData.endDate,
            text_lang: getUndefForAll(filterData.lang),
            entity_name: getUndefForAll(filterData.entity),
            observer_type: getUndefForAll(filterData.source),
            term: getUndefForAll(filterData.term)
        };

        getData('/entities', filters).then(response => setEntities(response));
        getData('/source-types', filters).then(response => setSourceTypes(response));
        getData('/terms', filters).then(response => setTerms(response));
        getData('/languages', filters).then(response => setLanguages(response.map((lang: string) => ({
            code: lang,
            name: LANG_CODE_TO_NAME[lang]
        }))));

        if (!showFilterButton) {
            filterHandler(filterData);
        }
    };

    const syncFilterFieldsRef = useRef(syncFilterFields);

    const setFPData = (fieldName: string, fieldValue: string | Date) => {
        const newValue = fieldValue || defaultValue[fieldName];
        if (!shallowEqual(filterPanelData[fieldName], newValue)) {
            if (fieldName === 'startDate' || fieldName === 'endDate') {
                setDateRange({ ...dateRange, [fieldName]: newValue });
            }
            const newData: FilterPanelData = { ...filterPanelData, [fieldName]: newValue };
            setFilterPanelData(newData);
            syncFilterFields(newData);

            trackFilter(location.pathname, newData);
        }
    };

    const filterButtonClickHandler = () => {
        filterHandler(filterPanelData);
    };

    useEffect(() => {
        syncFilterFieldsRef.current(filterPanelData);

        return () => {
            setLanguages([]);
            setEntities([]);
            setSourceTypes([]);
            setTerms([]);
        };
    }, [filterPanelData]);

    const allValue = {
        value: 'all',
        label: 'All'
    };

    const langData: SelectData = {
        id: 'langauge_id',
        label: 'Language',
        options: [].concat(allValue, languages.map(lang => ({ value: lang.code, label: lang.name })))
    };

    const entityData: SelectData = {
        id: 'entity_id',
        label: 'Entity',
        options: [].concat(allValue, entities.map(entity => ({ value: entity.name, label: entity.name })))
    };

    const sourceData: SelectData = {
        id: 'source_id',
        label: 'Data Source',
        options: [].concat(allValue, sourceTypes.map(sourceType => ({
            value: sourceType.name, label: sourceType.name
        })))
    };

    const termData: SelectData = {
        id: 'term_id',
        label: 'Term',
        options: [].concat(allValue, terms.map(term => ({ value: term.name, label: toPascalCase(term.name) })))
    };

    return (
        <Paper>
            <Grid
                sx={{
                    flexWrap: 'wrap',
                    minHeight: 100,
                    maxHeight: 300,
                    paddingLeft: '1rem'
                }}
                align="center"
                gutter="md"
            >
                <Grid.Col xs={1.6} sx={{ minWidth: '11.5rem' }}>
                    {/* <LocalizationProvider dateAdapter={AdapterDateFns}> */}
                    <DatePickerInput
                        label="Start"
                        value={filterPanelData.startDate}
                        minDate={getCurrentMinusNDays(60)}
                        maxDate={filterPanelData.endDate}
                        onChange={(newValue) => {
                            setFPData('startDate', newValue);
                        }}
                    />
                    {/* </LocalizationProvider> */}
                </Grid.Col>
                <Grid.Col xs={1.6} sx={{ minWidth: '11.5rem' }}>
                    {/* <LocalizationProvider dateAdapter={AdapterDateFns}> */}
                    <DatePickerInput
                        label="End"
                        value={filterPanelData.endDate}
                        minDate={filterPanelData.startDate}
                        maxDate={defaultValue.endDate}
                        onChange={(newValue) => {
                            setFPData('endDate', newValue);
                        }}
                    />
                    {/* </LocalizationProvider> */}
                </Grid.Col>

                <Grid.Col xs={4.5} md={6.8} lg={2} sx={{ minWidth: '10rem' }}>
                    <Select
                        label="Language"
                        id={langData.id}
                        data={langData.options}
                        defaultValue={filterPanelData.lang || 'all'}
                        onChange={(newValue: string) => {
                            setFPData('lang', newValue);
                        }}
                    />
                </Grid.Col>
                <Grid.Col md={4.5} lg={2} sx={{ minWidth: '10rem' }}>
                    <Select
                        label="Entity"
                        id={entityData.id}
                        data={entityData.options}
                        defaultValue={filterPanelData.entity || 'all'}
                        onChange={(newValue: string) => {
                            setFPData('entity', newValue);
                        }}
                    />
                </Grid.Col>
                <Grid.Col md={4.5} lg={2} sx={{ minWidth: '10rem' }}>
                    <Select
                        label="Source"
                        id={sourceData.id}
                        data={sourceData.options}
                        defaultValue={filterPanelData.source || 'all'}
                        onChange={(newValue: string) => {
                            setFPData('source', newValue);
                        }}
                    />
                </Grid.Col>
                <Grid.Col md={4} lg={2} sx={{ minWidth: '10rem' }}>
                    <Select
                        label="Term"
                        id={termData.id}
                        data={termData.options}
                        defaultValue={filterPanelData.term || 'all'}
                        onChange={(newValue: string) => {
                            setFPData('term', newValue);
                        }}
                    />
                </Grid.Col>
                {showFilterButton &&
                    <Grid.Col>
                        <Button variant="contained" onClick={filterButtonClickHandler}>
                            <IconFilter />
                        </Button>
                    </Grid.Col>
                }
            </Grid>
        </Paper>
    );
}

FilterPanel.defaultProps = {
    showFilterButton: false
};
