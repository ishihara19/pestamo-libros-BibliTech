from app.schemas.paginacion_sch import PaginationParams, PaginatedResponse

def test_pagination_params_offset_limit():
    params = PaginationParams(page=2, page_size=5)
    assert params.offset == 5
    assert params.limit == 5

def test_paginated_response_create():
    params = PaginationParams(page=1, page_size=2)
    items = [1,2]
    resp = PaginatedResponse.create(items=items, total=10, params=params)
    assert resp.items == items
    assert resp.total_pages == 5
    assert resp.has_next is True
    assert resp.has_prev is False
