from app import app, db, Mortgage, MortgageEvent, generate_mortgage_schedule
from datetime import date

def test_schedule():
    with app.app_context():
        # Create dummy mortgage in memory (or temp DB)
        # We'll just define one and pass it, but generate_mortgage_schedule needs db access for events? 
        # No, it passed mortgage object which has .events rel.
        
        # We need to mock.
        class MockEvent:
            def __init__(self, date, type, value, balance_after=None):
                self.date = date
                self.type = type
                self.value = value
                self.balance_after = balance_after
                
        class MockMortgage:
            def __init__(self):
                self.start_date = date(2024, 1, 1)
                self.term_years = 30
                self.original_principal = 500000.0
                self.has_mrta = True
                self.mrta_original_amount = 500000.0
                self.mrta_rate = 4.0
                self.events = [
                    MockEvent(date(2024, 1, 1), 'RATE_CHANGE', 4.0, 500000.0)
                ]
                
        m = MockMortgage()
        schedule = generate_mortgage_schedule(m)
        
        print(f"Schedule Length: {len(schedule)}")
        print("First 5 rows:")
        for r in schedule[:5]:
            print(f"Month {r['no']}: Bal={r['balance']:.2f}, MRTA={r['mrta_coverage']:.2f}, Net={r['net_exposure']:.2f}")
            
        print("...")
        print("Row 120 (10 years):")
        r = schedule[120]
        print(f"Month {r['no']}: Bal={r['balance']:.2f}, MRTA={r['mrta_coverage']:.2f}, Net={r['net_exposure']:.2f}")

if __name__ == "__main__":
    test_schedule()
