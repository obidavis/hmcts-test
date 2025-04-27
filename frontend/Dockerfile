FROM node:23-slim

RUN corepack enable

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

RUN yarn build:prod

CMD ["yarn", "start"]
