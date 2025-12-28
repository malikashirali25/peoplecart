from django.shortcuts import render, redirect
from .models import Product, Category, Profile, Order, Customer
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
from django.urls import reverse
import json
import decimal

def home(request):
	products = Product.objects.all()
	return render(request, 'home.html', {'products':products})


def about(request):
	return render(request, 'about.html', {})	

def product(request,pk):
	product = Product.objects.get(id=pk)
	return render(request, 'product.html', {'product':product})




def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			messages.success(request, ("You Have Been Logged In!"))
			return redirect('home')
		else:
			messages.success(request, ("There was an error, please try again..."))
			return redirect('login')

	else:
		return render(request, 'login.html', {})


def logout_user(request):
	logout(request)
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')



def register_user(request):
	form = SignUpForm()
	if request.method == "POST":
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			# log in user
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ("Username Created - Welcome! You can update your profile anytime."))
			return redirect('home')
		else:
			messages.success(request, ("Whoops! There was a problem Registering, please try again..."))
			return redirect('register')
	else:
		return render(request, 'register.html', {'form':form})
	
def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)
		
		# Get or create user profile
		try:
			user_profile = Profile.objects.get(user=current_user)
		except Profile.DoesNotExist:
			user_profile = Profile.objects.create(user=current_user)
		
		profile_form = UserInfoForm(request.POST or None, instance=user_profile)

		if request.method == 'POST':
			if user_form.is_valid() and profile_form.is_valid():
				user_form.save()
				profile_form.save()
				login(request, current_user)
				messages.success(request, "Profile Has Been Updated Successfully!")
				return redirect('home')
		
		return render(request, "update_user.html", {
			'user_form': user_form,
			'profile_form': profile_form
		})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')


def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated...")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')
	


def search(request):
	# Determine if they filled out the form
	if request.method == "POST":
		search_query = request.POST['searched']
		# Query The Products DB Model
		searched = Product.objects.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
		# Test for null
		if not searched:
			messages.info(request, f"No products found for '{search_query}'. Please try a different search term.")
			return render(request, "search.html", {'search_query': search_query})
		else:
			return render(request, "search.html", {'searched': searched, 'search_query': search_query})
	else:
		# Show all products or featured products when no search
		all_products = Product.objects.all()[:12]  # Limit to 12 for performance
		return render(request, "search.html", {'all_products': all_products})	


def category(request, foo):
	# Replace Hyphens with Spaces
	foo = foo.replace('-', ' ')
	# Grab the category from the url
	try:
		# Look Up The Category
		category = Category.objects.get(name=foo)
		products = Product.objects.filter(category=category)
		return render(request, 'category.html', {'products':products, 'category':category})
	except:
		messages.success(request, ("That Category Doesn't Exist..."))
		return redirect('home')


def cart(request):
	# Get all products for reference (in a real app, you'd use an API endpoint)
	products = Product.objects.all()
	# Create a dictionary for quick lookup
	products_dict = {}
	for p in products:
		products_dict[str(p.id)] = {
			'id': p.id,
			'name': p.name,
			'price': float(p.price),
			'sale_price': float(p.sale_price) if p.is_sale else None,
			'is_sale': p.is_sale,
			'image_url': p.image.url if p.image else None,
			'category': p.category.name,
			'description': p.description
		}
	# Convert to JSON string for template
	products_json = json.dumps(products_dict)
	return render(request, 'cart.html', {'products_json': products_json})


def checkout(request):
	if not request.user.is_authenticated:
		messages.warning(request, "Please login to proceed to checkout.")
		return redirect('login')
	
	# Get cart from session or request
	cart_data = request.GET.get('cart', '[]')
	try:
		cart_items = json.loads(cart_data)
	except:
		# Try to get from POST or use empty
		cart_items = []
	
	if not cart_items:
		messages.warning(request, "Your cart is empty. Add some items before checkout.")
		return redirect('cart')
	
	# Calculate totals
	subtotal = decimal.Decimal('0.00')
	items_list = []
	
	for item in cart_items:
		try:
			product = Product.objects.get(id=int(item['id']))
			price = decimal.Decimal(str(product.sale_price if product.is_sale else product.price))
			quantity = int(item.get('quantity', 1))
			item_total = price * quantity
			subtotal += item_total
			
			items_list.append({
				'product': product,
				'quantity': quantity,
				'price': price,
				'total': item_total
			})
		except Product.DoesNotExist:
			continue
	
	if not items_list:
		messages.warning(request, "No valid items in cart.")
		return redirect('cart')
	
	tax = subtotal * decimal.Decimal('0.10')  # 10% tax
	total = subtotal + tax
	
	# Get user profile for shipping info
	profile = None
	try:
		profile = Profile.objects.get(user=request.user)
	except Profile.DoesNotExist:
		pass
	
	# PayPal payment form
	paypal_dict = {
		"business": settings.PAYPAL_RECEIVER_EMAIL,
		"amount": str(total),
		"item_name": f"Order from PeopleCart - {len(items_list)} item(s)",
		"invoice": f"INV-{request.user.id}-{request.session.session_key[:8]}",
		"notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
		"return_url": request.build_absolute_uri(reverse('checkout_success')),
		"cancel_return": request.build_absolute_uri(reverse('checkout_cancel')),
		"custom": json.dumps({
			'user_id': request.user.id,
			'cart_items': cart_items
		}),
		"currency_code": "USD",
		"image_url": "https://www.paypalobjects.com/webstatic/mktg/logo/pp_cc_mark_111x69.jpg",
	}
	
	# Create custom PayPal form with modern button
	form = PayPalPaymentsForm(initial=paypal_dict)
	form.button_type = "subscribe"  # Use modern button style
	
	context = {
		'form': form,
		'items': items_list,
		'subtotal': subtotal,
		'tax': tax,
		'total': total,
		'profile': profile,
		'cart_items_json': json.dumps(cart_items)
	}
	
	return render(request, 'checkout.html', context)


def checkout_success(request):
	# Clear cart from localStorage will be handled by JavaScript
	messages.success(request, "Payment successful! Your order has been placed.")
	return render(request, 'checkout_success.html', {})


def checkout_cancel(request):
	messages.info(request, "Payment was cancelled. You can continue shopping.")
	return render(request, 'checkout_cancel.html', {})


@csrf_exempt
def paypal_ipn_handler(request):
	# This will be handled by django-paypal's IPN system
	# Orders will be created automatically when payment is verified
	pass
