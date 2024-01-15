import Link from 'next/link';

export default function WithLink({ children, href, ...props }) {
    if (href) {
        return (
            <Link href={href} target="_blank" {...props} style={{ textDecoration: 'none' }}>
                {children}
            </Link>
        );
    } else {
        return <>{children}</>;
    }
}
