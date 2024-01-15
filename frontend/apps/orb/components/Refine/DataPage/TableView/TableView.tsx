import { Box, Card, Group, Pagination, Table } from '@mantine/core';
import { useTable } from '@refinedev/react-table';
import { ColumnDef, flexRender } from '@tanstack/react-table';
import { useContext } from 'react';
import { EntityField, FieldType, ForeignData, SpecialField } from '../../Common/CommonModels';
import { get_special_field } from '../../Common/CommonUtils';
import { EntityMetaContext } from '../../Common/EntityMetaContext';
import FieldView from '../../Common/FieldView';
import { IModel } from '../../models';
import ControlButtonsPanel from '../ControlButtons/ControlButtonsPanel';
import EnableButton from '../ControlButtons/EnableButton';
import ColumnFilter from './ColumnFilter';
import ColumnSorter from './ColumnSorter';

function getColumnDef(
    resource: string, field: EntityField, idField: string, foreignData: ForeignData
): ColumnDef<IModel> {
    const columnObj: ColumnDef<IModel> = {
        id: field.objectKey,
        header: field.label,
        accessorKey: field.objectKey,
        meta: {
            filterOperator: field.type === 'string' ? 'contains' : 'eq'
        }
    };

    switch (field.type) {
        case FieldType.Boolean:
            if (field.special === SpecialField.Enabled) {
                columnObj.cell = function render({ getValue, row }) {
                    const id = row.original[idField];
                    return <EnableButton resource={resource} id={id} enabled={getValue() as boolean} />;
                };
            } else {
                columnObj.cell = function render({ row }) {
                    return FieldView({
                        rowData: row.original,
                        fieldMeta: field,
                        foreignData
                    });
                };
            }
            break;

        case FieldType.Date:
        case FieldType.Json:
        case FieldType.Array:
        case FieldType.DropDown:
            columnObj.cell = function render({ row }) {
                return FieldView({
                    rowData: row.original,
                    fieldMeta: field,
                    foreignData
                });
            };
            break;
    }
    return columnObj;
}

function get_columns_from_fields(
    resource: string, fields: EntityField[], foreignData: ForeignData
): ColumnDef<IModel>[] {
    const idField = get_special_field(SpecialField.Id, fields).objectKey;
    const enabledField = get_special_field(SpecialField.Enabled, fields);
    const columnList = fields
        .filter((f) =>
            f.special !== SpecialField.Enabled &&
            f.type !== FieldType.Json &&
            !f.isHide &&
            (f.special === SpecialField.Title || f.isSummary == null || f.isSummary)
        )
        .map((field: EntityField) => getColumnDef(resource, field, idField, foreignData));
    columnList.push({
        id: 'actions',
        header: 'Actions',
        accessorKey: idField,
        cell: function render({ getValue }) {
            return (
                <ControlButtonsPanel
                    id={getValue() as string | number}
                    resource={resource}
                    foreignData={foreignData}
                />
            );
        }
    });
    if (enabledField) {
        columnList.push(getColumnDef(resource, enabledField, idField, foreignData));
    }
    return columnList;
}

interface TableViewProps {
    resource: string;
    foreignData: ForeignData;
    enableFilter?: boolean;
    enableSort?: boolean;
}

export default function TableView({ resource, foreignData, enableFilter, enableSort }: TableViewProps) {
    const { fields } = useContext(EntityMetaContext);
    const columns = get_columns_from_fields(resource, fields, foreignData);

    const {
        getHeaderGroups,
        getRowModel,
        getFooterGroups,
        refineCore: { setCurrent, pageCount, current }
    } = useTable({
        refineCoreProps: {
            resource,
            pagination: {
                mode: 'client'
            }
        },
        columns
    });

    return (
        <Card p={15}>
            <Table striped highlightOnHover withTableBorder>
                <Table.Thead>
                    {getHeaderGroups().map((headerGroup) => (
                        <Table.Tr key={headerGroup.id}>
                            {headerGroup.headers.map((header) => (
                                <Table.Th key={header.id}>
                                    {!header.isPlaceholder && (
                                        <Group gap="xs" wrap="nowrap">
                                            <Box>
                                                {flexRender(
                                                    header.column.columnDef.header,
                                                    header.getContext()
                                                )}
                                            </Box>
                                            <Group gap="xs" wrap="nowrap">
                                                {enableSort && header.id !== 'actions' && (
                                                    <ColumnSorter column={header.column} />
                                                )}
                                                {enableFilter &&
                                                    header.id !== 'actions' && header.id !== 'is_enabled' && (
                                                        <ColumnFilter column={header.column} />
                                                    )
                                                }
                                            </Group>
                                        </Group>
                                    )}
                                </Table.Th>
                            ))}
                        </Table.Tr>
                    ))}
                </Table.Thead>
                <Table.Tbody>
                    {getRowModel().rows.map((row) => (
                        <Table.Tr key={row.id}>
                            {row.getVisibleCells().map((cell) => (
                                <Table.Td key={cell.id}>
                                    {flexRender(cell.column.columnDef.cell, cell.getContext())}
                                </Table.Td>
                            ))}
                        </Table.Tr>
                    ))}
                </Table.Tbody>
                <tfoot>
                    {getFooterGroups().map(footerGroup => (
                        <tr key={footerGroup.id}>
                            {footerGroup.headers.map(header => (
                                <th key={header.id}>
                                    {header.isPlaceholder
                                        ? null
                                        : flexRender(
                                            header.column.columnDef.footer,
                                            header.getContext()
                                        )}
                                </th>
                            ))}
                        </tr>
                    ))}
                </tfoot>
            </Table>
            {pageCount > 1 && (
                <Group mt={20} justify="flex-end">
                    <Pagination
                        total={pageCount}
                        value={current}
                        onChange={setCurrent}
                    />
                </Group>
            )}
        </Card>
    );
}

TableView.defaultProps = {
    enableFilter: false,
    enableSort: false
};
