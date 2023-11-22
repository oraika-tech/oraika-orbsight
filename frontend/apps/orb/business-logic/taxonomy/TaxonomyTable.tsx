import { Badge } from '@mantine/core';
import ChipArray from 'mantine-components/components/Chip/ChipArray';
import DataGridCard from 'mantine-components/components/DataGridCard';
import type { MRT_ColumnDef } from 'mantine-react-table';
import { useMemo } from 'react';

interface TaxonomyType {
    keyword: string
    term: string
    description: string
    tags: string[]
}

function TaxonomyTable({ rows, loading }) {
    const columns = useMemo<MRT_ColumnDef<TaxonomyType>[]>(
        () => [
            {
                accessorKey: 'keyword',
                header: 'Keyword',
                Cell: ({ cell }) => (
                    <Badge
                        size="md"
                        color="teal"
                        variant="filled"
                        style={{ fontWeight: 500, marginLeft: '0.1rem' }}
                    >
                        {cell.getValue() as string}
                    </Badge>
                )
            },
            {
                accessorKey: 'term',
                header: 'Term',
                Cell: ({ cell }) => (
                    <Badge
                        size="md"
                        color="lime"
                        variant="filled"
                        style={{ fontWeight: 500, marginLeft: '0.1rem' }}
                    >
                        {cell.getValue() as string}
                    </Badge>
                )
            },
            {
                accessorKey: 'description',
                header: 'Description'
            },
            {
                accessorKey: 'tags',
                header: 'Tags',
                Cell: ({ cell }) => <ChipArray chipList={cell.getValue<string[]>()} size="md" bgColor="blue" />
            }
        ],
        []
    );

    return <DataGridCard rows={rows} columns={columns} showLoading={loading} density="xs" />;
}

export default TaxonomyTable;
