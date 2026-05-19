from pydantic import BaseModel

class PaginatedMeta(BaseModel):
    total_rows: int
    current_page: int
    page_size: int
    total_pages: int 