const orbNextJest = require('next/jest');

const orbCreateJestConfig = orbNextJest({
    dir: process.cwd().includes('/apps/orb') ? './' : './apps/orb/'
});

const orbCustomJestConfig = {
    preset: 'ts-jest',
    moduleNameMapper: {
        '^@/components/(.*)$': '<rootDir>/components/$1',
        '^@/pages/(.*)$': '<rootDir>/pages/$1'
    },
    testEnvironment: 'jest-environment-jsdom',
    testMatch: ['**/__tests__/**/*.+(ts|tsx|js)', '**/?(*.)+(spec|test).+(ts|tsx|js)'],
    transform: {
        '^.+\\.(ts|tsx)$': 'ts-jest'
    }
};

module.exports = orbCreateJestConfig(orbCustomJestConfig);
