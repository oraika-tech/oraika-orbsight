import type { Meta, StoryObj } from '@storybook/react';
import GenericFilterPanel, { FilterFieldType } from '.';

type Story = StoryObj<typeof GenericFilterPanel>;

export default {
    title: 'Mantine/GenericFilterPanel',
    component: GenericFilterPanel,
    tags: ['autodocs'],
    argTypes: {
        filtersData: { control: 'object' },
        showFilterButton: { control: 'object' },
        filterHandler: { action: 'return' }
    }
} as Meta;

const defaultFiltersData = [
    {
        id: 'entity',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Entity',
        options: [
            {
                code: 'all'
            },
            {
                code: 'Play Arena'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'observerType',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Observer Type',
        options: [
            {
                code: 'all'
            },
            {
                code: 'GoogleMaps'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'category',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Category',
        options: [
            {
                code: 'all'
            },
            {
                code: 'booking'
            },
            {
                code: 'faulty equipment'
            },
            {
                code: 'maintenance'
            },
            {
                code: 'waiting'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'term',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Term',
        options: [
            {
                code: 'all'
            },
            {
                code: '7D Theatre'
            },
            {
                code: 'Archery'
            },
            {
                code: 'ATV'
            },
            {
                code: 'Bowling'
            },
            {
                code: 'Carnival Games'
            },
            {
                code: 'Car Simulator'
            },
            {
                code: 'Children'
            },
            {
                code: 'Cricket Simulator'
            },
            {
                code: 'Exit 404'
            },
            {
                code: 'finance'
            },
            {
                code: 'go-kart'
            },
            {
                code: 'Gokart'
            },
            {
                code: 'Gym'
            },
            {
                code: 'Juniors'
            },
            {
                code: 'Laser Maze'
            },
            {
                code: 'Laser Tag'
            },
            {
                code: 'Office'
            },
            {
                code: 'Paintball'
            },
            {
                code: 'Rocket Ejector'
            },
            {
                code: 'Rope Course'
            },
            {
                code: 'Sales'
            },
            {
                code: 'Shooting'
            },
            {
                code: 'Table Games'
            },
            {
                code: 'Toddler Zone'
            },
            {
                code: 'Trampoline Park'
            },
            {
                code: 'VR Games'
            },
            {
                code: 'Wall Climbing'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'taxonomy',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Taxonomy',
        options: [
            {
                code: 'all'
            },
            {
                code: 'Activities Indoors'
            },
            {
                code: 'Activities Outdoors'
            },
            {
                code: 'arena'
            },
            {
                code: 'b d'
            },
            {
                code: 'Cashier'
            },
            {
                code: 'Events'
            },
            {
                code: 'Facilities'
            },
            {
                code: 'finance'
            },
            {
                code: 'Food and Beverages'
            },
            {
                code: 'Food & Beverages'
            },
            {
                code: 'Guest Relations'
            },
            {
                code: 'Guest  Relations'
            },
            {
                code: 'Indoor Activities'
            },
            {
                code: 'Indoor Activity'
            },
            {
                code: 'Juniors'
            },
            {
                code: 'Medical'
            },
            {
                code: 'Outdoor Activities'
            },
            {
                code: 'Outdoor Activity'
            },
            {
                code: 'play children'
            },
            {
                code: 'Sales'
            },
            {
                code: 'Sports'
            },
            {
                code: 'studio'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'emotion',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Emotion',
        options: [
            {
                code: 'all'
            },
            {
                code: 'negative'
            },
            {
                code: 'neutral'
            },
            {
                code: 'positive'
            },
            {
                code: 'undetermined'
            }
        ],
        defaultValue: {
            code: 'all',
            label: 'All'
        },
        selectedValue: {
            code: 'all',
            label: 'All'
        }
    },
    {
        id: 'lang',
        minWidth: 40,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Language',
        options: [
            {
                code: 'all'
            },
            {
                code: 'ca'
            },
            {
                code: 'da'
            },
            {
                code: 'de'
            },
            {
                code: 'en'
            },
            {
                code: 'es'
            },
            {
                code: 'fr'
            },
            {
                code: 'hr'
            },
            {
                code: 'id'
            },
            {
                code: 'nl'
            },
            {
                code: 'pl'
            },
            {
                code: 'pt'
            },
            {
                code: 'ro'
            },
            {
                code: 'sl'
            },
            {
                code: 'sv'
            }
        ],
        defaultValue: {
            code: 'all'
        },
        selectedValue: {
            code: 'all'
        }
    },
    {
        id: 'period',
        type: FilterFieldType.DATE_RANGE,
        label: 'Period',
        defaultValue: {
            code: 'last-7-days'
        },
        selectedValue: {
            code: 'last-7-days'
        }
    },
    {
        id: 'interval',
        minWidth: 80,
        maxWidth: 80,
        type: FilterFieldType.AUTO_COMPLETE,
        label: 'Interval',
        options: [
            {
                code: 'hour'
            },
            {
                code: 'day'
            },
            {
                code: 'week'
            }
        ],
        defaultValue: {
            code: 'day'
        },
        selectedValue: {
            code: 'day'
        }
    }
];

export const Default: Story = {
    args: {
        showFilterButton: false,
        filtersData: defaultFiltersData
    }
};

export const ShowFilterButton: Story = {
    args: {
        showFilterButton: true,
        filtersData: defaultFiltersData
    }
};

export const WithoutDateRange: Story = {
    args: {
        showFilterButton: false,
        filtersData: defaultFiltersData.filter(filter => filter.type !== 'DATE_RANGE')
    }
};

export const WithoutDateRangeShowFilter: Story = {
    args: {
        showFilterButton: true,
        filtersData: defaultFiltersData.filter(filter => filter.type !== 'DATE_RANGE')
    }
};
