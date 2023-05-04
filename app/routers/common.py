from fastapi import HTTPException, status

def item_not_found_exception():
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

def access_denied_exception():
    return  HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")