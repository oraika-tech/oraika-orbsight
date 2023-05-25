import { createStyles } from '@mantine/core';
import { NoMaxWidthTooltip } from 'mantine-components/components/NoMaxWidthTooltip';
import Link from 'next/link';

const useStyles = createStyles(() => ({
    link: {
        textDecoration: 'none'
    }
}));

export default function LinkCell({ title, link }) {
    const { classes } = useStyles();
    if (link) {
        return (
            <NoMaxWidthTooltip label={link}>
                <Link
                    className={classes.link}
                    href={link}
                    target="_blank"
                    rel="noopener"
                    color="primary"
                >
                    {title}
                </Link>
            </NoMaxWidthTooltip>
        );
    } else {
        return title;
    }
}
