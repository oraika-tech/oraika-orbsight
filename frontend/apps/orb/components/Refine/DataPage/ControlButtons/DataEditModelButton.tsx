import { Box, Group, Modal, Stack, Table, Title } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { HttpError, useOne } from '@refinedev/core';
import { EditButton, SaveButton, useModalForm } from '@refinedev/mantine';
import { useContext } from 'react';
import { toPascalCase } from '../../../../business-logic/utils/utils';
import {
    EntityMetaContext, ExistingDataModelButtonProps,
    SpecialField,
    convertObjectKeys, getDefaultValue, get_field_editable,
    get_special_field_value, transformValues
} from '../../Common/CommonUtils';
import { IModel } from '../../models';

export function DataEditModelButton(
    { resource, foreignData, id, hideText, variant, children }: ExistingDataModelButtonProps
) {
    const [opened, { open, close }] = useDisclosure(false);
    const { fields } = useContext(EntityMetaContext);
    const { data, isLoading, isError } = useOne<IModel, HttpError>({ resource, id });
    const modelInfo = convertObjectKeys(data?.data);
    const titleValue = get_special_field_value(SpecialField.Title, fields, modelInfo);
    const title = titleValue ? toPascalCase(titleValue) : `Edit ${toPascalCase(resource)}`;
    const initialValues = getDefaultValue(fields, data?.data);

    const {
        getInputProps, saveButtonProps, errors
    } = useModalForm<typeof initialValues>({
        refineCoreProps: {
            action: 'edit',
            id,
            resource,
            onMutationSuccess: () => close()
        },
        initialValues,
        transformValues: (values) => transformValues(values, initialValues, fields),
        validate: {
            name: (value: string) => (value && value.length < 2 ? 'Too short title' : null)
        }
    });

    if (!modelInfo) {
        return (
            <Modal opened={opened} onClose={close} title={<Title order={2}>{title}</Title>} centered>
                <div>Empty Data</div>;
            </Modal>
        );
    }

    if (isError) {
        return (
            <Modal opened={opened} onClose={close} title={<Title order={2}>{title}</Title>} centered>
                <div>Something went wrong!</div>;
            </Modal>
        );
    }
    if (isLoading) {
        return (
            <Modal opened={opened} onClose={close} title={<Title order={2}>{title}</Title>} centered>
                <div>Loading...</div>;
            </Modal>
        );
    }

    const buttonChildren = children || title;

    const errorElements = Object.values(errors);

    if (errorElements.length > 0) {
        saveButtonProps.disabled = true;
    }

    return (
        <Box>
            <EditButton
                hideText={hideText}
                onClick={open}
                // @ts-ignore
                variant={variant}
                size="sm"
            >
                {buttonChildren}
            </EditButton>

            <Modal size="lg" opened={opened} onClose={close} title={<Title order={2}>{title}</Title>} centered>
                <Stack>
                    <Table withRowBorders={false}>
                        <Table.Tbody>
                            {fields.map((field) => (
                                <Table.Tr key={field.label}>
                                    <Table.Td>
                                        <Title order={6}> {field.label} </Title>
                                    </Table.Td>
                                    <Table.Td>
                                        {get_field_editable(
                                            modelInfo[field.objectKey],
                                            field,
                                            getInputProps(field.objectKey),
                                            foreignData
                                        )}
                                    </Table.Td>
                                </Table.Tr>
                            ))}
                        </Table.Tbody>
                    </Table>
                    <Group justify="flex-end">
                        {errorElements}
                        <SaveButton {...saveButtonProps}>Save</SaveButton>
                    </Group>
                </Stack>
            </Modal>
        </Box>
    );
}
