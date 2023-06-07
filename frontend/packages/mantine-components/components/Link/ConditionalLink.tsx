import Link from 'next/link';

interface ConditionalLinkProps {
    link?: string;
    className?: string;
    children: React.ReactNode;
}

export default function ConditionalLink({ link, className, children }: ConditionalLinkProps) {
    if (link) {
        return <Link className={className} href={link}>{children}</Link>;
    } else {
        return <>{children}</>;
    }
}
