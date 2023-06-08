import { Card, Center, Loader, Title } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import WordCloudCard from '.';
import { WordCloudTag } from './SimpleReactWordCloud';

interface WordCloudPanelProps {
    title: string
    words?: WordCloudTag[]
    isLoading: boolean
}

export default function WordCloudPanel({ title, words, isLoading }: WordCloudPanelProps) {
    return (
        <Card sx={{ minHeight: '40vh' }}>
            <Title order={2} sx={{ fontWeight: 800, textAlign: 'center' }}>
                {title} World Cloud
            </Title>
            {isLoading
                ? <Center h={200}><Loader /></Center>
                : words === undefined
                    ? (
                        <Title order={2} sx={{ fontWeight: 800, paddingTop: '1rem', textAlign: 'center' }}>
                            Please select filter !
                        </Title>
                    )
                    : words.length
                        ? <WordCloudCard height="40vh" bgColor="lightcyan" data={words} />
                        : <EmptyData />
            }
        </Card>
    );
}
