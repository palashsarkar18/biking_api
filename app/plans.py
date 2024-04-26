from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Plan:
    type: str
    max_principal: int
    annual_interest_rate: Decimal
    residual_percentage: Decimal
    max_duration_month: int
    monthly_payment: int


STARTER_PLAN = Plan(
    type="starter",
    max_principal=3500,
    annual_interest_rate=Decimal("0.12"),  # 12 %
    residual_percentage=Decimal("0.05"),  # 5 %
    max_duration_month=36,
    monthly_payment=100,
)

PRO_PLAN = Plan(
    type="pro",
    max_principal=4000,
    annual_interest_rate=Decimal("0.1"),  # 10 %
    residual_percentage=Decimal("0.05"),  # 5 %
    max_duration_month=48,
    monthly_payment=100,
)

ENTERPRISE_PLAN = Plan(
    type="enterprise",
    max_principal=5000,
    annual_interest_rate=Decimal("0.06"),  # 6 %
    residual_percentage=Decimal("0.05"),  # 5 %
    max_duration_month=60,
    monthly_payment=150,
)
