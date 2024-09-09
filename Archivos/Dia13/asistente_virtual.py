import pyttsx3
import speech_recognition as sr  # importante tener instalado pyAudio y Flask creo
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# opciones de voz
id1 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-MX_SABINA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0'


# escuchar microfono y devolver audio como texto
def transformar_audio():
    # Almacenar recognizer como variable
    r = sr.Recognizer()

    # Configurar micrófono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó
        print("Ya puedes hablar")

        try:
            # Guardar lo que escuche como audio, con un tiempo máximo de 10 segundos
            audio = r.listen(origen, timeout=14)

            # Buscar en Google
            pedido = r.recognize_google(audio, language="es-mx")

            # Prueba de que pudo ingresar
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido
        # En caso de no comprender audio
        except sr.UnknownValueError:
            # Prueba de que no comprendió
            print("No entendí")

            # Devolver error
            return "Sigo esperando"
        # En caso de no resolver pedido
        except sr.RequestError:
            # Prueba de que no comprendió
            print("No hay servicio")

            # Devolver error
            return "Sigo esperando"
        # Error inesperado
        except Exception as e:
            # Prueba de que no comprendió
            print(f"Algo salió mal: {e}")

            # Devolver error
            return "Sigo esperando"


# funcion para que hable el asistente
def hablar(mensaje):
    # encender el motor de pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)
    # pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


def pedir_dia():
    # crear variable
    dia = datetime.date.today()
    print(dia)

    # crear variable para dia semana
    dia_semana = dia.weekday()

    # diccionario con nombres de dias
    calendario = {0: 'Lunes',
                  1: 'Martes',
                  2: 'Miércoles',
                  3: 'Jueves',
                  4: 'Viernes',
                  5: 'Sábado',
                  6: 'Domingo'}

    # decir el dia de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


def pedir_hora():
    # crear una variable con datos de hora
    hora = datetime.datetime.now()

    hora_mensaje = (f'En este momento son las {hora.hour} horas'
                    f'con {hora.minute} minutos y {hora.second} segundos')
    # decir hora
    hablar(hora_mensaje)


def saludo_inicial():
    # crear variable con datos de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 13 > hora.hour >= 6:
        momento = 'Buen día'
    else:
        momento = 'Buenas tardes'

    # Saludo
    hablar(f'{momento}, soy Camila, tu asistente personal. Dime en qué te puedo ayudar')


# función central
def pedir_cosas():
    # activar saludo inicial
    saludo_inicial()

    # variable de corte
    comenzar = True

    # Loop central
    while comenzar:

        # activar el micro y guardar pedido en string
        pedido = transformar_audio().lower()

        if 'abre youtube' in pedido:
            hablar('Con gusto, estoy abriendo YouTube')
            webbrowser.open('https://www.youtube.com')
            continue
        elif 'abre el navegador' in pedido:
            hablar('Claro, estoy en eso')
            webbrowser.open('https://www.google.com')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido or 'qué horas son' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar('Wikipedia dice lo siguiente: ')
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que encontré')
            continue
        elif 'reproduce' in pedido:
            pedido = pedido.replace('reproduce', '')
            pywhatkit.playonyt(pedido)
            continue
        elif 'broma' in pedido or 'chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de ')[-1].strip()
            cartera = {'apple': 'AAPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion.lower()]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['currentPrice']
                hablar(f"La encontré, el precio de las acciones de {accion} es {precio_actual}")
                continue
            except KeyError:
                hablar("La acción no se encuentra en la cartera.")
                continue
            except Exception as e:
                hablar(f"Error al obtener el precio de la acción: {e}")
                continue
        elif 'adiós' in pedido:
            hablar('Sale vato')
            break


pedir_cosas()
