import {
    Box,
    Burger, Center,
    createStyles,
    Divider,
    Drawer,
    Group,
    Header,
    Image,
    Menu,
    ScrollArea,
    Stack
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconChevronDown } from '@tabler/icons-react';
import LOGO from 'assets/images/oraika-logo.png';
import { ColorSchemeToggle } from 'mantine-components/components/ColorSchemeToggle';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState } from 'react';

const useStyles = createStyles((theme) => ({
    header: {
        position: 'fixed',
        borderBottom: 'unset'
    },
    container: {
        borderRadius: 10,
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
        borderBottom: `1px solid ${theme.colorScheme === 'dark' ? theme.colors.dark[3] : theme.colors.gray[5]}`,
        height: '100%'
    },
    link: {
        display: 'flex',
        alignItems: 'center',
        height: '100%',
        paddingLeft: theme.spacing.sm,
        paddingRight: theme.spacing.sm,
        textDecoration: 'none',
        color: theme.colorScheme === 'dark' ? theme.white : theme.black,
        fontWeight: 500,
        fontSize: theme.fontSizes.md,

        [theme.fn.smallerThan('sm')]: {
            height: 42,
            display: 'flex',
            alignItems: 'center',
            width: '100%'
        },

        ...theme.fn.hover({
            backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0],
            textDecoration: 'none'
        })
    },

    subLink: {
        width: '100%',
        padding: `${theme.spacing.xs}px ${theme.spacing.md}px`,
        borderRadius: theme.radius.md,

        ...theme.fn.hover({
            backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0]
        }),

        '&:active': theme.activeStyles
    },

    dropdownFooter: {
        backgroundColor: theme.colorScheme === 'dark' ? theme.colors.dark[7] : theme.colors.gray[0],
        margin: -theme.spacing.md,
        marginTop: theme.spacing.sm,
        padding: `${theme.spacing.md}px calc(${theme.spacing.md} * 2)px`,
        paddingBottom: theme.spacing.xl,
        borderTop: `1px solid ${theme.colorScheme === 'dark' ? theme.colors.dark[5] : theme.colors.gray[1]
            }`
    },

    hiddenTablet: {
        [theme.fn.smallerThan('md')]: {
            display: 'none'
        }
    },

    hiddenMobile: {
        [theme.fn.smallerThan('sm')]: {
            display: 'none'
        }
    },

    hiddenDesktop: {
        [theme.fn.largerThan('md')]: {
            display: 'none'
        }
    },

    linkActive: {
        '&, &:hover': {
            backgroundColor: theme.fn.variant({ variant: 'light', color: theme.primaryColor })
                .background,
            color: theme.fn.variant({ variant: 'light', color: theme.primaryColor }).color
        }
    },

    linkLabel: {
        marginRight: 5
    }
}));

export interface HeaderLink {
    link: string;
    label: string;
    links?: HeaderLink[];
}

interface HeaderSearchProps {
    links: HeaderLink[];
}

export function HeaderMegaMenu({ links }: HeaderSearchProps) {
    const { asPath } = useRouter();
    const [drawerOpened, { toggle: toggleDrawer, close: closeDrawer }] = useDisclosure(false);
    // const [linksOpened, { toggle: toggleLinks }] = useDisclosure(false);
    const [active, setActive] = useState(asPath);
    const { classes, theme, cx } = useStyles();

    const items = links.map((link) => {
        const menuItems = link.links?.map((item) => (
            <Menu.Item key={item.link}>
                <Link
                    key={item.label}
                    href={item.link}
                    rel="noreferrer"
                    target={item.link.startsWith('http') ? '_blank' : '_self'}
                    className={cx(classes.link, { [classes.linkActive]: active.endsWith(item.link) })}
                >
                    {item.label}
                </Link>
            </Menu.Item>
        ));

        if (menuItems) {
            return (
                <Menu key={link.label} trigger="hover" transitionProps={{ exitDuration: 0 }}>
                    <Menu.Target>
                        <Link
                            href={link.link}
                            className={cx(classes.link, {
                                [classes.linkActive]: active.endsWith(link.link)
                            })}
                        >
                            <Center>
                                <span className={classes.linkLabel}>{link.label}</span>
                                <IconChevronDown size={12} stroke={1.5} />
                            </Center>
                        </Link>
                    </Menu.Target>
                    <Menu.Dropdown>{menuItems}</Menu.Dropdown>
                </Menu>
            );
        }

        return (
            <Link
                key={link.label}
                href={link.link}
                className={cx(classes.link, { [classes.linkActive]: active.endsWith(link.link) })}
                onClick={() => {
                    setActive(link.link);
                }}
            >
                {link.label}
            </Link>
        );
    });

    return (
        <Box>
            <Header className={classes.header} height={60} px="md">
                <Group position="apart" sx={{ height: '100%' }}>
                    <Group spacing={0}>
                        <Link href={process.env.NEXT_PUBLIC_HOME_URL} target="_blank">
                            <Image height={40} src={LOGO.src} alt="oraika" />
                        </Link>
                    </Group>

                    <Group sx={{ height: '100%' }} spacing={10} className={classes.hiddenTablet}>
                        {items}
                    </Group>

                    <Group position="right" noWrap>
                        {/* <Group className={classes.hiddenMobile}> */}
                        {/* <LoginButton /> */}
                        {/* <SignUpButton /> */}
                        {/* </Group> */}
                        <ColorSchemeToggle />
                        <Burger
                            opened={drawerOpened}
                            onClick={toggleDrawer}
                            className={classes.hiddenDesktop}
                        />
                    </Group>
                </Group>
            </Header>

            <Drawer
                opened={drawerOpened}
                onClose={closeDrawer}
                size="100%"
                padding="md"
                title="Navigation"
                className={classes.hiddenDesktop}
                zIndex={1000000}
            >
                <ScrollArea sx={{ height: 'calc(100vh - 60px)' }} mx="-md">
                    <Divider
                        my="sm"
                        color={theme.colorScheme === 'dark' ? 'dark.5' : 'gray.1'}
                    />

                    <Stack spacing={5}>
                        {items}
                    </Stack>

                    {/* <Divider
                        my="sm"
                        color={theme.colorScheme === 'dark' ? 'dark.5' : 'gray.1'}
                    /> */}

                    {/* <Group position="center" grow pb="xl" px="md">
                        <LoginButton />
                        <SignUpButton />
                    </Group> */}
                </ScrollArea>
            </Drawer>
        </Box>
    );
}
