import {
    Box,
    Burger,
    Button,
    Center,
    createStyles,
    Group,
    Header,
    Image,
    Menu
} from '@mantine/core';
import { useDisclosure } from '@mantine/hooks';
import { IconChevronDown } from '@tabler/icons-react';
import LOGO from 'assets/images/oraika-logo.png';
import { ColorSchemeToggle } from 'mantine-components/components/ColorSchemeToggle';
import { useState } from 'react';

const useStyles = createStyles((theme) => ({
    header: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        height: '100%'
    },

    inner: {
        height: 56,
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
    },

    links: {
        [theme.fn.smallerThan('sm')]: {
            display: 'none'
        }
    },

    burger: {
        [theme.fn.largerThan('sm')]: {
            display: 'none'
        },
        color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7]
    },

    headerButton: {
        [theme.fn.smallerThan('sm')]: {
            display: 'none'
        }
    },

    link: {
        display: 'block',
        lineHeight: 1,
        padding: '8px 12px',
        borderRadius: theme.radius.sm,
        textDecoration: 'none',
        color: theme.colorScheme === 'dark' ? theme.colors.dark[0] : theme.colors.gray[7],
        fontSize: theme.fontSizes.sm,
        fontWeight: 500,

        '&:hover': {
            backgroundColor:
                theme.colorScheme === 'dark' ? theme.colors.dark[6] : theme.colors.gray[0]
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

export function HeaderMenu({ links }: HeaderSearchProps) {
    const [opened, { toggle }] = useDisclosure(false);
    const [active, setActive] = useState(links[0].link);
    const { classes, cx } = useStyles();

    const items = links.map((link) => {
        const menuItems = link.links?.map((item) => (
            <Menu.Item key={item.link}>{item.label}</Menu.Item>
        ));

        if (menuItems) {
            return (
                <Menu key={link.label} trigger="hover" transitionProps={{ exitDuration: 0 }}>
                    <Menu.Target>
                        <a href={link.link} className={classes.link}>
                            <Center>
                                <span className={classes.linkLabel}>{link.label}</span>
                                <IconChevronDown size={12} stroke={1.5} />
                            </Center>
                        </a>
                    </Menu.Target>
                    <Menu.Dropdown>{menuItems}</Menu.Dropdown>
                </Menu>
            );
        }

        return (
            <a
                key={link.label}
                href={link.link}
                className={cx(classes.link, { [classes.linkActive]: active === link.link })}
                onClick={(event) => {
                    event.preventDefault();
                    setActive(link.link);
                }}
            >
                {link.label}
            </a>
        );
    });

    return (
        <Header height={60} mb={20}>
            <Group position="apart">
                <Box pl="lg">
                    <Image height={40} src={LOGO.src} alt="oraika" />
                </Box>
                <Group spacing={5} className={classes.links}>
                    {items}
                </Group>
                <Group position="center" grow px="md">
                    <Button className={classes.headerButton} variant="default" radius="xl">
                        Sign in
                    </Button>
                    <Button
                        className={classes.headerButton}
                        color="orange"
                        radius="xl"
                        variant="filled"
                    >
                        Apply for free access
                    </Button>
                </Group>
                <Box pr="xs">
                    <ColorSchemeToggle />
                </Box>
                <Burger opened={opened} onClick={toggle} className={classes.burger} size="sm" />
            </Group>
        </Header>
    );
}
