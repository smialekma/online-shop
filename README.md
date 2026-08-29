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

  <img src="https://github.com/user-attachments/assets/99b4059f-6609-4378-81be-bea0083f5fa2" width="80%" height="50%">
  
</details>

<details>
<summary><b>Product catalog</b> with categories, product details, search, filtering and pagination</summary>

* Server-side filtering by category, brand and price
* Detailed product pages with related products, customer reviews and rating

  <img src="https://github.com/user-attachments/assets/9ad88c8d-14ae-4dae-acb4-0cc9f4b23ddd" width="80%" height="50%">
  

</details>

<details>
<summary>Session-based <b>shopping cart and wishlist</b></summary>
  
* Cart available without requiring a user account
* Adding, removing and updating products from multiple places within the store
* AJAX-powered cart operations implemented in JavaScript, allowing cart contents and quantities to be updated without full page reloads
<img src="https://github.com/user-attachments/assets/fe1eb974-d455-457c-a7f8-c96e2edee87e" width="50%" height="50%">

</details>

<details>
<summary><b>Complete checkout and order flow</b></summary>

* Available to both registered and guest customers
* Automatic pre-filling of saved customer data for authenticated users
* Multiple shipping methods with AJAX-based dynamic recalculation of the order total
<img src="https://github.com/user-attachments/assets/6c483a8b-f0d4-4c8b-bbed-1da0e9fb4d5c" width="80%" height="50%">

</details>

<details>
<summary><b>Stripe payment integration</b> with payment processing and webhook handling</summary>

* Dedicated payment success and cancellation flows
* Email confirmation after successful payment

<img src="https://github.com/user-attachments/assets/69ad3af8-4769-435a-9970-cff98456e985" width="80%" height="50%">
</details>

<details>
<summary><b>Customer accounts</b> with registration, authentication, profile management, email verification and password recovery</summary>

* Custom user model with email-based authentication
* Email address verification based on Django password reset tokens
* Customer profile with:
  * shopping statistics
  * editable saved address
  * filterable order history and detailed order views
<img src="https://github.com/user-attachments/assets/27cf8d80-2a03-406e-a7f9-0d78b328eeff" width="80%" height="50%">

</details>

<details>
<summary><b>Product reviews and ratings</b></summary>

Integrated directly into product detail pages
<img src="https://github.com/user-attachments/assets/fe2356bd-7246-4b47-a441-e66cf9c9f903" width="80%" height="50%">

</details>

<details>
<summary><b>Newsletter</b> powered by Celery, Redis and Flower</summary>

* Email verification
* Asynchronous background tasks powered by Celery and Redis, with scheduled tasks and Flower monitoring
<img src="https://github.com/user-attachments/assets/9610bc1a-57e5-4abb-8f95-5318840a9967" width="50%" height="50%">

</details>

<details>
<summary><b>Store management panel</b> for admins</summary>

* Dedicated administration dashboard with store statistics
* Searchable and filterable management views for viewing and updating model objects
<img src="https://github.com/user-attachments/assets/facbf802-2737-41bb-88d9-30265bdbddac" width="80%" height="50%">

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

1. Clone the repository

```bash
git clone https://github.com/yourusername/online-shop.git
cd online-shop
```

2. Create the environment file

```bash
cp .env.dist .env
```

3. Fill in the required environment variables.

4. Install dependencies with [Poetry](https://python-poetry.org/):

```bash
poetry install
```

5. Activate the Poetry virtual environment:

```bash
poetry env activate
```

6. Set up the database - apply migrations:

```bash
python manage.py migrate
```

7. Run the development server:

```bash
python manage.py runserver
```

8. Alternatively, run with Docker:

```bash
docker compose up --build
```

## App view
<img src="https://github.com/user-attachments/assets/6881b50a-b075-4358-a958-e6da7e40a587" width="100%" height="80%">
