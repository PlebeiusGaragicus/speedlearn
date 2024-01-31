
```python
import streamlit_authenticator as stauth
print(stauth.Hasher([input("Enter password: ")]).generate()[0])
```
