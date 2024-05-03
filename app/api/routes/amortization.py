from fastapi import APIRouter, HTTPException
from typing import Dict
from decimal import Decimal
from app.plans import STARTER_PLAN, PRO_PLAN, ENTERPRISE_PLAN

router = APIRouter()


def get_plan(plan_type: str):
    """
    Retrieve a plan based on the provided plan type.

    Args:
        plan_type (str): The type of plan to retrieve.

    Returns:
        Plan: A plan object matching the provided type, or None if not found.
    """
    plans = {
        "starter": STARTER_PLAN,
        "pro": PRO_PLAN,
        "enterprise": ENTERPRISE_PLAN,
    }
    return plans.get(plan_type)


@router.get("/")
def calculate_amortization(plan_type: str, bike_price: float) -> Dict:
    """
    Calculate the amortization schedule for a bike leasing contract.

    Args:
        plan_type (str): The type of leasing plan (e.g., "starter", "pro").
        bike_price (float): The price of the bike being leased.

    Returns:
        dict: A dictionary containing:
            - "leasing_duration": int, duration of the lease in months
            - "total_interest_paid": float, total interest paid over the lease
            - "residual_value": float, residual value of the bike
            - "amortization_table": list of dicts, each dict containing:
                - "month_number": int, the month number
                - "loan_balance": float, the remaining balance after the payment
                - "monthly_interest_payment": float, interest paid this month
                - "monthly_principal_repayment": float, principal paid this month
    """
    plan = get_plan(plan_type)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    if bike_price > plan.max_principal:
        raise HTTPException(status_code=404,
                            detail="Bike price exceeds the maximum principal")

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
        principal_payment = min(plan.monthly_payment - interest_payment, current_balance)
        current_balance -= principal_payment

        total_interest_paid += interest_payment

        amortization_table.append({
            "month_number": month,
            "loan_balance": round(float(current_balance), 2),
            "monthly_interest_payment": round(float(interest_payment), 2),
            "monthly_principal_repayment": round(float(principal_payment), 2),
        })

    return {
        "leasing_duration": len(amortization_table),
        "total_interest_paid": round(float(total_interest_paid), 2),
        "residual_value": round(float(residual_value), 2),
        "amortization_table": amortization_table,
    }
