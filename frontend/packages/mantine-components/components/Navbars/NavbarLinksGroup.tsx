import { Box, Collapse, Group, ThemeIcon, UnstyledButton } from '@mantine/core';
import { IconChevronRight } from '@tabler/icons-react';
import Link from 'next/link';
import { useState } from 'react';
import ConditionalLink from '../Link/ConditionalLink';
import classes from './NavbarLinksGroup.module.css';

interface LinkProps {
    label: string;
    icon?: React.FC<any>;
    link: string;
}
interface LinksGroupProps {
    icon: React.FC<any>;
    label: string;
    initiallyOpened?: boolean;
    link?: string;
    links?: LinkProps[];
}

function getSubLinkItem({ icon: LinkIcon, label, link }: LinkProps) {
    return (
        <Link
            className={classes.link}
            href={link}
            key={label}
        >
            <Group gap={0}>
                {LinkIcon && (
                    <ThemeIcon size={30}>
                        <LinkIcon size="1.1rem" />
                    </ThemeIcon>
                )}
                {label}
            </Group>
        </Link>
    );
}

export function LinksGroup({ icon: Icon, label, initiallyOpened, link, links }: LinksGroupProps) {
    const hasLinks = Array.isArray(links);
    const [opened, setOpened] = useState(initiallyOpened || false);
    const ChevronIcon = IconChevronRight;
    const items = (hasLinks ? links : []).map((linkData) => getSubLinkItem(linkData));

    return (
        <>
            <UnstyledButton onClick={() => setOpened((o) => !o)} className={classes.control}>
                <ConditionalLink className={classes.sideLink} link={link}>
                    <Group justify="space-between" gap={0}>
                        <Box style={{ display: 'flex', alignItems: 'center' }}>
                            <ThemeIcon size={30}>
                                <Icon size="1.1rem" />
                            </ThemeIcon>
                            {label}
                        </Box>
                        {hasLinks && (
                            <ChevronIcon
                                className={classes.chevron}
                                size="1rem"
                                stroke={1.5}
                                style={{
                                    transform: opened ? `rotate(${-90}deg)` : 'none'
                                }}
                            />
                        )}
                    </Group>
                </ConditionalLink>
            </UnstyledButton>
            {hasLinks ? <Collapse in={opened}>{items}</Collapse> : null}
        </>
    );
}
