import { Flex, SimpleGrid, Skeleton, Space, Title } from '@mantine/core';
import { useList } from '@refinedev/core';
import Image from 'next/image';
import DATA_ERROR from '../../../../assets/images/data-fetch-error.png';
import { ForeignData } from '../../Common/CommonModels';
import { convertObjectKeys } from '../../Common/CommonUtils';
import CardView from './CardView';

interface CardViewProps {
    resource: string;
    foreignData: ForeignData;
}

export default function CardListView({ resource, foreignData }: CardViewProps) {
    const { data, isLoading, isError } = useList({ resource });
    if (isError) {
        return (
            <Flex direction="column" justify="center" align="center" h="100%" w="100%">
                <Image src={DATA_ERROR} alt="Error loading data" />
                <Space h="lg" />
                <Title order={3}>Error loading data</Title>
            </Flex>
        );
    }

    if (isLoading) {
        return (
            <Flex gap="sm" justify="flex-start" align="flex-start" direction="row" wrap="wrap">
                <Skeleton height={200} width={200} mb="xl" />
                <Skeleton height={200} width={200} mb="xl" />
                <Skeleton height={200} width={200} mb="xl" />
            </Flex>
        );
    }

    const cardDataList = data?.data?.map((row) => convertObjectKeys(row));
    return (
        <Flex gap="sm" justify="flex-start" align="flex-start" direction="row" wrap="wrap">
            <SimpleGrid cols={{ base: 1, md: 2, lg: 3 }} spacing={10}>
                {cardDataList.map((cardData) => (
                    <CardView
                        key={cardData.identifier}
                        resource={resource}
                        data={cardData}
                        foreignData={foreignData}
                    />
                ))}
            </SimpleGrid>
        </Flex>
    );
}
