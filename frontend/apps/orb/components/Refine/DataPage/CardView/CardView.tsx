import { Badge, Card, Group, Stack, Table, Title, useMantineColorScheme } from '@mantine/core';
import { useContext } from 'react';
import { dateToString } from '../../../../business-logic/utils/data-utils';
import {
    EntityMetaContext,
    ForeignData,
    SpecialField,
    get_field_view,
    get_special_field_value
} from '../../Common/CommonUtils';
import { IModel } from '../../models';
import ControlButtonsPanel from '../ControlButtons/ControlButtonsPanel';
import EnableButton from '../ControlButtons/EnableButton';

export interface CardViewProps {
    resource: string;
    data: IModel;
    foreignData: ForeignData;
}

export default function CardView({ resource, data, foreignData }: CardViewProps) {
    const { fields } = useContext(EntityMetaContext);
    const { colorScheme } = useMantineColorScheme();

    const id = get_special_field_value(SpecialField.Id, fields, data);
    const title = get_special_field_value(SpecialField.Title, fields, data);
    const enabled = get_special_field_value(SpecialField.Enabled, fields, data);
    const time: Date = get_special_field_value(SpecialField.Time, fields, data);

    const tableFields = fields.filter((field) => field.isSummary);
    const timeBg = colorScheme === 'light' ? 'var(--mantine-color-dark-1)' : 'var(--mantine-color-dark-3)';

    return (
        <Card shadow="sm" padding="lg" w={300} miw={350} maw={450} p={20} pb={10}>
            <Stack>
                <Title order={3}> {title} </Title>
                <Table withRowBorders={false}>
                    <Table.Tbody>
                        {tableFields.map((field) => (
                            <Table.Tr key={field.label}>
                                <Table.Td>
                                    <Title order={6}> {field.label} </Title>
                                </Table.Td>
                                <Table.Td>
                                    {get_field_view(data[field.objectKey], field, foreignData)}
                                </Table.Td>
                            </Table.Tr>
                        ))}
                    </Table.Tbody>
                </Table>
                <Group justify="space-between">
                    <ControlButtonsPanel resource={resource} id={id} foreignData={foreignData} />
                    {time && (
                        <Group justify="flex-start" align="flex-end">
                            <Badge size="sm" radius="sm" color={timeBg}>{dateToString(time)}</Badge>
                        </Group>
                    )}
                    <EnableButton resource={resource} id={id} enabled={enabled} />
                </Group>
            </Stack>
        </Card>
    );
}
