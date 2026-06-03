# node:24-slim → Node built-in node:sqlite available (the book graph needs it).
FROM node:24-slim
WORKDIR /app

# Install deps first for layer caching.
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY server.js ./
COPY bookgraph.mjs ./
COPY instructions.md ./
COPY public ./public
COPY data ./data
COPY seed ./seed

# Cloud Run injects PORT; the server already honours it (defaults to 8787).
ENV NODE_ENV=production
# Book-graph DB path. The read-only seed (seed/book.db) is copied here at startup
# so per-student session logs can be written (Cloud Run fs is ephemeral; /tmp is
# writable). Per-instance PoC log — point at a volume for cross-session persistence.
ENV BOOKGRAPH_DB=/tmp/book.db
CMD ["node", "server.js"]
