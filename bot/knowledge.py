"""Rule-based knowledge base for the Felo assistant."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Iterable, List, Optional

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "products.json"


@dataclass
class FAQItem:
    question: str
    answer: str


@dataclass
class Product:
    id: str
    name: str
    summary: str
    price_rub: int
    flavors: List[str]
    availability: str
    key_ingredients: List[str]
    recommended_for: List[str]
    benefits: List[str]
    how_to_use: str
    faq: List[FAQItem]


@dataclass
class SupportContact:
    email: str
    phone: str
    telegram: str


@dataclass
class DeliveryInfo:
    moscow: str
    regions: str
    pickup: str


@dataclass
class DeliveryCost:
    moscow: str
    regions: str
    pickup: str


class ProductKnowledge:
    """Encapsulates basic business logic for both the web and Telegram bot."""

    def __init__(
        self,
        *,
        brand: str,
        products: List[Product],
        support_contact: SupportContact,
        shipping: DeliveryInfo,
        payment: Iterable[str],
        return_policy: str,
        delivery_cost: DeliveryCost,
    ) -> None:
        self.brand = brand
        self.products = products
        self.support_contact = support_contact
        self.shipping = shipping
        self.payment = list(payment)
        self.return_policy = return_policy
        self.delivery_cost = delivery_cost

    @classmethod
    def load_default(cls) -> "ProductKnowledge":
        data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "ProductKnowledge":
        products = [
            Product(
                id=product["id"],
                name=product["name"],
                summary=product["summary"],
                price_rub=product["price_rub"],
                flavors=list(product["flavors"]),
                availability=product["availability"],
                key_ingredients=list(product["key_ingredients"]),
                recommended_for=list(product["recommended_for"]),
                benefits=list(product["benefits"]),
                how_to_use=product["how_to_use"],
                faq=[FAQItem(**faq_item) for faq_item in product.get("faq", [])],
            )
            for product in data.get("products", [])
        ]

        support_contact = SupportContact(**data["support_contact"])
        shipping = DeliveryInfo(**data["shipping"])
        delivery_cost = DeliveryCost(**data["delivery_cost"])

        return cls(
            brand=data.get("brand", "Felo"),
            products=products,
            support_contact=support_contact,
            shipping=shipping,
            payment=data.get("payment", []),
            return_policy=data.get("return_policy", ""),
            delivery_cost=delivery_cost,
        )

    def greeting(self) -> str:
        return (
            f"Здравствуйте! Я помогу подобрать продукты {self.brand}. Расскажите, что хотите улучшить — "
            "энергию, концентрацию, сон или иммунитет."
        )

    def _find_by_slug(self, slug: str) -> Optional[Product]:
        return next((product for product in self.products if product.id == slug), None)

    def find_product(self, text: str) -> Optional[Product]:
        normalized = text.lower()
        synonyms = {
            "spray": "focus-spray",
            "спрей": "focus-spray",
            "focus": "focus-spray",
            "фокус": "focus-spray",
            "energy": "energy-gummies",
            "энерг": "energy-gummies",
            "пастил": "energy-gummies",
            "gummies": "energy-gummies",
            "calm": "calm-tea",
            "сон": "calm-tea",
            "чай": "calm-tea",
            "immunity": "immunity-shot",
            "shot": "immunity-shot",
            "иммун": "immunity-shot",
        }

        for key, slug in synonyms.items():
            if key in normalized:
                product = self._find_by_slug(slug)
                if product:
                    return product

        for product in self.products:
            if normalized in product.name.lower():
                return product
            if any(normalized in tag.lower() for tag in product.recommended_for):
                return product

        return None

    def detect_need(self, text: str) -> Optional[str]:
        normalized = text.lower()
        need_patterns = {
            "energy": ["энерг", "бодр", "утро", "спорт", "тонус"],
            "focus": ["концент", "фокус", "работ", "учеб", "памят"],
            "sleep": ["сон", "расслаб", "вечер", "уснуть", "стресс"],
            "immunity": ["иммун", "простуд", "болеть", "витамин", "защит"],
        }

        for need, patterns in need_patterns.items():
            if any(pattern in normalized for pattern in patterns):
                return need
        return None

    def recommendations(self, need: str) -> List[Product]:
        rules = {
            "energy": lambda product: any(
                keyword in tag.lower() for keyword in ("энерг", "спорт") for tag in product.recommended_for
            ),
            "focus": lambda product: any(
                keyword in tag.lower() for keyword in ("концент", "работ") for tag in product.recommended_for
            ),
            "sleep": lambda product: any(
                keyword in tag.lower() for keyword in ("сон", "стресс") for tag in product.recommended_for
            ),
            "immunity": lambda product: any(
                keyword in tag.lower() for keyword in ("иммун", "восстанов") for tag in product.recommended_for
            ),
        }
        predicate = rules.get(need)
        return [product for product in self.products if predicate and predicate(product)]

    def product_brief(self, product: Product) -> str:
        return f"{product.name} — {product.summary} Стоимость: {product.price_rub} ₽."

    def product_details(self, product: Product) -> str:
        benefits = "; ".join(product.benefits)
        flavors = ", ".join(product.flavors)
        return (
            f"{product.name}. {product.summary}\n"
            f"Стоимость: {product.price_rub} ₽. Вкус: {flavors}.\n"
            f"Преимущества: {benefits}.\n"
            f"Как применять: {product.how_to_use}. Статус: {product.availability}."
        )

    def product_faq(self, product: Product) -> str:
        if not product.faq:
            return ""
        return "\n\n".join(f"Q: {item.question}\nA: {item.answer}" for item in product.faq)

    def general_info(self, text: str) -> Optional[List[str]]:
        normalized = text.lower()

        if any(word in normalized for word in ("достав", "курьер", "самовывоз")):
            return [
                f"Доставка по Москве: {self.shipping.moscow}",
                f"Регионы: {self.shipping.regions}",
                f"Самовывоз: {self.shipping.pickup}",
                (
                    "Стоимость доставки: "
                    f"Москва — {self.delivery_cost.moscow}, регионы — {self.delivery_cost.regions}, "
                    f"самовывоз — {self.delivery_cost.pickup}."
                ),
            ]

        if any(word in normalized for word in ("оплат", "карто", "сбп", "платеж")):
            methods = "\n".join(f"• {method}" for method in self.payment)
            return ["Мы принимаем:", methods]

        if any(word in normalized for word in ("возврат", "обмен", "гарант")):
            return [self.return_policy]

        if any(word in normalized for word in ("консульт", "связ", "контакт", "телефон")):
            contact = self.support_contact
            return [
                "Свяжитесь с нами удобным способом:",
                f"Email: {contact.email}",
                f"Телефон: {contact.phone}",
                f"Telegram: {contact.telegram}",
            ]

        if "предзаказ" in normalized or "налич" in normalized:
            immunity = self._find_by_slug("immunity-shot")
            if immunity:
                return [
                    f"Сейчас {immunity.name} доступен по предзаказу.",
                    f"Статус: {immunity.availability}. Можем закрепить упаковку и уведомить о доставке.",
                ]

        if any(word in normalized for word in ("заказ", "оформ", "купить")):
            return [
                (
                    "Чтобы оформить заказ, напишите контакты и предпочтительный способ связи. "
                    "Мы подтвердим наличие и отправим ссылку на оплату."
                )
            ]

        if any(word in normalized for word in ("спасибо", "благодар")):
            return ["Спасибо, что обратились! Если появятся вопросы, я всегда рядом."]

        return None

    def product_list(self) -> str:
        return "\n".join(
            f"• {product.name} — {product.price_rub} ₽" for product in self.products
        )

    def top_highlights(self, limit: int = 2) -> List[str]:
        return [self.product_brief(product) for product in self.products[:limit]]


__all__ = ["ProductKnowledge", "DATA_PATH"]
