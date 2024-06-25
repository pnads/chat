# chat

## Getting Started

```sh
npm run build
```

```sh
npm run start
```

Go to `localhost:8000/<roomname>`.

## Making Changes

If you update `chat_app/static/css/tailwind.css`, build the main CSS:

```sh
npm run build:css
```

If updating any static files in `chat_app/static/` or `./static/`, run:

```sh
npm run build:static
```

which will collect all static files into a `./staticfiles/` folder.
