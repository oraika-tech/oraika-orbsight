import { Box, Modal, Stack, Table, Title } from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { HttpError, useOne } from '@refinedev/core';
import { ShowButton } from '@refinedev/mantine';
import { useContext } from 'react';
import { toPascalCase } from '../../../../business-logic/utils/utils';
import {
    EntityMetaContext, ExistingDataModelButtonProps, SpecialField, convertObjectKeys,
    get_field_view,
    get_special_field_value
} from '../../Common/CommonUtils';
import { IModel } from '../../models';

export function DataShowModelButton(
    { resource, foreignData, id, hideText, variant, children }: ExistingDataModelButtonProps
) {
    const [opened, { open: show, close }] = useDisclosure(false);
    const { fields } = useContext(EntityMetaContext);
    const { data, isLoading, isError } = useOne<IModel, HttpError>({ resource, id });
    const modelInfo = convertObjectKeys(data?.data);
    const titleValue = get_special_field_value(SpecialField.Title, fields, modelInfo);
    const title = titleValue ? toPascalCase(titleValue) : `Show ${toPascalCase(resource)}`;

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

    const buttonChildren = children || 'Show';

    return (
        <Box>
            <ShowButton
                hideText={hideText}
                onClick={() => show()}
                // @ts-ignore
                variant={variant}
                size="sm"
            >
                {buttonChildren}
            </ShowButton>

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
                                        {modelInfo[field.objectKey] && (
                                            get_field_view(modelInfo[field.objectKey], field, foreignData)
                                        )}
                                    </Table.Td>
                                </Table.Tr>
                            ))}
                        </Table.Tbody>
                    </Table>
                </Stack>
            </Modal>
        </Box>
    );
}
