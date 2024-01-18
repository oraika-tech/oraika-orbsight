import { Card, Center, Loader, Title } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import WordCloudCard from '.';
import { WordCloudTag } from './SimpleReactWordCloud';

interface WordCloudPanelProps {
    title: string
    words?: WordCloudTag[]
    height?: string
    isLoading: boolean
}

export default function WordCloudPanel({ title, words, height, isLoading }: WordCloudPanelProps) {
    return (
        <Card style={{ minHeight: '45vh' }}>
            <Title order={2} style={{ fontWeight: 800, textAlign: 'center' }}>
                {title} World Cloud
            </Title>
            {isLoading
                ? <Center h={200}><Loader /></Center>
                : words === undefined
                    ? (
                        <Title order={2} style={{ fontWeight: 800, paddingTop: '1rem', textAlign: 'center' }}>
                            Please select filter !
                        </Title>
                    )
                    : words.length
                        ? <WordCloudCard height={height || '40vh'} bgColor="lightcyan" data={words} />
                        : <EmptyData />
            }
        </Card>
    );
}
