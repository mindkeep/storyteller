#!/bin/bash
# Database setup script for StoryTeller

set -e

# Default values
DB_NAME="storyteller"
DB_USER="storyteller_user"
DB_HOST="localhost"
DB_PORT="5432"
SCHEMA_FILE="schema.sql"
SAMPLE_DATA_FILE="sample_data.sql"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if PostgreSQL is installed and running
check_postgres() {
    print_status "Checking PostgreSQL installation..."
    
    if ! command -v psql &> /dev/null; then
        print_error "PostgreSQL is not installed or not in PATH"
        print_status "Please install PostgreSQL first:"
        print_status "  Ubuntu/Debian: sudo apt-get install postgresql postgresql-contrib"
        print_status "  macOS: brew install postgresql"
        print_status "  Windows: Download from https://www.postgresql.org/download/windows/"
        exit 1
    fi
    
    if ! pgrep -x "postgres" > /dev/null; then
        print_warning "PostgreSQL service doesn't appear to be running"
        print_status "Try starting it with:"
        print_status "  Linux: sudo systemctl start postgresql"
        print_status "  macOS: brew services start postgresql"
    fi
}

# Create database and user
setup_database() {
    print_status "Setting up database and user..."
    
    # Create user if it doesn't exist
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "
        DO \$\$
        BEGIN
            CREATE USER $DB_USER WITH PASSWORD 'storyteller_password';
            GRANT CREATE ON SCHEMA public TO $DB_USER;
            EXCEPTION WHEN duplicate_object THEN 
                RAISE NOTICE 'User $DB_USER already exists';
        END
        \$\$;
    " 2>/dev/null || print_warning "Could not create user (may already exist)"
    
    # Create database if it doesn't exist
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "
        SELECT 'CREATE DATABASE $DB_NAME OWNER $DB_USER' 
        WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '$DB_NAME')\\gexec
    " 2>/dev/null || print_warning "Could not create database (may already exist)"
    
    # Grant privileges
    psql -h $DB_HOST -p $DB_PORT -U postgres -c "
        GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
    " 2>/dev/null
}

# Run schema creation
create_schema() {
    print_status "Creating database schema..."
    
    if [ ! -f "$SCHEMA_FILE" ]; then
        print_error "Schema file $SCHEMA_FILE not found!"
        exit 1
    fi
    
    PGPASSWORD=storyteller_password psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$SCHEMA_FILE"
    
    if [ $? -eq 0 ]; then
        print_status "Schema created successfully"
    else
        print_error "Failed to create schema"
        exit 1
    fi
}

# Load sample data
load_sample_data() {
    if [ "$1" = "--with-sample-data" ] || [ "$1" = "-s" ]; then
        print_status "Loading sample data..."
        
        if [ ! -f "$SAMPLE_DATA_FILE" ]; then
            print_warning "Sample data file $SAMPLE_DATA_FILE not found, skipping..."
            return
        fi
        
        PGPASSWORD=storyteller_password psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f "$SAMPLE_DATA_FILE"
        
        if [ $? -eq 0 ]; then
            print_status "Sample data loaded successfully"
        else
            print_warning "Failed to load sample data"
        fi
    fi
}

# Verify installation
verify_setup() {
    print_status "Verifying database setup..."
    
    # Count tables
    TABLE_COUNT=$(PGPASSWORD=storyteller_password psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -t -c "
        SELECT COUNT(*) FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    " | xargs)
    
    print_status "Found $TABLE_COUNT tables in the database"
    
    if [ "$TABLE_COUNT" -gt 0 ]; then
        print_status "✅ Database setup completed successfully!"
        print_status ""
        print_status "Connection details:"
        print_status "  Database: $DB_NAME"
        print_status "  User: $DB_USER"
        print_status "  Host: $DB_HOST"
        print_status "  Port: $DB_PORT"
        print_status "  Password: storyteller_password"
        print_status ""
        print_status "Add these to your .env file:"
        echo "DATABASE_URL=postgresql://$DB_USER:storyteller_password@$DB_HOST:$DB_PORT/$DB_NAME"
    else
        print_error "❌ Database setup failed - no tables found"
        exit 1
    fi
}

# Main execution
main() {
    print_status "🎲 StoryTeller Database Setup"
    print_status "=============================="
    
    check_postgres
    setup_database
    create_schema
    load_sample_data "$1"
    verify_setup
}

# Show usage if requested
if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "StoryTeller Database Setup Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -s, --with-sample-data    Load sample data after creating schema"
    echo "  -h, --help               Show this help message"
    echo ""
    echo "This script will:"
    echo "  1. Check PostgreSQL installation"
    echo "  2. Create database and user"
    echo "  3. Run schema creation"
    echo "  4. Optionally load sample data"
    echo "  5. Verify the setup"
    echo ""
    echo "Requirements:"
    echo "  - PostgreSQL installed and running"
    echo "  - Access to 'postgres' superuser account"
    echo "  - schema.sql file in current directory"
    exit 0
fi

# Run main function
main "$@"