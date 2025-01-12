import dynamic from 'next/dynamic';
import LoginPage from 'mantine-components/components/Auth/LoginPage';

const DefaultLayout = dynamic(() => import('../business-logic/layout/DefaultLayout'), { ssr: false });

export default function Login() {
    return (
        <DefaultLayout>
            <LoginPage />
        </DefaultLayout>
    );
}
