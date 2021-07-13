# API for car tracker  

## Routes

### Create user

Do a ``POST`` on ``/user`` with

```json
{
    "email": "john@email.com",
    "name": "John Titor"
}
```

On success will return:

```json
{
  "id": 1,
  "name": "John Titor",
  "email": "john@email.com",
  "chip": null
}
```

On duplicate email will return:

```json
{
  "title": "400 Bad Request",
  "description": "User already registered"
}
```

### List all users

Do a ``GET``  on ``/user``. Will return a list of users, e.g.:

```json
[
  {
    "id": 1,
    "name": "John Titor",
    "email": "john@email.com",
    "chip": null
  },
  {
    "id": 2,
    "name": "John Titor",
    "email": "john2@email.com",
    "chip": null
  }
]
```

### Get one user by ID

Do a ``GET`` on ``/user/{user_id}``. Will return:

```json
{
  "id": 1,
  "name": "John Titor",
  "email": "john@email.com",
  "chip": null
}
```

---

### Create chip

Do a ``POST`` on ``/chip``

```json
{
    "iccid": "iccid_here"
}
```

On success will return:

```json
{
  "id": 1,
  "iccid": "iccid_here",
  "user_id": null
}
```

On duplicate ICCID will return:

```json
{
  "title": "400 Bad Request",
  "description": "A chip with this ICCID already exists"
}
```

### List all chips

Do a ``GET``  on ``/chip``. Will return a list of chips, e.g.:

```json
[
  {
    "id": 1,
    "iccid": "iccid_here",
    "user_id": null
  }
]
```

### Get one chip by ID

Do a ``GET`` on ``/user/{chip_id}``. Will return:

```json
{
  "id": 1,
  "iccid": "iccid_here",
  "user_id": null
}
```

### Link a chip to a user

Do a ``PATCH`` on ``/chip`` in this format:

```json
{
    "user_id": 1,
    "chip_id": 1
}
```

That will return:

```json
{
  "id": 1,
  "name": "John Titor",
  "email": "john@email.com",
  "chip": {
    "id": 1,
    "iccid": "2196532a1aad0f",
    "user_id": 1
  }
}
```

---

### Create a new location

Do a ``POST`` on ``/location`` in this format:

```json
{
    "id": "iccid_here",
    "timestamp": 1625682554,
    "lat": -3.056223,
    "lon": -60.045798,
    "speed": 3.0000,
    "batt": 51.0
}
```

On success will return:

```json
{
  "id": 1,
  "lat": -3.056223,
  "lon": -60.045798,
  "timestamp": "2021-07-07 18:29:14",
  "user_id": 1
}
```

If there's no chip with this ICCID registered, will return:

```json
{
  "title": "400 Bad Request",
  "description": "Invalid ICCID."
}
```

### List all locations of a user

Doing a ``GET`` on ``/location/{user_id}/all`` returns:

If the user has sent at least one:

```json
[
  {
    "id": 2,
    "lat": -3.056223,
    "lon": -60.045798,
    "timestamp": "2021-07-07 18:29:24",
    "user_id": 1
  },
  {
    "id": 1,
    "lat": -3.056223,
    "lon": -60.045798,
    "timestamp": "2021-07-07 18:29:14",
    "user_id": 1
  }
]
```

Otherwise:

```json
{
  "title": "400 Bad Request",
  "description": "This user didn't send any location yet."
}
```

### Get a link to Google Maps on the user's last location

Do a ``GET`` on ``/location/{user_id}/last`` to get:

```json
{
  "link": "https://www.google.com/maps/search/-3.056223%20-60.045798"
}
```
