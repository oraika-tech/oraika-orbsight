import { SimpleGrid } from '@mantine/core';
import IconComponent, { IconComponentProps } from '../IconComponent/IconComponent';

type IconDirection = 'row' | 'column';

interface IconGroupProps {
    iconGroup: IconComponentProps[]
    height: number
    direction?: IconDirection
    cols?: number
    mcols?: number
    scols?: number
    spacing?: number
}

function getColumn(direction: IconDirection, elementCount: number, cols: number) {
    return (direction === 'row') ? Math.ceil(elementCount / cols) : cols;
}

export default function IconGroup({ iconGroup, height, spacing, direction, cols, scols, mcols }: IconGroupProps) {
    const colsx = cols || 1;
    const scolsx = scols || colsx;
    const mcolsx = mcols || scolsx;
    const columns = getColumn(direction || 'row', iconGroup.length, colsx);
    const scolumns = getColumn(direction || 'row', iconGroup.length, scolsx);
    const mcolumns = getColumn(direction || 'row', iconGroup.length, mcolsx);
    return (
        <SimpleGrid
            spacing={spacing}
            cols={columns}
            breakpoints={[
                { maxWidth: 576, cols: scolumns },
                { maxWidth: 992, cols: mcolumns }
            ]}
        >
            {iconGroup.map((iconComponent) =>
                <IconComponent
                    key={iconComponent.src.src}
                    height={height}
                    src={iconComponent.src}
                    alt={iconComponent.alt}
                />
            )}
        </SimpleGrid>
    );
}

IconGroup.defaultProps = {
    direction: 'row',
    cols: 1,
    spacing: 10
};
