import { useRouter } from 'next/router';
import DemoLogin from '../business-logic/login/DemoLogin';

export default function DemoLoginPage() {
    const router = useRouter();
    if (process.env.NEXT_PUBLIC_DEMO_MODE !== 'true') {
        router.replace('/');
    } else {
        return <DemoLogin />;
    }
}
