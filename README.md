# PeopleCart - Modern E-Commerce Bookstore

A full-featured Django e-commerce web application for selling books online. Features a modern black-themed UI, complete shopping cart functionality, PayPal payment integration, and a responsive Bootstrap-based design.

![Django](https://img.shields.io/badge/Django-4.2.4-092E20?style=flat&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.2.3-7952B3?style=flat&logo=bootstrap&logoColor=white)

## 🚀 Features

### Core Functionality
- **Product Catalog**: Browse books by category with beautiful product cards
- **Product Search**: Advanced search functionality with real-time results
- **Product Details**: Detailed product pages with images, descriptions, and pricing
- **Shopping Cart**: Full cart functionality with quantity management
- **Checkout System**: Complete checkout flow with PayPal integration
- **User Authentication**: Registration, login, and profile management
- **Order Management**: Automatic order creation on successful payment

### User Experience
- **Modern Black Theme**: Sleek, professional black color scheme
- **Responsive Design**: Mobile-friendly layout that works on all devices
- **Smooth Animations**: Hover effects and transitions throughout
- **Professional UI**: Clean, modern interface with excellent UX
- **Category Navigation**: Dynamic category dropdown in navbar
- **User Profiles**: Complete profile management with shipping address

### Payment Integration
- **PayPal Sandbox**: Integrated PayPal payment processing
- **Order Tracking**: Automatic order creation via PayPal IPN
- **Payment Notifications**: Real-time payment status updates

## 📋 Tech Stack

- **Backend**: Django 4.2.4
- **Frontend**: Bootstrap 5.2.3, Custom CSS, JavaScript
- **Database**: SQLite (development), PostgreSQL ready
- **Payment**: django-paypal 2.1
- **Image Processing**: Pillow 10.0.0
- **Static Files**: WhiteNoise 6.6.0

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
git clone https://github.com/malikashirali25/peoplecart.git
cd peoplecart
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run Migrations
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Create Sample Data (Optional)
```bash
python create_sample_data.py
```

This will create sample categories and products for testing.

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## ⚙️ Configuration

### PayPal Setup
1. Update `PAYPAL_RECEIVER_EMAIL` in `ecom/settings.py` with your PayPal sandbox business account email
2. Ensure `PAYPAL_TEST = True` for sandbox testing
3. For production, set `PAYPAL_TEST = False` and use live credentials

### Environment Variables (Optional)
Create a `.env` file in the project root:
```
SECRET_KEY=your-secret-key-here
DEBUG=True
PAYPAL_RECEIVER_EMAIL=your-paypal-email@example.com
```

## 📁 Project Structure

```
peoplecart/
├── ecom/                  # Main Django project settings
│   ├── settings.py        # Project configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI configuration
├── store/                 # Main application
│   ├── models.py         # Database models (Product, Category, Order, etc.)
│   ├── views.py          # View functions
│   ├── urls.py           # App URL routing
│   ├── forms.py          # Django forms
│   ├── admin.py          # Admin panel configuration
│   ├── signals.py        # PayPal IPN signal handlers
│   └── templates/        # HTML templates
│       ├── base.html     # Base template
│       ├── home.html     # Home page
│       ├── cart.html     # Shopping cart
│       ├── checkout.html # Checkout page
│       └── ...
├── static/               # Static files (CSS, JS, images)
│   ├── css/
│   │   └── styles.css    # Main stylesheet
│   └── js/
│       └── scripts.js   # JavaScript functionality
├── media/                # User-uploaded files (product images)
├── requirements.txt      # Python dependencies
└── manage.py             # Django management script
```

## 🎨 Key Features Explained

### Shopping Cart
- Add products to cart with quantity selection
- View cart with product details and totals
- Update quantities and remove items
- Persistent cart using localStorage
- Real-time cart badge updates

### Checkout Process
1. Review cart items and totals
2. Verify shipping address
3. Complete payment via PayPal
4. Automatic order creation on payment success
5. Order confirmation page

### User Management
- User registration with email validation
- Login/logout functionality
- Profile management (username, email, name)
- Shipping address management
- Password change functionality

### Product Management
- Product listing with images
- Category-based browsing
- Search functionality
- Product detail pages
- Sale price support

## 🔧 Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Admin Panel
1. Create a superuser: `python manage.py createsuperuser`
2. Visit: `http://127.0.0.1:8000/admin/`
3. Login with your superuser credentials

### Updating Placeholder Images
If you need to regenerate placeholder images:
```bash
python update_placeholders.py
```

## 📦 Dependencies

See `requirements.txt` for the complete list. Key dependencies:
- Django 4.2.4
- django-paypal 2.1
- Pillow 10.0.0
- WhiteNoise 6.6.0
- Bootstrap 5.2.3 (via CDN)

## 🌐 Deployment

### Production Checklist
- [ ] Set `DEBUG = False` in settings.py
- [ ] Update `SECRET_KEY` with a secure key
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static file serving
- [ ] Set up SSL/HTTPS
- [ ] Update PayPal credentials for production
- [ ] Set up proper media file storage
- [ ] Configure email settings

### Recommended Hosting
- Heroku
- AWS
- DigitalOcean
- PythonAnywhere

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Malik Ashir Ali**
- GitHub: [@malikashirali25](https://github.com/malikashirali25)

## 🙏 Acknowledgments

- Django community for excellent documentation
- PayPal for payment integration
- Bootstrap for responsive UI components
- All contributors and users of this project

## 📞 Support

For support, email iammalikashirali@gmail.com or open an issue in the repository.

---

**Note**: This is a development project. Make sure to configure production settings before deploying to a live server.
