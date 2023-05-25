/* eslint-disable react/jsx-indent-props */
import { Card, Stack, Title } from '@mantine/core';
import { MRT_DensityState, MantineReactTable } from 'mantine-react-table';
import { useEffect, useState } from 'react';
import './style.css';

function isLoading(showLoading: boolean, rows: any[]) {
    return showLoading ?? (rows == null);
}

interface DataGridCardProps {
    title?: string
    showLoading: boolean
    density?: MRT_DensityState // require page reload to reflect
    hideFooter?: boolean
    autoHeight?: boolean
    rows: any[]
    columns: any[]
    sx?: any
}

export default function DataGridCard(
    { title, showLoading, density, hideFooter, autoHeight, rows, columns, sx }: DataGridCardProps) {
    const [showLoader, setShowLoader] = useState(isLoading(showLoading, rows));
    const stopShowLoader = () => {
        setShowLoader(false);
    };
    useEffect(() => {
        if (isLoading(showLoading, rows)) {
            setShowLoader(true);
            setTimeout(stopShowLoader, 10000);
        } else {
            stopShowLoader();
        }
    }, [showLoading, rows]);
    const sxStyle = showLoader ? { alignItems: 'center', paddingTop: '20%' } : {};
    return (
        <Card sx={{ ...sx, ...sxStyle }}>
            <Stack spacing="md">
                {title &&
                    <Title order={2}>
                        {title}
                    </Title>
                }
                <MantineReactTable
                    autoResetPageIndex={!autoHeight}
                    state={{ isLoading: showLoader }}
                    data={rows}
                    columns={columns}
                    enableBottomToolbar={!hideFooter && rows.length > 10}
                    enableTopToolbar={false}
                    initialState={{ density }}
                />
            </Stack>
        </Card>
    );
}

DataGridCard.defaultProps = {
    title: null,
    density: 'md',
    hideFooter: false,
    autoHeight: false
};
