import { ActionIcon, Group, Menu, Stack, TextInput } from '@mantine/core';
import { IconCheck, IconFilter, IconX } from '@tabler/icons';
import { Column } from '@tanstack/react-table';
import { useState } from 'react';

interface ColumnButtonProps {
    column: Column<any, any>; // eslint-disable-line
}

export default function ColumnFilter({ column }: ColumnButtonProps) {
    // eslint-disable-next-line
    const [state, setState] = useState(null as null | { value: any });

    if (!column.getCanFilter()) {
        return null;
    }

    const open = () =>
        setState({
            value: column.getFilterValue()
        });

    const close = () => setState(null);

    // eslint-disable-next-line
    const change = (value: any) => setState({ value });

    const clear = () => {
        column.setFilterValue(undefined);
        close();
    };

    const save = () => {
        if (!state) return;
        column.setFilterValue(state.value);
        close();
    };

    const renderFilterElement = () => {
        // eslint-disable-next-line
        const FilterComponent = (column.columnDef?.meta as any)?.filterElement;

        if (!FilterComponent && !!state) {
            return (
                <TextInput
                    autoComplete="off"
                    value={state.value}
                    onChange={(e) => change(e.target.value)}
                />
            );
        }

        return <FilterComponent value={state?.value} onChange={change} />;
    };

    return (
        <Menu
            opened={!!state}
            position="bottom"
            withArrow
            transitionProps={{ transition: 'scale-y' }}
            shadow="xl"
            onClose={close}
            width="256px"
        >
            <Menu.Target>
                <ActionIcon
                    size="xs"
                    onClick={open}
                    variant={column.getIsFiltered() ? 'light' : 'transparent'}
                    color={column.getIsFiltered() ? 'primary' : 'gray'}
                >
                    <IconFilter size={18} />
                </ActionIcon>
            </Menu.Target>
            <Menu.Dropdown>
                {!!state && (
                    <Stack p="xs" gap="xs">
                        {renderFilterElement()}
                        <Group justify="flex-end" gap={6} wrap="nowrap">
                            <ActionIcon
                                size="md"
                                color="gray"
                                variant="outline"
                                onClick={clear}
                            >
                                <IconX size={18} />
                            </ActionIcon>
                            <ActionIcon
                                size="md"
                                onClick={save}
                                color="primary"
                                variant="outline"
                            >
                                <IconCheck size={18} />
                            </ActionIcon>
                        </Group>
                    </Stack>
                )}
            </Menu.Dropdown>
        </Menu>
    );
}
