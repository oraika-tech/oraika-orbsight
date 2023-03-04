import { createStyles, SimpleGrid } from '@mantine/core';
import IconTextVertical, { IconTextVerticalProps } from './IconTextVertical';

const useStyles = createStyles((theme) => ({
    simplegrid: {
        width: '99%'
    }
}));

interface IconGridProps {
    items: IconTextVerticalProps[]
}

export default function IconGridDefault({ items }: IconGridProps) {
    const { classes } = useStyles();
    const gridItems = items.map(item => <IconTextVertical key={item.label} icon={item.icon} label={item.label} />);

    return (
        <SimpleGrid
            className={classes.simplegrid}
            breakpoints={[
                { maxWidth: 1980, cols: 4, spacing: 'lg' },
                { maxWidth: 980, cols: 3, spacing: 'md' },
                { maxWidth: 550, cols: 2, spacing: 'sm' },
                { maxWidth: 400, cols: 1, spacing: 'sm' }
            ]}
            verticalSpacing={60}
        >
            {gridItems}
        </SimpleGrid>
    );
}
