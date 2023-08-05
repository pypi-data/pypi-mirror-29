jwt_auth
--------

# Introduction

Use Special Staff Model use JWT Auth API Mode.
Don't change default user authentication.


# How to configure
@settings.py
```
        REST_FRAMEWORK = {
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework.permissions.IsAuthenticated',
            ),
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'jwt_auth.authentication.JWTAuthentication',
            )
        }

        # optional
        JWT_AUTH = {
            'JWT_RESPONSE_PAYLOAD_HANDLER':
                'jwt_auth.serializers.jwt_response_payload_handler',
            'JWT_PAYLOAD_HANDLER': 'jwt_auth.serializers.jwt_payload_handler',
        }
```
@urls.py
```
    urlpatterns = [
    url(r'^auth/', include("jwt_auth.urls", namespace="api-auth")),
    ]
```

That's All. Happy Coding.