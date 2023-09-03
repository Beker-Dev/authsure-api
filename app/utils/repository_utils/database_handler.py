from fastapi import HTTPException


def handle_session(func):
    def wrapper(*args, **kwargs):
        response = None

        try:
            response = func(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            error = "Database error: " + str(e)
            raise HTTPException(400, error)
        else:
            return response

    return wrapper
