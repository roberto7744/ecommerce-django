🛒 RobStore — E-commerce Fullstack (Django + REST API + Frontend HTML/CSS)

RobStore es un proyecto completo de eCommerce, desarrollado utilizando Django + Django REST Framework, con un frontend integrado en HTML/CSS/JS y desplegado en Railway. Incluye autenticación JWT, CRUD de productos, carrito persistente y flujo de compra real.

📌 Características principales

✔ Backend completo con Django
✔ API REST con JWT
✔ Frontend moderno integrado en /templates/index.html
✔ Registro e inicio de sesión
✔ Carrito persistente por usuario
✔ Checkout con validación de stock
✔ CRUD de productos desde /admin/
✔ Documentación Swagger integrada
✔ Google Analytics activo
✔ Deploy 100% funcional en Railway

🌐 Demo en producción

🔗 Frontend + Backend:
👉 https://ecommerce-django-production-39cb.up.railway.app/

🔗 Documentación Swagger:
👉 https://ecommerce-django-production-39cb.up.railway.app/swagger/

🧩 Tecnologías Utilizadas
Backend

Django 6.0

Django REST Framework

SimpleJWT

WhiteNoise

CORS Headers

SQLite

Frontend

HTML

CSS moderno

JavaScript (Fetch API)

Deploy

Railway

Google Analytics integrado

🏗️ Arquitectura
ecommerce-django/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── views.py ← Renderiza index.html
│
├── store/
│   ├── models.py       ← Product, Order, Cart, CartItem
│   ├── views.py        ← Lógica REST
│   ├── serializers.py
│   ├── urls.py
│
├── templates/
│   ├── index.html      ← Frontend de la tienda
│
└── staticfiles/        ← Archivos generados para deploy

🔥 Endpoints principales
🔐 Autenticación
Método	Endpoint	Descripción
POST	/api/auth/register/	Crear usuario
POST	/api/auth/login/	Obtener token JWT
📦 Productos
Método	Endpoint	Descripción
GET	/api/products/	Listar productos
POST	/api/products/	Crear producto (admin)
🛒 Carrito
Método	Endpoint	Descripción
GET	/api/cart/	Ver carrito
POST	/api/cart/add/	Agregar producto
POST	/api/cart/remove/	Quitar producto
POST	/api/cart/clear/	Vaciar carrito
POST	/api/cart/checkout/	Finalizar compra
🧾 Pedidos
Método	Endpoint	Descripción
GET	/api/orders/	Ver pedidos del usuario
POST	/api/orders/	Crear pedido manual
🖥️ Frontend integrado

El archivo:

/templates/index.html


Incluye:

Catálogo dinámico de productos

Panel moderno de login y registro

Carrito deslizable en el costado

Botón “Agregar al carrito” para cada producto

Checkout funcional

Google Analytics configurado

Diseño responsive

📈 Google Analytics

El proyecto incluye en index.html:

<script async src="https://www.googletagmanager.com/gtag/js?id=G-B4SK4KQDHW"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-B4SK4KQDHW');
</script>


Listo para medir:

Visitas

Eventos personalizados

Flujo de compra

📸 Capturas de pantalla

Agrega tus capturas en /screenshots/ y enlázalas así:

![Home](screenshots/home.png)
![Carrito](screenshots/cart.png)
![Admin](screenshots/admin.png)

⚙️ Instalación local
1️⃣ Clonar repositorio
git clone https://github.com/roberto7744/ecommerce-django.git
cd ecommerce-django

2️⃣ Crear entorno virtual
python -m venv venv


Activar:

Windows → venv\Scripts\activate

Linux/Mac → source venv/bin/activate

3️⃣ Instalar dependencias
pip install -r requirements.txt

4️⃣ Migraciones
python manage.py migrate

5️⃣ Crear superusuario
python manage.py createsuperuser

6️⃣ Ejecutar servidor
python manage.py runserver

🚀 Deploy en Railway

El proyecto ya está preparado:

✔ WhiteNoise configurado
✔ ALLOWED_HOSTS correcto
✔ CSRF_TRUSTED_ORIGINS configurado
✔ DEBUG manejado por variables de entorno
✔ SQLite persistente

Para actualizar desde tu PC:

git add .
git commit -m "Actualización final del proyecto"
git push

Railway actualizará automáticamente.
