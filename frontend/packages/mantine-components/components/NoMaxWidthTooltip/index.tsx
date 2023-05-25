import { Tooltip, TooltipProps } from '@mantine/core';

const noMaxWidthTooltipStyle = {
    maxWidth: 'none'
};

const NoMaxWidthTooltip = ({ label, children, className, ...props }: TooltipProps) => (
    <Tooltip
        {...props}
        label={label}
        className={`${className} no-max-width-tooltip`}
        style={noMaxWidthTooltipStyle}
    >
        {children}
    </Tooltip>
);

export { NoMaxWidthTooltip };
