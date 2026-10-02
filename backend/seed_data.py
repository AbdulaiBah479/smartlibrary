# backend/seed_data.py

print("LOADING SEED_DATA.PY NOW...")


from backend.dao import add_author, add_book, create_user, create_member
import traceback


def seed():
    print("Starting seed...")

    # 1. Create admin user
    try:
        create_user(username="admin", password="adminpass", role_id=1)
        print("Admin user created.")
    except Exception as e:
        print("Admin user ERROR:", e)
        traceback.print_exc()

    # 2. Add authors
    try:
        a1 = add_author("Chinua Achebe")
        print("Author 1:", a1)
    except Exception as e:
        print("Author 1 ERROR:", e)
        traceback.print_exc()
        return

    try:
        a2 = add_author("Ngugi wa Thiong'o")
        print("Author 2:", a2)
    except Exception as e:
        print("Author 2 ERROR:", e)
        traceback.print_exc()
        return

    try:
        a3 = add_author("Wole Soyinka")
        print("Author 3:", a3)
    except Exception as e:
        print("Author 3 ERROR:", e)
        traceback.print_exc()
        return

    # 3. Add books
    try:
        add_book(
            title="Things Fall Apart",
            author_id=a1,
            isbn="ISBN-001",
            copies=3
        )
        add_book(
            title="No Longer at Ease",
            author_id=a1,
            isbn="ISBN-002",
            copies=2
        )
        add_book(
            title="Petals of Blood",
            author_id=a2,
            isbn="ISBN-003",
            copies=1
        )
        add_book(
            title="The River Between",
            author_id=a2,
            isbn="ISBN-004",
            copies=2
        )
        add_book(
            title="Death and the King’s Horseman",
            author_id=a3,
            isbn="ISBN-005",
            copies=2
        )

        print("Books added OK!")
    except Exception as e:
        print("BOOK ERROR:", e)
        traceback.print_exc()
        return

    print("SEED COMPLETED SUCCESSFULLY!")


if __name__ == "__main__":
    seed()
