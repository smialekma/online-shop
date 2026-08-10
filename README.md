## General info
A full-stack e-commerce platform built with Django, designed as a portfolio project to demonstrate backend development, software architecture, testing, asynchronous processing, and modern development practices.
The application implements the complete customer purchasing flow, from browsing products to placing and paying for orders, while also providing management tools for store administrators.

## Features
* **Landing page** with recommended product rankings
* **Product catalog** with categories, product details, search, server-side filtering and pagination
* Session-based **shopping cart and wishlist**
* **Complete checkout and order flow** with option for non-registered customers
* **Stripe payment integration** with payment processing and webhook handling
* **Customer accounts** with registration, authentication, profile management, email verification and password recovery
* **Product reviews and rating**
* **Newsletter subscriptions**
* **Asynchronous background tasks** powered by Celery and Redis, with scheduled tasks and Flower monitoring
* **Store management panel** for admins

## Technologies & Tools
### Backend
* Python 3.13
* Django 5
* Django-filter
* PostgreSQL
* Celery, Flower, Redis
* Stripe API
### Frontend
* Django Templates
* Crispy Forms
* Bootstrap
* JavaScript (AJAX-based shopping cart interactions)
### DevOps
* Docker
* AWS
### Development & Code Quality
* Poetry
* MyPy
* Pre-commit
* Github actions
* Django Silk & Django Debug Toolbar
* Unit tests: Factory Boy, Coverage

## Setup
#To-do

## App view
#To-do
