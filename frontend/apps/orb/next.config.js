const sharedPackages = [
    '../../packages/mantine-components',
    '../../packages/headless-components',
    '../../packages/common-utils',
]

const withBundleAnalyzer = require('@next/bundle-analyzer')({
    enabled: process.env.ANALYZE === 'true'
});

const withMDX = require('@next/mdx')({
    extension: /\.mdx?$/,
    options: {
        // If you use remark-gfm, you'll need to use next.config.mjs
        // as the package is ESM only
        // https://github.com/remarkjs/remark-gfm#install
        remarkPlugins: [],
        rehypePlugins: [],
        providerImportSource: "@mdx-js/react"
    }
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

module.exports = withBundleAnalyzer(withMDX((nextConfig)))
