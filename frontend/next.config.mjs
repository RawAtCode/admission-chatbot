/** @type {import('next').NextConfig} */
const nextConfig = {
    output: "export", // Enables static site generation
    images: {
      unoptimized: true, // Required for static export if using next/image
    },
  };
  
  export default nextConfig;
  