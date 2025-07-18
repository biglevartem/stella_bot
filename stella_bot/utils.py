from sqlalchemy import or_
from .database import Session, Product


def search_products(query: str, limit: int = 3) -> list[Product]:
    session = Session()
    q = session.query(Product).filter(
        or_(
            Product.name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
    ).limit(limit)
    results = q.all()
    session.close()
    return results


def format_products(products: list[Product]) -> str:
    lines = []
    for p in products:
        line = f"{p.name}\n{p.description}\n{p.link}"
        lines.append(line)
    return "\n\n".join(lines)
