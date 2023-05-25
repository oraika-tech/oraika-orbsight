import { FieldValue, getValue } from '../../../apps/orb/components/DynamicDashboard';

describe('getValue', () => {
    const arrayObj: FieldValue[] = [
        { field: 'name', value: { value: 'John' } },
        { field: 'age', value: { value: 30 } },
        { field: 'email', value: { value: 'john@example.com' } }
    ];

    it('returns the value of the matching object field', () => {
        expect(getValue(arrayObj, 'name')).toEqual({ value: 'John' });
        expect(getValue(arrayObj, 'age')).toEqual({ value: 30 });
        expect(getValue(arrayObj, 'email')).toEqual({ value: 'john@example.com' });
    });

    it('returns null if no object has a matching field', () => {
        expect(getValue(arrayObj, 'address')).toBeNull();
        expect(getValue([], 'name')).toBeNull();
    });
});
