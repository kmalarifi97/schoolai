# node:24-slim → node:sqlite available without a flag.
FROM node:24-slim
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY db.mjs decompose.mjs mcp.mjs ./

ENV NODE_ENV=production
# Cloud Run fs is ephemeral; /tmp is writable. The log is per-instance (PoC) —
# for cross-session persistence, point GRAPHLOG_DB at a mounted volume / managed DB.
ENV GRAPHLOG_DB=/tmp/graphlog.db
# Cloud Run injects PORT; mcp.mjs honors it.
CMD ["node", "mcp.mjs"]
