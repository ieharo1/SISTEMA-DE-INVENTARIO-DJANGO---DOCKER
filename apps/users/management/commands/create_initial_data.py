from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.inventory.models import Inventory
from apps.movements.models import Movement
from apps.movements.services import MovementService
from apps.products.models import Category, Product
from apps.suppliers.models import Supplier
from apps.users.models import Company, User
from apps.warehouses.models import Warehouse


class Command(BaseCommand):
    help = "Crea datos iniciales para el sistema"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Creando datos iniciales...")
        self.create_groups_and_permissions()
        company = self.create_default_company()
        admin_user = self.create_superuser(company)
        self.create_sample_users(company)
        self.create_sample_data(company, admin_user)
        self.stdout.write(self.style.SUCCESS("Datos iniciales creados exitosamente!"))

    def create_groups_and_permissions(self):
        groups_permissions = {
            "Admin": ["add", "change", "delete", "view"],
            "Supervisor": ["add", "change", "view"],
            "Operador": ["view"],
        }

        models = [
            "user",
            "company",
            "product",
            "category",
            "warehouse",
            "supplier",
            "inventory",
            "movement",
            "kardex",
            "auditlog",
        ]

        for group_name, actions in groups_permissions.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"  Grupo creado: {group_name}")

            for model_name in models:
                for action in actions:
                    try:
                        perm = Permission.objects.get(codename=f"{action}_{model_name}")
                        group.permissions.add(perm)
                    except Permission.DoesNotExist:
                        continue

    def create_default_company(self):
        company, created = Company.objects.get_or_create(
            rut="76.123.456-7",
            defaults={
                "name": "TST Demo Company",
                "address": "Av. Principal 123",
                "phone": "+593997962747",
                "email": "negocios@tstsolutions.com.ec",
            },
        )
        if created:
            self.stdout.write(f"  Compania creada: {company.name}")
        return company

    def create_superuser(self, company):
        user = User.objects.filter(username="admin").first()
        if not user:
            user = User.objects.create_superuser(
                username="admin",
                email="admin@tstsolutions.com.ec",
                password="admin123",
                first_name="Admin",
                last_name="TST",
                company=company,
            )
            self.stdout.write("  Superusuario creado: admin / admin123")

        admin_group = Group.objects.get(name="Admin")
        user.groups.add(admin_group)
        user.company = company
        user.is_staff = True
        user.is_superuser = True
        user.save(update_fields=["company", "is_staff", "is_superuser"])
        return user

    def create_sample_users(self, company):
        users = [
            ("supervisor", "Supervisor", "TST", "Supervisor"),
            ("operador", "Operador", "TST", "Operador"),
        ]
        for username, first_name, last_name, role in users:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    "email": f"{username}@tstsolutions.com.ec",
                    "first_name": first_name,
                    "last_name": last_name,
                    "company": company,
                    "is_active": True,
                },
            )
            if created:
                user.set_password("admin123")
                user.save()
                self.stdout.write(f"  Usuario creado: {username} / admin123")

            group = Group.objects.get(name=role)
            user.groups.clear()
            user.groups.add(group)
            user.company = company
            user.save(update_fields=["company"])

    def create_sample_data(self, company, admin_user):
        categories = [
            {"name": "Electronica", "description": "Productos electronicos"},
            {"name": "Computacion", "description": "Computadores y accesorios", "parent": "Electronica"},
            {"name": "Audio", "description": "Equipos de audio", "parent": "Electronica"},
            {"name": "Oficina", "description": "Articulos de oficina"},
            {"name": "Muebles", "description": "Muebles de oficina", "parent": "Oficina"},
        ]

        cat_objects = {}
        for item in categories:
            parent = cat_objects.get(item.get("parent"))
            category, created = Category.objects.get_or_create(
                company=company,
                name=item["name"],
                defaults={"description": item["description"], "parent": parent},
            )
            cat_objects[item["name"]] = category
            if created:
                self.stdout.write(f"    Categoria creada: {category.name}")

        warehouses = [
            {"name": "Bodega Central", "code": "B001", "location": "Quito Norte", "is_active": True},
            {"name": "Bodega Sur", "code": "B002", "location": "Quito Sur", "is_active": True},
            {"name": "Bodega Externa", "code": "B003", "location": "Sangolqui", "is_active": True},
        ]

        wh_objects = {}
        for item in warehouses:
            warehouse, created = Warehouse.objects.get_or_create(
                company=company,
                code=item["code"],
                defaults={
                    "name": item["name"],
                    "location": item["location"],
                    "is_active": item["is_active"],
                    "description": f"Bodega {item['name']}",
                },
            )
            wh_objects[item["code"]] = warehouse
            if created:
                self.stdout.write(f"    Bodega creada: {warehouse.name}")

        suppliers = [
            {
                "name": "TST Tech Import",
                "identification": "1799990001001",
                "phone": "+593987654321",
                "email": "ventas@tstsolutions.com.ec",
                "address": "Av. Amazonas y Naciones Unidas",
            },
            {
                "name": "Distribuciones Office Pro",
                "identification": "1799990002001",
                "phone": "+593976543210",
                "email": "compras@officepro.ec",
                "address": "Av. Republica del Salvador",
            },
        ]

        for item in suppliers:
            _, created = Supplier.objects.get_or_create(
                company=company,
                identification=item["identification"],
                defaults={
                    "name": item["name"],
                    "phone": item["phone"],
                    "email": item["email"],
                    "address": item["address"],
                    "city": "Quito",
                    "country": "Ecuador",
                    "contact_name": "Equipo comercial",
                },
            )
            if created:
                self.stdout.write(f"    Proveedor creado: {item['name']}")

        products = [
            {
                "name": "Notebook Pro 14",
                "description": "Notebook empresarial 16GB RAM",
                "category": cat_objects.get("Computacion"),
                "cost_price": 850.00,
                "sale_price": 999.00,
                "sku": "NB001",
            },
            {
                "name": "Monitor 24 FHD",
                "description": "Monitor IPS para oficina",
                "category": cat_objects.get("Computacion"),
                "cost_price": 120.00,
                "sale_price": 169.00,
                "sku": "MN001",
            },
            {
                "name": "Parlantes Bluetooth",
                "description": "Parlantes inalambricos 20W",
                "category": cat_objects.get("Audio"),
                "cost_price": 35.00,
                "sale_price": 49.00,
                "sku": "AU001",
            },
            {
                "name": "Silla Ejecutiva",
                "description": "Silla ergonomica premium",
                "category": cat_objects.get("Muebles"),
                "cost_price": 110.00,
                "sale_price": 149.00,
                "sku": "MB001",
            },
        ]

        prod_objects = {}
        for item in products:
            product, created = Product.objects.get_or_create(
                company=company,
                sku=item["sku"],
                defaults={
                    "name": item["name"],
                    "description": item["description"],
                    "category": item["category"],
                    "cost_price": item["cost_price"],
                    "sale_price": item["sale_price"],
                    "is_active": True,
                },
            )
            prod_objects[item["sku"]] = product
            if created:
                self.stdout.write(f"    Producto creado: {product.name}")

        inventory_seed = [
            ("NB001", "B001", 14, 5, 30),
            ("MN001", "B001", 20, 8, 40),
            ("AU001", "B002", 35, 10, 60),
            ("MB001", "B003", 12, 4, 20),
        ]

        for sku, wh_code, qty, min_stock, max_stock in inventory_seed:
            product = prod_objects[sku]
            warehouse = wh_objects[wh_code]
            inv, _ = Inventory.objects.get_or_create(
                company=company,
                product=product,
                warehouse=warehouse,
                defaults={"quantity": qty, "min_stock": min_stock, "max_stock": max_stock},
            )
            inv.quantity = qty
            inv.min_stock = min_stock
            inv.max_stock = max_stock
            inv.save(update_fields=["quantity", "min_stock", "max_stock", "updated_at"])

        operations = [
            (
                "SEED-IN-001",
                lambda: MovementService.create_entry(
                    prod_objects["NB001"],
                    wh_objects["B001"],
                    6,
                    prod_objects["NB001"].cost_price,
                    admin_user,
                    "SEED-IN-001",
                    "Reposicion inicial",
                ),
            ),
            (
                "SEED-OUT-001",
                lambda: MovementService.create_output(
                    prod_objects["MN001"],
                    wh_objects["B001"],
                    3,
                    prod_objects["MN001"].cost_price,
                    admin_user,
                    "SEED-OUT-001",
                    "Salida por venta mostrador",
                ),
            ),
            (
                "SEED-TR-001",
                lambda: MovementService.create_transfer(
                    prod_objects["AU001"],
                    wh_objects["B002"],
                    wh_objects["B001"],
                    5,
                    admin_user,
                    "SEED-TR-001",
                    "Redistribucion interna",
                ),
            ),
        ]

        for reference, operation in operations:
            if Movement.objects.filter(company=company, reference=reference).exists():
                continue
            try:
                operation()
            except Exception as exc:
                self.stdout.write(self.style.WARNING(f"  No se pudo crear movimiento {reference}: {exc}"))
