# node:24-slim → Node built-in node:sqlite available (for the experience log).
FROM node:24-slim
WORKDIR /app

# Install deps first for layer caching.
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY server.js ./
COPY db.mjs ./
COPY decompose.mjs ./
COPY instructions.md ./
COPY public ./public
COPY data ./data

# Cloud Run injects PORT; the server already honours it (defaults to 8787).
ENV NODE_ENV=production
# Experience log path (Cloud Run fs is ephemeral; /tmp is writable). Per-instance
# PoC log — point at a volume / managed DB for cross-session persistence.
ENV GRAPHLOG_DB=/tmp/graphlog.db
CMD ["node", "server.js"]
