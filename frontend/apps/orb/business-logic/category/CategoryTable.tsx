import ChipArray from 'mantine-components/components/Chip/ChipArray';

function CategoryTable({ rows }) {
    const categories = rows.map((row) => row.name);
    return (
        <ChipArray
            justify="center"
            chipList={categories}
            direction="column"
            spacing="md"
            size="lg"
            bgColor="orange"
        />
    );
}

export default CategoryTable;
