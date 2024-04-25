/** @type {import('next').NextConfig} */
const nextConfig = {
    async rewrites() {
      return [
        {
          source: '/api/:path*',
          destination: 'http://host.docker.internal:5000/:path*' // Proxy to Backend
        }
      ]
    }
  }
export default nextConfig;
