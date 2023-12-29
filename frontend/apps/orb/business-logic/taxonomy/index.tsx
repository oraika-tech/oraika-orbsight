import { Grid } from '@mantine/core';

// import Category from 'layouts/category';
import { useEffect, useState } from 'react';
// import { getTaxonomies } from 'service/taxonomy-service';
import { getTaxonomies } from '../../lib/service/taxonomy-service';
import CategoryRefine from './CategoryRefine';
import TaxonomyRefine from './TaxonomyRefine';

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
            <Grid.Col span={{ base: 12, xs: 8 }}>
                <TaxonomyRefine />
            </Grid.Col>
            <Grid.Col span={{ base: 12, xs: 4 }}>
                <CategoryRefine />
            </Grid.Col>
        </Grid>
    );
}
