/* eslint-disable no-case-declarations */
import { Card, Grid, Loader, Paper, Text, createStyles } from '@mantine/core';
import { trackFilter } from 'common-utils/scripts/mixpanel';
import { arrayEquals } from 'common-utils/utils';
import ReactEcharts from 'echarts-for-react';
import DataGridCard from 'mantine-components/components/DataGridCard';
import GenericFilterPanel, { FilterChangeEvent } from 'mantine-components/components/GenericFilterPanel';
import LiveFeedTable from 'mantine-components/components/LiveFeedTable';
import { Heading } from 'mantine-components/components/Simple/Heading';
import { StatsCard } from 'mantine-components/components/StatsCard';
import { MiniStatisticsCard, StatsCardTitleProps } from 'mantine-components/components/StatsCard/MiniStatisticsCard';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import LiveFeedWrapper from '../../business-logic/live-feed/LiveFeedWrapper';
import HomeTextAnalysis from '../../business-logic/text-analysis/HomeTextAnalysis';
import { getDashboard } from '../../lib/service/dashboard-service';

interface ChartConfig {
    type: string
    option: { tooltip: { formatter: string | ((params: any) => string) } }
    chart_type: string
}

interface Field {
    field: string
}

export interface FieldValue {
    field: string
    value: any
}

interface Component {
    identifier: string
    type: string
    width: number
    height?: string
    name?: string
    inputs?: FieldValue[]
    outputs?: string[]
}

interface ComponentLayout {
    spacing: number
    variables: Field[]
    components: Component[]
}

interface FilterValue {
    name: string
    values: string[]
    operator: string
}

export interface Dashboard {
    identifier: string
    frontend_keys: string[]
    title: string
    component_layout?: ComponentLayout
}

interface DynamicDashboardProps {
    dashboard_id: string
}

export function getValue(arrayObj: FieldValue[], key: string) {
    const result = arrayObj.find((obj) => obj.field === key);
    return result ? result.value : null;
}

const useStyles = createStyles(() => ({
    loader: {
        position: 'absolute',
        top: '50%',
        left: '50%',
        transform: 'translate(-50%, -50%)'
    }
}));

export default function DynamicDashboard({ dashboard_id }: DynamicDashboardProps) {
    const { classes } = useStyles();
    const location = useRouter();

    const [loading, setLoading] = useState<boolean>(false);
    const [filterValues, setFilterValues] = useState<FilterValue[]>([]);
    const [dashboardInfo, setDashboardInfo] = useState<Dashboard>(null);

    const handleFilterChange = (filterChangeEvent: FilterChangeEvent) => {
        if (filterChangeEvent.newValues.find(value => value.toLocaleLowerCase() === 'all')) {
            if (filterValues.find(filter => filter.name === filterChangeEvent.name)) {
                const cleanValues = filterValues.filter(filter => filter.name !== filterChangeEvent.name);
                trackFilter(location.pathname, cleanValues);
                setFilterValues([...cleanValues]);
            }
        } else {
            const selectedFilterValue = filterValues.find(filter => filter.name === filterChangeEvent.name);
            if (selectedFilterValue) {
                if (!arrayEquals(selectedFilterValue.values, filterChangeEvent.newValues)) {
                    selectedFilterValue.values = filterChangeEvent.newValues;
                    trackFilter(location.pathname, filterValues);
                    setFilterValues([...filterValues]);
                }
            } else {
                setFilterValues(filterValueArray => [...filterValueArray, {
                    name: filterChangeEvent.name,
                    values: filterChangeEvent.newValues,
                    operator: '='
                }]);
            }
        }
        return false;
    };

    const lineTooltipFormatter = (params) => {
        let output = `<b>${params[0].axisValueLabel.replace(' 00:00:00', '')}</b><br/>`;
        for (let i = 0; i < params.length; i += 1) {
            const dim = params[i].dimensionNames[params[i].encode.y[0]];
            if (dim in params[i].value) {
                output += `${params[i].marker + params[i].seriesName}: ${params[i].value[dim]}`;
                if (i !== params.length - 1) { // Append a <br/> tag if not last in loop
                    output += '<br/>';
                }
            }
        }
        return output;
    };

    useEffect(() => {
        const syncDashboard = (filterValueList: FilterValue[]) => {
            getDashboard(dashboard_id, filterValueList)
                .then(dashboardResp => {
                    setLoading(false);
                    setDashboardInfo(dashboardResp);
                })
                .catch(() => {
                    setLoading(false);
                });
        };

        setLoading(true);
        syncDashboard(filterValues);

        // return () => setDashboardInfo(null)
    }, [filterValues, dashboard_id]);

    if (!dashboardInfo) {
        return (
            <Card sx={{ height: '40vh', paddingTop: '30vh', alignItems: 'center' }}>
                {loading
                    ? <Loader className={classes.loader} />
                    : <Text>Something went wrong, try again !</Text>
                }
            </Card>
        );
    }

    const layout = dashboardInfo.component_layout;
    const getGridComponents = (components) => {
        const localGridComponents = [];
        for (let i = 0; i < components.length; i += 1) {
            const component = components[i];
            switch (component.type) {
                case 'chart':
                    const chartConfig: ChartConfig = getValue(component.inputs, 'chart_config');
                    switch (chartConfig.chart_type) {
                        case 'echarts':
                            if (chartConfig.option.tooltip) {
                                switch (chartConfig.option.tooltip.formatter) {
                                    case 'lineTooltipFormatter':
                                        chartConfig.option.tooltip.formatter = lineTooltipFormatter;
                                        break;
                                }
                            }
                            const styleConfig = component.height ? { height: component.height } : {};
                            localGridComponents.push(
                                <Grid.Col
                                    key={component.identifier || component.name}
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Card>
                                        <ReactEcharts
                                            notMerge
                                            showLoading={loading}
                                            style={{ ...styleConfig, padding: '0.5rem' }}
                                            option={chartConfig.option}
                                        />
                                    </Card>
                                </Grid.Col>
                            );
                            break;
                        default:
                            // eslint-disable-next-line no-console
                            console.log(`Wrong chart name: ${chartConfig.type}`);
                    }
                    break;
                case 'react-component':
                    switch (component.name) {
                        case 'FilterPanel':
                            const filtersData = getValue(component.inputs, 'filters');
                            const showFilterButton = getValue(component.inputs, 'showFilterButton');
                            filtersData.forEach(filter => {
                                // eslint-disable-next-line no-param-reassign
                                filter.width = filter.xs;
                            });
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Paper>
                                        <GenericFilterPanel
                                            filtersData={filtersData}
                                            filterHandler={handleFilterChange}
                                            showFilterButton={showFilterButton}
                                        />
                                    </Paper>
                                </Grid.Col>
                            );
                            break;
                        case 'LiveFeedTable':
                            const liveFeeds = getValue(component.inputs, 'live_feeds');
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Card>
                                        <LiveFeedTable showLoading={loading} dataset={liveFeeds} />
                                    </Card>
                                </Grid.Col>
                            );
                            break;
                        case 'Heading':
                            const title = getValue(component.inputs, 'title');
                            const style = getValue(component.inputs, 'style');

                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Heading title={title} sx={style} />
                                </Grid.Col>
                            );
                            break;
                        case 'SimpleTable':
                            const tableData = getValue(component.inputs, 'table_data');
                            const colDefs = getValue(component.inputs, 'column_definition');
                            const maxRows = getValue(component.inputs, 'max_rows') || 10;
                            if (tableData && colDefs) {
                                const col_nos = colDefs.length;
                                const rows = tableData.slice(1).map((row: string[]) => {
                                    const rowData = {
                                        id: row[0]
                                    };
                                    for (let j = 0; j < col_nos; j += 1) {
                                        rowData[colDefs[j].accessorKey] = row[j];
                                    }
                                    return rowData;
                                });
                                const multiPage = rows.length > maxRows;
                                // const effectiveLength = multiPage ? maxRows : rows.length;
                                // const footerHeight = multiPage ? 1.5 : 0;

                                // const titleHeight = 3;
                                // const headerHeight = 1.1;
                                // const rowHeight = 2.25;
                                // const totalRowHeight = (effectiveLength + 1.1 + footerHeight) * rowHeight;
                                // const tableHeight = `${totalRowHeight + headerHeight + titleHeight}rem`;
                                localGridComponents.push(
                                    <Grid.Col
                                        xs={component.xs}
                                        sm={component.sm}
                                        md={component.md}
                                        lg={component.lg}
                                        xl={component.xl}
                                    >
                                        <DataGridCard
                                            title={component.title}
                                            showLoading={loading}
                                            hideFooter={!multiPage}
                                            autoHeight={!multiPage}
                                            density="xs"
                                            rows={rows}
                                            columns={colDefs}
                                            sx={{ padding: '0.5rem' }}
                                        />
                                    </Grid.Col>
                                );
                            } else {
                                localGridComponents.push(
                                    <Card
                                        sx={{
                                            height: '10rem',
                                            width: '100%',
                                            alignItems: 'center',
                                            justifyContent: 'center'
                                        }}
                                    >
                                        <Text>Something went wrong, try again !</Text>
                                    </Card>
                                );
                            }
                            break;
                        case 'StatsCard':
                            const template = getValue(component.inputs, 'template');
                            const seriesData = getValue(component.inputs, 'series_data');
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <StatsCard
                                        height={component.height}
                                        template={template}
                                        values={seriesData}
                                    />
                                </Grid.Col>
                            );
                            break;
                        case 'TextAnalysis':
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <HomeTextAnalysis height={component.height} />
                                </Grid.Col>
                            );
                            break;
                        case 'LiveFeed':
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}

                                >
                                    <LiveFeedWrapper isTitle={false} height={component.height} />
                                </Grid.Col>
                            );
                            break;
                        case 'MiniStatisticsCard':
                            const statsTitle: StatsCardTitleProps = { text: getValue(component.inputs, 'text') };
                            const count = getValue(component.inputs, 'count');
                            const percentage = getValue(component.inputs, 'percentage');
                            const iconColor = getValue(component.inputs, 'icon_color');
                            const icon = getValue(component.inputs, 'icon');
                            /*
                                check: src/assets/theme/base/breakpoints.js
                                xs, extra-small :    0 -  576 px : mobile
                                sm, small       :  576 -  768 px : tablet, landscape mobile
                                md, medium      :  768 -  992 px : landscape tablet
                                lg, large       :  992 - 1200 px : laptop
                                xl, extra-large : 1200 - 1400 px : wide laptop
                                xxl,xxtra-large : 1400 -  ∞   px : tv
                            */
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <MiniStatisticsCard
                                        title={statsTitle}
                                        count={count}
                                        percentage={{ color: ['green', 'red'], text: percentage }}
                                        icon={icon}
                                        countColor={iconColor}
                                    />
                                </Grid.Col>
                            );
                            break;
                        case 'EmptyCard':
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Card sx={{ minHeight: component.height }}>
                                        &nbsp;
                                    </Card>
                                </Grid.Col>
                            );
                            break;
                        case 'Grid':
                            const childGridComponents = getGridComponents(component.components);
                            localGridComponents.push(
                                <Grid.Col
                                    xs={component.xs}
                                    sm={component.sm}
                                    md={component.md}
                                    lg={component.lg}
                                    xl={component.xl}
                                >
                                    <Grid gutter={layout.spacing}>
                                        {childGridComponents}
                                    </Grid>
                                </Grid.Col>
                            );
                            break;
                        default:
                        // console.log(`Wrong component name: ${component.name}`);
                        // send sentry event
                    }
                    break;
                default:
                // console.log(`Wrong component type: ${component.type}`);
                // send sentry event
            }
        }
        return localGridComponents;
    };

    const gridComponents = getGridComponents(layout.components);

    return (
        <Grid gutter={layout.spacing}>
            {gridComponents}
        </Grid>
    );
}
