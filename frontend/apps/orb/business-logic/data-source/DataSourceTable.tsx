import DataGridCard from 'mantine-components/components/DataGridCard';
import ToggleButton from 'mantine-components/components/ToggleButton';
import type { MRT_ColumnDef } from 'mantine-react-table';
import { useMemo } from 'react';
import LinkCell from './LinkCell';
import ObserverTypeCell from './ObserverTypeCell';

interface DataSourceTableProps {
    rows: any[]
    handleEnableToggle: (id: string, isEnabled: boolean, handlerDone: (isSuccess: boolean) => void) => void
    showLoading: boolean
}

interface NameLink {
    name: string
    link: string
}

interface DataSourceType {
    dataSourceType: string
    nameLink: NameLink
    entityName: string
    isEnabled: boolean
}

export default function DataSourceTable({ rows, handleEnableToggle, showLoading }: DataSourceTableProps) {
    const columns = useMemo<MRT_ColumnDef<DataSourceType>[]>(
        () => [
            {
                accessorKey: 'dataSourceType',
                header: 'Type',
                Cell: ({ cell }) => <ObserverTypeCell observerType={cell.getValue()} />
            },
            {
                accessorKey: 'nameLink',
                header: 'Source',
                Cell: ({ cell }) => <LinkCell
                    title={cell.getValue<NameLink>().name}
                    link={cell.getValue<NameLink>().link}
                />
            },
            {
                accessorKey: 'entityName',
                header: 'Entity Name'
            },
            {
                accessorKey: 'isEnabled',
                header: 'Enabled',
                Cell: ({ cell }) => <ToggleButton value={cell.getValue()} handleToggle={handleEnableToggle} />,
                sortDescFirst: true
            }
        ],
        []
    );

    return (
        <DataGridCard
            title="Data Source"
            rows={rows}
            columns={columns}
            showLoading={showLoading}
        />
    );
}
