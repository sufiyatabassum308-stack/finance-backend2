# Finance Data Processing and Access Control Backend

## Overview
This project implements a backend system for managing financial data with role-based access control. It supports user management, financial records CRUD operations, and dashboard-level summary APIs.

## Tech Stack
- Python
- FastAPI
- SQLite
- SQLAlchemy
- Uvicorn

## Features
- User and role management
- Financial records CRUD operations
- Dashboard summary APIs
- Role-based access control
- Input validation and error handling
- SQLite-based data persistence

## Roles
- Viewer → can view records and dashboard data
- Analyst → can read records and access summaries
- Admin → can create, update, delete, and manage users/records

## API Endpoints

### Users
- POST /users
- GET /users

### Records
- POST /records
- GET /records
- PUT /records/{id}
- DELETE /records/{id}

### Dashboard
- GET /dashboard-summary

## Setup Instructions

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload