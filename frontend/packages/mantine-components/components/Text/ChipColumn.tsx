/* eslint-disable react/jsx-indent-props */
import { Card, Loader, Text } from '@mantine/core';
import ChipArray from '../Chip/ChipArray';

interface ChipColumnProps {
    title: string;
    words: string[];
    isLoading: boolean;
    bgColor?: string;
    height?: string;
}

export default function ChipColumn({ title, words, isLoading, bgColor, height }: ChipColumnProps) {
    const sx = { height };

    return (
        <Card style={{ ...sx, paddingTop: '0.3rem', paddingBottom: '0.5rem' }}>
            <Text style={{ fontSize: '1.1rem', padding: '1%', fontWeight: 500, textAlign: 'center' }}>
                {title}
            </Text>
            {isLoading
                ? <Loader />
                : words?.length > 0
                    ? <ChipArray
                        sx={{ fontWeight: 500, fontSize: '1rem', flexWrap: 'wrap', minWidth: '8rem' }}
                        chipList={words}
                        direction="column"
                        bgColor={bgColor}
                        spacing={0.5}
                    />
                    : <Text style={{ fontWeight: 800, paddingTop: '7rem', textAlign: 'center' }}> No Data ! </Text>
            }
        </Card>
    );
}

ChipColumn.defaultProps = {
    height: undefined
};
