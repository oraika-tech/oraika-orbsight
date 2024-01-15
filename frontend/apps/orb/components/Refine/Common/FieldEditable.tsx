import { JsonInput, NumberInput, Select, Switch, TagsInput, TextInput } from '@mantine/core';
import { DateInput } from '@mantine/dates';
import { ReactNode } from 'react';
import ObserverInput from '../../../business-logic/data-source/ObserverInput';
import { cleanObject } from '../../../business-logic/utils/utils';
import { FieldData, FieldType, SpecialField } from './CommonModels';
import FieldView from './FieldView';

export default function FieldEditable(fieldData: FieldData, inputProps): ReactNode {
    const { rowData, fieldMeta, foreignData } = fieldData;
    const value = rowData[fieldMeta.objectKey];
    const fieldProps = inputProps(fieldMeta.objectKey);
    if (fieldMeta.isReadOnly) {
        return FieldView(fieldData);
    }
    switch (fieldMeta.type) {
        case FieldType.Date:
            return <DateInput {...fieldProps} />;

        case FieldType.Boolean:
            fieldProps.checked = value;
            return <Switch {...fieldProps} disabled />;

        case FieldType.Number:
            return <NumberInput {...fieldProps} />;

        case FieldType.Array:
            return <TagsInput placeholder="Press Enter or Comma to add" {...fieldProps} />;

        case FieldType.DropDown: {
            if (fieldMeta.special === SpecialField.SourceType) {
                const configValue = rowData[fieldMeta.linkData.fieldKey];
                return (
                    <ObserverInput
                        observerValue={value}
                        configValue={configValue}
                        inputProps={inputProps}
                        fieldData={fieldData}
                        getFieldComponent={FieldEditable} />
                );
            } else {
                const selectData = fieldMeta.foreign
                    ? foreignData[fieldMeta.foreign.resource]
                    : fieldMeta.data;
                fieldProps.data = selectData.map((d) => ({ value: d.value.toString(), label: d.label }));
                if (value != null) {
                    fieldProps.value = value.toString();
                }
                return <Select placeholder={`Select ${fieldMeta.label}`} {...fieldProps} />;
            }
        }

        case FieldType.Json:
            if (typeof fieldProps.value === 'object') {
                const cleanValue = cleanObject(fieldProps.value);
                fieldProps.value = JSON.stringify(cleanValue, null, 2);
            }
            return (
                <JsonInput
                    validationError="Invalid JSON"
                    formatOnBlur
                    autosize
                    {...fieldProps} />
            );

        default:
            fieldProps.placeholder = fieldMeta.label;
            return <TextInput {...fieldProps} />;
    }
}
