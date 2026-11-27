import pytest

from src.manager import Manager
from src.models import Parameters, Transfer


def test_tenant_charges_add_up_to_apartment_cost():
    manager = Manager(Parameters())
    settlement = manager.get_settlement("apart-polanka", 2025, 1)
    assert settlement is not None
    assert settlement.total_due_pln == pytest.approx(910)

    tenant_settlements = manager.create_tenants_settlements(settlement)
    assert tenant_settlements is not None
    assert len(tenant_settlements) == 3
    total = sum(tenant.total_due_pln for tenant in tenant_settlements)
    assert total == pytest.approx(settlement.total_due_pln)


def test_get_tax_filters_by_period_and_rounds():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=amount,
            date=date,
            settlement_year=year,
            settlement_month=month,
            tenant="tenant-1",
        )
        for amount, date, year, month in [
            (100, "2025-01-04", 2025, 1),
            (110, "2025-01-05", 2025, 1),
            (500, "2025-02-04", 2025, 2),
            (900, "2024-01-04", 2024, 1),
        ]
    ]

    assert manager.get_tax(2025, 1, 0.085) == 18
    assert manager.get_tax(2025, 3, 0.085) == 0