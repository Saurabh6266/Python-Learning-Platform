import database

if __name__ == '__main__':
    print("Initializing database...")
    database.init_db()
    print("Database tables created.")
    
    print("Migrating data from JSON files...")
    database.migrate_from_json()
    print("Migration completed.")