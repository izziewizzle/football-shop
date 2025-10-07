from django.shortcuts import render, redirect, get_object_or_404
from main.forms import ProductForm
from main.models import Product
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.html import strip_tags
from django.views.decorators.http import require_POST

# ===========================================================
# SHOW MAIN
# ===========================================================
@login_required(login_url='/login')
def show_main(request):
    filter_type = request.GET.get("filter", "all")  # default 'all'
    category_filter = request.GET.get("category")

    # Get all products
    product_list = Product.objects.all()

    # Filter berdasarkan kategori
    if category_filter:
        product_list = product_list.filter(category__iexact=category_filter)

    # Filter berdasarkan kepemilikan produk
    if filter_type == "my" and request.user.is_authenticated:
        product_list = product_list.filter(user=request.user)

    context = {
        'name': request.user.username,
        'owner_name': 'Izzati Maharani Yusmananda',
        'class': 'PBP F',
        'product_list': product_list,
        'last_login': request.COOKIES.get('last_login', 'Never')
    }
    return render(request, "main.html", context)

# ===========================================================
# CREATE PRODUCT
# ===========================================================
@login_required(login_url='/login')
def create_product(request):
    form = ProductForm(request.POST or None)

    if form.is_valid() and request.method == 'POST':
        product_entry = form.save(commit=False)
        product_entry.user = request.user
        product_entry.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "create_product.html", context)

# ===========================================================
# SHOW PRODUCT DETAIL
# ===========================================================
@login_required(login_url='/login')
def show_product(request, id):
    product = get_object_or_404(Product, pk=id)
    context = {'product': product}
    return render(request, "product_detail.html", context)

# ===========================================================
# SHOW JSON / XML
# ===========================================================
def show_xml(request):
    product_list = Product.objects.all()
    xml_data = serializers.serialize("xml", product_list)
    return HttpResponse(xml_data, content_type="application/xml")

def show_json(request):
    product_list = Product.objects.all()
    data = [
        {
            "id": str(p.id),
            "name": p.name,
            "price": p.price,
            "description": p.description,
            "thumbnail": p.thumbnail,
            "category": p.category,
            "is_featured": p.is_featured,
            "user_id": p.user.id if p.user else None,
            "user_username": p.user.username if p.user else "Anonymous",
        }
        for p in product_list
    ]
    return JsonResponse(data, safe=False)

def show_xml_by_id(request, product_id):
    try:
        product_item = Product.objects.filter(pk=product_id)
        xml_data = serializers.serialize("xml", product_item)
        return HttpResponse(xml_data, content_type="application/xml")
    except Product.DoesNotExist:
        return HttpResponse(status=404)

def show_json_by_id(request, product_id):
    try:
        product = Product.objects.select_related('user').get(pk=product_id)
        data = {
            "id": str(product.id),
            "name": product.name,
            "price": product.price,
            "description": product.description,
            "thumbnail": product.thumbnail,
            "category": product.category,
            "is_featured": product.is_featured,
            "user_id": product.user.id if product.user else None,
            "user_username": product.user.username if product.user else "Anonymous",
        }
        return JsonResponse(data)
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)

# ===========================================================
# REGISTER USER
# ===========================================================
def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": True})
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
        else:
            # Respon AJAX gagal
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "message": "Form invalid."})
    context = {'form': form}
    return render(request, 'register.html', context)

# ===========================================================
# LOGIN USER
# ===========================================================
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = JsonResponse({"success": True}) if request.headers.get("X-Requested-With") == "XMLHttpRequest" else HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"success": False, "message": "Invalid credentials."})

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

# ===========================================================
# LOGOUT USER
# ===========================================================
def logout_user(request):
    logout(request)
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"success": True})
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

# ===========================================================
# EDIT PRODUCT
# ===========================================================
@login_required(login_url='/login')
def edit_product(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == 'POST':
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "edit_product.html", context)

# ===========================================================
# DELETE PRODUCT
# ===========================================================
@csrf_exempt
@login_required(login_url='/login')
def delete_product(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        product.delete()
        return JsonResponse({'status': 'success'}, status=200)

    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

# ===========================================================
# ADD PRODUCT VIA AJAX (MODAL)
# ===========================================================
@csrf_exempt
@require_POST
@login_required(login_url='/login')
def add_product_ajax(request):
    name = strip_tags(request.POST.get("name"))
    description = strip_tags(request.POST.get("description"))
    price = request.POST.get("price")
    category = request.POST.get("category")
    thumbnail = request.POST.get("thumbnail")
    is_featured = request.POST.get("is_featured") == "on"
    user = request.user

    new_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        thumbnail=thumbnail,
        is_featured=is_featured,
        user=user
    )
    new_product.save()

    return JsonResponse({"success": True, "message": "Product created successfully."}, status=201)