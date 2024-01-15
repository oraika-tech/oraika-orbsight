import { ActionIcon, Card, Group, Stack, Title } from '@mantine/core';
import { useLocalStorage } from '@mantine/hooks';
import { useList } from '@refinedev/core';
import { IconLayoutGrid, IconTable } from '@tabler/icons-react';
import { EntityField, EntityOptions, ForeignData, ForeignField } from '../Common/CommonModels';
import { EntityMetaContext } from '../Common/EntityMetaContext';
import CardListView from './CardView/CardListView';
import { DataCreateModelButton } from './ControlButtons/DataCreateModelButton';
import TableView from './TableView/TableView';

export enum ViewMode {
    CardMode = 'card',
    TableMode = 'table'
}

interface DataPageProps {
    title: string;
    resource: string;
    cardOptions: EntityOptions;
    allowedViewModes?: ViewMode[];
}

/*
    Function to get foreign entity data for dropdown fields. E.g.
    [
        { value: '50228706-f2c6-465d-a0ca-a00d097789fc', label: 'PlayArena' }
        { value: '7733c02b-43a1-4094-b393-eeda6ca6fe97', label: 'PlayJuniors' }
    ]
*/
function getForeignData(fields: EntityField[]): ForeignData {
    const foreigns: { [resource: string]: ForeignField } = fields
        .filter((field) => field.foreign)
        .map((field) => field.foreign)
        .reduce((acc, curr) => ({ ...acc, [curr.resource]: curr }), {});
    return Object.fromEntries(Object.entries(foreigns)
        .map(([resource, value]) => {
            const { resource: foreignResource, labelKey } = value;
            const { data: foreignData } = useList({ resource: foreignResource });
            const foreignEntityList = foreignData?.data?.map((row) => (
                { value: row.identifier, label: row[labelKey] }
            ));
            return [resource, foreignEntityList || []];
        }));
}

function getViewModeIcons(viewMode: ViewMode): React.ReactNode {
    switch (viewMode) {
        case ViewMode.CardMode:
            return <IconLayoutGrid />;
        case ViewMode.TableMode:
            return <IconTable />;
    }
    return <></>;
}

function getViewModeContent(viewMode: ViewMode, resource: string, foreignData: ForeignData): React.ReactNode {
    switch (viewMode) {
        case ViewMode.CardMode:
            return <CardListView resource={resource} foreignData={foreignData} />;
        case ViewMode.TableMode:
            return <TableView resource={resource} foreignData={foreignData} />;
    }
    return <></>;
}

export default function DataPage({ title, resource, cardOptions, allowedViewModes }: DataPageProps) {
    if (!allowedViewModes) {
        allowedViewModes = Object.values(ViewMode);
    }

    const [viewModeIndex, setViewModeIndex] = useLocalStorage<number>({
        key: `${title}-ViewMode-Index`,
        defaultValue: 0
    });

    // Set default if local storage value is invalid
    if (viewModeIndex >= allowedViewModes.length) {
        setViewModeIndex(0);
    }

    const foreignDataMap = getForeignData(cardOptions.fields);

    return (
        <EntityMetaContext.Provider value={cardOptions}>
            <Stack>
                <Card>
                    <Group pr={20} justify="space-between" align="center">
                        <Title order={2} pt="0.1rem">{title}</Title>
                        <Group>
                            {allowedViewModes.length > 1 && (
                                <ActionIcon
                                    variant="filled"
                                    size="lg"
                                    radius="sm"
                                    onClick={() => setViewModeIndex((currentViewModeIndex) =>
                                        ((currentViewModeIndex + 1) % allowedViewModes.length)
                                    )}
                                >
                                    {getViewModeIcons(allowedViewModes[viewModeIndex])}
                                </ActionIcon>
                            )}
                            <DataCreateModelButton resource={resource} foreignData={foreignDataMap} />
                        </Group>
                    </Group>
                </Card>
                {getViewModeContent(allowedViewModes[viewModeIndex], resource, foreignDataMap)}
            </Stack>
        </EntityMetaContext.Provider>
    );
}
