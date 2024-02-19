import { getTitleWord } from 'common-utils/utils';
import { getLogoFromObserverType } from 'common-utils/utils/common';
import type { MRT_ColumnDef } from 'mantine-react-table';
import Link from 'next/link';
import { useMemo } from 'react';
import ChipArray from '../Chip/ChipArray';
import DataGridCard from '../DataGridCard';
import IconText from '../IconText';
import TypographyWrap from '../TypographyWrap';

interface LiveFeedTableProps {
    showLoading?: boolean
    dataset?: any[]
}

interface LinkType {
    name: string
    link: string
}

interface TextLinkType {
    text: string
    url: string
}

interface ObserverType {
    name: string
    type: string
}

interface LiveFeedType {
    event_time: string
    rating: number
    emotion: string
    comment: LinkType
    observer: ObserverType
}

export default function LiveFeedTable({ showLoading, dataset }: LiveFeedTableProps) {
    const datasetValue = dataset ?? [];
    const dimensions = datasetValue.length ? datasetValue[0] : [];
    const columnIndex = dimensions ? Object.fromEntries(dimensions.map((e: any, i: any) => [e, i])) : {};

    const dataRows = [];
    let firstRow = true;
    for (const row of datasetValue) {
        if (firstRow) {
            firstRow = false;
        } else {
            dataRows.push({
                id: row[columnIndex.rawDataId],
                event_time: new Date(row[columnIndex.eventTime]).toLocaleString(),
                comment: {
                    text: row[columnIndex.rawText],
                    url: row[columnIndex.url]
                },
                entity_name: row[columnIndex.entity],
                observer: {
                    name: row[columnIndex.observer],
                    type: row[columnIndex.observerType]
                },
                rating: row[columnIndex.rating],
                emotion: getTitleWord(row[columnIndex.emotion]),
                people: row[columnIndex.people],
                author_name: row[columnIndex.author],
                taxonomy_tags: row[columnIndex.taxonomyTags]
            });
        }
    }

    const stringToArray = (tags: string): string[] => {
        if (!tags || tags.trim().length === 0) {
            return [];
        }
        return tags.trim().split(/\s*,\s*/);
    };

    const columns = useMemo<MRT_ColumnDef<LiveFeedType>[]>(
        () => [
            {
                accessorKey: 'event_time',
                header: 'Event Time',
                size: 150
            },
            {
                accessorKey: 'emotion',
                header: 'Emotion',
                size: 80
            },
            {
                accessorKey: 'rating',
                header: 'Rating',
                size: 80
            },
            {
                accessorKey: 'comment',
                header: 'Comment',
                size: 300,
                Cell: ({ cell }) =>
                    process.env.NEXT_PUBLIC_DEMO_MODE === 'true'
                        ? (
                            <TypographyWrap length={cell.getValue<TextLinkType>().text.length}>
                                {cell.getValue<TextLinkType>().text}
                            </TypographyWrap>
                        )
                        : (
                            <Link
                                href={cell.getValue<TextLinkType>().url}
                                target="_blank"
                                rel="noreferrer"
                                color="primary"
                                style={{ textDecoration: 'none' }}
                            >
                                <TypographyWrap maw={400} length={cell.getValue<TextLinkType>().text.length}>
                                    {cell.getValue<TextLinkType>().text}
                                </TypographyWrap>
                            </Link>
                        )
            },
            {
                accessorKey: 'observer',
                header: 'Observer Name',
                size: 150,
                Cell: ({ cell }) =>
                    <IconText
                        icon={getLogoFromObserverType(cell.getValue<ObserverType>().type)}
                        altText={cell.getValue<ObserverType>().type}
                    >
                        {cell.getValue<ObserverType>().name}
                    </IconText>
            },
            {
                accessorKey: 'taxonomy_tags',
                header: 'Tags',
                size: 100,
                Cell: ({ cell }) => <ChipArray chipList={stringToArray(cell.getValue<string>())} />
            },
            {
                accessorKey: 'people',
                header: 'People',
                size: 100,
                Cell: ({ cell }) => <ChipArray chipList={stringToArray(cell.getValue<string>())} bgColor="yellow" />
            }
        ],
        []
    );

    return <DataGridCard
        showLoading={showLoading ?? false}
        rows={dataRows}
        columns={columns}
        density="xs"
        hideFooter={false}
        // fixedHeader={true}
        // fixedFooter={true}
        sx={{ padding: '0.5rem', height: '90vh' }}
    />;
}

LiveFeedTable.defaultProps = {
    showLoading: null
};
