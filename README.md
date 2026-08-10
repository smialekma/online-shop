## General info
A full-stack e-commerce platform built with Django, designed as a portfolio project to demonstrate backend development, software architecture, testing, asynchronous processing, and modern development practices.
The application implements the complete customer purchasing flow, from browsing products to placing and paying for orders, while also providing management tools for store administrators.

## Features

<details>
<summary><b>Home page</b> with product recommendations and rankings</summary>

* Main storefront interface based on the Electro template
* New and top-selling products grouped by category
* Random, discounted and top-rated product sections
* Product cards displaying ratings and providing quick access to cart and wishlist actions

</details>

<details>
<summary><b>Product catalog</b> with categories, product details, search, filtering and pagination</summary>

* Server-side filtering by category, brand and price
* Detailed product pages with related products, customer reviews and rating

</details>

<details>
<summary>Session-based <b>shopping cart and wishlist</b></summary>
  
* Cart available without requiring a user account
* Adding, removing and updating products from multiple places within the store
* AJAX-powered cart operations implemented in JavaScript, allowing cart contents and quantities to be updated without full page reloads

</details>

<details>
<summary><b>Complete checkout and order flow</b></summary>

* Available to both registered and guest customers
* Automatic pre-filling of saved customer data for authenticated users
* Multiple shipping methods with AJAX-based dynamic recalculation of the order total

</details>

<details>
<summary><b>Stripe payment integration</b> with payment processing and webhook handling</summary>

* Dedicated payment success and cancellation flows
* Email confirmation after successful payment

</details>

<details>
<summary><b>Customer accounts</b> with registration, authentication, profile management, email verification and password recovery</summary>

* Custom user model with email-based authentication
* Email address verification based on Django password reset tokens
* Customer profile with:
  * shopping statistics
  * editable saved address
  * filterable order history and detailed order views

</details>

<details>
<summary><b>Product reviews and ratings</b></summary>

Integrated directly into product detail pages

</details>

<details>
<summary><b>Newsletter</b> powered by Celery, Redis and Flower</summary>

* Email verification
* Asynchronous background tasks powered by Celery and Redis, with scheduled tasks and Flower monitoring

</details>

<details>
<summary><b>Store management panel</b> for admins</summary>

* Dedicated administration dashboard with store statistics
* Searchable and filterable management views for viewing and updating model objects

</details>

<details>
<summary><b>Developer features</b></summary>

* Django management command for populating the database with test data
* Custom error views and context processors

</details>

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
1. Clone repository
```bash
git clone https://github.com/yourusername/online-shop.git
cd online-shop
```
2. Create environment file
```bash
cp .env.dist .env
```

3. Fill in the required environment variables.

4. Run with Docker
```bash
docker compose up --build
```
5. Or run locally:

- Install dependencies
```bash
pip install -r requirements.txt
```

- Apply migrations
```bash
python manage.py migrate
```
- Run development server
```bash
python manage.py runserver
```

## App view
#To-do
