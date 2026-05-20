/** Proxy /api/* to the FastAPI backend so the frontend stays same-origin
 *  (lets <video src="/api/video/...?t=token"> work cleanly). */
const BACKEND = process.env.BACKEND_URL || "http://localhost:8000";
module.exports = {
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${BACKEND}/api/:path*` }];
  },
};
