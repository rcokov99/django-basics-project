# MedCentral - Doctor \& Specialist Booking System

MedCentral is a Django web application that allows users to find healthcare specialists, view doctor profiles, check available hours, schedule appointments, and leave reviews or ratings.

This application was developed as an individual project for the Django Basics course at SoftUni.

## Key Features

* Specialist Directory: Search and filter doctors by specialty, department, location, or rating.
* Doctor Profiles: View detailed information about qualifications, bios, offered services, and open appointment slots.
* Appointment Booking: Schedule visits with built-in form validation.
* Patient Reviews \& Ratings: Leave feedback and star ratings for specialists.
* Appointment Overview: View and manage booked appointments across the platform.

## Architecture \& Structure

The project is built using Django and follows a modular structure divided into three distinct applications:

1. common - Landing pages, site navigation, static views, and custom 404 error handling.
2. specialists - Doctor profile management, departments, specialties, and service listings.
3. appointments - Appointment scheduling logic, time slot availability, user reviews, and ratings.

## Prerequisites

* Python 3.10+
* Django 5.x
* SQLite3 (default database engine)

## Local Installation \& Setup

1. Clone the repository:
git clone
cd
2. Set up and activate a virtual environment:
python -m venv venv

   # On Windows:

   venv\\Scripts\\activate

   # On Linux/macOS:

   source venv/bin/activate

3. Install requirements:
pip install django
4. Apply database migrations:
python manage.py migrate
5. Run the development server:
python manage.py runserver

Access the site in your browser at http://127.0.0.1:8000/

