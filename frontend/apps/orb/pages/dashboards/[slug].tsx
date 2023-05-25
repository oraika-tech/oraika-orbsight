import { useRouter } from 'next/router';
import DefaultLayout from '../../business-logic/layout/DefaultLayout';
import DynamicDashboard from '../../components/DynamicDashboard';
// import { clearLocalUser } from '../../lib/local-storage/user-info';
// import { getDashboards } from '../../lib/service/dashboard-service';

export default function DashboardPage() {
    const router = useRouter();
    const { slug } = router.query;

    // if (!router.isFallback && !dashboardParams?.slug) {
    //     return <ErrorPage statusCode={404} />;
    // }

    const dashboard_id = slug as string;

    return (
        <DefaultLayout>
            <DynamicDashboard dashboard_id={dashboard_id} />
        </DefaultLayout>
    );
}

// export async function getStaticProps({ params }) {
//     return {
//         props: {
//             dashboardParams: params
//         }
//     };
// }

// dynamically generate the slugs
// export async function getStaticPaths() {
//     const dashboardSlug = 'dashboard-list';
//     const response = await getDashboards(clearLocalUser, dashboardSlug);
//     localStorage.setItem(dashboardSlug, JSON.stringify(response));

//     const paths = response.map((dashboardObj) => ({
//         params: {
//             slug: dashboardObj.title.replace(' ', '-').toLowerCase(),
//             dashboard_id: dashboardObj.identifier,
//             title: dashboardObj.title
//         }
//     }));

//     return {
//         paths,
//         fallback: true
//     };
// }
