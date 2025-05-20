from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("cars/", views.cars, name="cars"),
    path("available_cars/", views.available_cars, name="available_cars"),
    path("booking.html", views.booking, name="booking"),
    path('get-models/<int:brand_id>/', views.get_models, name='get_models'),
    path("clients", views.clients, name="clients"),
    path("add-client/", views.add_client_ajax, name="add_client_ajax"),
    path('get-plate/<int:model_id>/', views.get_plate, name='get_plate'),
    path('chart/', views.chart_view, name='chart_view'),
    # path("add_car/", views.add_car_ajax, name="add_car_ajax"),
    path('timeline/', views.rental_timeline, name='rental-timeline'),
    path("add_car/", views.add_car, name="add_car"),
    path("client/<int:client_id>", views.client_card, name="client_card"),
    path("car/<int:car_id>", views.edit_car, name="edit_car"),  
    path('invoice/<int:rental_id>/', views.generate_invoice, name='generate_invoice'),
    path("rentals/", views.rentals_list, name="rentals"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
