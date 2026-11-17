# MedCentral - Doctor & Specialist Booking System

MedCentral is a Django web application for finding healthcare specialists, viewing doctor profiles and booking appointments. Users can browse doctors by department, search and sort them, book appointments with built-in validation, and leave reviews with star ratings.

Developed as an individual project for the Django Basics course at SoftUni.

## Features

- **Doctor directory:** search by name or specialty, filter by department, sort by name, experience or rating.
- **Doctor profiles:** biography, department, specialty, years of experience, offered services, average rating and patient reviews.
- **Appointments:** book, edit and cancel appointments. Booking validates future dates, working hours (08:00 to 17:00), the services a doctor offers and overlapping appointments.
- **Reviews and ratings:** leave a 1 to 5 star review for any doctor.
- **Departments and services:** create and browse departments and services.
- **Custom 404 page** and a reusable Bootstrap layout.

## Project Structure

The project has three Django apps:

| App | Responsibility |
|---|---|
| `common` | Home page, shared form mixin, custom 404 handling |
| `specialists` | Departments, services and doctors, including the custom `stars` template filter |
| `appointments` | Appointments (booking, editing, cancelling) and doctor reviews |

Templates live in the root `templates/` folder (`base.html`, `partials/`, and one subfolder per app). Static files are in `static/`.

## Database Models

| Model | App | Key fields and relations |
|---|---|---|
| `Department` | specialists | `name` (unique), `description` |
| `Service` | specialists | `name` (unique), `description`, `price`, `duration_minutes` |
| `Doctor` | specialists | `full_name`, `specialty`, `bio`, `years_of_experience`; **many-to-one** to `Department`; **many-to-many** to `Service` |
| `Appointment` | appointments | `patient_name`, `patient_email`, `appointment_date_time`; many-to-one to `Doctor` and `Service`; unique doctor and time constraint |
| `Review` | appointments | `reviewer_name`, `rating` (1 to 5), `comment`, `created_at`; many-to-one to `Doctor` |

Departments group doctors into broad clinical areas, while a doctor's specialty describes a narrower focus within the department.

## Pages

Home, doctor list (with search, filter and sort), doctor details, add/edit/delete doctor, department list, add department, service list, service details, add service, appointment list (with filters), book/edit/cancel appointment, leave a review, and a custom 404 page. Every page is reachable from the navigation bar or from buttons on the related pages.

Full CRUD is implemented for **doctors** and **appointments**. Departments, services and reviews support creating and viewing.

## Requirements

- Python 3.12 or newer (developed and tested with Python 3.14)
- Django 6.1 (installed from `requirements.txt`)
- SQLite (the default Django database, no setup needed)

No environment variables, credentials or API keys are required. The project has no login or user accounts.

## Installation and Setup

1. Clone the repository:
   ```
   git clone https://github.com/rcokov99/django-basics-project.git
   cd django-basics-project
   ```
2. Create and activate a virtual environment:
   ```
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # Linux / macOS
   source .venv/bin/activate
   ```
3. Install the dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply the migrations:
   ```
   python manage.py migrate
   ```
5. Start the development server:
   ```
   python manage.py runserver
   ```
6. Open http://127.0.0.1:8000/ in your browser.

## Using the Application

The database starts empty, and everything can be created through the interface. Create objects in this order:

1. **Department** (Departments, then Add department)
2. **Service** (Services, then Add service)
3. **Doctor** (Doctors, then Add Doctor): requires a department and at least one service
4. **Appointment** (Appointments, then Book appointment): the selected doctor must offer the chosen service
5. **Review** (open a doctor's profile, then Leave a review)

## Validation Highlights

- Department and service names are unique (case-insensitive) and cannot be only digits.
- Doctor names allow letters, spaces, dots, hyphens and apostrophes, and cannot include a "Dr." prefix.
- Appointments cannot be in the past, must fall between 08:00 and 17:00, cannot overlap another appointment for the same doctor, and must use a service the doctor offers.
- Reviews require a rating from 1 to 5 and a comment of at least 10 characters.

