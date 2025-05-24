/** @type {import('next-sitemap').IConfig} */
module.exports = {
  siteUrl: process.env.SITE_URL || 'https://tableau-de-bord-de-suivi-gpta.vercel.app',
  generateRobotsTxt: true,
  generateIndexSitemap: false,
} 