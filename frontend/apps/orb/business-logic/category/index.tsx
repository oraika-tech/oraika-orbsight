import { useEffect, useState } from 'react';
import { getCategories } from '../../lib/service/category-service';
import CategoryTable from './CategoryTable';

interface ResponseCategory {
    identifier: string
    name: string
    is_enabled: boolean
}

interface CategoryState {
    id: string
    name: string
    is_enabled: boolean
}

function Category() {
    const [categories, setCategories] = useState<CategoryState[]>([]);

    const convertData = (category: ResponseCategory) => ({
        id: category.identifier,
        name: category.name,
        is_enabled: category.is_enabled
    });

    useEffect(() => {
        const syncCategories = () => getCategories()
            .then(response => setCategories(response.map(convertData)));

        syncCategories();

        return () => setCategories([]);
    }, []);

    return (
        <CategoryTable rows={categories} />
    );
}

export default Category;
