# node:24-slim → Node built-in node:sqlite available.
FROM node:24-slim
WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY db.mjs mcp.mjs ./
COPY seed ./seed

ENV NODE_ENV=production
# Read-only book graph ships in seed/book.db; mcp.mjs copies it to this writable
# path at startup so session logs can be written (per-instance / ephemeral PoC).
ENV BOOKGRAPH_DB=/tmp/book.db
CMD ["node", "mcp.mjs"]
