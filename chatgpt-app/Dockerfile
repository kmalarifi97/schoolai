FROM node:22-slim
WORKDIR /app

# Install deps first for layer caching.
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

COPY server.js ./
COPY kst.js ./
COPY gapgraph.js ./
COPY instructions.md ./
COPY public ./public
COPY data ./data

# Cloud Run injects PORT; the server already honours it (defaults to 8787).
ENV NODE_ENV=production
CMD ["node", "server.js"]
