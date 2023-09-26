from .dependency import ProductQueryParams
from .models import Product


class ProductFilter:
    def __init__(self, params: ProductQueryParams):
        self.params = params

    def apply_filters(self, query):
        if self.params.category_id is not None:
            query = query.filter(Product.category_id == self.params.category_id)
        if self.params.search_query:
            query = query.filter(Product.name.ilike(f"%{self.params.search_query}%"))
        return query

    def apply_sort(self, query):
        if self.params.sort_order == "low_to_high":
            return query.order_by(Product.price)
        elif self.params.sort_order == "high_to_low":
            return query.order_by(Product.price.desc())
        return query
