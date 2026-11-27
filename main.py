from src.manager import Manager
from src.models import Parameters
import sys

def print_section_header(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}")


def print_subsection_header(title: str):
    """Print a formatted subsection header"""
    print(f"\n  {title}")
    print(f"  {'-' * 40}")


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"{amount:,.2f} PLN"


def display_apartments(manager):
    """Display all apartments with their rooms and bills"""
    print_section_header("APARTMENTS")
    
    for apartment in manager.apartments.values():
        print(f"\n📍 {apartment.name} ({apartment.key})")
        print(f"   Location: {apartment.location}")
        print(f"   Total Area: {apartment.area_m2} m²")
        
        print_subsection_header("Rooms")
        for room in apartment.rooms.values():
            print(f"      • {room.name:<25} {room.area_m2:>6} m²")
        
        # Find bills for this apartment
        apartment_bills = [bill for bill in manager.bills if bill.apartment == apartment.key]
        if apartment_bills:
            print_subsection_header("Bills")
            for bill in apartment_bills:
                month_year = f"{bill.settlement_month}/{bill.settlement_year}" if bill.settlement_month and bill.settlement_year else "N/A"
                print(f"      • {bill.type:<15} {format_currency(bill.amount_pln):>15}  Due: {bill.date_due}  Period: {month_year}")


def display_tenants(manager):
    """Display all tenants with their details and transfers"""
    print_section_header("TENANTS")
    
    for tenant in manager.tenants.values():
        print(f"\n👤 {tenant.name}")
        print(f"   Apartment: {tenant.apartment}")
        print(f"   Room: {tenant.room}")
        print(f"   Rent: {format_currency(tenant.rent_pln)}/month")
        print(f"   Deposit: {format_currency(tenant.deposit_pln)}")
        print(f"   Agreement: {tenant.date_agreement_from} to {tenant.date_agreement_to}")
        
        # Find transfers for this tenant
        tenant_transfers = [transfer for transfer in manager.transfers if transfer.tenant == tenant.name]
        if tenant_transfers:
            print_subsection_header("Transfers")
            for transfer in tenant_transfers:
                month_year = f"{transfer.settlement_month}/{transfer.settlement_year}" if transfer.settlement_month and transfer.settlement_year else "N/A"
                print(f"      • {format_currency(transfer.amount_pln):>15}  Date: {transfer.date}  Period: {month_year}")


def main() -> int:
    args = sys.argv[1:]
    if not args:
        manager = Manager(Parameters())
        display_apartments(manager)
        display_tenants(manager)
        print(f"\n{'=' * 70}\n")
        return 0

    if len(args) != 3:
        print("Usage: python main.py APARTMENT_KEY YEAR MONTH", file=sys.stderr)
        return 2

    apartment_key, year_arg, month_arg = args
    try:
        year = int(year_arg)
        month = int(month_arg)
    except ValueError:
        print("Year and month must be integers.", file=sys.stderr)
        return 2

    if not 1 <= month <= 12:
        print("Month must be between 1 and 12.", file=sys.stderr)
        return 2

    manager = Manager(Parameters())
    settlement = manager.get_settlement(apartment_key, year, month)
    if settlement is None:
        print(f"Unknown apartment: {apartment_key}", file=sys.stderr)
        return 1

    print_section_header(f"SETTLEMENT {apartment_key} {year}-{month:02d}")
    print(f"Apartment costs: {format_currency(settlement.total_due_pln)}")
    for tenant in manager.create_tenants_settlements(settlement) or []:
        print(f"{tenant.tenant}: {format_currency(tenant.total_due_pln)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())