# Car Dealership Review Platform (Full-Stack Capstone Project)

## 📌 Project Overview
This project is a **full-stack web application** developed as the **Capstone Project** for the IBM / Coursera Full-Stack Software Developer program.

The application provides a centralized platform for customers to:
- Browse car dealerships across the United States
- Filter dealerships by state
- View customer reviews for each dealership
- Register, log in, and submit reviews (authorized users)
- Manage dealership data through Django Admin (admin users)

The goal is to improve transparency, customer trust, and accessibility of dealership reviews nationwide.

---

## 🏗️ Architecture
The system follows a **modern full-stack architecture**:

- **Frontend**: React (Single Page Application)
- **Backend**: Django (REST-style JSON APIs)
- **Authentication**: Django Auth
- **Database**: JSON-based mock data (dealerships, cars, reviews)
- **CI**: GitHub Actions (linting for Python & JavaScript)
- **Containerization**: Docker (for development and deployment)

---

## 👥 User Roles & Use Cases

### 🔓 Anonymous Users
- View **Home**, **About Us**, and **Contact Us** pages
- View a list of all dealerships
- Filter dealerships by **state**
- View dealership details and reviews
- Navigate to login and registration pages

---

### 🔐 Authorized Users
In addition to anonymous features:
- Log in and log out
- Submit reviews for dealerships
- Reviews include:
  - Purchase information
  - Vehicle make, model, and year
  - Purchase date
  - Review text
- Newly submitted reviews appear **at the top**, sorted by time

**Review JSON Structure**
```json
{
  "user_id": 1,
  "name": "Berkly Shepley",
  "dealership": 15,
  "review": "Total grid-enabled service-desk",
  "time": "2025-12-17T20:15:00Z",
  "purchase": true,
  "purchase_date": "07/11/2020",
  "car_make": "Audi",
  "car_model": "A6",
  "car_year": 2010
}
