from fastapi import HTTPException

def raise_404(detailed_str:str):
    raise HTTPException(status_code=404, detail=detailed_str)