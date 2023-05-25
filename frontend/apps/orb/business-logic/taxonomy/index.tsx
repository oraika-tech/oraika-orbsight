import { Card, Grid, Space, Stack, Title } from '@mantine/core';

// import Category from 'layouts/category';
import { useEffect, useState } from 'react';
// import { getTaxonomies } from 'service/taxonomy-service';
import { getTaxonomies } from '../../lib/service/taxonomy-service';
import Category from '../category';
import TaxonomyTable from './TaxonomyTable';

interface ResponseTaxonomy {
    identifier: string
    keyword: string
    term: string
    description: string
    tags: string[]
    is_enabled: boolean
}

interface TaxonomyState {
    id: string
    keyword: string
    term: string
    description: string
    tags: string[]
    is_enabled: boolean
}

export default function Taxonomy() {
    const [taxonomies, setTaxonomies] = useState<TaxonomyState[]>([]);
    const [loading, setLoading] = useState<boolean>(false);

    const convertData = (taxonomy: ResponseTaxonomy) => ({
        id: taxonomy.identifier,
        keyword: taxonomy.keyword,
        term: taxonomy.term,
        description: taxonomy.description,
        tags: taxonomy.tags,
        is_enabled: taxonomy.is_enabled
    });

    useEffect(() => {
        setLoading(true);
        const syncTaxonomies = () => getTaxonomies()
            .then(response => setTaxonomies(response.map(convertData)))
            .finally(() => setLoading(false));

        syncTaxonomies();

        return () => setTaxonomies([]);
    }, []);

    return (
        <Grid gutter="md">
            <Grid.Col xs={8}>
                <Card>
                    <Stack spacing="xs">
                        <Title order={2} sx={{ height: '3rem', padding: '0.3rem' }}>Terms</Title>
                        <TaxonomyTable rows={taxonomies} loading={loading} />
                    </Stack>
                </Card>
            </Grid.Col>
            <Grid.Col xs={4}>
                <Card sx={{ height: '71vh' }}>
                    <Stack spacing="xl">
                        <Title order={2} sx={{ height: '3rem' }}>Categories</Title>
                        <Space h="xl" />
                        <Category />
                    </Stack>
                </Card>
            </Grid.Col>
        </Grid >
    );
}
