📋 Descripción
myCRYPTO es una aplicación web moderna desarrollada en Flask que simula inversiones en criptomonedas. Permite a los usuarios realizar operaciones de compra, venta e intercambio de las principales criptomonedas utilizando datos en tiempo real.
✨ Características Principales

💰 Compra de criptomonedas con euros (inversión inicial)
🔄 Intercambio entre criptomonedas para maximizar ganancias
💸 Venta de criptomonedas a euros (retorno de inversión)
📊 Seguimiento de movimientos con historial detallado
📈 Estado de inversión con cálculos de ganancias/pérdidas
🌐 Precios en tiempo real mediante API de CoinGecko
🎨 Diseño moderno con efectos glassmorphism y animaciones

🛠️ Tecnologías Utilizadas

Backend: Flask 3.1.1
Base de Datos: SQLite 3
API: CoinGecko API (gratuita)
Frontend: HTML5, CSS3, Jinja2
Diseño: Pico CSS + Estilos personalizados
Fuentes: Google Fonts (Inter)

📦 Instalación
Prerrequisitos

Python 3.8 o superior
pip (gestor de paquetes de Python)

Pasos de instalación

Clonar el repositorio:

bashgit clone (https://github.com/xXDiegoXx23/simulador-cryptos)
cd simulador-criptomonedas

Crear entorno virtual:

bashpython -m venv venv

Activar entorno virtual:

bash# En Windows
venv\Scripts\activate

# En Mac/Linux
source venv/bin/activate

Instalar dependencias:

bashpip install -r requirements.txt

Crear base de datos:

pythonpython
>>> import sqlite3
>>> conn = sqlite3.connect('movements.db')
>>> conn.execute('''
    CREATE TABLE movements (
        id INTEGER PRIMARY KEY,
        date TEXT,
        time TEXT,
        from_currency TEXT,
        from_quantity REAL,
        to_currency TEXT,
        to_quantity REAL
    )
''')
>>> conn.commit()
>>> conn.close()
>>> exit()

Ejecutar la aplicación:

bashpython app.py

Abrir en navegador:

http://localhost:5000
🎮 Uso de la Aplicación
🏠 Inicio (/)

Visualiza el historial completo de movimientos
Muestra fecha, hora, monedas y cantidades de cada transacción
Interfaz moderna con efectos hover y animaciones

💰 Compra (/purchase)

Formulario de transacciones con listas desplegables
Cálculo automático de conversiones usando API en tiempo real
Validaciones de saldo para evitar operaciones inválidas
Confirmación en dos pasos (calcular → aceptar)

📊 Estado (/status)

Resumen de inversión con euros invertidos totales
Valor actual de todas las criptomonedas en cartera
Cálculo de ganancias/pérdidas en tiempo real
Balances individuales por cada criptomoneda

💱 Criptomonedas Soportadas
SímboloNombreDescripciónEUREuroMoneda base para inversionesBTCBitcoinLa criptomoneda líderETHEthereumPlataforma de contratos inteligentesUSDTTetherStablecoin vinculado al dólarADACardanoBlockchain de tercera generaciónSOLSolanaBlockchain de alto rendimientoXRPRippleRed de pagos globalesDOTPolkadotBlockchain interoperableDOGEDogecoinLa criptomoneda memeSHIBShiba InuToken de la comunidad
📂 Estructura del Proyecto
simulador-criptomonedas/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── movements.db          # Base de datos SQLite
├── README.md             # Este archivo
└── templates/
    ├── layout.html       # Plantilla base
    ├── index.html        # Página de movimientos
    ├── purchase.html     # Página de compra/venta
    └── status.html       # Página de estado de inversión
🔧 Configuración Avanzada
Variables de Entorno (Opcional)
bash# Crear archivo .env
DEBUG=True
SECRET_KEY=tu_clave_secreta_aqui
DATABASE_URL=sqlite:///movements.db
Personalización de Estilos
Los estilos están definidos en cada template y en layout.html. Puedes modificar:

Colores en las variables CSS (--accent-color, --gradient-primary)
Efectos de glassmorphism (backdrop-filter: blur())
Animaciones y transiciones

🐛 Resolución de Problemas
Error de API

Problema: "Error al conectar con CoinGecko"
Solución: Verificar conexión a internet y disponibilidad de la API

Saldo Insuficiente

Problema: "Saldo insuficiente para la operación"
Solución: Verificar balance actual en la página de Estado

Base de Datos

Problema: Error al crear la tabla
Solución: Eliminar movements.db y volver a crear la tabla

🚀 Funcionalidades Futuras

 Autenticación de usuarios con sesiones
 Gráficos históricos de precios
 Alertas de precio por email/SMS
 Portfolio diversificado con múltiples carteras
 Análisis técnico con indicadores
 Modo paper trading sin dinero real
 API REST para integración externa

🤝 Contribuciones
Las contribuciones son bienvenidas. Para contribuir:

Fork el proyecto
Crea una rama para tu feature (git checkout -b feature/nueva-funcionalidad)
Commit tus cambios (git commit -m 'Agregar nueva funcionalidad')
Push a la rama (git push origin feature/nueva-funcionalidad)
Abre un Pull Request
