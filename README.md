## General info
A full-stack e-commerce platform built with Django, designed as a portfolio project to demonstrate backend development, software architecture, testing, asynchronous processing, and modern development practices.
The application implements the complete customer purchasing flow, from browsing products to placing and paying for orders, while also providing management tools for store administrators.

## Features
<details>
<summary><b>Home page</b> with recommended product rankings</summary>
  Main storefront interface (Electro template)
  - New and top-selling products sorted by category
  - Random, discounted and top-rated products
 - product card with rating and possibility to  add products to cart/wishlist
  - ability to add products to cart/wishlist
</details>
* **Product catalog** with categories, product details, search, server-side filtering and pagination

- filters: category, price, brand
- product details: related products, reviews and rating
* Session-based **shopping cart and wishlist**
- possibility to add products in various places within the store (eg, home page, product details)
- AJAX-powered cart operations implemented in JavaScript, with asynchronous requests to Django views for updating cart contents without full page reloads
* **Complete checkout and order flow** with option for non-registered customers
- populating saved user data
- shopping methods with dynamic total amount re-calculating using AJAX
* **Stripe payment integration** with payment processing and webhook handling
- success and cancel pages, payment email confirmation
* **Customer accounts** with registration, authentication, profile management, email verification and password recovery
- custom user model for email-based authentication
- email verification based on Django password reset tokens
- customer profile view with shopping statistics, possibility to edit saved address (later pre-filled during checkout) and order history view (filters, order details)
* **Product reviews and rating**
  - in product details view
* **Newsletter subscriptions**
  - email verification
* **Asynchronous background tasks** powered by Celery and Redis, with scheduled tasks and Flower monitoring
* **Store management panel** for admins
  - dashboard with statistics
  - list views with search and filters for subscribers, newsletter posts, shipping methods, orders, payments, reviews, products, brands, categories
  - update views
- Command for populating db with test data for developers
- Custom error views
- custom context processors

## Technologies & Tools
### Backend
* Python 3.13
* Django 5
* Django-filter
* PostgreSQL
* Celery, Flower, Redis
* Stripe API
### Frontend
* Django Templates (HTML, CCS)
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
