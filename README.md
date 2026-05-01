# Grocery Store - Complete Tech Stack

A VueJS and Flask fullstack application for managing a grocery store with user authentication, role-based access control, and async task processing.

## Languages

- Vue: 53.5%
- Python: 39.2%
- JavaScript: 3.9%
- HTML: 3.4%

## Frontend

- Vue.js 3.2.13 - Progressive JavaScript framework
- Vue Router 4.2.5 - Official router for Vue.js
- Bootstrap 5.3.2 - CSS framework for responsive design
- Babel - JavaScript compiler
- ESLint - Code quality and linting

## Backend

- Python - Primary backend language
- Flask - Web framework for REST API development
- Flask-SQLAlchemy - ORM for database operations
- Flask-Security - User authentication and authorization
- Flask-CORS - Cross-origin resource sharing
- Flask-Bcrypt - Password hashing and security
- Flask-Excel - Excel file generation and export
- Celery - Distributed task queue for async operations
- Redis - Caching and message broker for Celery

## Database

- SQLite - Embedded relational database

## Core Features

- User Authentication - Token-based authentication with role-based access control
- Database Models - User, Role, Category, Item, Cart, Admin Request
- Role Management - Admin, User, StoreManager roles
- Caching - Redis caching layer
- Async Task Processing - Celery for background jobs (daily/monthly reminders, email notifications)
- CSV Export - Product data export functionality
- Email Service - Mail notifications for reminders

## API Architecture

- RESTful API endpoints
- Token-based authentication
- Role-based authorization (Admin, Store Manager, User)
- Periodic tasks scheduling using Celery Beat