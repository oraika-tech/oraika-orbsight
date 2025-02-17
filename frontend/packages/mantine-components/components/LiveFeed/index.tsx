import { Card, Grid, Title } from '@mantine/core';
import { useEffect, useRef, useState } from 'react';
import FeedCard from './FeedCard';

export interface FeedData {
    rawDataId: number
    eventTime?: Date
    emotion?: string
    entityName: string
    observerType: string
    rawText: string
    textLang?: string
    authorName?: string
    categories: string[]
    taxonomies: string[]
}

interface LiveFeedProps {
    isTitle?: boolean
    height?: string | number
    feeds: FeedData[]
    displayCount: number
}

export default function LiveFeed({ isTitle, height, feeds, displayCount }: LiveFeedProps) {
    const totalFeedSize = 30; // not able to take it from feeds.length
    const containerRef = useRef(null);
    const [feedIndex, setFeedIndex] = useState(0);

    const cycleSelectArray = (list: any[], size: number, index: number) => {
        const newIndex = (index >= list.length) ? 0 : index;
        const newList = list.slice(newIndex, newIndex + size);
        const remainingSize = size - newList.length;
        if (remainingSize > 0) {
            return newList.concat(list.slice(0, remainingSize));
        }
        return newList;
    };

    const doSlide = () => {
        setFeedIndex((index) => (index + 1) >= totalFeedSize ? 0 : index + 1);
    };

    useEffect(() => {
        setInterval(doSlide, 10000);
    }, []);

    const style = height ? { height } : {};

    return (
        <Card padding="md" style={{ ...style, overflow: 'scroll' }} ref={containerRef}>
            <Grid style={{ justifyContent: 'stretch' }}>
                {isTitle && (
                    <Grid.Col span={12}>
                        <Title order={4} style={{ height: '3rem', padding: '1rem' }}>Recent Review</Title>
                    </Grid.Col>
                )}
                {cycleSelectArray(feeds, displayCount, feedIndex).map(feed => (
                    <Grid.Col key={feed.rawDataId} style={{ padding: '0.5rem' }}>
                        <FeedCard {...feed} />
                    </Grid.Col>
                ))}
            </Grid>
        </Card>
    );
}

LiveFeed.defaultProps = {
    isTitle: true,
    height: null
};
