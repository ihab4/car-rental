from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Car, CarModel, Brand, Rental, Client
from django.views.decorators.csrf import csrf_exempt
from .forms import CarFilterForm
from datetime import datetime
from django.db.models import Count
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from weasyprint import HTML
from .models import Rental
import tempfile



# Create your views here.
def home(request):
    cars = Car.objects
    total_cars = cars.all().count()
    available_cars = cars.filter(status="Available").count()
    rented_cars = cars.filter(status="Rented").count()

    rental = Rental.objects.all().order_by("-created_at")[:5]
    clients_overview = []
    for rent in rental:
        overview = {"name": rent.client, "car": rent.car, "days": rent.days, 
                    "phone": rent.client.phone, "total_price": rent.total_price}
        clients_overview.append(overview)

    rentals = Rental.objects.select_related('car').all()
    
    rental_data = [
        {
            'car': f"{str(rental.car)} {rental.car.plate_number}",
            'client': str(rental.client),
            'start': rental.start_date.isoformat(),
            'end': rental.end_date.isoformat()
        }
        for rental in rentals
    ]
 
    context = {"total": total_cars, "available": available_cars, 
               "rented": rented_cars, "overview": clients_overview, 'rental_data': rental_data}

    return render(request, 'dashboard.html', context)

def cars(request):
    cars = Car.objects.all()
    
    context = {"cars": cars}

    return render(request, "cars.html", context)

def available_cars(request):
    available = Car.objects.filter(status="Available")
    
    context = {"available_cars": available}

    return render(request, "available_cars.html", context)


def booking(request):
    brands = Brand.objects.all()
    clients = Client.objects.order_by("first_name", "last_name")
    # carform = CarFilterForm()
    if request.method == "POST":
        # brand = request.POST.get("brand")
        # model = request.POST.get("model")
        plate = request.POST.get("plate")
        price = request.POST.get("price")
        pickup = request.POST.get("pickup_date")
        dropoff = request.POST.get("dropoff_date")
        if request.POST["client_type"] == "new":       
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            phone = request.POST.get("phone")
            cin = request.POST.get("cin")
            permis = request.POST.get("permis")
            new_client = Client.objects.create(first_name=first_name, last_name=last_name, 
                                               phone=phone, cin=cin, driver_licence=permis)
            client_id = new_client.id

        else:
            client_id = request.POST.get("client_id")
            # client_name = Client.objects.filter(id=client_id).values("first_name", "last_name")
            # print(client_id, client_name.first)
        
        car = Car.objects.get(id=plate)
        print(car)
        client = Client.objects.get(id=client_id)
        if not price:
            price = car.price_per_day

        pickup_date = datetime.strptime(pickup, "%Y-%m-%d").date()
        dropoff_date = datetime.strptime(dropoff, "%Y-%m-%d").date()
        rental = Rental.objects.create(car=car, client=client, start_date=pickup_date, 
                                       end_date=dropoff_date, price_per_day=float(price))
        
        return redirect("booking")
            

    return render(request, "booking.html", {"brands": brands, "clients": clients})

def get_models(request, brand_id):
    # brand_obj = get_object_or_404(Brand, brand__iexact=brand)
    # brand_obd = get_object_or_404(Brand, id=id)
    models = CarModel.objects.filter(brand_id=brand_id).values("id", "model_name")
    # print({'models': list(models)})
    return JsonResponse({'models': list(models)})

def get_plate(request, model_id):
    available_cars = Car.objects.filter(model_id=model_id, status="Available").values("id", "plate_number")
    # models = CarModel.objects.filter(brand_id=brand_id).values("id", "model_name")
    # print({'models': list(models)})
    return JsonResponse({'available_cars': list(available_cars)})

def clients(request):
    clients = Client.objects.all().order_by("-created_at")

    if request.method == "GET":
        query = request.GET.get('q')
        if query:
            clients = Client.objects.filter(first_name__icontains=query)                 


    context = {"clients": clients, "query": query}

    return render(request, 'clients.html', context)

    # context = {"details": details}
    # return render(request, "clients.html", context)


@csrf_exempt
def add_client_ajax(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        phone = request.POST.get('phone')
        cin = request.FILES.get('cin')
        permis = request.FILES.get('permis')
        print("ajaxclient", cin, permis)
        
        # Add more fields as needed
        try:
            client = Client.objects.create(first_name=first_name, last_name=last_name, 
                                       phone=phone, cin=cin, driver_licence=permis)
            return JsonResponse({'success': True, 'client_id': client.id})              
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        # return JsonResponse({'success': True, 'client_id': client.id})

        # return redirect("home")

    # return JsonResponse({'success': False})


def chart_view(request):
    # Example: Get number of rentals per car
    rental_data = Rental.objects.values('car__model').annotate(rental_count=Count('car')).order_by('car__model')

    # Prepare data for the chart
    labels = [CarModel.objects.get(id=data['car__model']).model_name for data in rental_data]
    data = [data['rental_count'] for data in rental_data]
    print(labels, data)

    context = {
        'labels': labels,
        'data': data,
    }

    return render(request, 'dashboard.html', context)

# @csrf_exempt
# def add_car_ajax(request):
#     if request.method == "POST":
#         brand = request.POST.get("brand")
#         model = request.POST.get("model")
#         image = request.FILES.get("image")
#         print("ajax", image)
        

#         try:
#             new_brand = Brand.objects.create(brand=brand)
        
#             new_model = CarModel.objects.create(brand=new_brand, model_name=model, image=image)
#             # return JsonResponse({'success': True, 'brand_id': new_brand.id})
#         except Exception as e:
#             return JsonResponse({'success': False, 'error': str(e)})
        
        
#         return JsonResponse({'success': True, 'brand_id': new_brand.id, "model_id": new_model.id})
        
    
def add_car(request):
    # models = get_models(brand_id)
    brands = Brand.objects.all()
    if request.method == "POST":
        brand_id = request.POST.get("brand")
        brand = Brand.objects.get(id=brand_id)
        model_id = request.POST.get("model")
        model = CarModel.objects.get(id=model_id)
        plate = f'{request.POST.get("num_part")}-{request.POST.get("letter_part")}-{request.POST.get("region_part")}'
        year = request.POST.get("year")
        price = request.POST.get("price")
        image = request.FILES.get("image")
        print("addcar", image)
        try:
            car = Car.objects.create(brand=brand, model=model, year=year, plate_number=plate,
                                    status="Available", price_per_day=price, image=image)
            # messages.success(request, "car created successfully")
            return redirect("add_car")
        except Exception as e:
            messages.success(request, f"error {e}")
            return redirect("add_car")

    return render(request, "add_car.html", {"brands": brands})

def rental_timeline(request): 
    rentals = Rental.objects.select_related('car').all()
      
    rental_data = [
        {
            'car': f"{str(rental.car)} {rental.car.plate_number}",
            'client': str(rental.client),
            'start': rental.start_date.isoformat(),
            'end': rental.end_date.isoformat()
        }
        for rental in rentals
    ]


    context = {
        "rental_data": rental_data
    }

    return render(request, "rental_timeline.html", context)

def client_card(request, client_id):
    client = Client.objects.get(id=client_id)
    context = {"client": client}
    return render(request, "client-card.html", context)

def edit_car(request, car_id):
    car = Car.objects.get(id=car_id)
    if car.plate_number.startswith("WW"):
        plate1 = car.plate_number
        plate2 = ""
        plate3 = ""
    else:
        plate1, plate2, plate3 = car.plate_number.split("-")

    if request.method == "POST":
        car.plate_number = f'{request.POST.get("num_part")}-{request.POST.get("letter_part")}-{request.POST.get("region_part")}'
        car.price_per_day = request.POST.get("price")

        car.save()
        return redirect("cars")
        

    context = {"car": car, "plate1": plate1, "plate2": plate2, "plate3": plate3}
    return render(request, "car-card.html", context)


def generate_invoice(request, rental_id):
    rental = Rental.objects.get(id=rental_id)
    total_days = (rental.end_date - rental.start_date).days
    total_price = rental.price_per_day * total_days

    html_string = render_to_string('invoice.html', {
        'rental': rental,
        'total_days': total_days,
        'total_price': total_price,
    })

    html = HTML(string=html_string)
    result = html.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=invoice_{rental.id}.pdf'
    return response

def rentals_list(request):
    rentals = Rental.objects.all().order_by("-created_at")

    return render(request, "rentals.html", {"rentals": rentals})


