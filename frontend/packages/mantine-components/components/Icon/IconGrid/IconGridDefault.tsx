import { SimpleGrid } from '@mantine/core';
import classes from './IconGridDefault.module.css';
import IconTextVertical, { IconTextVerticalProps } from './IconTextVertical';

interface IconGridProps {
    items: IconTextVerticalProps[]
}

export default function IconGridDefault({ items }: IconGridProps) {
    const gridItems = items.map(item => <IconTextVertical key={item.label} icon={item.icon} label={item.label} />);

    return (
        <SimpleGrid
            className={classes.simplegrid}
            cols={{ base: 1, xs: 2, sm: 3, xl: 4 }}
            spacing={{ base: 'sm', xs: 'md', xl: 'lg' }}
            verticalSpacing={60}
        >
            {gridItems}
        </SimpleGrid>
    );
}
