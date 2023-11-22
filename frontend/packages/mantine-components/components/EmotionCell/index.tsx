import { Text } from '@mantine/core';

interface EmotionCellParams {
    emotion: string
}

export default function EmotionCell({ emotion }: EmotionCellParams) {
    let sx = {};
    const emotionText = emotion;
    switch (emotion) {
        case 'Positive':
            sx = { backgroundColor: 'lightgreen' };
            break;
        case 'Negative':
            sx = { backgroundColor: 'red', color: 'common.white' };
            break;
        case 'Undetermined':
            sx = { backgroundColor: 'lightgray' };
            // emotionText = '-  NA  -'
            break;
        default:
            break;
    }
    return (
        <Text
            style={{
                ...sx,
                fontSize: '1rem',
                overflow: 'hidden',
                width: '100%',
                padding: '1rem'
            }}
        >
            {emotionText}
        </Text>
    );
}
