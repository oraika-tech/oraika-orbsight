import { Group, JsonInput, Switch, TextInput } from '@mantine/core';
import { DateField } from '@refinedev/mantine';
import ChipArray from 'mantine-components/components/Chip/ChipArray';
import Link from 'next/link';
import ObserverInput from '../../../business-logic/data-source/ObserverInput';
import ObserverTypeCell from '../../../business-logic/data-source/ObserverTypeCell';
import { FieldData, FieldType, SpecialField } from './CommonModels';

export default function FieldView(fieldData: FieldData, isSummary?: boolean) {
    const { rowData, fieldMeta, foreignData } = fieldData;
    const value = rowData[fieldMeta.objectKey];
    if (value == null || value === undefined) {
        return <TextInput disabled />;
    }
    let fieldNode = null;
    switch (fieldMeta.type) {
        case FieldType.Date:
            fieldNode = <DateField format="lll" value={value} />;
            break;

        case FieldType.Array:
            fieldNode = <ChipArray chipList={value} bgColor="teal" />;
            break;

        case FieldType.Boolean:
            fieldNode = <Switch checked={value} disabled />;
            break;

        case FieldType.DropDown:
            if (fieldMeta.special === SpecialField.SourceType && !isSummary) {
                const configValue = rowData[fieldMeta.linkData.fieldKey];
                fieldNode = <ObserverInput
                    readOnly
                    observerValue={value}
                    configValue={configValue}
                    fieldData={fieldData}
                    getFieldComponent={FieldView} />;
            } else {
                const data = fieldMeta.foreign
                    ? foreignData[fieldMeta.foreign.resource]
                    : fieldMeta.data;
                const valueLabel = data.find((d) => d.value === value)?.label;
                if (fieldMeta.special === SpecialField.SourceType) {
                    fieldNode = <Group gap={5}><ObserverTypeCell observerType={valueLabel} /> {valueLabel}</Group>;
                } else {
                    fieldNode = <>{valueLabel}</>;
                }
            }
            break;

        case FieldType.Json: {
            const jsonValue = (typeof value === 'object')
                ? JSON.stringify(value, null, 2)
                : value;
            fieldNode = (
                <JsonInput
                    validationError="Invalid JSON"
                    formatOnBlur
                    autosize
                    disabled
                    value={jsonValue} />
            );
            break;
        }

        default:
            fieldNode = <TextInput disabled value={value.toString()} />;
            break;
    }
    if (fieldMeta.linkData) {
        const linkData = rowData[fieldMeta.linkData.fieldKey];
        if (linkData) {
            const linkValue = typeof linkData === 'string' ? linkData : linkData[fieldMeta.linkData.valueKey];
            if (linkValue) {
                return (
                    <Link target="_blank" href={linkValue} style={{ textDecoration: 'none' }}>
                        {fieldNode}
                    </Link>
                );
            }
        }
    }
    return fieldNode;
}
