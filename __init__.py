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
prises = { 1: 15, 2: 6, 3: 13, 4: 19}

# Intitialisation du GPIO
def initGPIO():

    print("    * Initialisation du GPIO")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Setup PINS
    for prise in prises:
        GPIO.setup(prises[prise], GPIO.OUT)
        GPIO.output(prises[prise], GPIO.LOW)

        print("         * Prise ", prises[prise], " -- OK : ", GPIO.input(prises[prise]))

        time.sleep(1)


# Méthode d'accès au GPIO
def switchGPIO(prise: int):

    old_state = getGPIOState(prises[prise])
    if old_state == "on" or old_state == 1:
        new_state = GPIO.LOW
    else:
        new_state = GPIO.HIGH

    print("Old ", old_state, " New ", new_state)

    # 1. Récupération de l'état actuel et Changement
    GPIO.output(prises[prise], new_state)

    # 2. Renvoi du nouvel état
    print("             * Etat ", new_state)
    return new_state


# Méthode pour lire l'etat de la prise
def getGPIOState(prise_bcm: int):

    state = GPIO.input(prise_bcm)
    if state:
        state_text = GPIO.HIGH
    else:
        state_text = GPIO.LOW

    print( "Etat de la prise ", prise_bcm, " : ", state_text)
    return state_text


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
                'state': getGPIOState(prises[1])
            },
            {
                'Prise': 2,
                'state': getGPIOState(prises[2])
            },
            {
                'Prise': 3,
                'state': getGPIOState(prises[3])
            },
            {
                'Prise': 4,
                'state': getGPIOState(prises[4])
            }
        ]
    )


# Switch POST
# ----------------------
@app.route(
    "/api/switch/<int:prise>",
    methods=['POST']
)
def api_switch_post(prise: int):

    switched_state = switchGPIO(prise)

    return jsonify(
        {
            'Prise': prise,
            'state': switched_state
        }
    )

@app.route(
    "/api/switch/<int:prise>",
    methods=['GET']
)
def api_switch_get(prise: int):

    return jsonify(
        {
            'Prise': prise,
            'state': getGPIOState(prises[prise])
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
    "/switch/<int:prise>",
    methods=['GET']
)
def web_switch(prise: int):
    state = switchGPIO(prises[prise])

    return render_template("switch.html", prise=prise, state=state)




if __name__ == '__main__':
    app.run(
        use_reloader=True,
        debug=True,
        host='0.0.0.0',
        port=5000
    )
