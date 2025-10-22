import sqlite3
import time
import random
import string

# Step 1: Connect to SQLite Database (will create file if not exist)
conn = sqlite3.connect("users_performance.db")
cursor = conn.cursor()

# Step 2: Create Users table
cursor.execute("DROP TABLE IF EXISTS Users;")
cursor.execute("""
CREATE TABLE Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Email TEXT,
    LastLoginDate TEXT
);
""")

conn.commit()
print("Users table created.")

# Step 3: Generate Random Data (simulate millions of users)
def random_string(length):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

print("Inserting sample data (this might take a while)...")

for i in range(100000):  # 1 lakh rows — you can increase to 1 million if you want
    name = random_string(8)
    email = f"{name}{i}@example.com"
    date = f"2025-10-{random.randint(1,28)}"
    cursor.execute("INSERT INTO Users (Name, Email, LastLoginDate) VALUES (?, ?, ?)", (name, email, date))

conn.commit()
print("Sample data inserted successfully.")

# Step 4: Query before adding index
email_to_find = "abc500@example.com"  # A random email that might exist or not
print("\n Searching before index...")
start = time.time()

cursor.execute("SELECT * FROM Users WHERE Email = ?", (email_to_find,))
result = cursor.fetchall()

end = time.time()
print(f" Query time without index: {end - start:.4f} seconds")
print(f"Result: {result}")

# Step 5: Add Index on Email
print("\n Creating index on Email...")
cursor.execute("CREATE INDEX idx_email ON Users(Email);")
conn.commit()

# Step 6: Query after adding index
print("\n Searching after index...")
start = time.time()

cursor.execute("SELECT * FROM Users WHERE Email = ?", (email_to_find,))
result = cursor.fetchall()

end = time.time()
print(f" Query time with index: {end - start:.4f} seconds")
print(f"Result: {result}")

conn.close()
print("\n  Done. You can see the speed difference above.")
