/** @type {import('next').NextConfig} */
const nextConfig = {
  output: "standalone",
  eslint: {
    ignoreDuringBuilds: true,
  },
  async rewrites() {
    // Fallback value in case environment variable not set
    const apiEndpoint =
      process.env.NEXT_PUBLIC_API_ENDPOINT || "http://localhost:8020";

    return [
      {
        source: "/stt/transcribe/:path*",
        destination: `${apiEndpoint}/stt/transcribe/:path*`,
      },
      {
        source: "/data/:path*",
        destination: `${apiEndpoint}/data/:path*`,
      },
    ];
  },
};

export default nextConfig;
