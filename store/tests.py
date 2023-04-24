from django.test import TestCase
from django.contrib.auth.models import User
from store.models import Customer, Product, Order, Customer, OrderItem

class CustomerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test Customer',
            email='test@example.com'
        )

    def test_customer_creation(self):
        customer = Customer.objects.get(name='Test Customer')
        self.assertEqual(customer.user, self.user)
        self.assertEqual(customer.email, 'test@example.com')



class ProductModelTestCase(TestCase):
    def setUp(self):
        # Create a test product object
        self.test_product = Product.objects.create(
            name='Test Product',
            price=10.00,
            digital=True,
            image=None
        )

    def test_product_creation(self):
        # Test that the product object was created and saved to the database
        product_count = Product.objects.count()
        self.assertEqual(product_count, 1)
        self.assertEqual(self.test_product.name, 'Test Product')
        self.assertEqual(self.test_product.price, 10.00)
        self.assertTrue(self.test_product.digital)
        # self.assertIsNone(self.test_product.image)

    def test_image_url(self):      #test_image_url() method tests the imageURL
        # Test that the image URL property returns a valid URL
        self.assertEqual(self.test_product.imageURL, '')

    def tearDown(self):
        # Delete the test product from the database
        self.test_product.delete()



class OrderModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Alice", email="alice@example.com")
        self.product1 = Product.objects.create(name="Product 1", price=10.0, digital=False)
        self.product2 = Product.objects.create(name="Product 2", price=5.0, digital=True)
        self.order = Order.objects.create(customer=self.customer, transaction_id="123456")
        self.order_item1 = OrderItem.objects.create(order=self.order, product=self.product1, quantity=2)
        self.order_item2 = OrderItem.objects.create(order=self.order, product=self.product2, quantity=1)

    def test_order_fields(self):
        self.assertEqual(self.order.customer, self.customer)
        # self.assertTrue(isinstance(self.order.date_ordered, datetime))
        self.assertFalse(self.order.complete)
        self.assertEqual(self.order.transaction_id, "123456")

    def tearDowns(self):
        self.order.delete()
        self.customer.delete()






    def test_shipping_property(self):
        self.assertTrue(self.order.shipping)

    def tearDownss(self):
        self.order.delete()
        self.customer.delete()
        self.product1.delete()
        self.product2.delete()
        self.order_item1.delete()
        self.order_item2.delete()



    def test_cart_total_property(self):
        self.assertEqual(self.order.get_cart_total, 25.0)

    def tearDown(self):
        self.order.delete()
        self.customer.delete()
        self.product1.delete()
        self.product2.delete()
        self.order_item1.delete()
        self.order_item2.delete()




class OrderItemTestCase(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Product A', price=10.00)
        self.order = Order.objects.create(order_id = 123)
        self.order_item = OrderItem.objects.create(product=self.product, order=self.order, quantity=2)

    def test_order_item_creation(self):
        self.assertIsInstance(self.order_item, OrderItem)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.quantity, 2)
        self.assertIsNotNone(self.order_item.date_added)

    def test_get_total(self):
        total = self.order_item.get_total()
        self.assertEqual(total, 20.00)

    
