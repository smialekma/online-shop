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

<img src="https://github.com/user-attachments/assets/20fe82b1-bc56-4d40-a4f8-5424e9b835db" width="80%" height="50%">
  
</details>

<details>
<summary><b>Product catalog</b> with categories, product details, search, filtering and pagination</summary>

* Server-side filtering by category, brand and price
* Detailed product pages with related products, customer reviews and rating

  <img src="https://github.com/user-attachments/assets/e60a93b0-de48-4617-b5ff-e0dcc507e949" width="80%" height="50%">
  

</details>

<details>
<summary>Session-based <b>shopping cart and wishlist</b></summary>
  
* Cart available without requiring a user account
* Adding, removing and updating products from multiple places within the store
* AJAX-powered cart operations implemented in JavaScript, allowing cart contents and quantities to be updated without full page reloads
<img src="https://github.com/user-attachments/assets/248b860e-cf1b-4f1b-ad63-ac0a17c0f46a" width="50%" height="50%">

</details>

<details>
<summary><b>Complete checkout and order flow</b></summary>

* Available to both registered and guest customers
* Automatic pre-filling of saved customer data for authenticated users
* Multiple shipping methods with AJAX-based dynamic recalculation of the order total
<img src="https://github.com/user-attachments/assets/82384c47-ead3-4341-8c43-388f5e589458" width="80%" height="50%">

</details>

<details>
<summary><b>Stripe payment integration</b> with payment processing and webhook handling</summary>

* Dedicated payment success and cancellation flows
* Email confirmation after successful payment

<img src="https://github.com/user-attachments/assets/df76be1b-8ad7-450f-a1dc-42b901fa5334" width="80%" height="50%">
</details>

<details>
<summary><b>Customer accounts</b> with registration, authentication, profile management, email verification and password recovery</summary>

* Custom user model with email-based authentication
* Email address verification based on Django password reset tokens
* Customer profile with:
  * shopping statistics
  * editable saved address
  * filterable order history and detailed order views
<img src="https://github.com/user-attachments/assets/20fbe4ff-0433-4086-9dac-820033d19ab0" width="80%" height="50%">

</details>

<details>
<summary><b>Product reviews and ratings</b></summary>

Integrated directly into product detail pages
<img src="https://github.com/user-attachments/assets/03dd7a2d-8731-4b4e-b3a4-378e28b17e42" width="70%" height="50%">

</details>

<details>
<summary><b>Newsletter</b> powered by Celery, Redis and Flower</summary>

* Email verification
* Asynchronous background tasks powered by Celery and Redis, with scheduled tasks and Flower monitoring
<img src="https://github.com/user-attachments/assets/28e9f5a0-70a1-4b4a-84fa-dd487f46abd4" width="50%" height="50%">

</details>

<details>
<summary><b>Store management panel</b> for admins</summary>

* Dedicated administration dashboard with store statistics
* Searchable and filterable management views for viewing and updating model objects
<img src="https://github.com/user-attachments/assets/9f5247a8-a0af-48a5-a92c-26492a93d233" width="80%" height="50%">

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
* Django Templates (HTML, CSS)
* Crispy Forms
* Bootstrap
* JavaScript (AJAX-based shopping cart interactions)
### DevOps
* Docker
* AWS
* Sentry
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
<img src="https://github.com/user-attachments/assets/9a4b0f11-2f96-489e-9342-3f058048a19e" width="100%" height="80%">
