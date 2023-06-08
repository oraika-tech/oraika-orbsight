/* eslint-disable max-len */
import { Card, Center, Grid, Loader, Title } from '@mantine/core';
import EmptyData from 'mantine-components/components/AlertMessage/EmptyData';
import ChipArray from 'mantine-components/components/Chip/ChipArray';

interface KeyPhrasesPanelProps {
    title: string
    keyPhrases?: string[]
    chipColor?: string
    isLoading?: boolean
}

function getNArrays(strArray: string[], chunks: number) {
    const result = [];
    const n = Math.ceil(strArray.length / chunks);
    for (let i = 0; i < strArray.length; i += n) {
        result.push(strArray.slice(i, i + n));
    }
    return result;
}

export default function KeyPhrasesPanel({ title, keyPhrases, chipColor, isLoading }: KeyPhrasesPanelProps) {
    // divide keyPhrases string array to n number of chunks
    const keyPhrasesList = getNArrays(keyPhrases || [], 2);
    return (
        <Card style={{ textAlign: 'center', minHeight: '45vh', maxHeight: '85vh', overflow: 'scroll' }}>
            <Grid style={{ height: '90%' }} gutter="xl">
                <Grid.Col xs={12}>
                    <Title style={{ fontWeight: 800 }} order={2}>{title} Key Phrases</Title>
                </Grid.Col>
                <Grid.Col xs={12} style={{ height: '100%' }}>
                    {isLoading
                        ? <Center h={200}><Loader /></Center>
                        : keyPhrases === undefined
                            ? (
                                <Title
                                    order={3}
                                    style={{
                                        fontWeight: 800,
                                        paddingTop: '1rem',
                                        textAlign: 'center'
                                    }}
                                >
                                    Please select filter !
                                </Title>
                            )
                            : keyPhrases.length
                                ? (
                                    <Grid style={{ justifyContent: 'left' }} gutter="sm">
                                        {keyPhrasesList.map((phrases) => (
                                            <Grid.Col key={phrases[0]} span={12} xs={6} md={12} lg={6}>
                                                <ChipArray
                                                    sx={{
                                                        fontWeight: 700,
                                                        fontSize: '0.8rem',
                                                        flexWrap: 'wrap',
                                                        minWidth: '13.5rem',
                                                        height: '1.5rem'
                                                    }}
                                                    chipList={phrases}
                                                    direction="column"
                                                    spacing="xs"
                                                    size="sm"
                                                    bgColor={chipColor}
                                                />
                                            </Grid.Col>
                                        ))}
                                    </Grid>
                                )
                                : <EmptyData />
                    }
                    <Grid.Col xs={6} />
                </Grid.Col>
            </Grid>
        </Card>
    );
}
