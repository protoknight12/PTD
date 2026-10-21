"""Data access layer.

Every function returns what its PostgreSQL query will return (dicts with schema.sql column
names), so wiring in the database only changes this file. Each TODO(db) shows the query.
"""

ITEMS = [
    {"id": 1, "type": "movie", "title": "Dune: Part Two", "creator": "Denis Villeneuve", "year": 2024, "genre": "Sci-Fi",
     "color1": "#c9813f", "color2": "#3b1d0e", "featured": True, "rating": 4.6, "rating_count": 142000,
     "description": "Paul Atreides unites with the Fremen on a path of revenge against the conspirators who destroyed his family."},
    {"id": 2, "type": "movie", "title": "Oppenheimer", "creator": "Christopher Nolan", "year": 2023, "genre": "Drama",
     "color1": "#2a4c91", "color2": "#0d1530", "rating": 4.4, "rating_count": 98000},
    {"id": 3, "type": "movie", "title": "Past Lives", "creator": "Celine Song", "year": 2023, "genre": "Romance",
     "color1": "#d14f8a", "color2": "#3a0f2a", "rating": 4.2, "rating_count": 31000},
    {"id": 4, "type": "movie", "title": "Perfect Days", "creator": "Wim Wenders", "year": 2023, "genre": "Drama",
     "color1": "#4c9a7a", "color2": "#0e2a22", "rating": 4.2, "rating_count": 12000},
    {"id": 5, "type": "movie", "title": "Poor Things", "creator": "Yorgos Lanthimos", "year": 2023, "genre": "Comedy",
     "color1": "#6339a4", "color2": "#170c2b", "rating": 4.1, "rating_count": 54000},
    {"id": 6, "type": "movie", "title": "Anatomy of a Fall", "creator": "Justine Triet", "year": 2023, "genre": "Thriller",
     "color1": "#a8432f", "color2": "#2a0e0a", "rating": 4.0, "rating_count": 27000},
    {"id": 7, "type": "book", "title": "Project Hail Mary", "creator": "Andy Weir", "year": 2021, "genre": "Sci-Fi",
     "color1": "#b7a0ff", "color2": "#2b2150", "rating": 4.5, "rating_count": 64000},
    {"id": 8, "type": "book", "title": "Tomorrow, and Tomorrow, and Tomorrow", "creator": "Gabrielle Zevin", "year": 2022,
     "genre": "Fiction", "color1": "#d8a44a", "color2": "#3a2608", "rating": 4.2, "rating_count": 41000},
    {"id": 9, "type": "book", "title": "Piranesi", "creator": "Susanna Clarke", "year": 2020, "genre": "Fantasy",
     "color1": "#3f7bb5", "color2": "#0b1d33", "rating": 4.3, "rating_count": 38000},
    {"id": 10, "type": "book", "title": "Circe", "creator": "Madeline Miller", "year": 2018, "genre": "Myth",
     "color1": "#872f67", "color2": "#22091a", "rating": 4.3, "rating_count": 52000},
    {"id": 11, "type": "book", "title": "The Overstory", "creator": "Richard Powers", "year": 2018, "genre": "Fiction",
     "color1": "#5d8a4a", "color2": "#142410", "rating": 4.1, "rating_count": 19000},
    {"id": 12, "type": "music", "title": "Blonde", "creator": "Frank Ocean", "year": 2016, "genre": "R&B",
     "color1": "#9b9aff", "color2": "#1a1a4a", "rating": 4.6, "rating_count": 47000},
    {"id": 13, "type": "music", "title": "To Pimp a Butterfly", "creator": "Kendrick Lamar", "year": 2015, "genre": "Hip-Hop",
     "color1": "#e06c4c", "color2": "#3a120a", "rating": 4.7, "rating_count": 51000},
    {"id": 14, "type": "music", "title": "In Rainbows", "creator": "Radiohead", "year": 2007, "genre": "Alt Rock",
     "color1": "#4cb5c9", "color2": "#0b2a30", "rating": 4.5, "rating_count": 45000},
    {"id": 15, "type": "music", "title": "Brat", "creator": "Charli XCX", "year": 2024, "genre": "Pop",
     "color1": "#c4a5ff", "color2": "#2a1a45", "rating": 4.3, "rating_count": 22000},
    {"id": 16, "type": "music", "title": "Rumours", "creator": "Fleetwood Mac", "year": 1977, "genre": "Rock",
     "color1": "#b58a3f", "color2": "#2a1d08", "rating": 4.5, "rating_count": 39000},
]

REVIEWS = [
    {"name": "Maya K.", "title": "Past Lives", "type": "movie", "rating": 5,
     "body": "Quiet, aching and devastatingly honest. The final walk to the taxi says more than any monologue could."},
    {"name": "Jonah R.", "title": "Piranesi", "type": "book", "rating": 4,
     "body": "A strange, gentle labyrinth of a novel. Slow at first, then impossible to put down."},
    {"name": "Sofia L.", "title": "In Rainbows", "type": "music", "rating": 5,
     "body": 'Seventeen years later and "Reckoner" still sounds like it came from the future.'},
]

# ponytail: in-memory until PostgreSQL is wired in; signups are lost on restart.
_users = []

# TODO(db): every item query selects ratings computed from reviews:
#   SELECT i.*, ROUND(AVG(r.rating), 1)::float AS rating, COUNT(r.id) AS rating_count
#   FROM items i LEFT JOIN reviews r ON r.item_id = i.id ... GROUP BY i.id


def get_featured():
    # TODO(db): <item select> WHERE i.featured GROUP BY i.id LIMIT 1
    return next((item for item in ITEMS if item.get("featured")), None)


def get_top_rated(item_type, limit=5):
    # TODO(db): <item select> WHERE i.type = %s GROUP BY i.id
    #           ORDER BY rating DESC NULLS LAST, rating_count DESC LIMIT %s
    items = [item for item in ITEMS if item["type"] == item_type]
    return sorted(items, key=lambda item: item["rating"], reverse=True)[:limit]


def get_latest_reviews(limit=3):
    # TODO(db): SELECT r.rating, r.body, r.created_at, u.name, i.title, i.type
    #           FROM reviews r JOIN users u ON u.id = r.user_id JOIN items i ON i.id = r.item_id
    #           WHERE r.body IS NOT NULL ORDER BY r.created_at DESC LIMIT %s
    return REVIEWS[:limit]


def get_user_by_email(email):
    # TODO(db): SELECT * FROM users WHERE lower(email) = lower(%s)
    return next((user for user in _users if user["email"].lower() == email.lower()), None)


def create_user(name, email, password_hash):
    """Returns the new user, or None if the email is already registered (case-insensitive)."""
    # TODO(db): INSERT INTO users (name, email, password_hash) VALUES (%s, %s, %s) RETURNING *
    #           and return None on psycopg.errors.UniqueViolation.
    if get_user_by_email(email):
        return None
    user = {"id": len(_users) + 1, "name": name, "email": email, "password_hash": password_hash}
    _users.append(user)
    return user
