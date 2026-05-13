from fastapi import FastAPI, Query

# Create FastAPI app
app = FastAPI()

# ---------------------------------------------------
# Fake Database
# ---------------------------------------------------
fake_users = [
    {"id": i, "name": f"User {i}"}
    for i in range(1, 101)
]


# ---------------------------------------------------
# Get Users with Pagination
# ---------------------------------------------------
@app.get("/users")
def get_users(
        limit: int = Query(
            default=5,
            ge=1,
            le=50,
            description="Number of users to return"
        ),

        skip: int = Query(
            default=0,
            ge=0,
            description="Number of users to skip"
        )
):
    """
    Pagination API

    limit -> number of records to return
    skip  -> number of records to skip
    """

    # Pagination logic
    paginated_users = fake_users[skip: skip + limit]

                                # fake_users[start : end]
                                # skip = 0, limit = 5
                                # fake_user[0 : 5]
                                # skip =3 , limit =3
                                # fake_user[3 : 6]

    # Response
    return {
        "total_users": len(fake_users),        # total data count
        "limit": limit,                        # how many returned
        "skip": skip,                          # how many skipped
        "users": paginated_users               # actual result
    }



