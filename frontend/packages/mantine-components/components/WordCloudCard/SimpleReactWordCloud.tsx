import ReactWordcloud, { Optional, Options } from 'react-wordcloud';

export interface WordCloudTag {
    term: string
    weight: number
}

interface Props {
    data: Array<WordCloudTag>
}

export default function SimpleReactWordcloud({ data }: Props) {
    const words = data.slice(0, 30).map((word) => ({
        text: word.term,
        value: word.weight
    }));

    const options: Optional<Options> = {
        rotations: 0, // 0 - off, > 0 - division of angle range
        rotationAngles: [-30, -30],
        transitionDuration: 0,
        // deterministic: true,
        fontSizes: [24, 96],
        fontFamily: 'Tahoma',
        enableTooltip: false,
        padding: 4
    };

    return (
        <ReactWordcloud
            words={words}
            options={options}
        />
    );
}
