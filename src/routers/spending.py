from fastapi import APIRouter


router = APIRouter(prefix="/spending", tags=["spending"])


@router.get("/")
async def get_spendings():
    # return all spendings.
    return {"message": "Hello, World!"}


@router.post("/")
async def create_spending():
    # create a spending.
    return {"message": "Hello, World!"}


@router.get("/{spending_id}")
async def get_spending(spending_id: int):
    # return a spending.
    return {"message": "Hello, World!"}


@router.put("/{spending_id}")
async def update_spending(spending_id: int):
    # update a spending.
    return {"message": "Hello, World!"}


@router.delete("/{spending_id}")
async def delete_spending(spending_id: int):
    # delete a spending.
    return {"message": "Hello, World!"}
