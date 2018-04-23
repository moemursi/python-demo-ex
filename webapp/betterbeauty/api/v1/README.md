# Authorization
## Getting auth token with email/password credentials
In order to make requests to the API, client needs a JWT token. There are 2 ways to obtain
the token - authorize with existing user's credentials, or register new user.

**POST /api/v1/auth/get-token**:

`curl -X POST -d "email=email@example.com&password=clients_password" http://apiserver/api/v1/auth/get-token`

**Responce 200 OK**:

```
{
    "token": "jwt_token",
    "expires_in": 86400,
    "stylist": {
        "id": 1,
        "first_name": "Jane",
        "last_name": "McBob",
        "phone": "(650) 350-1234",
        "profile_photo_url": null,
        "salon_name": "Jane salon",
        "salon_address": "1234 Front Street"
    }
}
```

Note: if user doesn't have stylist profile - `stylist` field will be `null`

## Getting auth token with Facebook credentials

See **Registration** - **Register user with Facebook credentials**

## Using auth token for authorization

Every subsequent request to the API should have `Authorization` header set with the following string:

`Token jwt_token`

Example call:

`curl -H "Authorization: Token jwt_token" http://apiserver/api/v1/stylist/profile`

## Refreshing auth token

If the token has not yet expired, it can be refreshed to a new one:

**POST /api/v1/auth/refresh-token**

`curl -X POST -H "Content-Type: application/json" -d '{"token": "old_but_not_expired_jwt_token"}' http://apiserver/api/v1/auth/refresh-token`

**Responce 200 OK**

```
{
    "token": "refreshed_jwt_token",
    "expires_in": 86400,
    "stylist": null
}
```

Note: make sure to set proper content type (to `application/json`)

# Registration

Before creating customer or stylist, new user must be registered. There will be multtiple
ways of creation of user entity using social networks; section below is about registering
a user with email credentials. Social network methods are to be added.

## Register user with Facebook credentials
This endpoint creates a user based on Facebook auth token and returns JWT token back to client.
If user already exists - endpoint just refreshes the JWT token.

**POST /api/v1/auth/get-token-fb**

`curl -X POST -d "fbAccessToken=long_facebook_token&fbUserID=numeric_facebook_user_id" http://apiserver/api/v1/auth/get-token-fb`

**Response 200 OK**

```
{
    "token": "jwt_token",
    "expires_in": 86400,
    "stylist": {
        "id": 17,
        "first_name": "Charlie",
        "last_name": "Martinazzison",
        "phone": "",
        "profile_photo_url": "http://profile_photo_url",
        "salon_name": null,
        "salon_address": null
    }
}
```

## Register user with email and password credentials

This endpoint creates a user, authenticates and returns JWT token back to client.

The endpoint **does not** create a stylist or salon; you should use **profile** API
(see below) to actually fill in stylist's profile information once after user is created with this API.

**POST /api/v1/auth/register**

`curl -X POST -d "email=stylist2@example.com&password=my_new_password http://apiserver//api/v1/auth/register`

**Response 200 OK**

```
{
    "token": "jwt_token",
    "expires_in": 86400,
    "stylist": null
}
```

**Error 400 Bad Request**
```
{
    "email": [
        "This email is already taken"
    ]
}
```


# Stylist/Salon API

## Profile

### Retrieve profile information
**GET /api/v1/stylist/profile**

`curl -H "Authorization: Token jwt_token" http://apiserver/api/v1/stylist/profile`

**Response 200 OK**

```
{
    "id": 1,
    "first_name": "Freya",
    "last_name": "McBob",
    "phone": "(650) 350-1234",
    "profile_photo_url": "http://example.com/profile_photo.jpg",
    "salon_name": "Jane's Beauty",
    "salon_address": "3945 El Camino Real"
}
```

### Create new profile
**POST/PUT /api/v1/stylist/profile**

```
curl -X POST \
  http://apiserver/api/v1/stylist/profile \
  -H 'Authorization: Token jwt_token' \
  -F first_name=Jane \
  -F last_name=McBob \
  -F 'phone=(650) 350-1234' \
  -F 'salon_name=Jane salon' \
  -F 'salon_address=1234 Front Street'
```

Note: all fields listed above are required.

**Response 201 OK**

```
{
    "id": 1,
    "first_name": "Jane",
    "last_name": "McBob",
    "phone": "(650) 350-1234",
    "profile_photo_url": null,
    "salon_name": "Jane salon",
    "salon_address": "1234 Front Street"
}
```

### Update existing profile with all required fields
**POST/PUT /api/v1/stylist/profile**

```
curl -X POST \
  http://apiserver/api/v1/stylist/profile \
  -H 'Authorization: Token jwt_token' \
  -F first_name=Jane \
  -F last_name=McBob \
  -F 'phone=(650) 350-1234' \
  -F 'salon_name=Jane salon' \
  -F 'salon_address=1234 Front Street'
```

Note: all fields listed above are required.

**Response 200 OK**

```
{
    "id": 1,
    "first_name": "Jane",
    "last_name": "McBob",
    "phone": "(650) 350-1234",
    "profile_photo_url": null,
    "salon_name": "Jane salon",
    "salon_address": "1234 Front Street"
}
```

### Partially update existing profile
**PATCH /api/v1/stylist/profile**

```
curl -X PATCH \
  http://apiserver/api/v1/stylist/profile \
  -H 'Authorization: Token jwt_token' \
  -F first_name=Jane \
  -F 'salon_address=1234 Front Street'
```

Note: you can patch individual fields with PATCH.

**Response 200 OK**

```
{
    "id": 1,
    "first_name": "Jane",
    "last_name": "McBob",
    "phone": "(650) 350-1234",
    "profile_photo_url": null,
    "salon_name": "Jane salon",
    "salon_address": "1234 Front Street"
}
```

## Service templates and template sets

Service template object is a blueprint for stylist's service. Service template
is characterized by duration and base price. Stylists can create their own services
based on selected service templates, supplying their own price and duration.

Stylist can also add their own custom services, not based on existing templates.

Service templates are logically organized into template sets (so 'template set' - is
basically just a named list of templates).

### Get list of service template sets

This API call returns list of service template sets, and for each set
includes list of first 50 service templates with only basic information (name only).

**GET /api/v1/stylist/service-template-sets**
```
curl http://apiserver/api/v1/stylist/service-template-sets \
  -H 'Authorization: Token jwt_token'
```

**Response 200 OK**
```
{
    "service_template_sets": [
        {
            "id": 1,
            "name": "set 1",
            "description": "this is set 1",
            "templates": [
                {
                    "name": "service 1",
                },
                {
                    "name": "service 2",
                }
            ]
        },
        {
            "id": 2,
            "name": "set 2",
            "description": null,
            "templates": [
                {
                    "name": "service 1",
                },
                {
                    "name": "service 3",
                }
            ]
        }
    ]
}
```

### Get full info for template set's services
**GET /api/v1/stylist/service-template-sets/{template_set_id}**

```
curl http://apiserver/api/v1/stylist/service-template-sets/{template_set_id} \
  -H 'Authorization: Token jwt_token'
```

**Response 200 OK**
```
    {
        "id": 1,
        "name": "set 1",
        "description": "this is set 1",
        "templates": [
            {
                "name": "service 1",
                "description": "Great service",
                "base_price": 10.0,
                "duration_minutes": 25
            },
            {
                "name": "service 2",
                "description": "Even better service service",
                "base_price": 20.0,
                "duration_minutes": 45
            }
        ]
    }
```


## Stylist's services

### Get list of services
**GET /aip/v1/stylist/services**

```
curl http://apiserver/api/v1/stylist/services \
  -H 'Authorization: Token jwt_token'
```


**Response 200 OK**
```
{
    "services": [
        {
            "id": 1,
            "name": "Service 1",
            "description": "Great service",
            "duration_minutes": 25,
            "base_price": 25.0,
            "is_enabled": true,
            "photo_samples": []
        },
        {
            "id": 2,
            "name": "Service 2",
            "description": "Even better service",
            "duration_minutes": 35,
            "base_price": 35.0,
            "is_enabled": false,
            "photo_samples": [
                {
                    "url": "http://example.com/photo_1.jpg"
                },
                {
                    "url": "http://example.com/photo_1.jpg"
                }
            ]
        },
    ]
}
```


### Bulk add/update services

Note on semantics: this endpoint is **very NOT RESTFul**, because it allows to mix
updates to existing objects and creation of new objects in one batch. Semantically,
PUT cannot be used here, because indempotence is not guaranteed (nor even pretended
to be observed). Hence, this endpoint only supports **POST** method.

Endpoint accepts array (list) of objects to be replaced or added. If `id` field is
supplied - object will be updated with new values. If `id` field is missing or is `null`,
new object will be created.

**POST /api/v1/stylist/services**
**Content-Type=application/json**

```
curl -X POST http://apiserver/api/v1/stylist/services \
  -H 'Authorization: Token jwt_token' \
  -H 'Content-Type: application/json' \
  -d '[
    {
        "name": "Nail polish",
        "description": "We're adding new service here",
        "base_price": 25.0,
        "duration_minutes": 25,
        "is_enabled": true
    },
    {
        "id": 25,
        "name": "Hair cut",
        "description": "Updating existing service here",
        "base_price": 35.0,
        "duration_minutes": 45,
        "is_enabled": false
    }
   ]'
```


**Response 200/201 OK** (200 if no new objects were created, 201 if new objects created)
```
{
    "services": [
        {
            "id": 26, // note: DB object was created, hence the id
            "name": "Nail polish",
            "description": "We're adding new service here",
            "base_price": 25.0,
            "duration_minutes": 25,
            "is_enabled": true
        },
        {
            "id": 25, // note: it was an existing object, so id is unchanged
            "name": "Hair cut",
            "description": "Updating existing service here",
            "base_price": 35.0,
            "duration_minutes": 45,
            "is_enabled": false
        }
    ]
}
```

### Permanently delete a service
Note: this will actually delete it from list, rather than just disable.
Actual `salon.StylistService` object will be kept in the DB, but `deleted_at` field will be non-null

**DELETE /api/v1/stylist/services/{service_id}**
(ex. if we have `26` for service id, will delete the last one from previous example)


**Response 200 OK**
```
[
    {
        "id": 25,
        "name": "Hair cut",
        "description": "Updating existing service here",
        "base_price": 35.0,
        "duration_minutes": 45,
        "is_enabled": false
    }
]
```