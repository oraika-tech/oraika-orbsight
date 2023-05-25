import ChipArray from 'mantine-components/components/Chip/ChipArray';
import DataGridCard from 'mantine-components/components/DataGridCard';
import ToggleButton from 'mantine-components/components/ToggleButton';
import type { MRT_ColumnDef } from 'mantine-react-table';
import { useMemo } from 'react';

export interface EntityState {
    id: string
    name: string
    entityType: string[]
    isEnabled: {
        id: string
        isEnabled: boolean
    }
}

interface EntityType {
    name: string
    entityType: string
    isEnabled: boolean
}

interface EntityTableProps {
    rows: EntityState[]
    handleEnableToggle: (id: string, isEnabled: boolean, handlerDone: (isSuccess: boolean) => void) => void;
    showLoader: boolean
}

function EntityTable({ rows, handleEnableToggle, showLoader }: EntityTableProps) {
    const columns = useMemo<MRT_ColumnDef<EntityType>[]>(
        () => [
            {
                accessorKey: 'name',
                header: 'Name'
            },
            {
                accessorKey: 'entityType',
                header: 'Type',
                Cell: ({ cell }) => <ChipArray chipList={cell.getValue<string[]>()} bgColor="info" />
            },
            {
                accessorKey: 'isEnabled',
                header: 'Enabled',
                align: 'center',
                type: 'boolean',
                Cell: ({ cell }) => <ToggleButton value={cell.getValue()} handleToggle={handleEnableToggle} />,
                cellClassName: 'borderless',
                editable: false
            }
        ],
        []
    );

    return <DataGridCard title="Entity" rows={rows} columns={columns} showLoading={showLoader} />;
}

export default EntityTable;
