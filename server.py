# Prises connectées via un Raspberry

# Import -------------------------
# FLASK
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)        # Active CORS pour toutes les routes

# GPIO
# On essaie RPi.GPIO si on est sur un Raspberry, sinon Mock
try:
    import RPi.GPIO as GPIO
except:
    import Mock.GPIO as GPIO
    # from Mock.GPIO import GPIO
# Time
import time

# #Import -------------------------

# Definitions correspondence GPIO / Prises
tab_prises_bcm = {
    "1": 21,  # Prise 1 -- GPIO 21 - Pin 40
    "2": 20,  # Prise 2 -- GPIO 20 - Pin 38
    "3": 26,  # Prise 3 -- GPIO 26 - Pin 37
    "4": 19  # Prise 4 -- GPIO 19 - Pin 35
}


def get_bcm(prise: int):
    bcm = ""

    # Récupération de la broche PCM correspondant à cette prise
    if str(prise) in tab_prises_bcm:
        bcm: str = tab_prises_bcm[str(prise)]
    else:
        print("Aucune BCM correspondante")
        # Quit the program
        quit()

    return bcm


# Check API Key validity
def is_valid(api_key):
    if api_key == "raspB3rr1":
        return True
    else:
        return False


# Initialisation du GPIO
def initGPIO():
    print("    * Initialisation du GPIO")

    # Initialisation du GPIO
    GPIO.setmode(GPIO.BCM)  # Utilisation du GPIO en mode BCM
    GPIO.setwarnings(False)

    # Setup des GPIO utilisés
    for prise in tab_prises_bcm:
        # On définit ce GPIO en Output (on lui enverra des données)
        GPIO.setup(tab_prises_bcm[prise], GPIO.OUT)
        # Par défaut, ce GPIO sera à 0
        GPIO.output(tab_prises_bcm[prise], GPIO.LOW)

        print("         * Prise ", tab_prises_bcm[prise], " -- OK : ", getGPIOState(tab_prises_bcm[prise]))

        time.sleep(1)


# Méthode d'accès au GPIO
def switchGPIO(prise: int):
    print("----------------------------")
    print("Switch de la prise " + str(prise))  # str(prise) pour caster un int en string

    # Récupération de la broche PCM correspondant à cette prise
    bcm = get_bcm(prise)

    print("Prise ", prise, " correspond au BCM ", bcm)

    # Lecture de l'état actuel
    current_state: int = getGPIOState(bcm)

    print("----------------------------")
    print("Etat actuel de la prise ", prise, " --> ", current_state)

    if current_state == "on" or current_state == 1:
        print(" On passe de 1 à 0")
        new_state = GPIO.LOW
    else:
        print(" On passe de 0 à 1")
        new_state = GPIO.HIGH

    print("Old ", current_state, " New ", new_state)

    # 1. Récupération de l'état actuel et Changement
    GPIO.output(bcm, new_state)

    # 2. Renvoi du nouvel état
    print("             * Etat (supposé)", new_state, " Etat (réel): ", getGPIOState(bcm))
    print("----------------------------")

    return new_state


# Méthode pour lire l'etat de la prise
# Renvoie 1 ou 0
def getGPIOState(prise_bcm: int):
    state = GPIO.input(prise_bcm)
    if state:
        state_text = GPIO.HIGH
    else:
        state_text = GPIO.LOW

    print("Etat de la prise ", prise_bcm, " : ", state_text)
    return state_text


# Méthode pour ire TOUS les états
def getAllGPIOState():
    for prise in tab_prises_bcm:
        getGPIOState(prise)


# -----------------------------------------------------

# Définition des routes
# ----------------------

# ----------------------
# API
# ----------------------

# Read all GPIO state
# ----------------------
@app.route(
    '/api/',
    methods=['POST']
)
def api_index():
    # Check if request contains JSON
    if request.json:
        api_key = request.json.get("api_key")
    else:
        return {"message": "Please provide an API key"}, 400

    # Check if API key is correct and valid
    if request.method != "POST" and not is_valid(api_key):
        return {"message": "The provided API key is not valid"}, 403
    else:
        # 1. Initialisation
        initGPIO()
        return jsonify(
            [
                {
                    'Prise': 1,
                    'state': getGPIOState(get_bcm(1))
                },
                {
                    'Prise': 2,
                    'state': getGPIOState(get_bcm(2))
                },
                {
                    'Prise': 3,
                    'state': getGPIOState(get_bcm(3))
                },
                {
                    'Prise': 4,
                    'state': getGPIOState(get_bcm(4))
                }
            ]
        )


# Switch POST
# ----------------------
@app.route(
    "/api/switch/<int:prise>",
    methods=['POST']
)
def api_switch(prise: int):
    # Check if request contains JSON
    if request.json:
        api_key = request.json.get("api_key")
    else:
        return {"message": "Please provide an API key"}, 400

    # Check if API key is correct and valid
    if request.method != "POST" and not is_valid(api_key):
        return {"message": "The provided API key is not valid"}, 403
    else:
        # Récupération de l'état APRES le switch
        switched_state = switchGPIO(prise)

        return jsonify(
            {
                'Prise': prise,
                'state': switched_state
            }
        )


@app.route(
    "/api/switch/state/<int:prise>",
    methods=['POST']
)
def api_switch_state(prise: int):
    # Check if request contains JSON
    if request.json:
        api_key = request.json.get("api_key")
    else:
        return {"message": "Please provide an API key"}, 400

    # Check if API key is correct and valid
    if request.method != "POST" and not is_valid(api_key):
        return {"message": "The provided API key is not valid"}, 403
    else:
        return jsonify(
            {
                'Prise': prise,
                'state': getGPIOState(get_bcm(prise))
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
    print("----------------------------")
    print("WEB Switch de la prise " + str(prise))  # str(prise) pour caster un int en string

    # Récupération de la broche PCM correspondant à cette prise
    if str(prise) in tab_prises_bcm:
        bcm: str = tab_prises_bcm[str(prise)]
    else:
        print("Aucune BCM correspondante")
        # Quit the program
        quit()

    print("Prise ", prise, " correspond au BCM ", bcm)

    # Changement d'état
    state: int = switchGPIO(prise)
    print("----------------------------")

    return render_template("switch.html", prise=prise, state=state)


if __name__ == '__main__':
    initGPIO()

    app.run(
        use_reloader=True,
        debug=True,
        host='0.0.0.0',
        port=5000
    )
