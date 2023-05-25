import { Badge } from '@mantine/core';

interface HighlightedProps {
    text?: string;
    chipHighlights?: string[];
    markHighlights?: string[];
}

export default function Highlighted({ text = '', chipHighlights = [], markHighlights = [] }: HighlightedProps) {
    const wordRegex = /^\w+$/;

    const arrayToRegex = (arr: string[]) => arr
        .map(el => wordRegex.test(el) ? `\\b${el}\\b` : el)
        .join('|');

    if (chipHighlights.length === 0 && markHighlights.length === 0) {
        return <span>{text}</span>;
    }
    const chipExpression = arrayToRegex(chipHighlights);
    const markExpression = arrayToRegex(markHighlights);
    const wholeExpression = chipExpression ? `${chipExpression}|${markExpression}` : markExpression;
    const chipRegex = new RegExp(`^${chipExpression}$`, 'gi');
    const markRegex = new RegExp(`^${markExpression}$`, 'gi');
    const wholeRegex = new RegExp(`(${wholeExpression})`, 'gi');
    const parts = text.split(wholeRegex);

    return (
        <span>
            {parts.filter(String).map((part, i) => chipRegex.test(part)
                ? <Badge sx={{ fontWeight: 500 }} key={i} size="small" color="success">{part}</Badge>
                : markRegex.test(part)
                    ? <mark key={i}>{part}</mark>
                    : <span key={i}>{part}</span>)}
        </span>
    );
}
