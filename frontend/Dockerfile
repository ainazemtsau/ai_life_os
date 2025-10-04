# Frontend dev (Next.js + pnpm)
FROM node:20-alpine

# pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# deps слой
COPY package.json pnpm-lock.yaml ./
RUN pnpm install

# исходники
COPY . ./

ENV HOST=0.0.0.0
ENV PORT=3000

# dev сервер на внешнем интерфейсе
CMD ["pnpm", "dev", "-p", "3000", "-H", "0.0.0.0"]
