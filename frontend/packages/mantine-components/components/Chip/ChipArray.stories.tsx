import { Meta } from '@storybook/react';
import ChipArray from './ChipArray';

export default {
    title: 'ChipArray',
    component: ChipArray,
    argTypes: {
        chipList: { control: 'array' },
        bgColor: { control: 'color' },
        spacing: { control: 'number' },
        direction: { control: { type: 'select', options: ['row', 'column'] } },
        justify: {
            control: { type: 'select', options: ['center', 'left', 'right', 'apart'] }
        }
    }
} as Meta;

export const Default = {
    args: {
        chipList: ['Chip 1', 'Chip 2', 'Chip 3']
    }
};

export const CustomColor = {
    args: {
        chipList: ['Chip 1', 'Chip 2', 'Chip 3'],
        bgColor: 'teal'
    }
};

export const CustomSpacing = {
    args: {
        chipList: ['Chip 1', 'Chip 2', 'Chip 3'],
        spacing: 2
    }
};

export const ColumnDirection = {
    args: {
        chipList: ['Chip 1', 'Chip 2', 'Chip 3'],
        direction: 'column'
    }
};

export const CustomJustify = {
    args: {
        chipList: ['Chip 1', 'Chip 2', 'Chip 3'],
        justify: 'apart'
    }
};
