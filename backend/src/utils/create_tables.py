"""Script to create user and prompts tables in testdb database"""

import os
import psycopg2
from dotenv import load_dotenv

# env variables
env_path = os.path.join(os.path.dirname(__file__), "../../../.env")
load_dotenv(dotenv_path=env_path)

# database connection variables
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_SERVER")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB_Test")
def check_tables_exist():
    """Check if tables exist in the database"""
    try:
        print("**********DATABASE SELF-CHECKING START**********")
        # Print connection parameters (excluding password)
        print(f"Connection parameters: database={DB_NAME}, user={DB_USER}, host={DB_HOST}, port={DB_PORT}")
        
        # Ensure password is not empty
        if not DB_PASSWORD:
            print("WARNING: Database password is empty!")
        
        # Connect to testdb database
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        
        # Create cursor
        with conn.cursor() as cur:
            # Check if user schema exists
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'user';")
            user_schema_exists = cur.fetchone() is not None
            
            # Check if prompt schema exists
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'prompt';")
            prompt_schema_exists = cur.fetchone() is not None
            
            # Check if team schema exists
            cur.execute("SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'team';")
            team_schema_exists = cur.fetchone() is not None
            
            # Check if users table exists in user schema
            users_table_exists = False
            if user_schema_exists:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'user' 
                        AND table_name = 'users'
                    );
                """)
                users_table_exists = cur.fetchone()[0]
            
            # Check if prompts table exists in prompt schema
            prompts_table_exists = False
            if prompt_schema_exists:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'prompt' 
                        AND table_name = 'prompts'
                    );
                """)
                prompts_table_exists = cur.fetchone()[0]
            
            # Check if team table exists in team schema
            team_table_exists = False
            if team_schema_exists:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'team' 
                        AND table_name = 'team'
                    );
                """)
                team_table_exists = cur.fetchone()[0]
            
            # Check if team_members table exists in team schema
            team_members_table_exists = False
            if team_schema_exists:
                cur.execute("""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'team' 
                        AND table_name = 'team_members'
                    );
                """)
                team_members_table_exists = cur.fetchone()[0]
            
            # Close connection
            conn.close()
            
            # Return check results
            return {
                'user_schema': user_schema_exists,
                'prompt_schema': prompt_schema_exists,
                'team_schema': team_schema_exists,
                'users_table': users_table_exists,
                'prompts_table': prompts_table_exists,
                'team_table': team_table_exists,
                'team_members_table': team_members_table_exists
            }
    
    except Exception as e:
        print(f"Error checking tables: {e}")
        return None
    
    finally:
        # Close connection
        if 'conn' in locals():
            conn.close()

def check_and_update_foreign_keys():
    """Check and update foreign key constraints to ensure CASCADE DELETE is properly set"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        
        # Create cursor
        with conn.cursor() as cur:
            # Check team_members foreign key constraints
            cur.execute("""
                SELECT
                    tc.constraint_name,
                    tc.table_schema,
                    tc.table_name,
                    kcu.column_name,
                    ccu.table_schema AS foreign_table_schema,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name,
                    rc.delete_rule
                FROM
                    information_schema.table_constraints AS tc
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                    JOIN information_schema.referential_constraints AS rc
                      ON rc.constraint_name = tc.constraint_name
                WHERE
                    tc.constraint_type = 'FOREIGN KEY'
                    AND tc.table_schema = 'team'
                    AND tc.table_name = 'team_members';
            """)
            
            team_member_fks = cur.fetchall()
            fk_issues = []
            
            for fk in team_member_fks:
                constraint_name, table_schema, table_name, column_name, foreign_table_schema, foreign_table_name, foreign_column_name, delete_rule = fk
                
                if delete_rule != 'CASCADE':
                    fk_issues.append({
                        'constraint_name': constraint_name,
                        'table': f"{table_schema}.{table_name}",
                        'column': column_name,
                        'references': f"{foreign_table_schema}.{foreign_table_name}({foreign_column_name})",
                        'current_delete_rule': delete_rule,
                        'desired_delete_rule': 'CASCADE'
                    })
            
            if not fk_issues:
                print("All foreign key constraints are correctly set")
                return True
            
            # Display issues
            print("\nThe following foreign key constraints do not have CASCADE DELETE rule:")
            for i, issue in enumerate(fk_issues, 1):
                print(f"{i}. {issue['table']}.{issue['column']} -> {issue['references']} (current: {issue['current_delete_rule']})")
            
            user_input = input("\nUpdate foreign key constraints to CASCADE DELETE? (Y/N): ").strip().upper()
            if user_input != 'Y':
                print("User cancelled foreign key constraint update")
                return False
            
            # Update foreign key constraints
            print("\nUpdating foreign key constraints...")
            for issue in fk_issues:
                constraint_name = issue['constraint_name']
                table = issue['table']
                
                # Drop the existing constraint
                print(f"Dropping constraint {constraint_name} from {table}...")
                cur.execute(f"""
                    ALTER TABLE {table}
                    DROP CONSTRAINT {constraint_name};
                """)
                
                # Add the new constraint with CASCADE DELETE
                column = issue['column']
                references = issue['references']
                print(f"Adding new constraint to {table}.{column} referencing {references} with CASCADE DELETE...")
                cur.execute(f"""
                    ALTER TABLE {table}
                    ADD CONSTRAINT {constraint_name}
                    FOREIGN KEY ({column})
                    REFERENCES {references}
                    ON DELETE CASCADE;
                """)
            
            # Commit the changes
            conn.commit()
            print("Successfully updated foreign key constraints!")
            return True
            
    except Exception as e:
        print(f"Error checking/updating foreign key constraints: {e}")
        return False
    
    finally:
        # Close connection
        if 'conn' in locals():
            conn.close()

def create_tables():
    """Create user and prompts tables, and check/update foreign key constraints"""
    # First check if tables exist
    tables_status = check_tables_exist()
    
    if tables_status is None:
        print("Unable to check table status, table creation failed")
        print("**********DATABASE SELF-CHECKING END**********")
        return False
    
    # Check if all tables already exist
    all_tables_exist = (tables_status['user_schema'] and tables_status['prompt_schema'] and tables_status['team_schema'] and
                        tables_status['users_table'] and tables_status['prompts_table'] and 
                        tables_status['team_table'] and tables_status['team_members_table'])
    
    if all_tables_exist:
        print("All tables already exist, no need to create")
        # Even if all tables exist, we still need to check foreign key constraints
        fk_check_result = check_and_update_foreign_keys()
        print("**********DATABASE SELF-CHECKING END**********")
        return True
    
    # Ask user if they want to create tables
    print("\nThe following tables or schemas do not exist:")
    if not tables_status['user_schema']:
        print("- user schema")
    if not tables_status['prompt_schema']:
        print("- prompt schema")
    if not tables_status['team_schema']:
        print("- team schema")
    if not tables_status['users_table']:
        print("- user.users table")
    if not tables_status['prompts_table']:
        print("- prompt.prompts table")
    if not tables_status['team_table']:
        print("- team.team table")
    if not tables_status['team_members_table']:
        print("- team.team_members table")
    
    user_input = input("\nCreate missing tables? (Y/N): ").strip().upper()
    if user_input != 'Y':
        print("User cancelled table creation")
        print("**********DATABASE SELF-CHECKING END**********")
        return False
    
    try:
        # Connect to testdb database
        conn = psycopg2.connect(
            database=DB_NAME,
            user=DB_USER,
            host=DB_HOST,
            password=DB_PASSWORD,
            port=DB_PORT,
        )
        
        # Create cursor
        with conn.cursor() as cur:
            # Check if user schema exists, create if not
            if not tables_status['user_schema']:
                print("Creating user schema...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS \"user\";")
            
            # Check if prompt schema exists, create if not
            if not tables_status['prompt_schema']:
                print("Creating prompt schema...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS prompt;")
            
            # Check if team schema exists, create if not
            if not tables_status['team_schema']:
                print("Creating team schema...")
                cur.execute("CREATE SCHEMA IF NOT EXISTS team;")
            
            # Check if users table exists in user schema
            if not tables_status['users_table']:
                # Create users table in user schema
                print("Creating user.users table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS "user".users (
                        id SERIAL PRIMARY KEY,
                        user_id VARCHAR(255) UNIQUE NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        username VARCHAR(255) UNIQUE NOT NULL,
                        hashed_password VARCHAR(255) NOT NULL,
                        full_name VARCHAR(255),
                        is_active BOOLEAN DEFAULT TRUE,
                        is_superuser BOOLEAN DEFAULT FALSE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE
                    );
                """)
            
            # Check if prompts table exists in prompt schema
            if not tables_status['prompts_table']:
                # Create prompts table in prompt schema
                print("Creating prompt.prompts table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS prompt.prompts (
                        id SERIAL PRIMARY KEY,
                        prompt_name VARCHAR(255) NOT NULL,
                        content TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            
            # Check if team table exists in team schema
            if not tables_status['team_table']:
                # Create team table in team schema
                print("Creating team.team table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS team.team (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL,
                        description TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );
                """)
            
            # Check if team_members table exists in team schema
            if not tables_status['team_members_table']:
                # Create team_members table in team schema
                print("Creating team.team_members table...")
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS team.team_members (
                        id SERIAL PRIMARY KEY,
                        team_id INTEGER NOT NULL REFERENCES team.team(id) ON DELETE CASCADE,
                        user_id INTEGER NOT NULL REFERENCES "user".users(id) ON DELETE CASCADE,
                        role VARCHAR(50) NOT NULL DEFAULT 'member',
                        joined_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        CONSTRAINT uq_team_member UNIQUE (team_id, user_id)
                    );
                """)
            
            # Commit transaction
            conn.commit()
            print("Successfully created missing tables!")
            
            # After creating tables, check and update foreign key constraints
            check_and_update_foreign_keys()
            return True
    
    except Exception as e:
        print(f"Error creating tables: {e}")
        return False
    
    finally:
        # Close connection
        if 'conn' in locals():
            conn.close()
        # Print end message only once at the end of the function
        print("**********DATABASE SELF-CHECKING END**********")
