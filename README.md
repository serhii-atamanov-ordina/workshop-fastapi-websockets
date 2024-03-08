# FastAPI Example

Example FastAPI application.

Plan:

1. Complete endpoints to be able to use CREATE, GET (single, list), DELETE methods. You can test result in Postman/Insomnia or in docs by "http://127.0.0.1:8000/api/v1/docs"
2. Provide data validation for Post model (unique post name, content limits).
3. Add one more model, User with fields name and password.
4. Implement Authentication based on bearer token. you can get one in auth.py. You should retrieve name and password from database and compare to one that you have in your token.

Advanced level:

5. Implement WebSockets to extend create Post view logic. Frontend will constantly listen your events. To enable frontend . You should send new, latest list with each call of the create object logic.
Frontend accepts this format:

[
    {
        "name": "First one",
        "content": "My first post. Very promissing",
        "user_id": 1,
        "id": "1",
        "created_at": "2024-01-01T00:00:00"
    }
]

6. Implement testing of each endpoing.

Extras:

7. Link posts to be accessible by users/1/posts/
8. Test linked endpoints
