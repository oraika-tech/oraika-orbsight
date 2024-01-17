/** @type {import('next-sitemap').IConfig} */
module.exports = {
    siteUrl: process.env.WEBSITE_URL,
    generateIndexSitemap: false,
    generateRobotsTxt: true,
    changefreq: 'weekly',
    robotsTxtOptions: {
        policies: [
            {
                userAgent: '*',
                allow: '/',
                disallow: ['/cgi-bin/', '/auth']
            }
        ]
    }
}
