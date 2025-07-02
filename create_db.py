from app import db, Booking, Order

# Force create all tables
with db.engine.begin() as conn:
    db.metadata.drop_all(bind=conn)
    db.metadata.create_all(bind=conn)

# Add test data
booking = Booking(name="Isaac", room_type="Deluxe", date_from="2025-07-02", date_to="2025-07-03")
order = Order(name="Isaac", food_items="Pizza, Sushi, Fries")

db.session.add_all([booking, order])
db.session.commit()

print("Tables in metadata:", db.metadata.tables)

