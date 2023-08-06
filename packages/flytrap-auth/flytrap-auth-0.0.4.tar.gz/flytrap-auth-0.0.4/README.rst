Django base package
==============
## adduser

```
url('^api/auth/', include('flytrap.auth.account.token.urls'))
```

## set auth

```
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'flytrap.auth.account.token.auth.TokenAuthentication',
    ),
```

## don't signup
add to setting

```
SHOW_SIGNUP = False
```