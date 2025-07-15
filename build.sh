#!/bin/bash
# Build script for Render deployment

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating uploads directory..."
mkdir -p uploads

echo "Setting up database..."
python -c "
from app import app, db
import models
with app.app_context():
    db.create_all()
    print('Database tables created successfully')
"

echo "Build completed successfully!"