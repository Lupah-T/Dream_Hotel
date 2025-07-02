# inspect_db.py
from app import db, Booking, Order

print("📦 Bookings:")
for b in Booking.query.all():
    print(f"👤 {b.name} | 🏨 {b.room_type} | 📅 {b.date_from} → {b.date_to}")

print("\n🍽️ Orders:")
for o in Order.query.all():
    print(f"👤 {o.name} | 🍕 {o.food_items}")

