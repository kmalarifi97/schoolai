FROM node:22-slim
WORKDIR /app

# deps first (layer cache)
COPY package.json package-lock.json* ./
RUN npm install --omit=dev

# app code + the named Physics-2 graph (small, derived from our own spine)
COPY src ./src
COPY public ./public
COPY graph/physics2.graph.json ./graph/physics2.graph.json

ENV NODE_ENV=production
ENV GRAPH_PATH=graph/physics2.graph.json
# Cloud Run injects PORT; serve.mjs maps it to the public MCP listener and runs
# GraphQL internally on :4000.
CMD ["node", "src/serve.mjs"]
