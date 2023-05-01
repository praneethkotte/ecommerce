# ecommerce

Create a new project folder called 'ecommerce' and then cd into the folder via the terminal and execute these commands:

pyenv local 3.10.7 # this sets the local version of python to 3.10.7
python3 -m venv .venv # this creates the virtual environment for you
source .venv/bin/activate # this activates the virtual environment
pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
We will use Django (https://www.djangoproject.com) as our web framework for the application. We install that with

    pip install Django==4.1.2
And that will install django version 4.1.2 (or pick a different version if there's something newer) with its associated dependencies. We can now start to build the application.

Now we can start to create the site using the django admin tools. Issue this command, and don't forget the '.' at the end of the line, which says 'create the project in this directory'. This will create the admin part of our application, which will sit alongside the actual site.

    django-admin startproject ecommerce .
We're using the name 'ecommerce' but you could use whatever seems appropriate. We'll save the ecommerce' label for later in the app. For now we're setting up the support structure for the site, which will live in a separate folder inside of this one.

We need to specify some settings for the site, which we do in the ecommerce/settings.py file. Open this and add this line above the line for pathlib import Path:

    import os
Now go to the end of the file to add a line specifying the root directory for the static files.

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
Now go further up the file to 'ALLOWED_HOSTS' so that we can run this beyond 'localhost' and 127.0.0.1, which are the only allowed ones if this is empty. Modify this accordingly to suit your needs:

    ALLOWED_HOSTS = ['solarpodium-exportvelvet-8000.codio-box.uk']
Although we are not using a database for this application, django uses one in the background. We now need to configure this database, which you saw was already detailed in the settings.py file. As django has a built-in admin tool, it already knows some of the tables that it needs to use. We can set this up with the command:

    python3 manage.py migrate
You should see a number of steps being run, each hopefully ending ... OK If not, then look to the errors in the terminal. If you see one that says 'NameError: name 'os' is not defined', then go back and add the import for the 'os' library.

Start the Server
We can now use the manage.py command tool to start the development server by entering this command in the terminal:

    python3 manage.py runserver
If you're doing this on another platform, then you might need to use this instead (change the port number from 8000 as required):

    python3 manage.py runserver 0.0.0.0:8000 
If it went well, then you should see the python rocket launching your site when you open the browser at the site.

Creating the Story content
Leave the server running. Open a new terminal and navigate as required to the same directory. We can now set about creating the space for our temperature stories by running this command:

    python3 manage.py startapp store
This will create a new folder for us including space for database migrations, and other details specific to our content. By the way, we need to use an underscore to join the words in temp_stories as a hyphen is not allowed as part of an identifier in django applications.

Django needs to know the urls of the site so that it can serve up pages to visitors, and tell others that the page requested isn't part of the site. We do that by opening mysite/urls.py and adding a line for the pages that will be under temp_stories.

First, add 'include' to the line with 'import path' so that it reads

    from django.urls import path, include
Second, add this line (plus the , at the end of the line above it), to have django find your store pages:

    path('', include('store.urls')),
Third, we need to modify the settings.py file in the mysite app, so that it knows to include the 'store' contents. We do this by adding a line in the section on 'INSTALLED_APPS'. Add this line to the end of the block ( plus the , at the end of the line above it).

    'temp_stories.apps.TempStoriesConfig',
Fourth, we need to tell temp_stories about the URLs it is using, so that they can be added to the list of URLs (pages) used by 'mysite'. We do that by creating the file urls.py in the 'store' folder. It should hold these details:

    from django.urls import path
    from . import views

    urlpatterns = [
        path('', views.index, name='index')
    ]
We can now start the logic for our application. Before we do that we need to add the Faker library to our application from https://pypi.org/project/Faker/. Add it with the command:

    pip install faker
Now create a blank main.html file and put this code into it. This is almost the same as what we used in the flask version. We've only changed the text in the file.
<!DOCTYPE html>
{% load static %}
<html>
<head>
	<title>Ecom</title>

	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, minimum-scale=1" />

	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css" integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">

	<link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}">

	<script type="text/javascript">
		var user = '{{request.user}}'

		function getToken(name) {
		    var cookieValue = null;
		    if (document.cookie && document.cookie !== '') {
		        var cookies = document.cookie.split(';');
		        for (var i = 0; i < cookies.length; i++) {
		            var cookie = cookies[i].trim();
		            // Does this cookie string begin with the name we want?
		            if (cookie.substring(0, name.length + 1) === (name + '=')) {
		                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		                break;
		            }
		        }
		    }
		    return cookieValue;
		}
		var csrftoken = getToken('csrftoken')

		function getCookie(name) {
		    // Split cookie string and get all individual name=value pairs in an array
		    var cookieArr = document.cookie.split(";");

		    // Loop through the array elements
		    for(var i = 0; i < cookieArr.length; i++) {
		        var cookiePair = cookieArr[i].split("=");

		        /* Removing whitespace at the beginning of the cookie name
		        and compare it with the given string */
		        if(name == cookiePair[0].trim()) {
		            // Decode the cookie value and return
		            return decodeURIComponent(cookiePair[1]);
		        }
		    }

		    // Return null if not found
		    return null;
		}
		var cart = JSON.parse(getCookie('cart'))

		if (cart == undefined){
			cart = {}
			console.log('Cart Created!', cart)
			document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
		}
		console.log('Cart:', cart)
	
	</script>

</head>
<body>

	<nav class="navbar navbar-expand-lg navbar-dark bg-dark">
	  <a class="navbar-brand" href="{% url 'store' %}">Ecom</a>
	  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
	    <span class="navbar-toggler-icon"></span>
	  </button>

	  <div class="collapse navbar-collapse" id="navbarSupportedContent">
	    <ul class="navbar-nav mr-auto">
	      <li class="nav-item active">
	        <a class="nav-link" href="{% url 'store' %}">Store <span class="sr-only">(current)</span></a>
	      </li>
	 
	    </ul>
      	<!-- <form class="d-flex" role="search" method="POST" action="{% url 'store' %}">
        	{% csrf_token %}
			<input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
			<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
		</form> -->
		<form class="d-flex" role="search" method="POST" action="{% url 'store' %}">
			{% csrf_token %}
			<input class="form-control mr-sm-2" type="search" name="search_query" placeholder="Search" aria-label="Search">
			<button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
		</form>
		
	    <div class="form-inline my-2 my-lg-0">
	     	<a href="#"class="btn btn-warning">Login</a>
	     	
	     	<a href="{% url 'cart' %}">
	    		<img  id="cart-icon" src="{% static 'images/cart.png' %}">
	    	</a>
	    	<p id="cart-total">{{cartItems}}</p>

	    </div>
	  </div>
	</nav>

     <div class="container">
            <br>
            {% block content %}


            {% endblock content %}
         </div>


	<script src="https://code.jquery.com/jquery-3.4.1.slim.min.js" integrity="sha384-J6qa4849blE2+poT4WnyKhv5vZF5SrPo0iEjwBvKU7imGFAV0wwj1yYfoRSJoZ+n" crossorigin="anonymous"></script>

	<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>

	<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js" integrity="sha384-wfSDF2E50Y2D1uUdj0O3uMBJnjuUD4Ih7YwaYd1iqfktj0Uod8GCExl3Og8ifwB6" crossorigin="anonymous"></script>

	<script type="text/javascript" src="{% static 'js/cart.js' %}"></script>
</body>
</html>
 and similarly repeat the same steps for cart, checkout and store.html
 store.html 
 {% extends 'store/main.html' %}
{% load static %}
{% block content %}
	<div class="row">
		{% for product in products %}
		<div class="col-lg-4">
			<img class="thumbnail" src="{{product.imageURL}}">
			<div class="box-element product">
				<h6><strong>{{product.name}}</strong></h6>
				<hr>

				<button data-product="{{product.id}}" data-action="add" class="btn btn-outline-secondary add-btn update-cart">Add to Cart</button>
				
				<a class="btn btn-outline-success" href="#">View</a>
				<h4 style="display: inline-block; float: right"><strong>${{product.price|truncatechars:7}}</strong></h4>

			</div>
		</div>
		{% endfor %}
	</div>

{% endblock content %}

Cart.html code 
{% extends 'store/main.html' %}
{% load static %}
{% block content %}
	<div class="row">
		<div class="col-lg-12">
			<div class="box-element">

				<a  class="btn btn-outline-dark" href="{% url 'store' %}">&#x2190; Continue Shopping</a>

				<br>
				<br>
				<table class="table">
					<tr>
						<th><h5>Items: <strong>{{order.get_cart_items}}</strong></h5></th>
						<th><h5>Total:<strong> ${{order.get_cart_total|floatformat:2}}</strong></h5></th>
						<th>
							<a  style="float:right; margin:5px;" class="btn btn-success" href="{% url 'checkout' %}">Checkout</a>
						</th>
					</tr>
				</table>

			</div>

			<br>
			<div class="box-element">
				<div class="cart-row">
					<div style="flex:2"></div>
					<div style="flex:2"><strong>Item</strong></div>
					<div style="flex:1"><strong>Price</strong></div>
					<div style="flex:1"><strong>Quantity</strong></div>
					<div style="flex:1"><strong>Total</strong></div>
				</div>
				{% for item in items %}
				<div class="cart-row">
					<div style="flex:2"><img class="row-image" src="{{item.product.imageURL}}"></div>
					<div style="flex:2"><p>{{item.product.name}}</p></div>
					<div style="flex:1"><p>${{item.product.price|floatformat:2}}</p></div>
					<div style="flex:1">
						<p class="quantity">{{item.quantity}}</p>
						<div class="quantity">
							<img data-product="{{item.product.id}}" data-action="add" class="chg-quantity update-cart" src="{% static  'images/arrow-up.png' %}">
					
							<img data-product="{{item.product.id}}" data-action="remove" class="chg-quantity update-cart" src="{% static  'images/arrow-down.png' %}">
						</div>
					</div>
					<div style="flex:1"><p>${{item.get_total|floatformat:2}}</p></div>
				</div>
				{% endfor %}
			</div>
		</div>
	</div>
{% endblock content %}
 
Checkout.html code 
{% extends 'store/main.html' %}
{% load static %}
{% block content %}
     <div class="row">
		<div class="col-lg-6">
			<div class="box-element" id="form-wrapper">
				<form id="form">
					<div id="user-info">
						<div class="form-field">
							<input required class="form-control" type="text" name="name" placeholder="Name..">
						</div>
						<div class="form-field">
							<input required class="form-control" type="email" name="email" placeholder="Email..">
						</div>
					</div>
					
					<div id="shipping-info">
						<hr>
						<p>Shipping Information:</p>
						<hr>
						<div class="form-field">
							<input class="form-control" type="text" name="address" placeholder="Address..">
						</div>
						<div class="form-field">
							<input class="form-control" type="text" name="city" placeholder="City..">
						</div>
						<div class="form-field">
							<input class="form-control" type="text" name="state" placeholder="State..">
						</div>
						<div class="form-field">
							<input class="form-control" type="text" name="zipcode" placeholder="Zip code..">
						</div>
						<div class="form-field">
							<input class="form-control" type="text" name="country" placeholder="Zip code..">
						</div>
					</div>

					<hr>
					<input id="form-button" class="btn btn-success btn-block" type="submit" value="Continue">
				</form>
			</div>

			<br>
			<div class="box-element hidden" id="payment-info">
				<small>Paypal Options</small>
				<!--<button id="make-payment">Make payment</button>-->
				<div id="paypal-button-container"></div>
			</div>
			
		</div>

		<div class="col-lg-6">
			<div class="box-element">
				<a  class="btn btn-outline-dark" href="{% url 'cart' %}">&#x2190; Back to Cart</a>
				<hr>
				<h3>Order Summary</h3>
				<hr>
				{% for item in items %}
				<div class="cart-row">
					<div style="flex:2"><img class="row-image" src="{{item.product.imageURL}}"></div>
					<div style="flex:2"><p>{{item.product.name}}</p></div>
					<div style="flex:1"><p>${{item.product.price|floatformat:2}}</p></div>
					<div style="flex:1"><p>x{{item.quantity}}</p></div>
				</div>
				{% endfor %}
				<h5>Items:   {{order.get_cart_items}}</h5>
				<h5>Total:   ${{order.get_cart_total|floatformat:2}}</h5>
			</div>
		</div>
	</div>

	<script src="https://www.paypal.com/sdk/js?client-id=YOUR-CLIENT-ID&currency=USD&disable-funding=credit"></script>

	<script>
		var total = '{{order.get_cart_total}}'
        // Render the PayPal button into #paypal-button-container
        paypal.Buttons({

        	style: {
                color:  'blue',
                shape:  'rect',
            },

            // Set up the transaction
            createOrder: function(data, actions) {
                return actions.order.create({
                    purchase_units: [{
                        amount: {
                            value:parseFloat(total).toFixed(2)
                        }
                    }]
                });
            },

            // Finalize the transaction
            onApprove: function(data, actions) {
                return actions.order.capture().then(function(details) {
                    // Show a success message to the buyer
                    submitFormData()
                });
            }

        }).render('#paypal-button-container');
    </script>

	<script type="text/javascript">
		var shipping = '{{order.shipping}}'

		if (shipping == 'False'){
		 	document.getElementById('shipping-info').innerHTML = ''
		}

		if (user != 'AnonymousUser'){
		 	document.getElementById('user-info').innerHTML = ''
		 }

		if (shipping == 'False' && user != 'AnonymousUser'){
			//Hide entire form if user is logged in and shipping is false
				document.getElementById('form-wrapper').classList.add("hidden");
				//Show payment if logged in user wants to buy an item that does not require shipping
			    document.getElementById('payment-info').classList.remove("hidden");
		}

		var form = document.getElementById('form')
		form.addEventListener('submit', function(e){
	    	e.preventDefault()
	    	console.log('Form Submitted...')
	    	document.getElementById('form-button').classList.add("hidden");
	    	document.getElementById('payment-info').classList.remove("hidden");
	    })

		/*
	    document.getElementById('make-payment').addEventListener('click', function(e){
	    	submitFormData()
	    })
	    */

	    function submitFormData(){
	    	console.log('Payment button clicked')

	    	var userFormData = {
				'name':null,
				'email':null,
				'total':total,
			}

			var shippingInfo = {
				'address':null,
				'city':null,
				'state':null,
				'zipcode':null,
			}

			if (shipping != 'False'){
	    		shippingInfo.address = form.address.value
		    	shippingInfo.city = form.city.value
		    	shippingInfo.state = form.state.value
		    	shippingInfo.zipcode = form.zipcode.value
	    	}

	    	if (user == 'AnonymousUser'){
	    		userFormData.name = form.name.value
	    		userFormData.email = form.email.value
	    	}

	    	console.log('Shipping Info:', shippingInfo)
	    	console.log('User Info:', userFormData)

	    	var url = "/process_order/"
	    	fetch(url, {
	    		method:'POST',
	    		headers:{
	    			'Content-Type':'applicaiton/json',
	    			'X-CSRFToken':csrftoken,
	    		}, 
	    		body:JSON.stringify({'form':userFormData, 'shipping':shippingInfo}),
	    		
	    	})
	    	.then((response) => response.json())
	    	.then((data) => {
				console.log('Success:', data);
				alert('Transaction completed');  

				cart = {}
				document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"

				window.location.href = "{% url 'store' %}"

				})
	    }
	</script>
{% endblock content %}

we have created a admin user with password when we write /admin at the end of our main url then that redirects to the admin page where we need to enter user name and password 
user name= praneeth
password= Prani@143

after implementing all the html pages then the basic shopping page will be created and now we can parse our data and create a data set in our repository by using creating the us_data folder under store and uploading our US_Superstore_data.xlsx file 
and now create a folder called management/commands  under that create a file called data_parse.py and write the following code

import os
from pathlib import Path
from django.core.management.base import BaseCommand
from openpyxl import load_workbook
from store.models import Product

class Command(BaseCommand):
    help = 'Load data from excel'

    def handle(self, *args, **options):
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('table dropped'))
        
        base_dir = Path(__file__).resolve().parent.parent.parent.parent
        book_path = os.path.join(base_dir, 'store/us_data/US_Superstore_data.xlsx')
        book = load_workbook(book_path)
        sheet = book['Orders']
        self.stdout.write(self.style.SUCCESS(sheet.title))
        max_row_num = sheet.max_row
        max_col_num = sheet.max_column
        self.stdout.write(self.style.SUCCESS(str(max_row_num)))
        self.stdout.write(self.style.SUCCESS(str(max_col_num)))

        for i in range(2, max_row_num+1): # for each row, minus the first (headers) and last (total count)
            product_name = sheet.cell(row=i, column=16).value
            if not product_name:
                continue
            sales = sheet.cell(row=i, column=18).value

            data = Product.objects.create(
                name=product_name,
                price=sales,
            )

            data.save()
        
            if (i % 100 == 0):
                self.stdout.write(self.style.SUCCESS(f'{i} records parsed'))

        self.stdout.write(self.style.SUCCESS("successfully parsed"))
