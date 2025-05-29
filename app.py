from flask import Flask, render_template, request, redirect, flash
import sqlite3 
import requests
from datetime import datetime


COINGECKO_IDS = {
    'BTC': 'bitcoin',
    'ETH': 'ethereum',
    'ADA': 'cardano',
    'SOL': 'solana',
    'XRP': 'ripple',
    'DOT': 'polkadot',
    'DOGE': 'dogecoin',
    'SHIB': 'shiba-inu',
    'USDT': 'tether',
    'EUR': 'eur'  # EUR se maneja como base directa
}

app = Flask(__name__)
app.secret_key = 'a8f7e9c4d213b5e69f9c2a1e4b3d7f6c9a0e1d2f3b4c5d6e'  # Necesaria para flash messages

API_KEY = 'f705fb14-d111-4d21-a7a6-757aacc4cb8a' 
CRYPTOCURRENCIES = ['EUR', 'BTC', 'ETH', 'USDT', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'SHIB']

def get_user_balance(currency):
    """Obtiene el balance actual de una moneda específica"""
    with sqlite3.connect('movements.db') as conn:
        cursor = conn.cursor()
        
        # Sumar todas las entradas de esta moneda
        cursor.execute('SELECT SUM(to_quantity) FROM movements WHERE to_currency = ?', (currency,))
        ingresos = cursor.fetchone()[0] or 0
        
        # Sumar todas las salidas de esta moneda
        cursor.execute('SELECT SUM(from_quantity) FROM movements WHERE from_currency = ?', (currency,))
        gastos = cursor.fetchone()[0] or 0
        
        return ingresos - gastos

def get_exchange_rate(from_currency, to_currency):
    """Obtiene la tasa de cambio desde CoinGecko"""
    from_id = COINGECKO_IDS.get(from_currency)
    to_id = COINGECKO_IDS.get(to_currency)

    if not from_id or not to_id:
        return None

    # Si una de las monedas es EUR, usar el endpoint simple
    if from_currency == 'EUR':
        # EUR → crypto: pedir el precio de 1 EUR en crypto (inverso)
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={to_id}&vs_currencies=eur'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                price_in_eur = response.json()[to_id]['eur']
                return 1 / price_in_eur if price_in_eur != 0 else None
        except:
            return None
    elif to_currency == 'EUR':
        # crypto → EUR: pedir el precio directamente
        url = f'https://api.coingecko.com/api/v3/simple/price?ids={from_id}&vs_currencies=eur'
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()[from_id]['eur']
        except:
            return None
    else:
        # crypto → crypto: convertir a EUR y luego a destino
        rate_from_eur = get_exchange_rate(from_currency, 'EUR')
        rate_to_eur = get_exchange_rate(to_currency, 'EUR')
        if rate_from_eur and rate_to_eur:
            return rate_from_eur / rate_to_eur
        return None

@app.route('/')
def index():
    with sqlite3.connect('movements.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM movements ORDER BY id DESC')
        rows = cursor.fetchall()
    return render_template('index.html', movements=rows)

@app.route('/purchase', methods=['GET', 'POST'])
def purchase():
    result = None
    error = None
    from_currency = None
    to_currency = None
    cantidad = None
    
    if request.method == 'POST':
        from_currency = request.form['moneda_from']
        to_currency = request.form['moneda_to']
        
        try:
            cantidad = float(request.form['cantidad'])
        except ValueError:
            error = "La cantidad debe ser un número válido"
            return render_template('purchase.html', monedas=CRYPTOCURRENCIES, result=result, error=error, 
                                 from_currency=from_currency, to_currency=to_currency)

        if from_currency == to_currency:
            error = "Las monedas deben ser distintas"
        elif cantidad <= 0:
            error = "La cantidad debe ser mayor que 0"
        else:
            # Verificar si el usuario tiene suficiente balance (excepto para EUR que es infinito según el proyecto)
            if from_currency != 'EUR':
                balance = get_user_balance(from_currency)
                if balance < cantidad:
                    error = f"Saldo insuficiente. Tienes {balance:.8f} {from_currency}"
                    return render_template('purchase.html', monedas=CRYPTOCURRENCIES, result=result, error=error,
                                         from_currency=from_currency, to_currency=to_currency, cantidad=cantidad)
            
            # Obtener tasa de cambio
            rate = get_exchange_rate(from_currency, to_currency)
            
            if rate:
                resultado = cantidad * rate
                result = round(resultado, 8)

                # Si se aceptó la operación
                if 'aceptar' in request.form:
                    now = datetime.now()
                    fecha = now.strftime("%Y-%m-%d")
                    hora = now.strftime("%H:%M:%S.%f")[:-3]  # Incluir milisegundos
                    
                    with sqlite3.connect('movements.db') as conn:
                        conn.execute('''
                            INSERT INTO movements (date, time, from_currency, from_quantity, to_currency, to_quantity)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (fecha, hora, from_currency, cantidad, to_currency, result))
                    
                    flash(f'Operación realizada: {cantidad} {from_currency} → {result} {to_currency}', 'success')
                    return redirect('/')
            else:
                error = "Error al conectar con CoinGecko o tasa no disponible"

    return render_template('purchase.html', monedas=CRYPTOCURRENCIES, result=result, error=error,
                         from_currency=from_currency, to_currency=to_currency, cantidad=cantidad)

@app.route('/status')
def status():
    # Calcular euros invertidos totales
    with sqlite3.connect('movements.db') as conn:
        cursor = conn.cursor()
        
        # Total de euros gastados (invertidos)
        cursor.execute('SELECT SUM(from_quantity) FROM movements WHERE from_currency = ?', ('EUR',))
        euros_invertidos = cursor.fetchone()[0] or 0
        
        # Euros recuperados (vendidos)
        cursor.execute('SELECT SUM(to_quantity) FROM movements WHERE to_currency = ?', ('EUR',))
        euros_recuperados = cursor.fetchone()[0] or 0
        
        # Saldo de euros invertidos (atrapados en cryptos)
        saldo_euros_invertidos = euros_invertidos - euros_recuperados
    
    # Calcular valor actual de todas las cryptos
    valor_actual_cryptos = 0
    balances = {}
    
    for crypto in CRYPTOCURRENCIES:
        if crypto != 'EUR':
            balance = get_user_balance(crypto)
            if balance > 0:
                balances[crypto] = balance
                # Convertir a euros
                rate = get_exchange_rate(crypto, 'EUR')
                if rate:
                    valor_actual_cryptos += balance * rate
    
    # Valor total actual
    valor_actual_total = euros_recuperados + valor_actual_cryptos
    
    # Ganancia/Pérdida
    ganancia_perdida = valor_actual_total - euros_invertidos
    
    return render_template('status.html', 
                         euros_invertidos=euros_invertidos,
                         valor_actual_total=valor_actual_total,
                         ganancia_perdida=ganancia_perdida,
                         balances=balances,
                         saldo_euros_invertidos=saldo_euros_invertidos)

if __name__ == '__main__':
    app.run(debug=True)