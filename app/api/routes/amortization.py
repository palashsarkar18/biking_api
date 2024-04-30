from fastapi import APIRouter, HTTPException
from typing import Dict
from decimal import Decimal
from app.plans import STARTER_PLAN, PRO_PLAN, ENTERPRISE_PLAN

router = APIRouter()


def get_plan(plan_type: str):
    if plan_type == "starter":
        return STARTER_PLAN
    elif plan_type == "pro":
        return PRO_PLAN
    elif plan_type == "enterprise":
        return ENTERPRISE_PLAN
    else:
        return None


@router.get("/")
def calculate_amortization(plan_type: str, bike_price: float) -> Dict:
    plan = get_plan(plan_type)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    residual_value: Decimal = Decimal(bike_price) * plan.residual_percentage
    initial_loan_balance: Decimal = Decimal(bike_price) - residual_value
    monthly_interest_rate = plan.annual_interest_rate / 12

    amortization_table = []
    current_balance = initial_loan_balance
    total_interest_paid = 0

    for month in range(1, plan.max_duration_month + 1):
        if current_balance <= 0:
            break
        interest_payment = current_balance * monthly_interest_rate
        principal_payment = min(
            plan.monthly_payment - interest_payment,
            current_balance
            )
        current_balance -= principal_payment

        total_interest_paid += interest_payment

        amortization_table.append({
            "month_number": month,
            "loan_balance": float(current_balance),
            "monthly_interest_payment": float(interest_payment),
            "monthly_principal_repayment": float(principal_payment)
        })

    return {
        "leasing_duration": len(amortization_table),
        "total_interest_paid": float(total_interest_paid),
        "residual_value": float(residual_value),
        "amortization_table": amortization_table
    }
