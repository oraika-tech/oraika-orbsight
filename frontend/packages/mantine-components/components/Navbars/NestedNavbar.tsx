import { Navbar, ScrollArea, Title, createStyles, rem } from '@mantine/core';
import Link from 'next/link';
import { UserButton } from '../Buttons/UserButton';
import { LinksGroup } from './NavbarLinksGroup';

export interface SubLinkData {
    label: string;
    icon?: any;
    link: string;
}

export interface LinkData {
    label: string;
    icon: any;
    link?: string;
    initiallyOpened?: boolean;
    links?: SubLinkData[];
}

interface NavbarNestedProps {
    links: LinkData[];
    opened: boolean,
    name: string
    email: string
}

const useStyles = createStyles((theme) => ({
    navbar: {
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.white,
        paddingBottom: 0,
        borderRadius: '5px'
    },
    hidden: {
        display: 'none'
    },
    header: {
        padding: theme.spacing.md,
        paddingTop: 0,
        marginLeft: `calc(${theme.spacing.md} * -1)`,
        marginRight: `calc(${theme.spacing.md} * -1)`,
        color: theme.colorScheme === 'dark' ? theme.white : theme.black,
        borderBottom: `${rem(1)} solid ${theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]}`
    },

    links: {
        marginLeft: `calc(${theme.spacing.md} * -1)`,
        marginRight: `calc(${theme.spacing.md} * -1)`
    },

    linksInner: {
        paddingTop: theme.spacing.xl,
        paddingBottom: theme.spacing.xl
    },

    footer: {
        marginLeft: `calc(${theme.spacing.md} * -1)`,
        marginRight: `calc(${theme.spacing.md} * -1)`,
        borderTop: `${rem(1)} solid ${theme.colorScheme === 'dark' ? theme.colors.dark[4] : theme.colors.gray[3]}`
    }
}));

export default function NavbarNested({ links, opened, name, email }: NavbarNestedProps) {
    const { classes } = useStyles();
    const linksGroup = links.map((item) => <LinksGroup {...item} key={item.label} />);

    return (
        <Navbar height="90vh" width={{ sm: 250 }} p="md" hidden className={opened ? classes.navbar : classes.hidden}>
            <Navbar.Section className={classes.header}>
                <Link href="/" style={{ textDecoration: 'none' }}>
                    <Title order={3}>
                        OrbSight
                    </Title>
                </Link>
            </Navbar.Section>

            <Navbar.Section grow className={classes.links} component={ScrollArea}>
                <div className={classes.linksInner}>{linksGroup}</div>
            </Navbar.Section>

            <Navbar.Section className={classes.footer}>
                <UserButton
                    image=""
                    name={name}
                    email={email}
                />
            </Navbar.Section>
        </Navbar>
    );
}
