"""Generate synthetic data for Frying Nemo restaurant."""

from __future__ import annotations

import random
from datetime import date, datetime, timedelta
from pathlib import Path

import polars as pl
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

OUTPUT_DIR = Path(__file__).resolve().parent
COMPRESSION = "zstd"

# Volume constants
NUM_VENDORS = 12
NUM_STAFF = 25
NUM_MENU_ITEMS = 45
NUM_GUESTS = 500
DATE_START = date(2024, 1, 1)
DATE_END = date(2025, 12, 31)
AVG_DAILY_ORDERS = 55
TAX_RATE = 0.08
MONTHLY_RENT = 8500.0
MONTHLY_UTILITIES = 2200.0

# Realistic seafood restaurant data
SEAFOOD_DISHES: dict[str, list[tuple[str, float, float]]] = {
    "appetizer": [
        ("Clam Chowder Cup", 9.50, 2.85),
        ("Coconut Shrimp", 14.00, 4.20),
        ("Ahi Tuna Tartare", 16.00, 5.60),
        ("Crispy Calamari", 13.00, 3.90),
        ("Oysters on the Half Shell", 18.00, 7.20),
        ("Lobster Bisque", 12.00, 4.20),
        ("Ceviche", 14.50, 4.35),
        ("Crab Cakes", 15.00, 5.25),
    ],
    "entree": [
        ("Grilled Atlantic Salmon", 28.00, 9.80),
        ("Fish and Chips", 19.00, 5.70),
        ("Lobster Tail", 42.00, 16.80),
        ("Pan-Seared Sea Bass", 34.00, 11.90),
        ("Shrimp Scampi", 24.00, 7.20),
        ("Blackened Mahi Mahi", 26.00, 7.80),
        ("Seafood Paella", 32.00, 11.20),
        ("Grilled Swordfish", 30.00, 10.50),
        ("Cioppino", 29.00, 10.15),
        ("Stuffed Flounder", 27.00, 8.10),
        ("Surf and Turf", 45.00, 18.00),
        ("Cedar Plank Trout", 25.00, 7.50),
        ("Miso-Glazed Cod", 26.00, 7.80),
        ("Tuna Poke Bowl", 22.00, 7.70),
        ("Shrimp Po' Boy", 18.00, 5.40),
    ],
    "dessert": [
        ("Key Lime Pie", 10.00, 2.50),
        ("Chocolate Lava Cake", 12.00, 3.00),
        ("Crème Brûlée", 11.00, 2.75),
        ("Coconut Panna Cotta", 10.50, 2.63),
        ("Seasonal Sorbet", 8.00, 1.60),
    ],
    "side": [
        ("Garlic Mashed Potatoes", 7.00, 1.40),
        ("Grilled Asparagus", 8.00, 2.40),
        ("Coleslaw", 5.00, 0.75),
        ("Hush Puppies", 6.00, 1.20),
        ("Mac and Cheese", 7.50, 1.50),
        ("Seasoned Fries", 6.00, 1.20),
        ("Side Salad", 7.00, 1.75),
    ],
    "drink": [
        ("Iced Tea", 3.50, 0.35),
        ("Lemonade", 4.00, 0.60),
        ("Craft IPA", 8.00, 2.40),
        ("House White Wine", 11.00, 3.30),
        ("House Red Wine", 11.00, 3.30),
        ("Margarita", 13.00, 3.25),
        ("Sparkling Water", 3.00, 0.60),
        ("Soda", 3.00, 0.45),
    ],
    "kids": [
        ("Kid's Fish Sticks", 8.00, 1.60),
        ("Kid's Mac and Cheese", 7.00, 1.05),
    ],
}

VENDOR_DATA = [
    ("Ocean Fresh Seafood Co.", "seafood", "net_30"),
    ("Atlantic Fish Supply", "seafood", "net_30"),
    ("Harbor Shellfish", "seafood", "net_15"),
    ("Green Valley Farms", "produce", "net_15"),
    ("Sunny Acres Produce", "produce", "cod"),
    ("Dairy Direct", "dairy", "net_15"),
    ("Pacific Dry Goods", "dry_goods", "net_30"),
    ("Metro Beverage Dist.", "beverages", "net_30"),
    ("Coastal Spirits", "beverages", "net_15"),
    ("Restaurant Depot", "supplies", "cod"),
    ("ProKitchen Equipment", "equipment", "net_60"),
    ("CleanRight Supply", "supplies", "net_30"),
]

ROLES_CONFIG: dict[str, tuple[int, float, float]] = {
    "manager": (2, 28.00, 35.00),
    "chef": (2, 22.00, 30.00),
    "sous_chef": (2, 18.00, 24.00),
    "line_cook": (4, 15.00, 20.00),
    "prep_cook": (3, 14.00, 17.00),
    "server": (5, 12.00, 16.00),
    "bartender": (2, 14.00, 19.00),
    "host": (2, 13.00, 16.00),
    "busser": (2, 12.00, 14.00),
    "dishwasher": (1, 12.00, 14.00),
}

INGREDIENTS = [
    ("Atlantic Salmon Fillet", "lb", 12.50, "seafood"),
    ("Cod Fillet", "lb", 9.00, "seafood"),
    ("Jumbo Shrimp", "lb", 14.00, "seafood"),
    ("Lobster Tail", "each", 18.00, "seafood"),
    ("Sea Bass Fillet", "lb", 16.00, "seafood"),
    ("Ahi Tuna", "lb", 22.00, "seafood"),
    ("Calamari", "lb", 8.00, "seafood"),
    ("Littleneck Clams", "lb", 6.00, "seafood"),
    ("Oysters", "each", 1.50, "seafood"),
    ("Mahi Mahi", "lb", 11.00, "seafood"),
    ("Swordfish Steak", "lb", 15.00, "seafood"),
    ("Flounder Fillet", "lb", 10.00, "seafood"),
    ("Trout", "lb", 9.50, "seafood"),
    ("Crab Meat", "lb", 20.00, "seafood"),
    ("Butter", "lb", 4.50, "dairy"),
    ("Heavy Cream", "l", 5.00, "dairy"),
    ("Parmesan Cheese", "lb", 12.00, "dairy"),
    ("Lemons", "each", 0.50, "produce"),
    ("Garlic", "lb", 3.00, "produce"),
    ("Asparagus", "lb", 4.50, "produce"),
    ("Potatoes", "lb", 1.20, "produce"),
    ("Mixed Greens", "lb", 3.50, "produce"),
    ("Tomatoes", "lb", 2.50, "produce"),
    ("Onions", "lb", 1.00, "produce"),
    ("Flour", "lb", 0.60, "dry_goods"),
    ("Olive Oil", "l", 8.00, "dry_goods"),
    ("Panko Breadcrumbs", "lb", 3.00, "dry_goods"),
    ("Rice", "lb", 1.50, "dry_goods"),
    ("Pasta", "lb", 1.80, "dry_goods"),
    ("Coconut Milk", "l", 3.00, "dry_goods"),
    ("Craft IPA (keg)", "each", 180.00, "beverages"),
    ("House White Wine (case)", "case", 85.00, "beverages"),
    ("House Red Wine (case)", "case", 85.00, "beverages"),
    ("Tequila (bottle)", "each", 28.00, "beverages"),
    ("Soda Syrup (box)", "each", 45.00, "beverages"),
]

REVIEW_TEMPLATES_POSITIVE = [
    "The {dish} was absolutely incredible! Fresh and perfectly prepared.",
    "Best seafood in town. Our server {server} was fantastic.",
    "We loved the {dish}. Will definitely be coming back!",
    "Great atmosphere and even better food. The {dish} is a must-try.",
    "Everything was delicious. {server} gave us excellent recommendations.",
    "Fresh catch of the day was outstanding. Perfect date night spot.",
    "The {dish} melted in my mouth. Five stars all around!",
    "Wonderful experience from start to finish. Can't wait to return.",
]

REVIEW_TEMPLATES_NEGATIVE = [
    "The {dish} was overcooked and dry. Disappointing for the price.",
    "Long wait times even with a reservation. Food was just okay.",
    "Service was slow and our server seemed overwhelmed.",
    "Expected better quality for a seafood place. The {dish} was bland.",
]

REVIEW_TEMPLATES_MIXED = [
    "Food was great but the wait was too long. The {dish} saved the night.",
    "Nice ambiance. {dish} was good but portions could be bigger.",
    "Solid meal overall. {server} was friendly but kitchen was backed up.",
    "The appetizers were amazing but the {dish} didn't live up to the hype.",
]

CAMPAIGN_NAMES = [
    ("Summer Seafood Festival", "email", "families"),
    ("Happy Hour Tuesdays", "instagram", "young_professionals"),
    ("Lobster Night Launch", "facebook", "foodies"),
    ("Valentine's Dinner Special", "email", "couples"),
    ("Lunch Express Promo", "sms", "office_workers"),
    ("Grand Opening Anniversary", "local_print", "local_residents"),
    ("Weekend Brunch Launch", "instagram", "brunch_crowd"),
    ("Thanksgiving Pre-Order", "email", "families"),
    ("Holiday Party Packages", "facebook", "corporate"),
    ("New Year's Eve Gala", "email", "couples"),
    ("Oyster Half-Price Mondays", "sms", "regulars"),
    ("Kids Eat Free Sundays", "local_print", "families"),
]


def _uid(prefix: str, n: int) -> str:
    return f"{prefix}-{n:04d}"


def generate_vendors() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for i, (name, category, terms) in enumerate(VENDOR_DATA, 1):
        rows.append(
            {
                "vendor_id": _uid("VND", i),
                "name": name,
                "contact_name": fake.name(),
                "contact_email": fake.company_email(),
                "contact_phone": fake.phone_number(),
                "category": category,
                "payment_terms": terms,
            }
        )
    return rows


def generate_staff() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1
    for role, (count, rate_min, rate_max) in ROLES_CONFIG.items():
        for _ in range(count):
            hire = fake.date_between(
                start_date=date(2020, 1, 1), end_date=DATE_START
            )
            rows.append(
                {
                    "staff_id": _uid("STF", idx),
                    "first_name": fake.first_name(),
                    "last_name": fake.last_name(),
                    "role": role,
                    "hire_date": hire,
                    "hourly_rate": round(random.uniform(rate_min, rate_max), 2),
                    "is_active": random.random() > 0.08,
                }
            )
            idx += 1
    return rows


def generate_menu_items() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1
    for category, items in SEAFOOD_DISHES.items():
        for name, price, cost in items:
            rows.append(
                {
                    "item_id": _uid("MNU", idx),
                    "name": name,
                    "category": category,
                    "price": price,
                    "cost": cost,
                    "is_active": True,
                }
            )
            idx += 1
    return rows


def generate_recipes(
    menu_items: list[dict[str, object]],
    ingredients: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1
    units = ["oz", "lb", "g", "cup", "tbsp", "tsp", "each", "ml"]
    for item in menu_items:
        if item["category"] == "drink":
            n_ingredients = random.randint(1, 3)
        else:
            n_ingredients = random.randint(2, 6)
        chosen = random.sample(
            ingredients, min(n_ingredients, len(ingredients))
        )
        for ing in chosen:
            rows.append(
                {
                    "recipe_id": _uid("RCP", idx),
                    "item_id": item["item_id"],
                    "ingredient": ing["name"],
                    "quantity": round(random.uniform(0.5, 8.0), 2),
                    "unit": random.choice(units),
                }
            )
            idx += 1
    return rows


def generate_inventory(
    vendors: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    seafood_vendors = [v for v in vendors if v["category"] == "seafood"]
    produce_vendors = [v for v in vendors if v["category"] == "produce"]
    dairy_vendors = [v for v in vendors if v["category"] == "dairy"]
    dry_vendors = [v for v in vendors if v["category"] == "dry_goods"]
    bev_vendors = [v for v in vendors if v["category"] == "beverages"]
    supply_vendors = [v for v in vendors if v["category"] == "supplies"]

    category_vendor_map = {
        "seafood": seafood_vendors,
        "produce": produce_vendors,
        "dairy": dairy_vendors,
        "dry_goods": dry_vendors,
        "beverages": bev_vendors,
        "supplies": supply_vendors,
    }

    for i, (name, unit, cost, cat) in enumerate(INGREDIENTS, 1):
        vendor_pool = category_vendor_map.get(cat, supply_vendors)
        vendor = random.choice(vendor_pool) if vendor_pool else vendors[0]
        rows.append(
            {
                "ingredient_id": _uid("ING", i),
                "name": name,
                "unit": unit,
                "qty_on_hand": round(random.uniform(5, 100), 1),
                "reorder_point": round(random.uniform(2, 20), 1),
                "unit_cost": cost,
                "vendor_id": vendor["vendor_id"],
                "last_ordered": fake.date_between(
                    start_date=DATE_END - timedelta(days=14), end_date=DATE_END
                ),
            }
        )
    return rows


def generate_guests() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for i in range(1, NUM_GUESTS + 1):
        first_visit = fake.date_between(start_date=DATE_START, end_date=DATE_END)
        visits = max(1, int(random.expovariate(0.3)))
        last_delta = timedelta(days=random.randint(0, (DATE_END - first_visit).days))
        last_visit = min(first_visit + last_delta, DATE_END)
        rows.append(
            {
                "guest_id": _uid("GST", i),
                "first_name": fake.first_name(),
                "last_name": fake.last_name(),
                "email": fake.email() if random.random() > 0.30 else None,
                "phone": fake.phone_number() if random.random() > 0.20 else None,
                "visit_count": visits,
                "first_visit": first_visit,
                "last_visit": last_visit,
            }
        )
    return rows


def generate_reservations(
    guests: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1
    times = ["17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30"]
    statuses = ["confirmed", "seated", "completed", "no_show", "cancelled"]
    status_weights = [0.05, 0.05, 0.70, 0.10, 0.10]

    for guest in guests:
        n_reservations = max(0, guest["visit_count"] - random.randint(0, 2))  # type: ignore[operator]
        for _ in range(n_reservations):
            res_date = fake.date_between(start_date=DATE_START, end_date=DATE_END)
            rows.append(
                {
                    "reservation_id": _uid("RSV", idx),
                    "guest_id": guest["guest_id"],
                    "reservation_date": res_date,
                    "reservation_time": random.choice(times),
                    "party_size": random.choices(
                        [1, 2, 3, 4, 5, 6], weights=[5, 35, 15, 25, 10, 10]
                    )[0],
                    "status": random.choices(statuses, weights=status_weights)[0],
                    "notes": (
                        fake.sentence(nb_words=6) if random.random() > 0.7 else None
                    ),
                }
            )
            idx += 1
    return rows


def generate_orders_and_items(
    staff: list[dict[str, object]],
    guests: list[dict[str, object]],
    menu_items: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    orders: list[dict[str, object]] = []
    items: list[dict[str, object]] = []
    order_idx = 1
    item_idx = 1

    servers = [s for s in staff if s["role"] in ("server", "bartender")]
    active_items = [m for m in menu_items if m["is_active"]]
    entrees = [m for m in active_items if m["category"] == "entree"]
    appetizers = [m for m in active_items if m["category"] == "appetizer"]
    desserts = [m for m in active_items if m["category"] == "dessert"]
    sides = [m for m in active_items if m["category"] == "side"]
    drinks = [m for m in active_items if m["category"] == "drink"]
    kids_items = [m for m in active_items if m["category"] == "kids"]

    payment_methods = ["credit_card", "debit_card", "cash", "gift_card"]
    payment_weights = [0.55, 0.20, 0.20, 0.05]

    current = DATE_START
    while current <= DATE_END:
        dow = current.weekday()
        is_weekend = dow >= 4  # Fri-Sat
        base = AVG_DAILY_ORDERS
        if is_weekend:
            base = int(base * 1.4)
        # seasonal bump in summer
        month = current.month
        if month in (6, 7, 8):
            base = int(base * 1.15)
        elif month == 12:
            base = int(base * 1.25)

        n_orders = max(10, int(random.gauss(base, base * 0.15)))

        for _ in range(n_orders):
            # lunch (11:30-14:00) or dinner (17:00-21:30)
            if random.random() < 0.35:
                hour = random.randint(11, 13)
                minute = random.choice([0, 15, 30, 45])
            else:
                hour = random.randint(17, 21)
                minute = random.choice([0, 15, 30, 45])

            ts = datetime(current.year, current.month, current.day, hour, minute)
            server = random.choice(servers)
            guest = random.choice(guests) if random.random() > 0.3 else None
            table = random.randint(1, 20)

            # build the order items
            order_items: list[dict[str, object]] = []

            # party composition
            party = random.choices([1, 2, 3, 4], weights=[15, 40, 20, 25])[0]
            for _ in range(party):
                # each person gets an entree
                entree = random.choice(entrees)
                order_items.append(
                    {
                        "item_id": entree["item_id"],
                        "quantity": 1,
                        "unit_price": entree["price"],
                        "modifiers": None,
                    }
                )
                # 40% chance of appetizer
                if random.random() < 0.40 and appetizers:
                    app = random.choice(appetizers)
                    order_items.append(
                        {
                            "item_id": app["item_id"],
                            "quantity": 1,
                            "unit_price": app["price"],
                            "modifiers": None,
                        }
                    )
                # 60% chance of drink
                if random.random() < 0.60 and drinks:
                    drink = random.choice(drinks)
                    order_items.append(
                        {
                            "item_id": drink["item_id"],
                            "quantity": 1,
                            "unit_price": drink["price"],
                            "modifiers": None,
                        }
                    )
                # 25% chance of side
                if random.random() < 0.25 and sides:
                    side = random.choice(sides)
                    order_items.append(
                        {
                            "item_id": side["item_id"],
                            "quantity": 1,
                            "unit_price": side["price"],
                            "modifiers": None,
                        }
                    )
                # 20% chance of dessert
                if random.random() < 0.20 and desserts:
                    des = random.choice(desserts)
                    order_items.append(
                        {
                            "item_id": des["item_id"],
                            "quantity": 1,
                            "unit_price": des["price"],
                            "modifiers": None,
                        }
                    )
                # 5% chance of kids item
                if random.random() < 0.05 and kids_items:
                    kid = random.choice(kids_items)
                    order_items.append(
                        {
                            "item_id": kid["item_id"],
                            "quantity": 1,
                            "unit_price": kid["price"],
                            "modifiers": None,
                        }
                    )

            subtotal = round(
                sum(
                    float(oi["unit_price"]) * int(oi["quantity"])
                    for oi in order_items
                ),
                2,
            )
            tax = round(subtotal * TAX_RATE, 2)
            tip_pct = max(0, random.gauss(0.18, 0.05))
            tip = round(subtotal * tip_pct, 2)
            total = round(subtotal + tax + tip, 2)

            oid = _uid("ORD", order_idx)
            orders.append(
                {
                    "order_id": oid,
                    "order_timestamp": ts,
                    "table_number": table,
                    "server_id": server["staff_id"],
                    "guest_id": guest["guest_id"] if guest else None,
                    "payment_method": random.choices(
                        payment_methods, weights=payment_weights
                    )[0],
                    "subtotal": subtotal,
                    "tax": tax,
                    "tip": tip,
                    "total": total,
                }
            )

            for oi in order_items:
                items.append(
                    {
                        "order_item_id": _uid("OIT", item_idx),
                        "order_id": oid,
                        **oi,
                    }
                )
                item_idx += 1

            order_idx += 1

        current += timedelta(days=1)

    return orders, items


def generate_reviews(
    guests: list[dict[str, object]],
    menu_items: list[dict[str, object]],
    staff: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    servers = [s for s in staff if s["role"] == "server"]
    entree_names = [
        m["name"] for m in menu_items if m["category"] in ("entree", "appetizer")
    ]
    platforms = ["google", "yelp", "tripadvisor", "internal"]
    platform_weights = [0.35, 0.30, 0.15, 0.20]

    idx = 1
    for guest in guests:
        if random.random() > 0.25:
            continue
        n_reviews = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
        for _ in range(n_reviews):
            # skewed positive: mostly 4-5, some 3, few 1-2
            rating = random.choices(
                [1, 2, 3, 4, 5], weights=[3, 5, 12, 35, 45]
            )[0]
            dish = random.choice(entree_names)
            server_name = f"{random.choice(servers)['first_name']}"

            if rating >= 4:
                tmpl = random.choice(REVIEW_TEMPLATES_POSITIVE)
            elif rating == 3:
                tmpl = random.choice(REVIEW_TEMPLATES_MIXED)
            else:
                tmpl = random.choice(REVIEW_TEMPLATES_NEGATIVE)

            text = tmpl.format(dish=dish, server=server_name)

            rows.append(
                {
                    "review_id": _uid("REV", idx),
                    "guest_id": guest["guest_id"],
                    "review_date": fake.date_between(
                        start_date=DATE_START, end_date=DATE_END
                    ),
                    "rating": rating,
                    "review_text": text,
                    "platform": random.choices(platforms, weights=platform_weights)[0],
                }
            )
            idx += 1
    return rows


def generate_campaigns() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for i, (name, channel, audience) in enumerate(CAMPAIGN_NAMES, 1):
        start = fake.date_between(start_date=DATE_START, end_date=DATE_END)
        duration = random.randint(7, 30)
        end = min(start + timedelta(days=duration), DATE_END)
        rows.append(
            {
                "campaign_id": _uid("CMP", i),
                "name": name,
                "channel": channel,
                "start_date": start,
                "end_date": end,
                "budget": round(random.uniform(200, 3000), 2),
                "target_audience": audience,
            }
        )
    return rows


def generate_campaign_events(
    campaigns: list[dict[str, object]],
    guests: list[dict[str, object]],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    idx = 1

    for campaign in campaigns:
        n_sends = random.randint(100, 500)
        start = campaign["start_date"]
        end = campaign["end_date"]
        assert isinstance(start, date)
        assert isinstance(end, date)
        campaign_days = max(1, (end - start).days)

        for _ in range(n_sends):
            guest = random.choice(guests)
            day_offset = random.randint(0, campaign_days)
            event_date = start + timedelta(days=day_offset)
            ts = datetime(
                event_date.year,
                event_date.month,
                event_date.day,
                random.randint(8, 20),
                random.randint(0, 59),
            )

            # funnel: send -> open (40%) -> click (20%) -> conversion (5%)
            rows.append(
                {
                    "event_id": _uid("EVT", idx),
                    "campaign_id": campaign["campaign_id"],
                    "event_type": "send",
                    "event_timestamp": ts,
                    "guest_id": guest["guest_id"],
                }
            )
            idx += 1

            if random.random() < 0.40:
                rows.append(
                    {
                        "event_id": _uid("EVT", idx),
                        "campaign_id": campaign["campaign_id"],
                        "event_type": "open",
                        "event_timestamp": ts
                        + timedelta(minutes=random.randint(5, 1440)),
                        "guest_id": guest["guest_id"],
                    }
                )
                idx += 1

                if random.random() < 0.50:
                    rows.append(
                        {
                            "event_id": _uid("EVT", idx),
                            "campaign_id": campaign["campaign_id"],
                            "event_type": "click",
                            "event_timestamp": ts
                            + timedelta(minutes=random.randint(6, 1500)),
                            "guest_id": guest["guest_id"],
                        }
                    )
                    idx += 1

                    if random.random() < 0.25:
                        rows.append(
                            {
                                "event_id": _uid("EVT", idx),
                                "campaign_id": campaign["campaign_id"],
                                "event_type": "conversion",
                                "event_timestamp": ts
                                + timedelta(minutes=random.randint(10, 2880)),
                                "guest_id": guest["guest_id"],
                            }
                        )
                        idx += 1
            elif random.random() < 0.03:
                rows.append(
                    {
                        "event_id": _uid("EVT", idx),
                        "campaign_id": campaign["campaign_id"],
                        "event_type": "unsubscribe",
                        "event_timestamp": ts
                        + timedelta(minutes=random.randint(1, 60)),
                        "guest_id": guest["guest_id"],
                    }
                )
                idx += 1

    return rows


def generate_daily_financials(
    orders: list[dict[str, object]],
    menu_items: list[dict[str, object]],
    order_items: list[dict[str, object]],
    staff: list[dict[str, object]],
    campaigns: list[dict[str, object]],
) -> list[dict[str, object]]:
    item_cost_map = {m["item_id"]: float(m["cost"]) for m in menu_items}

    # aggregate orders by date
    daily_revenue: dict[date, float] = {}
    daily_cogs: dict[date, float] = {}
    order_dates: dict[str, date] = {}

    for o in orders:
        ts = o["order_timestamp"]
        assert isinstance(ts, datetime)
        d = ts.date()
        order_dates[str(o["order_id"])] = d
        daily_revenue[d] = daily_revenue.get(d, 0.0) + float(o["subtotal"])

    for oi in order_items:
        d = order_dates.get(str(oi["order_id"]))
        if d is None:
            continue
        cost = item_cost_map.get(str(oi["item_id"]), 0.0)
        daily_cogs[d] = daily_cogs.get(d, 0.0) + cost * int(oi["quantity"])

    # daily labor cost estimate
    active_staff = [s for s in staff if s["is_active"]]
    avg_hourly = sum(float(s["hourly_rate"]) for s in active_staff) / len(active_staff)
    # ~12 staff working ~7 hours avg per day
    daily_labor = round(avg_hourly * 12 * 7, 2)

    daily_rent = round(MONTHLY_RENT / 30, 2)
    daily_utilities = round(MONTHLY_UTILITIES / 30, 2)

    # campaign spend by date
    campaign_daily: dict[date, float] = {}
    for c in campaigns:
        start = c["start_date"]
        end = c["end_date"]
        assert isinstance(start, date)
        assert isinstance(end, date)
        days = max(1, (end - start).days)
        daily_spend = float(c["budget"]) / days
        current = start
        while current <= end:
            campaign_daily[current] = campaign_daily.get(current, 0.0) + daily_spend
            current += timedelta(days=1)

    rows: list[dict[str, object]] = []
    current = DATE_START
    while current <= DATE_END:
        rev = round(daily_revenue.get(current, 0.0), 2)
        cogs = round(daily_cogs.get(current, 0.0), 2)
        mktg = round(campaign_daily.get(current, 0.0), 2)
        other = round(random.uniform(50, 200), 2)
        expenses = cogs + daily_labor + daily_rent + daily_utilities + mktg + other
        net = round(rev - expenses, 2)

        rows.append(
            {
                "financial_date": current,
                "revenue": rev,
                "cogs": cogs,
                "labor_cost": daily_labor,
                "rent": daily_rent,
                "utilities": daily_utilities,
                "marketing_spend": mktg,
                "other_expenses": other,
                "net_income": net,
            }
        )
        current += timedelta(days=1)

    return rows


def write_parquet(data: list[dict[str, object]], name: str) -> None:
    df = pl.DataFrame(data)
    path = OUTPUT_DIR / f"{name}.parquet"
    df.write_parquet(path, compression=COMPRESSION)
    print(f"  {name}: {len(data):,} rows -> {path}")


def main() -> None:
    print("Generating Frying Nemo synthetic data...")
    print(f"  Date range: {DATE_START} to {DATE_END}")
    print(f"  Output: {OUTPUT_DIR}")
    print()

    vendors = generate_vendors()
    write_parquet(vendors, "vendors")

    staff = generate_staff()
    write_parquet(staff, "staff")

    menu_items = generate_menu_items()
    write_parquet(menu_items, "menu_items")

    recipes = generate_recipes(menu_items, [{"name": i[0]} for i in INGREDIENTS])
    write_parquet(recipes, "recipes")

    inventory = generate_inventory(vendors)
    write_parquet(inventory, "inventory")

    guests = generate_guests()
    write_parquet(guests, "guests")

    reservations = generate_reservations(guests)
    write_parquet(reservations, "reservations")

    orders, order_items = generate_orders_and_items(staff, guests, menu_items)
    write_parquet(orders, "orders")
    write_parquet(order_items, "order_items")

    reviews = generate_reviews(guests, menu_items, staff)
    write_parquet(reviews, "reviews")

    campaigns = generate_campaigns()
    write_parquet(campaigns, "campaigns")

    campaign_events = generate_campaign_events(campaigns, guests)
    write_parquet(campaign_events, "campaign_events")

    financials = generate_daily_financials(
        orders, menu_items, order_items, staff, campaigns
    )
    write_parquet(financials, "daily_financials")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
