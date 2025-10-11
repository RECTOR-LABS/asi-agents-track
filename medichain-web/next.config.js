/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  env: {
    COORDINATOR_URL: process.env.COORDINATOR_URL || 'http://localhost:8080',
  },
}

module.exports = nextConfig
