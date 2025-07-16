
# Database Setup Instructions for Toolora AI

## Option 1: Neon Database (Recommended)
1. Go to https://neon.tech
2. Create a new project
3. Copy the connection string from the dashboard
4. Set as environment variable: DATABASE_URL=postgresql://username:password@ep-xxx.neon.tech/dbname

## Option 2: Render PostgreSQL
1. Go to https://render.com
2. Create a new PostgreSQL database
3. Copy the Internal Database URL
4. Set as environment variable: DATABASE_URL=postgresql://username:password@xxx.render.com/dbname

## Option 3: Supabase
1. Go to https://supabase.com
2. Create a new project
3. Go to Settings → Database → Connection string
4. Copy the connection string (use Transaction pooler)
5. Replace [YOUR-PASSWORD] with your actual password
6. Set as environment variable: DATABASE_URL=postgresql://username:password@xxx.supabase.co/postgres

## Current Configuration
Your app is configured to automatically detect and optimize for any of these providers.
