const sharedPackages = [
    '../../packages/common-utils',
]

const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true'
});

/** @type {import('next').NextConfig} */
const nextConfig = {
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

module.exports = withBundleAnalyzer((nextConfig))
