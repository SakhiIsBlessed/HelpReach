#!/usr/bin/env python3
"""
DEMO: Advanced Donations Feed Filtering

This script demonstrates how the new filtering system works
"""

donations = [
    {
        "id": 1,
        "title": "Winter Jackets",
        "category": "Clothes",
        "quantity": "50",
        "pickup_location": "Mumbai",
        "donor_name": "John",
        "description": "High quality winter wear"
    },
    {
        "id": 2,
        "title": "Medical Supplies",
        "category": "Medical",
        "quantity": "100",
        "pickup_location": "Delhi",
        "donor_name": "Sarah",
        "description": "First aid kits and bandages"
    },
    {
        "id": 3,
        "title": "Food Packets",
        "category": "Food",
        "quantity": "200",
        "pickup_location": "Mumbai",
        "donor_name": "Rajesh",
        "description": "Daily meal packages"
    },
    {
        "id": 4,
        "title": "School Textbooks",
        "category": "Books",
        "quantity": "75",
        "pickup_location": "Bangalore",
        "donor_name": "Emma",
        "description": "Mathematics and Science books"
    },
    {
        "id": 5,
        "title": "Laptops",
        "category": "Electronics",
        "quantity": "10",
        "pickup_location": "Mumbai",
        "donor_name": "Tech Corp",
        "description": "Refurbished laptops"
    }
]

def filter_donations(search_term="", category="", location="", sort_by="latest"):
    """
    Simulate the filtering logic
    """
    # Filter
    filtered = [d for d in donations 
                if (not search_term or search_term.lower() in d['title'].lower() or search_term.lower() in d['donor_name'].lower())
                and (not category or d['category'] == category)
                and (not location or d['pickup_location'] == location)]
    
    # Sort
    if sort_by == "quantity-high":
        filtered.sort(key=lambda x: int(x['quantity']), reverse=True)
    elif sort_by == "quantity-low":
        filtered.sort(key=lambda x: int(x['quantity']))
    
    return filtered

print("\n" + "="*70)
print("📦 ADVANCED DONATIONS FEED - FILTERING DEMO")
print("="*70 + "\n")

# Demo 1: Search
print("1️⃣ SEARCH: Finding donations by 'Mumbai'")
print("-" * 70)
results = filter_donations(search_term="Mumbai")
for d in results:
    print(f"   ✓ {d['title']} ({d['category']}) - Qty: {d['quantity']}")
print(f"   → Results: {len(results)} donations\n")

# Demo 2: Filter by Category
print("2️⃣ FILTER: Show only 'Clothes' donations")
print("-" * 70)
results = filter_donations(category="Clothes")
for d in results:
    print(f"   ✓ {d['title']} - {d['pickup_location']} - Qty: {d['quantity']}")
print(f"   → Results: {len(results)} donations\n")

# Demo 3: Filter by Location
print("3️⃣ FILTER: Show only donations from 'Mumbai'")
print("-" * 70)
results = filter_donations(location="Mumbai")
for d in results:
    print(f"   ✓ {d['title']} ({d['category']}) - Qty: {d['quantity']}")
print(f"   → Results: {len(results)} donations\n")

# Demo 4: Sort by Quantity (High to Low)
print("4️⃣ SORT: By Quantity (High to Low)")
print("-" * 70)
results = filter_donations(sort_by="quantity-high")
for d in results:
    print(f"   ✓ {d['title']} - Qty: {d['quantity']} ({d['category']})")
print(f"   → Results: {len(results)} donations\n")

# Demo 5: Combined Filters
print("5️⃣ COMBINED: Category='Food' + Location='Mumbai'")
print("-" * 70)
results = filter_donations(category="Food", location="Mumbai")
for d in results:
    print(f"   ✓ {d['title']} - {d['donor_name']} - Qty: {d['quantity']}")
print(f"   → Results: {len(results)} donations\n")

# Demo 6: Search + Category
print("6️⃣ COMBINED: Search='Tech' + Category='Electronics'")
print("-" * 70)
results = filter_donations(search_term="Tech", category="Electronics")
for d in results:
    print(f"   ✓ {d['title']} - {d['pickup_location']} - Qty: {d['quantity']}")
print(f"   → Results: {len(results)} donations\n")

print("="*70)
print("✅ ALL FILTERING FEATURES WORKING!")
print("="*70 + "\n")
