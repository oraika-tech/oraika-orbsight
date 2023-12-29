import { Box, Group, Modal, Stack, Table, Title } from '@mantine/core';
import { CreateButton, SaveButton, useModalForm } from '@refinedev/mantine';
import { useContext } from 'react';
import { toPascalCase } from '../../../../business-logic/utils/utils';
import {
    EntityMetaContext,
    ForeignData,
    ModelButtonProps,
    getDefaultValue,
    get_field_editable,
    transformValues
} from '../../Common/CommonUtils';

interface DataCreateModelButtonProps extends ModelButtonProps {
    foreignData: ForeignData;
}

export function DataCreateModelButton(
    { resource, foreignData, hideText, variant, children }: DataCreateModelButtonProps
) {
    const { fields } = useContext(EntityMetaContext);
    const title = `Create ${toPascalCase(resource)}`;
    const initialValues = getDefaultValue(fields);

    const {
        getInputProps, saveButtonProps, modal: { show, visible, close }
    } = useModalForm<typeof initialValues>({
        refineCoreProps: {
            action: 'create',
            resource
        },
        initialValues,
        transformValues: (values) => transformValues(values, initialValues, fields),
        validate: {
            // name: (value: string) => (value.length < 2 ? 'Too short title' : null)
        }
    });

    const buttonChildren = children || 'Create';
    const creatableFields = fields.filter((field) => (field.isCreatable));

    return (
        <Box>
            <CreateButton
                hideText={hideText}
                onClick={() => show()}
                // @ts-ignore
                variant={variant}
                size="sm"
            >
                {buttonChildren}
            </CreateButton>

            <Modal size="lg" opened={visible} onClose={close} title={<Title order={2}>{title}</Title>} centered>
                <Stack>
                    <Table withRowBorders={false}>
                        <Table.Tbody>
                            {creatableFields.map((field) => (
                                <Table.Tr key={field.label}>
                                    <Table.Td>
                                        <Title order={6}> {field.label} </Title>
                                    </Table.Td>
                                    <Table.Td>
                                        {get_field_editable(
                                            null,
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
                        <SaveButton {...saveButtonProps}>Save</SaveButton>
                    </Group>
                </Stack>
            </Modal>
        </Box>
    );
}
