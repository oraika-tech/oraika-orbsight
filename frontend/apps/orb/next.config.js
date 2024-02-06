const sharedPackages = [
    '../../packages/mantine-components',
    '../../packages/headless-components',
    '../../packages/common-utils',
    '../../packages/blog-utils'
]

const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true'
});

/** @type {import('next').NextConfig} */
const nextConfig = {
    output: 'export',
    pageExtensions: ['ts', 'tsx', 'js', 'jsx', 'md', 'mdx'],
    reactStrictMode: true,
    eslint: {
        ignoreDuringBuilds: true
    },
    images: {
        unoptimized: true
    },
    transpilePackages: sharedPackages
}

module.exports = withBundleAnalyzer(nextConfig)
