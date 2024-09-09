# Product Name
> Knox connect

Project for technical interview.

## Run project

BUild container:

```sh
docker-compose build
```

Run container:

```sh
docker-compose up
```

##Create superuser for django:

```sh
docker-compose exec web python manage.py createsuperuser
```

##List of api end_points
1. Signing Up (`http://127.0.0.1:8000/api/knox_connect/sign-up`)

2. Login (`http://127.0.0.1:8000/api/token/`)

3. Send friend request (`http://127.0.0.1:8000/api/knox_connect/send-friend-request`)

4. Accept or Reject Friend request (`http://127.0.0.1:8000/api/knox_connect/respond-on-request/<str:pk>`)

5. Accepted friend list (`http://127.0.0.1:8000/api/knox_connect/friends-list/Accepted`)

6. Pending friend list (`http://127.0.0.1:8000/api/knox_connect/friends-list/Pending`)

7. Search users (`http://127.0.0.1:8000/api/knox_connect/search-users/?q=a`)

9. Add users for testing (`http://127.0.0.1:8000/api/knox_connect/add-users-for-testing`)

 checkout http://127.0.0.1:8000/api/schema/docs for more api documentation

## Development setup

 checkout Knox Connect apis.postman_collection.json file

