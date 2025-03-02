from decimal import Decimal
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from ndio_app.models import Payment, User_Detail
from ndio_app.models import User
from .forms import PaymentForm, RegisterForm, UserDetailForm, OrderForm
from . import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import requests


# Create your views here.
def get_session():
    """ This function creates an API session, allowing
        us to interact with the API for 1 hour. And
        we can request another one after 1 hour. """

    url = "https://apitest.axxess.co.za/calls/rsapi/getSession.json?strUserName=KAB149&strPassword=cW3j*-NUmKG~$5!"
    username = "ResellerAdmin"
    password = "jFbd5lg7Djfbn48idmlf4Kd"
    # Authenticating before we can access the sessionID
    response = requests.get(url, auth=(username, password))

    # Getting the session ID
    if response.status_code == 200:
        session_id = response.json().get("strSessionId")
        return session_id
    else:
        print("Something went wrong. Try again")
        return None

def get_coordinates(address):
    
    """Converts a user's address into latitude and longitude using the Google Maps API."""
    
    # Dont forget to hide this
    google_maps_api_key = "AIzaSyDvsvOuUIWak9axNX97yBDoa0oKm_f1suY"
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={google_maps_api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        location = response.json()["results"][0]["geometry"]["location"]
        print(location["lat"], location["lng"])
        return (location["lat"], location["lng"])
    else:
        print("Failed to get coordinates.")
        return None, None

providers_list = []
# Check if fibre is available in that area
def check_fibre_availability(address):
    """This function checks if fibre is available in the user's address.
        It accepts 3 parameters: 
        - The latitude coordinate (str)
        - The longitude coordinate (str)
        - address of the user (str)

        And it returns a message which confirms if fibre is available in your area or not"""
    
    session_id = get_session()
    latitude_coordinate, longitude_coordinate = get_coordinates(address=address)
    url = f"https://apitest.axxess.co.za/calls/rsapi/checkFibreAvailability.json?"

    params = {
        "strSessionId": session_id,
        "strLatitude": str(latitude_coordinate),
        "strLongitude": str(longitude_coordinate),
        "strAddress": address
    }

    # Authentication for api
    username = "ResellerAdmin"
    password = "jFbd5lg7Djfbn48idmlf4Kd"
    response = requests.get(url, auth=(username, password), params=params)

    # Check if the request was successful
    if response.status_code == 200:
        network_providers = response.json()#["arrAvailableProvidersGuids"]
        
        for providers in network_providers["arrAvailableProvidersGuids"]:
            provider_id = (f"{providers['guidNetworkProviderId']}")
            providers_list.append(provider_id)
            print(providers_list)
        print(providers_list)
        return providers_list
    else:
        return None

print(providers_list)    
# Get the network provider products
def get_network_provider_products(address):
    session_id = get_session()
    network_provider_id = check_fibre_availability(address=address)
    
    pass


def home(request):
    request.session.flush()
    if request.method == "POST":
        address = request.POST.get("address")
        check_fibre_availability(address=address)

    return render(request, "ndio_app/home.html")
      

def referral_home(request, ref_code=None):
    """Home view with referral tracking."""
    # Use ref_code from URL if provided
    print(request.session.items())
    request.session.flush()
    if ref_code:
        try:
            # Check if the referral code exists in the database
            referrer = User_Detail.objects.get(code=ref_code)
            request.session['referral_code'] = ref_code  # Store ref_code in session
            referrer_id = referrer.user.id  
            request.session['referrer'] = referrer_id # Store referrer in session    
            request.session.modify = True
            request.session.save()    
            print(f"Referrer code: {referrer_id} stored in session")
            print(f"Referrer: {referrer_id}")
            print(f"Session items After: {request.session.items()}")
        except User_Detail.DoesNotExist:
            print(f"Invalid referral code: {ref_code}")

    mtn_products = get_mtn_lte_products()
    telkom_products = get_telkom_products()

    if "address" in request.GET:  # Check if the user submitted the form
        address = request.GET.get("address")  # Get the address from the form
        lat, lng = get_coordinates(address)  # Get coordinates from the address
        session_id = get_session()  # Get a session ID for API requests
        bbox = request.GET.get("strBBox")
        width = request.GET.get("strWidth")
        height = request.GET.get("strHeight")
        i_coordinate = request.GET.get("strICoOrdinate")
        j_coordinate = request.GET.get("strJCoOrdinate")

        # Store address in session
        request.session['address'] = address
            
        if lat and lng and session_id:  # Ensure we have valid coordinates and session
            results = {
                "mtn_lte": check_mtn_lte_availability(lat, lng, address, bbox, height, width, i_coordinate, j_coordinate),
                "telkom_lte": check_telkom_lte_availability(lat, lng, address),
            }

            context = {
                "results": results,
                "address": address,
                "latitude": lat,
                "longitude": lng,
                "mtn_products": mtn_products,
                "telkom_products": telkom_products
            }
            return render(request, "ndio_app/referral_home.html", context)
        else:
            return render(request, "ndio_app/referral_home.html", {"error": "Could not determine location or session expired."})

    return render(request, "ndio_app/referral_home.html")

def create_user(first_name, last_name, email, client_password, id_number, address, city, postal_code):
    """ This function creates a user on the api end
    using the information retrieved from a form. 
    It accepts the following parameters:
        - SessionId 
        - strName
        - strLastName
        - strEmail
        - strPassword
        - strIdNumber
        - strAddress
        - strCity
        - intPostalCode """
    
    # Get session ID before interacting with API 
    session_id = get_session()

    url = f"https://apitest.axxess.co.za/calls/rsapi/createClient.json?strUserName=KAB149&strPassword=cW3j*-NUmKG~$5!"
    params = {"strSessionId": session_id,
              "strName": first_name,
              "strLastName": last_name,
              "strEmail": email,
              "strPassword": client_password,
              "strIdNumber": id_number,
              "strAddress": address,
              "strCity": city,
              "intPostalCode": postal_code
              }
    username = "ResellerAdmin"
    password = "jFbd5lg7Djfbn48idmlf4Kd"

    # Building the API query
    response = requests.put(url, params=params, auth=(username, password))

    # Check if the user was created or not
    if response.status_code == 201:
        print(response.json().get("guidClientId"))
        return response.json().get("guidClientId")
    else:
        print("User not created")

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately
            
            # Capture user information for client creation on API
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['password'] = user.password
           
            return redirect('order_details')  # Redirect to the desired page
        else:
            # Add error messages for invalid form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")
    else:
        form = RegisterForm()
        selected_product = request.GET.get('selected_product')
        request.session['selected_product'] = selected_product

    return render(request, 'accounts/register.html', {'form': form})

def referral_register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in the user immediately

            # Capture user information for client creation on API
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            request.session['email'] = user.email
            request.session['password'] = user.password
            
        return redirect("user_account")  # Redirect to the desired page
    else:
        # Handle referral code
        ref_code = request.session.get('referral_code')
        if ref_code:
            try:
                referring_user = User_Detail.objects.get(code=ref_code).user
                user.referral.referred_by = referring_user
                user.referral.save()
                referring_user.referral.save()
                print("ref_code saved!!")
                    
            except User_Detail.DoesNotExist:
                messages.error(request, "Invalid referral code.")

        else:
            # Add error messages for invalid form
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

        form = RegisterForm()
        ref_code = request.GET.get('ref_code')
        request.session['ref_code'] = ref_code

    return render(request, 'accounts/referral_register.html', {'form': form, 'ref_code': ref_code})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('user_account')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def login_view_order(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('order_details')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login_order.html', {'form': form})

def logout_view(request):
    logout(request)
    request.session.flush() # clear session
    return redirect('home')  # Redirect to the home page after logout

def lte_view(request):
    #items = get_products()
    return render(request, 'ndio_app/lte.html', {})

def hosting_view(request):
    return render(request, 'ndio_app/hosting.html')

def fibre_view(request):
    return render(request, 'ndio_app/fibre.html')

@login_required
def order_details(request):
    """Handles order details submission."""
    # Store referrer id 
    referrer_id = request.session.get('referrer')
    print(referrer_id)

    # Get referrer as user instance
    # By using the referrer_id
    if referrer_id:
        referrer = User.objects.get(id=referrer_id)
        print(referrer)
    else:
        referrer = None

    if request.method == "POST":
        form = forms.UserDetailForm(request.POST)
        form_order = forms.OrderForm(request.POST)


        if form.is_valid() and form_order.is_valid():
            client = form.save(commit=False)
            order = form_order.save(commit=False)

            client.user = request.user
            # populate referrered_by field with uer instance of referrer
            client.referred_by = referrer
            # set the id_number of client
            order.id_number = client
            
            client_first_name = request.session.get('first_name')
            client_last_name = request.session.get('last_name')
            client_email = "alhiyha@ndio.co.za" 
            client_password = request.session.get('password')
            client_id_number = client.id_number
            client_address = order.address
            client_city = order.city
            client_postal_code = order.postal_code

            """create_user(client_first_name, client_last_name, client_email, client_password, client_id_number, client_address,
                        client_city, client_postal_code)"""
            client.save()
            order.save()
            
        return redirect('payment_view')  # Redirect to another page 
    
    else:
        # If GET request or invalid form, show the form again
        address = request.session.get('address', '')  # Provide default empty string if None
        address_split = address.split(', ')
        city = address_split[2]
        print(request.session.items())
        # setting initial values for forms
        order_initial_data = {'address': address, 'city':city}
        user_detail_intial_data = {'referred_by': referrer}
        
        form = forms.UserDetailForm(initial=user_detail_intial_data)
        form_order = forms.OrderForm(initial=order_initial_data)

        context = {
            'form': form, 
            'form_order': form_order,
        }

        return render(request, 'ndio_app/order_details.html', context=context)
    
@login_required
def user_account(request):
    # Get user_id
    user_id = request.user.id
    
    # Check if Yoco sent back relevant payment data
    payment_id = request.GET.get('id')  # Example: Yoco might return an ID or reference
    status = request.GET.get('status')
    print(status)
    
    # Get user referral code using id, handling case where user has no entry
    ref_code = User_Detail.objects.filter(user_id=user_id).first()
    
    if not ref_code:
        print('No referral code found for this user.')
    
    context = {
        'ref_code': ref_code
    }

    if status == 'success':  # Ensure the payment was successful
        Payment.objects.filter(payment_id=payment_id).update(status="Paid")
        return render(request, 'accounts/user_account.html', context)  # Render the template with context
    else:
        return redirect('unsuccessful_payment')  # Handle unsuccessful cases

def unsuccessful_payment(request):
    return render(request, "ndio_app/unsuccessful.html")

def process_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data.get('token')
            amount = form.cleaned_data.get('amount')
            currency = form.cleaned_data.get('currency')
            name = form.cleaned_data.get('name')

            try:
                amount = Decimal(amount)
            except:
                return JsonResponse({'status': 'error', 'message': 'Invalid amount'})

            url = "https://payments.yoco.com/api/checkouts"
            headers = {
                'Authorization': f'Bearer {settings.YOCO_SECRET_KEY}',
                'Content-Type': 'application/json'
            }
            
            try:
                data = json.dumps({
                    'amount': float(amount),  # Convert to cents for the Yoco API
                    'currency': currency,
                    'successUrl': request.build_absolute_uri('/user_account/'),
                    'cancelUrl': request.build_absolute_uri('/unsuccessful_payment/')
                })
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f'Invalid amount: {e}'})

            response = requests.post(url, headers=headers, data=data)

            if response.status_code < 400:
                # Redirect user to Yoco's payment page
                redirect_url = response.json().get('redirectUrl')
                if redirect_url:
                    return redirect(redirect_url)
                return JsonResponse({'status': 'success', 'message': 'Payment initiated but no redirect URL received'})
            else:
                return redirect('unsuccessful')  # If Yoco request fails

        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data', 'errors': form.errors})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@csrf_exempt  # Avoid this if possible; use CSRF tokens.
def payment_view(request):

    products = {
        '15308809-e706-11ec-bb2d-0050568d6656': 'Telkom Mobile Off-Peak Uncapped Smart Combo',
        '15308463-e706-11ec-bb2d-0050568d6656': 'Telkom Mobile 10Mbps Uncapped Smart Combo',
        '153085ed-e706-11ec-bb2d-0050568d6656': 'Telkom Mobile 20Mbps Uncapped Smart Combo',
        '55ce17ad-9616-11ec-bb2d-0050568d6656': 'MTN LTE 10Mbps Uncapped Smart Combo',
        '55ce1813-9616-11ec-bb2d-0050568d6656': 'MTN LTE 20Mbps Uncapped Smart Combo',
        '55ce187e-9616-11ec-bb2d-0050568d6656': 'MTN LTE 50Mbps Uncapped Smart Combo',
    }

    prices = {
        '15308809-e706-11ec-bb2d-0050568d6656': 800,
        '15308463-e706-11ec-bb2d-0050568d6656': 554,
        '153085ed-e706-11ec-bb2d-0050568d6656': 769,
        '55ce17ad-9616-11ec-bb2d-0050568d6656': 890,
        '55ce1813-9616-11ec-bb2d-0050568d6656': 565,
        '55ce187e-9616-11ec-bb2d-0050568d6656': 500
    }

    selected_product = request.session.get('selected_product')
    if not selected_product:
        return JsonResponse({'status': 'error', 'message': 'No product selected'})

    product_name = products.get(selected_product, 'Unknown Product')
    product_price = prices.get(selected_product, 0)
    total_price = product_price + 300
    public_key = settings.YOCO_PUBLIC_KEY

    initial_data = {'amount': total_price}
    form = PaymentForm(initial=initial_data)

    context = {
        'yoco_public_key': public_key,
        'currency': 'ZAR',
        'product_name': product_name,
        'product_price': product_price,
        'form': form,
        'amount': total_price
    }

    return render(request, 'ndio_app/payments.html', context)