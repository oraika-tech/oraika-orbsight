import { NoMaxWidthTooltip } from 'mantine-components/components/NoMaxWidthTooltip';
import Link from 'next/link';
import classes from './LinkCell.module.css';

export default function LinkCell({ title, link }) {
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
