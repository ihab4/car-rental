# 🚗 Rental Car Management System - Project Plan (Django)

## 🧠 1. Project Conception

### Purpose
Manage car rentals for a company: vehicles, clients, reservations, payments, availability, and reports.

### Key Features
- Admin dashboard for management
- User authentication (admin, staff)
- Car CRUD (create, read, update, delete)
- Client management
- Rental/booking system
- Return & payment tracking
- Rental availability logic
- Reports/statistics
- Responsive UI (using TailAdmin)

### Tech Stack
- Backend: Django
- Frontend: HTML/CSS + Tailwind (TailAdmin)
- Database: SQLite (dev), PostgreSQL (prod)
- Optional: Docker, Celery, Stripe (for payments)

---

## 🗂️ 2. Models Design

### Car
- id
- make
- model
- year
- plate_number
- status (available, rented, maintenance)
- rental_price_per_day
- image

### Client
- id
- full_name
- email
- phone
- driver_license_number

### Rental
- id
- car (FK to Car)
- client (FK to Client)
- start_date
- end_date
- total_price
- status (booked, ongoing, returned)

### Payment
- id
- rental (FK)
- amount
- date
- payment_method (cash, card)
- status

---

## 🛠️ 3. Development Checklist

### 🧱 Setup
- [ ] Create Django project and app
- [ ] Setup TailAdmin dashboard template
- [ ] Configure database
- [ ] Create superuser
- [ ] Setup Git repo

### 🔐 Auth
- [ ] Staff login/logout
- [ ] User roles & permissions

### 🚘 Car Management
- [ ] Car model
- [ ] Admin views (add, update, delete cars)
- [ ] Image upload for cars

### 👤 Client Management
- [ ] Client model
- [ ] Admin views (add/edit clients)

### 📆 Rental System
- [ ] Rental model
- [ ] Book car: date validation
- [ ] Update car availability
- [ ] End rental process
- [ ] Calculate total price based on days

### 💳 Payments
- [ ] Payment model
- [ ] Manual payment input
- [ ] Display history per rental/client

### 📊 Dashboard & Reports
- [ ] Overview: number of cars, rentals, income
- [ ] Recent activity
- [ ] Rental stats by date range

### 💅 UI/UX
- [ ] Integrate TailAdmin templates
- [ ] Display messages & alerts
- [ ] Mobile responsive

### 🧪 Testing
- [ ] Unit tests for models
- [ ] Rental logic validation
- [ ] Car availability tests

### 🚀 Deployment
- [ ] Set up production DB
- [ ] Configure static/media files
- [ ] Deploy to Render/Heroku/VPS

---

## ✅ MVP Done When:
- Staff can manage cars and clients
- Rentals can be booked and returned
- Payments are logged
- Admin can view key stats

