# chat

```sh
brew services start redis
```

```sh
daphne -p 8001 chat_project.asgi:application
```

Go to `localhost:8001/chat/<roomname>`.
