from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from core.forms import *
from django.contrib import messages
from django.utils import timezone
from .models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from core.forms import ProductForm, CheckoutForm
from core.models import Product, Order, OrderItem, CheckoutAddress
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth.decorators import login_required




def index(request):
    products = Product.objects.all()
    return render(request, 'core/index.html', {'products': products})

def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully")
            return redirect('/')
        else:
            messages.error(request, "Product is not added")
            print(form.errors)  # Print form errors to console for debugging
    else:
        form = ProductForm()
    return render(request, 'core/add_product.html', {'form': form})

def product_disc(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'core/product_disc.html', {'product': product})


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False,
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Added Quantity Item")
        else:
            order.items.add(order_item)
            messages.info(request, "Item Added to Cart")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item Added to Cart")

    # Redirect to the index page after adding an item to the cart
    return redirect('/')

# Your other views remain unchanged



def orderlist(request):
    if Order.objects.filter(user=request.user, ordered=False).exists():
        order = Order.objects.get(user=request.user, ordered=False)
        return render(request, 'core/orderlist.html', {'order': order})
    return render(request, 'core/orderlist.html', {'message': "Your Cart is Empty"})




def remove_item(request, pk):
    item = get_object_or_404(Product, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            order_item = OrderItem.objects.filter(
                product=item,
                user=request.user,
                ordered=False,
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, "Item Quantity Was Updated")
            return redirect("orderlist")
        else:
            messages.info(request, "This item is not in your Cart")
            return redirect("orderlist")
    else:
        messages.info(request, "You Do Not Have Any Order")
        return redirect("orderlist")



def add_item(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        user=request.user,
        ordered=False
    )

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(product__pk=pk).exists():
            if order_item.quantity < product.product_available_count:
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "Added Quantity Item")
                return redirect("orderlist")
            else:
                messages.info(request, "Sorry! Product is out of stock")
                return redirect('orderlist')
        else:
            order.items.add(order_item)
            messages.info(request, "Item Added to Cart")
            return redirect("product_desc", pk=pk)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item Added to Cart")
        return redirect("product_desc", pk=pk)

@login_required
def payment(request):
    try:
        order = Order.objects.get(user=request.user, ordered=False)
        order.ordered = True
        order.save()
        return redirect('payment_success')
    except Order.DoesNotExist:
        return HttpResponse("404 Error")

def checkout_page(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            street_address = form.cleaned_data.get('street_address')
            appartment_address = form.cleaned_data.get('appartment_address')
            country = form.cleaned_data.get('country')
            zip_code = form.cleaned_data.get('zip_code')

            checkout_address = CheckoutAddress(
                user=request.user,
                street_address=street_address,
                appartment_address=appartment_address,
                country=country,
                zip_code=zip_code
            )
            checkout_address.save()

            try:
                order = Order.objects.get(user=request.user, ordered=False)
                order.checkoutaddress = checkout_address
                order.save()
                return redirect('payment')
            except Order.DoesNotExist:
                messages.error(request, "No pending order found. Please add items to your cart before checking out.")
                return redirect('checkout_page')
    else:
        form = CheckoutForm()
    return render(request, 'core/checkout_address.html', {'form': form})



@login_required
def payment_success(request):
    try:
        orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
        if orders.exists():
            order = orders.first()
            messages.success(request, "Your order has been placed successfully!")
            return render(request, 'core/payment_success.html', {'order': order})
        else:
            messages.error(request, "No completed orders found.")
            return redirect('/')
    except Exception as e:
        messages.error(request, f"An error occurred: {e}")
        return redirect('/')



@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user, ordered=True).order_by('-ordered_date')
    return render(request, 'core/order_history.html', {'orders': orders})



@login_required
def delete_item(request, pk):
    order_item = get_object_or_404(OrderItem, product__pk=pk, order__user=request.user, order__ordered=False)
    order_item.delete()
    return redirect('orderlist')


