import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eta_estimator.settings')
django.setup()

from estimator.models import Job, ResourceGroup, Trade, Estimator
from django.db import connection

def cleanup_database():
    """Clean up all data from the database tables."""
    print("Starting database cleanup...")
    
    try:
        # Delete in correct order to maintain referential integrity
        print("Deleting Jobs...")
        Job.objects.all().delete()
        
        print("Deleting Resource Groups...")
        ResourceGroup.objects.all().delete()
        
        print("Deleting Estimators...")
        Estimator.objects.all().delete()
        
        print("Deleting Trades...")
        Trade.objects.all().delete()
        
        # Reset sequences if using PostgreSQL
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$ 
                DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                        EXECUTE 'ALTER SEQUENCE IF EXISTS ' || quote_ident(r.tablename) || '_id_seq RESTART WITH 1';
                    END LOOP;
                END $$;
            """)
        
        print("Database cleanup completed successfully!")
        
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Ask for confirmation before proceeding
    response = input("This will delete ALL data from the database. Are you sure you want to continue? (yes/no): ")
    if response.lower() == 'yes':
        cleanup_database()
    else:
        print("Cleanup cancelled.") 