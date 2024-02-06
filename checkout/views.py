from django.views.generic import TemplateView
from checkout.models import Order, OrderItem, Address
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse
from django.views.generic import View
from django.contrib import messages
from main.models import Product


class CartView(TemplateView):
    template_name = 'cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.request.session.get('cart', {})
        cart_items = []
        total_price = 0

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            total_item_price = product.price * quantity
            total_price += total_item_price
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total_item_price': total_item_price,
            })

        context['cart_items'] = cart_items
        context['total_price'] = total_price
        return context


class AddToCartView(View):
    def post(self, request, *args, **kwargs):
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        cart = request.session.get('cart', {})

        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1

        request.session['cart'] = cart
        return redirect('cart')


class UpdateCartView(View):
    def post(self, request, product_id):
        submitted_quantity = request.POST.get('quantity', '').strip()
        cart = request.session.get('cart', {})

        current_quantity = cart.get(str(product_id), 1)

        if submitted_quantity.isdigit() and int(submitted_quantity) > 0:
            new_quantity = int(submitted_quantity)
            product = get_object_or_404(Product, id=product_id)
            if new_quantity > product.stock:
                new_quantity = current_quantity
        else:
            new_quantity = current_quantity

        cart[str(product_id)] = new_quantity
        request.session['cart'] = cart
        request.session.modified = True

        return redirect(reverse('cart'))


class RemoveFromCartView(View):
    def get(self, request, product_id):
        cart = request.session.get('cart', {})

        if str(product_id) in cart:
            del cart[str(product_id)]

        request.session['cart'] = cart
        return redirect(reverse('cart'))  # Adjust 'cart' to your cart view's URL name


class CheckoutView(View):
    def get(self, request):
        # Calculate total price from session cart
        cart = request.session.get('cart', {})
        total_price = 0
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            total_price += product.price * quantity

        # Pass total price to template
        context = {
            'total_price': total_price,
        }
        return render(request, 'checkout.html', context)

    def post(self, request):
        # Extract form data
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone_number = request.POST.get('number')
        street = request.POST.get('street_name')
        street_number = request.POST.get('street_number')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        payment_method = request.POST.get('payment_method')

        try:
            # First, create an Address instance
            address = Address.objects.create(
                street=street,
                street_number=street_number,
                city=city,
                postal_code=postal_code,
                country=country
            )

            # Then create an Order instance
            order = Order.objects.create(
                user=request.user,  # Assuming the user is logged in
                address=address,
                payment_method=payment_method,
                name=name,
                surname=surname,
                email=email,
                phone_number=phone_number,
                paid=False,  # Default value, adjust as necessary
                status=Order.CART  # Default status, adjust as necessary
            )

            # Process cart items from session
            cart = request.session.get('cart', {})
            for product_id, quantity in cart.items():
                product = Product.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity
                )

            # Clear the cart from session after processing
            request.session['cart'] = {}

            messages.success(request, "Your order has been placed successfully!")
            return redirect(reverse('order-confirmation', kwargs={'order_id': order.id}))

        except Exception as e:
            messages.error(request, f"There was an error processing your order: {str(e)}")
            return redirect('checkout')


class OrderConfirmationView(View):
    def get(self, request, order_id):
        # Retrieve the order using the order_id
        order = get_object_or_404(Order, id=order_id)
        # Add any additional context you want to pass to the template
        context = {
            'order': order,
        }
        return render(request, 'order-confirmation.html', context)
