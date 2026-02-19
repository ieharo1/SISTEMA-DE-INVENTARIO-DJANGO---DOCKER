#  TST SOLUTIONS - Sistema de Inventarios By TST Solutions

**Sistema de Inventarios By TST Solutions** es una plataforma web de gestion de inventarios desarrollada por **TST Solutions** ("Te Solucionamos Todo").

---

##  ¿Que es Sistema de Inventarios By TST Solutions?

**Sistema de Inventarios By TST Solutions** es una aplicacion empresarial que permite administrar productos, bodegas, proveedores, movimientos de inventario, auditoria y reportes operativos en tiempo real.

> *"Tecnologia que funciona. Soluciones que escalan."*

---

## ✨ Caracteristicas Principales

### ️ Gestion de Inventario
- CRUD de productos y categorias
- CRUD de bodegas
- CRUD de proveedores
- Control de stock por producto/bodega

###  Movimientos y Kardex
- Registro de entradas, salidas, transferencias y ajustes
- Trazabilidad por usuario y fecha
- Kardex por producto

###  Reportes y Auditoria
- Reportes en PDF y Excel
- Bitacora de auditoria por acciones
- Dashboard con metricas principales

### ⚙️ Infraestructura Docker
- Django + Gunicorn
- PostgreSQL
- Nginx como reverse proxy
- Despliegue con Docker Compose

---

## ️ Estructura Tecnica del Proyecto

```
apps/
├── users/
├── products/
├── suppliers/
├── warehouses/
├── inventory/
├── movements/
├── audit/
└── reports/

inventory/
├── settings/
│   ├── __init__.py
│   ├── base.py
│   ├── development.py
│   └── production.py
├── urls.py
└── wsgi.py

templates/
nginx/
Dockerfile
docker-compose.yml
entrypoint.sh
```

---

## ️ Tecnologias Utilizadas

- **Backend:** Django 5.0.6
- **Lenguaje:** Python 3.12+
- **Base de datos:** PostgreSQL 15
- **Servidor WSGI:** Gunicorn
- **Proxy:** Nginx
- **Contenedores:** Docker / Docker Compose

---

##  Identidad Visual

### Nombre Comercial
- **Sistema de Inventarios By TST Solutions**

### Marca
- **TST Solutions**
- **Slogan:** Technology that works. Solutions that scale.

---

##  Caracteristicas Tecnicas

✅ Arquitectura modular por apps Django  
✅ CRUD completo en modulos principales  
✅ Control de acceso por permisos  
✅ Auditoria de operaciones  
✅ Reportes operativos  
✅ Despliegue reproducible con Docker  

---

##  Informacion de Contacto - TST Solutions

 **Quito - Ecuador**

 **WhatsApp:** +593 99 796 2747  
 **Telegram:** @TST_Ecuador  
 **Email:** negocios@tstsolutions.com.ec

 **Web:** https://tst-solutions.netlify.app/  
 **Facebook:** https://www.facebook.com/tstsolutionsecuador/  
 **Twitter/X:** https://x.com/SolutionsT95698

---

##  Requisitos del Sistema

- Docker Desktop / Docker Engine 24+
- Docker Compose v2+
- (Opcional) Python 3.12+

---

##  Ejecucion

```bash
docker compose up -d --build
```

- URL principal: `http://localhost` (puerto 80)
- Alternativa directa: `http://localhost:8000`

Credenciales iniciales (si no existen):
- Usuario: `admin`
- Clave: `admin123`

---

##  Licencia

© 2026 Sistema de Inventarios By TST Solutions - Todos los derechos reservados.

---

## ‍ Desarrollado por TST SOLUTIONS

*Technology that works. Solutions that scale.*

---

<div align="center">
  <p><strong>TST Solutions</strong> - Te Solucionamos Todo</p>
</div>
