from app import create_app
from db import get_db

def verify_optimizations():
    app = create_app()
    with app.app_context():
        try:
            db = get_db()
            print("Testing Dashboard Queries...")
            
            # Test 1: Product Count
            count_res = db.execute('SELECT COUNT(*) as count FROM productos').fetchone()
            print(f"Product Count Result: {count_res}")
            print(f"Product Count Value: {count_res['count']}")
            
            # Test 2: Sale Count
            sale_res = db.execute('SELECT COUNT(*) as count FROM ventas').fetchone()
            print(f"Sale Count Result: {sale_res}")
            print(f"Sale Count Value: {sale_res['count']}")
            
            # Test 3: Income
            income_res = db.execute('SELECT SUM(total) as total FROM ventas WHERE estado != "cancelado"').fetchone()
            print(f"Income Result: {income_res}")
            # Handle None if no sales
            val = income_res['total'] or 0
            print(f"Income Value: {val}")
            
            print("\nVERIFICATION SUCCESSFUL: All dashboard queries work with dictionary access.")
            
        except Exception as e:
            print(f"\nVERIFICATION FAILED: {e}")

if __name__ == '__main__':
    verify_optimizations()
