import { wrapSentence } from '../utils/common';

describe('wrapSentence', () => {
    it('should wrap sentence into multiple lines', () => {
        const sentence = 'This is a sample sentence for testing purposes';
        const result = wrapSentence(sentence, 10);
        expect(result).toEqual(['This is a', 'sample', 'sentence', 'for', 'testing', 'purposes']);
    });

    it('should wrap sentence into multiple lines wider', () => {
        const sentence = 'This is a sample sentence for testing purposes';
        const result = wrapSentence(sentence, 20);
        expect(result).toEqual(['This is a sample', 'sentence for testing', 'purposes']);
    });

    it('should return the whole sentence if it is shorter than the line count', () => {
        const sentence = 'Short sentence';
        const result = wrapSentence(sentence, 20);
        expect(result).toEqual(['Short sentence']);
    });

    it('should throw an error if line character count is less than 1', () => {
        const sentence = 'Another sentence';
        expect(() => wrapSentence(sentence, 0)).toThrow('lineCharacterCount must be at least 1');
    });

    it('should handle a sentence with a single word correctly', () => {
        const sentence = 'oneword';
        const result = wrapSentence(sentence, 3);
        expect(result).toEqual(['oneword']);
    });

    it('should handle an empty string correctly', () => {
        const sentence = '';
        const result = wrapSentence(sentence, 10);
        expect(result).toEqual(['']);
    });

    it('should handle a sentence of exactly the line character count', () => {
        const sentence = 'Exactly ten';
        const result = wrapSentence(sentence, 11);
        expect(result).toEqual(['Exactly ten']);
    });

    it('should handle a sentence with multiple spaces between words', () => {
        const sentence = 'Extra   spaces';
        const result = wrapSentence(sentence, 6);
        expect(result).toEqual(['Extra', 'spaces']);
    });
});
