import {
    Box,
    Collapse,
    Group,
    ThemeIcon,
    UnstyledButton,
    createStyles,
    rem
} from '@mantine/core';
import { IconChevronLeft, IconChevronRight } from '@tabler/icons-react';
import Link from 'next/link';
import { useState } from 'react';
import ConditionalLink from '../Link/ConditionalLink';

const useStyles = createStyles((theme) => ({
    control: {
        fontWeight: 500,
        display: 'block',
        width: '100%',
        padding: `${theme.spacing.xs} ${theme.spacing.md}`,
        color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.black,
        fontSize: theme.fontSizes.sm,

        '&:hover': {
            backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
            color: theme.colorScheme === 'dark' ? theme.white : theme.black
        }
    },

    sideLink: {
        textDecoration: 'none',
        color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7]
    },

    link: {
        fontWeight: 500,
        display: 'block',
        textDecoration: 'none',
        padding: `${theme.spacing.xs} ${theme.spacing.md}`,
        paddingLeft: rem(31),
        marginLeft: rem(30),
        fontSize: theme.fontSizes.sm,
        color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
        borderLeft: `${rem(1)} solid ${theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]
            }`,

        '&:hover': {
            backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
            color: theme.colorScheme === 'dark' ? theme.white : theme.black
        }
    },

    chevron: {
        transition: 'transform 200ms ease'
    }
}));

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

function getSubLinkItem({ icon: LinkIcon, label, link }: LinkProps, classes: { [key: string]: string }) {
    return (
        <Link
            className={classes.link}
            href={link}
            key={label}
        >
            <Group spacing="xs">
                {LinkIcon && (
                    <ThemeIcon variant="light" size={30}>
                        <LinkIcon size="1.1rem" />
                    </ThemeIcon>
                )}
                {label}
            </Group>
        </Link>
    );
}

export function LinksGroup({ icon: Icon, label, initiallyOpened, link, links }: LinksGroupProps) {
    const { classes, theme } = useStyles();
    const hasLinks = Array.isArray(links);
    const [opened, setOpened] = useState(initiallyOpened || false);
    const ChevronIcon = theme.dir === 'ltr' ? IconChevronRight : IconChevronLeft;
    const items = (hasLinks ? links : []).map((linkData) => getSubLinkItem(linkData, classes));

    return (
        <>
            <UnstyledButton onClick={() => setOpened((o) => !o)} className={classes.control}>
                <ConditionalLink className={classes.sideLink} link={link}>
                    <Group position="apart" spacing={0}>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                            <ThemeIcon variant="light" size={30}>
                                <Icon size="1.1rem" />
                            </ThemeIcon>
                            <Box ml="md">
                                {label}
                            </Box>
                        </Box>
                        {hasLinks && (
                            <ChevronIcon
                                className={classes.chevron}
                                size="1rem"
                                stroke={1.5}
                                style={{
                                    transform: opened ? `rotate(${theme.dir === 'rtl' ? -90 : 90}deg)` : 'none'
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
