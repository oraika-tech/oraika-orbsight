import { Badge, Card, Group, Stack, Table, Title, useMantineColorScheme } from '@mantine/core';
import { useContext } from 'react';
import { dateToString } from '../../../../business-logic/utils/data-utils';
import { ForeignData, SpecialField } from '../../Common/CommonModels';
import { get_special_field, get_special_field_value } from '../../Common/CommonUtils';
import { EntityMetaContext } from '../../Common/EntityMetaContext';
import FieldView from '../../Common/FieldView';
import { IModel } from '../../models';
import ControlButtonsPanel from '../ControlButtons/ControlButtonsPanel';
import EnableButton from '../ControlButtons/EnableButton';
import WithLink from 'mantine-components/components/WithLInk';

export interface CardViewProps {
    resource: string;
    data: IModel;
    foreignData: ForeignData;
}

function getLink(fields, data) {
    const linkField = get_special_field(SpecialField.Link, fields);
    if (!linkField) {
        return null;
    }
    const linkData = get_special_field_value(SpecialField.Link, fields, data);
    return linkData[linkField.linkData.valueKey];
}

export default function CardView({ resource, data, foreignData }: CardViewProps) {
    const { fields } = useContext(EntityMetaContext);
    const { colorScheme } = useMantineColorScheme();

    const id = get_special_field_value(SpecialField.Id, fields, data);
    const title = get_special_field_value(SpecialField.Title, fields, data);
    const enabled = get_special_field_value(SpecialField.Enabled, fields, data);
    const time: Date = get_special_field_value(SpecialField.Time, fields, data);

    const link = getLink(fields, data);

    const tableFields = fields.filter((field) => field.isSummary && !field.isHide);
    const timeBg = colorScheme === 'light' ? 'var(--mantine-color-dark-1)' : 'var(--mantine-color-dark-3)';

    return (
        <Card shadow="sm" padding="lg" miw={300} maw={400} p={20} pb={10}>
            <Stack justify="space-between" h="100%">
                <WithLink href={link}><Title order={4}> {title} </Title></WithLink>
                <Stack>
                    <Table verticalSpacing={6} withRowBorders={false}>
                        <Table.Tbody>
                            {tableFields.map((field) => (
                                <Table.Tr key={field.label}>
                                    <Table.Td>
                                        <Title order={6}> {field.label} </Title>
                                    </Table.Td>
                                    <Table.Td>
                                        {FieldView({
                                            rowData: data,
                                            fieldMeta: field,
                                            foreignData
                                        }, true)}
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
            </Stack>
        </Card>
    );
}
