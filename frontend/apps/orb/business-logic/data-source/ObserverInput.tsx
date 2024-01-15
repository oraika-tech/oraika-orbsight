import { Group, Paper, Select, Stack, Table, Title } from '@mantine/core';
import { useState } from 'react';
import {
    EntityField,
    FieldData, FieldType, ForeignData
} from '../../components/Refine/Common/CommonModels';
import { IModel } from '../../components/Refine/models';
import { cleanObject, removeNulls } from '../utils/utils';
import ObserverTypeCell from './ObserverTypeCell';

enum ObserverType {
    Twitter = 1,
    Android = 2,
    iOS = 3,
    GoogleMaps = 4,
    Facebook = 5,
    Reddit = 6,
    GoogleNews = 7,
    GoogleSearch = 8
}

interface ObserverMeta {
    name: string;
    type: ObserverType;
    config_data_fields: {
        label: string;
        placeholder: string;
        objectKey: string;
        fieldType: FieldType;
        data?: any[];
    }[];
}

const observers: ObserverMeta[] = [
    {
        name: 'GoogleMaps',
        type: ObserverType.GoogleMaps,
        config_data_fields: [
            {
                label: 'Url',
                placeholder: 'Enter map url',
                objectKey: 'url',
                fieldType: FieldType.String
            }
        ]
    },
    {
        name: 'GoogleNews',
        type: ObserverType.GoogleNews,
        config_data_fields: [
            {
                label: 'Query',
                placeholder: 'Enter news search query',
                objectKey: 'query',
                fieldType: FieldType.String
            },
            {
                label: 'Number of Pages',
                placeholder: 'Enter number of result pages required',
                objectKey: 'number_of_pages',
                fieldType: FieldType.Number
            },
            {
                label: 'Period',
                placeholder: 'Time Based Search',
                objectKey: 'tbs',
                fieldType: FieldType.DropDown,
                data: [
                    { value: 'h', label: 'Last Hour' },
                    { value: 'd', label: 'Last Day' },
                    { value: 'w', label: 'Last Week' },
                    { value: 'm', label: 'Last Month' },
                    { value: 'y', label: 'Last Year' }
                ]
            }
        ]
    },
    {
        name: 'GoogleSearch',
        type: ObserverType.GoogleSearch,
        config_data_fields: [
            {
                label: 'Query',
                placeholder: 'Enter Google search query',
                objectKey: 'query',
                fieldType: FieldType.String
            },
            {
                label: 'Number of Pages',
                placeholder: 'Enter number of result pages required',
                objectKey: 'number_of_pages',
                fieldType: FieldType.Number
            }
        ]
    },
    {
        name: 'Android',
        type: ObserverType.Android,
        config_data_fields: [
            {
                label: 'Url',
                placeholder: 'Enter map url',
                objectKey: 'url',
                fieldType: FieldType.String
            }
        ]
    },
    {
        name: 'iOS',
        type: ObserverType.iOS,
        config_data_fields: [
            {
                label: 'Url',
                placeholder: 'Enter map url',
                objectKey: 'url',
                fieldType: FieldType.String
            }
        ]
    }
];

interface ObserverInputProps {
    observerValue?: any;
    configValue: any;
    readOnly?: boolean;
    getFieldComponent: (fieldData: FieldData, inputProps) => React.ReactNode;
    fieldData: FieldData;
    inputProps?: any;
}

export default function ObserverInput(
    { observerValue, configValue, readOnly, getFieldComponent, fieldData, inputProps }: ObserverInputProps
) {
    const [observerType, setObserverType] = useState<ObserverType>(observerValue || observers[0].type);
    const observerMeta = observers.find((o) => o.type === observerType);
    const selectProps = readOnly ? null : inputProps(fieldData.fieldMeta.objectKey);
    const configDataProps = readOnly ? null : inputProps(fieldData.fieldMeta.linkData.fieldKey);

    const configData = fieldData.rowData[fieldData.fieldMeta.linkData.fieldKey] || {};
    removeNulls(configData);

    const getFieldInputProps = (fieldKey: string) => ({
        value: configData[fieldKey],
        onChange: (event_value) => {
            switch (typeof event_value) {
                case 'object':
                    configData[fieldKey] = event_value.target.value;
                    break;
                default:
                    configData[fieldKey] = event_value;
            }
            configDataProps.onChange(cleanObject(configData));
        }
    });

    return (
        <Paper withBorder shadow="xs">
            <Stack>
                {readOnly
                    ? <Group gap={5}><ObserverTypeCell observerType={observerMeta.name} /> {observerMeta.name}</Group>
                    : (
                        <Select
                            value={observerType.toString()}
                            onChange={(_value) => {
                                setObserverType(Number(_value));
                                selectProps.onChange(Number(_value));
                            }}
                            data={observers.map((d) => ({ value: d.type.toString(), label: d.name }))}
                        />
                    )
                }
                {observerMeta.config_data_fields.length > 0 && (
                    <Table withRowBorders={false}>
                        <Table.Tbody>
                            {observerMeta.config_data_fields.map((field) => {
                                const rowData: IModel = configValue;
                                const fieldMeta: EntityField = {
                                    label: field.label,
                                    objectKey: field.objectKey,
                                    type: field.fieldType,
                                    data: field.data
                                };
                                const foreignData: ForeignData = {};
                                return (
                                    <Table.Tr key={field.label}>
                                        <Table.Td>
                                            <Title order={6}> {field.label} </Title>
                                        </Table.Td>
                                        <Table.Td>
                                            {getFieldComponent({ rowData, fieldMeta, foreignData }, getFieldInputProps)}
                                        </Table.Td>
                                    </Table.Tr>
                                );
                            })}
                        </Table.Tbody>
                    </Table>
                )}
            </Stack>
        </Paper>
    );
}
