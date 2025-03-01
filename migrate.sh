#!/bin/bash

echo "🔥 Running Database Migration Script..."

# Step 1: Ensure Alembic is tracking the latest schema
echo "📌 Stamping Alembic to the latest migration..."
alembic stamp head

# Step 2: Generate a new migration (if needed)
echo "📌 Generating migration files..."
alembic revision --autogenerate -m "Auto-migration"

# Step 3: Apply all new migrations
echo "📌 Applying database migrations..."
alembic upgrade head

echo "✅ Database migration completed successfully!"
