import { Stack, Title } from '@mantine/core';
import Link from 'next/link';
import { UserButton } from '../Buttons/UserButton';
import { LinksGroup } from './NavbarLinksGroup';
import classes from './NestedNavbar.module.css';

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

export default function NavbarNested({ links, opened, name, email }: NavbarNestedProps) {
    const linksGroup = links.map((item) => <LinksGroup {...item} key={item.label} />);

    return (
        <nav className={opened ? classes.navbar : classes.hidden}>
            <Stack justify="space-between" h="100%">
                <Stack>
                    <div className={classes.header}>
                        <Link href="/" style={{ textDecoration: 'none' }}>
                            <Title order={3}>
                                OrbSight
                            </Title>
                        </Link>
                    </div>

                    <div className={classes.links}>
                        <div className={classes.linksInner}>{linksGroup}</div>
                    </div>
                </Stack>

                <div className={classes.footer}>
                    <UserButton
                        image=""
                        name={name}
                        email={email}
                    />
                </div>
            </Stack>
        </nav>
    );
}
