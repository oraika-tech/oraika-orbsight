import type { Meta, StoryObj } from '@storybook/react';
import GenericDateRange, { DateRangeType } from './GenericDateRange';

type Story = StoryObj<typeof GenericDateRange>;

export default {
    title: 'Mantine/GenericDateRange',
    component: GenericDateRange,
    tags: ['autodocs'],
    argTypes: {
        label: { control: 'string' },
        dateValue: { control: 'object' },
        allowedPeriod: { control: 'object' },
        onChange: { action: 'return' }
    }
} as Meta;

/** story: 'Renders the DateRange component with the' */
export const Default: Story = {
    args: {
        label: 'Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-30-days'
        }
    }
};

export const Today = {
    args: {
        label: 'Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'today'
        }
    }
};

export const Dec2023 = {
    args: {
        label: 'Period',
        dateValue: {
            rangeType: DateRangeType.MONTH,
            rangeValue: new Date('2023-12-11')
        }
    }
};

export const DRSameMonth = {
    args: {
        label: 'Period',
        dateValue: {
            rangeType: DateRangeType.CUSTOM,
            rangeValue: [new Date('2024-01-10'), new Date('2024-01-24')]
        }
    }
};

export const DRSameYear = {
    args: {
        label: 'Period',
        dateValue: {
            rangeType: DateRangeType.CUSTOM,
            rangeValue: [new Date('2024-01-10'), new Date('2024-02-09')]
        }
    }
};

export const DRAcrossYear = {
    args: {
        dateValue: {
            rangeType: DateRangeType.CUSTOM,
            rangeValue: [new Date('2023-12-20'), new Date('2024-01-10')]
        }
    }
};

export const RestrictedDR9Days = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            period: '9d'
        }
    }
};

export const RestrictedDR30Days = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            period: '30d'
        }
    }
};

export const RestrictedDR90Days = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            period: '90d'
        }
    }
};

export const RestrictedDR2Month = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            period: '2M'
        }
    }
};

export const RestrictedDR1Year = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            period: '1y'
        }
    }
};
export const RestrictedDRWithStartFeb3 = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            start: new Date(2024, 1, 3)
        }
    }
};
export const RestrictedDRWithStartJan24AndEndFeb7 = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            start: new Date(2024, 0, 24),
            end: new Date(2024, 1, 7)
        }
    }
};
export const RestrictedDRWithEndJan31 = {
    args: {
        label: 'Restricted Period',
        dateValue: {
            rangeType: DateRangeType.PERIOD,
            rangeValue: 'last-7-days'
        },
        allowedPeriod: {
            end: new Date(2024, 0, 31)
        }
    }
};
