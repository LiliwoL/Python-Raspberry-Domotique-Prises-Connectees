# Prises connectées via un Raspberry

# Import -------------------------
# FLASK
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# GPIO
# On essaie RPi.GPIO si on est sur un Raspberry, sinon Mock
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
# Time
import time
# #Import -------------------------


# Definitions correspondence GPIO / Prises
PRISE_1=18
PRISE_2=17
PRISE_3=18
PRISE_4=18

# Intitialisation du GPIO
def initGPIO():

    print("    * Initialisation du GPIO")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup PINS
    GPIO.setup(PRISE_1, GPIO.OUT)
    GPIO.output(PRISE_1, GPIO.LOW)

    print("         * Prise 1 -- OK")

    time.sleep(1)

    GPIO.setup(PRISE_2, GPIO.OUT)
    GPIO.output(PRISE_2, GPIO.LOW)

    print("         * Prise 2 -- OK")

    time.sleep(1)

    GPIO.setup(PRISE_3, GPIO.OUT)
    GPIO.output(PRISE_3, GPIO.LOW)

    print("         * Prise 3 -- OK")

    time.sleep(1)

    GPIO.setup(PRISE_4, GPIO.OUT)
    GPIO.output(PRISE_4, GPIO.LOW)

    print("         * Prise 4 -- OK")


# Méthode d'accès au GPIO
def switchGPIO( prise ):

    print("         * Prise ", prise)

    # 1. Récupération de l'état actuel et Changement
    GPIO.output( prise, not GPIO.input(prise) )

    # 2. Renvoi du nouvel état
    print("             * Etat ", GPIO.input(prise) )
    return GPIO.input(prise)



# Méthode pour lire l'etat de la prise
def getGPIOState( prise ):
    return GPIO.input(prise)




# Définition des routes
# ----------------------

# ----------------------
# API
# ----------------------
@app.route(
    '/api/',
    methods=['GET']
)
def api_index():

    # On est sur la page de base

    # 1. Initialisation
    initGPIO()
    return jsonify(
        [
            {
                'Prise': 1,
                'state': getGPIOState(1)
            },
            {
                'Prise': 2,
                'state': getGPIOState(2)
            },
            {
                'Prise': 3,
                'state': getGPIOState(3)
            },
            {
                'Prise': 4,
                'state': getGPIOState(4)
            }
        ]
    )


# Switch POST
# ----------------------
@app.route(
    "/api/switch/<prise>",
    methods=['POST']
)
def api_switch_post(prise):

    return jsonify(
        {
            'Prise': prise,
            'state': switchGPIO(prise)
        }
    )

@app.route(
    "/api/switch/<prise:num>",
    methods=['GET']
)
def api_switch_get(prise):

    return jsonify(
        {
            'Prise': prise,
            'state': getGPIOState(prise)
        }
    )


# ----------------------
# Web
# ----------------------

@app.route(
    '/',
    methods=['GET']
)
def web_index():

    # On est sur la page de base

    # 1. Initialisation
    initGPIO()
    return render_template("index.html")

# Switch GET
# To  switch
# ----------------------
@app.route(
    "/switch/<prise:num>",
    methods=['GET']
)
def web_switch(prise):
    switchGPIO(prise)

    return render_template("switch.html", prise=prise)




if __name__ == '__main__':
    app.run(
        use_reloader=True,
        debug=True,
        host="0.0.0.0",
        port=105
    )
