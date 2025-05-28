FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

<<<<<<< HEAD
EXPOSE 8080
CMD ["gunicorn", "car_rental.wsgi:application", "--bind", "0.0.0.0:8080"]
=======
# # Expose port (change if needed)
EXPOSE 7070

# Run the app
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
CMD ["gunicorn", "car_rental.wsgi:application", "--bind", "0.0.0.0:7070"]
>>>>>>> b61623cdc1034a85fa1681be8100c63e79695f53


