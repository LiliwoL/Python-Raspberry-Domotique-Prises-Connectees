# Prises connectées via un Raspberry

# Import -------------------------
# FLASK
from flask import Flask, render_template, jsonify, request

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
tab_prises_bcm = {
    1: 21,  # Prise 1 -- GPIO 15
    2: 20,
    3: 26,
    4: 19
}


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
    # Lecture de l'état actuel
    current_state = getGPIOState(tab_prises_bcm[prise])

    print("Current state ", current_state)

    if current_state == "on" or current_state == 1:
        print("On passe de 1 à 0")
        new_state = GPIO.LOW
    else:
        print("On passe de 0 à 1")
        new_state = GPIO.HIGH

    print("Old ", current_state, " New ", new_state)

    # 1. Récupération de l'état actuel et Changement
    GPIO.output(tab_prises_bcm[prise], new_state)

    # 2. Renvoi du nouvel état
    print("             * Etat ", new_state, " Etat reel: ", getGPIOState(tab_prises_bcm[prise]))
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


# Méthode pour lire TOUS les états
def getAllGPIOState():
    for prise in tab_prises_bcm:
        getGPIOState(prise)


# -----------------------------------------------------

# Définition des routes
# ----------------------

# ----------------------
# API
# ----------------------
@app.post(
    '/api/'
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
                    'state': getGPIOState(tab_prises_bcm[1])
                },
                {
                    'Prise': 2,
                    'state': getGPIOState(tab_prises_bcm[2])
                },
                {
                    'Prise': 3,
                    'state': getGPIOState(tab_prises_bcm[3])
                },
                {
                    'Prise': 4,
                    'state': getGPIOState(tab_prises_bcm[4])
                }
            ]
        )


# Read all GPIO state
# ----------------------
@app.post(
    '/api/all'
)
def api_read_all():
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
            [
                {
                    'Prise': 1,
                    'state': getGPIOState(tab_prises_bcm[1])
                },
                {
                    'Prise': 2,
                    'state': getGPIOState(tab_prises_bcm[2])
                },
                {
                    'Prise': 3,
                    'state': getGPIOState(tab_prises_bcm[3])
                },
                {
                    'Prise': 4,
                    'state': getGPIOState(tab_prises_bcm[4])
                }
            ]
        )


# Switch POST
# ----------------------
@app.post(
    "/api/switch/<int:prise>"
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


@app.post(
    "/api/switch/state/<int:prise>"
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
                'state': getGPIOState(tab_prises_bcm[prise])
            }
        )


# ----------------------
# Web
# ----------------------

@app.get(
    '/'
)
def web_index():
    # On est sur la page de base

    # 1. Initialisation
    initGPIO()
    return render_template("index.html")


# Switch GET
# To  switch
# ----------------------
@app.get(
    "/switch/<int:prise>"
)
def web_switch(prise: int):
    state = switchGPIO(tab_prises_bcm[prise])

    return render_template("switch.html", prise=prise, state=state)


if __name__ == '__main__':
    initGPIO()

    app.run(
        use_reloader=True,
        debug=True,
        host='0.0.0.0',
        port=5000
    )
