
```python
import streamlit_authenticator as stauth
print(stauth.Hasher([input("Enter password: ")]).generate()[0])
```

---


# install redis

```sh
# MacOS
brew install redis

# brew services start redis

# Debian
sudo apt update
sudo apt install redis-server

# sudo service redis-server start

```

To start redis now and restart at login:
  brew services start redis
Or, if you don't want/need a background service you can just run:
  /usr/local/opt/redis/bin/redis-server /usr/local/etc/redis.conf

```sh
brew services start redis
```