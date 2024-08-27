
from flask import Flask, render_template, request
from keras.models import load_model
from src.get_data import GetData
from src.utils import create_figure, prediction_from_model
import flask_monitoringdashboard as dashboard

# configuration de base de logging
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s %(name)s %(message)s')
logger = logging.getLogger(__name__)


app = Flask(__name__)

# accés aux données de l'API
try:
    data_retriever = GetData(
        url="https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B")           # Json
    data = data_retriever()       # dataframe
    logger.debug("Accès au données de l'API avec succès ")
except Exception as e:
    logger.error(f"Echec accès aux donneés de l'API: {e}")
    data = None


# chargement du modèle
try:
    logger.debug("chargement du model...")
    model = load_model('model.h5', compile=False)
    logger.debug("model chargé avec succès")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise


@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':  # prédiction + carte

            logger.debug("Processing POST request.")
            fig_map = create_figure(data)
            graph_json = fig_map.to_json()

            selected_hour = request.form['hour']

            cat_predict = prediction_from_model(model, selected_hour)  # err
            logger.debug(
                f"La prediction pour {selected_hour} h est {cat_predict}")

            color_pred_map = {
                0: ["Prédiction : Libre", "green"],
                1: ["Prédiction : Dense", "orange"],
                2: ["Prédiction : Bloqué", "red"]}

            return render_template(
                'index.html',
                graph_json=graph_json,
                text_pred=color_pred_map[cat_predict][0],
                color_pred=color_pred_map[cat_predict][1])

        else:  # carte seule

            logger.debug("Processing GET request.")
            if data is not None:
                fig_map = create_figure(data)
                graph_json = fig_map.to_json()  # err
            else:
                logger.error("Pas de données à afficher.")
                return "Données non disponibles", 500

            return render_template('index.html', graph_json=graph_json)

    except Exception as e:
        logger.error(f"Erreur dans la route principale : {e}")
        return "Une erreur est survenue", 500


# suivi de la performance
dashboard.config.enable_logging = True
dashboard.bind(app)
dashboard.config.monitor_level = 3  # high level

if __name__ == '__main__':
    try:
        app.run(debug=True, use_reloader=False)
    except Exception as e:
        logger.critical(f"L'app n'a pas pu démarrer: {e}")


"""from flask import Flask, render_template, request
# import plotly.graph_objs as go
# import plotly.express as px
# import numpy as np

from keras.models import load_model

from src.get_data import GetData
from src.utils import create_figure, prediction_from_model

import flask_monitoringdashboard as dashboard

# création de l'app
app = Flask(__name__)

# mise en place du monitorage
dashboard.bind(app)

# récupération des données, data_retriever est une instance de la classe GetData qui prend en paramètre l'URL de l'API
data_retriever = GetData(
    url="https://data.rennesmetropole.fr/api/explore/v2.1/catalog/datasets/etat-du-trafic-en-temps-reel/exports/json?lang=fr&timezone=Europe%2FBerlin&use_labels=true&delimiter=%3B")
# obtention des données en format DataFrame
data = data_retriever()


# chargement du modèle préentrainé (fonction Keras)
model = load_model('model.h5')


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':
        # récupération des données du formulaire (heure) et envoie d'une prédiction.

        # création des graphiques
        fig_map = create_figure(data)
        graph_json = fig_map.to_json()

        selected_hour = request.form.get('hour')  # USING GET
        if selected_hour is not None:
            cat_predict = prediction_from_model(model, selected_hour)
            color_pred_map = {
                0: ["Prédiction : Libre", "green"],
                1: ["Prédiction : Dense", "orange"],
                2: ["Prédiction : Bloqué", "red"]}
            text_pred = color_pred_map[cat_predict][0]color_pred = color_pred_map[cat_predict][1]

        if cat_predict is not None:
            text_pred, color_pred = color_pred_map.get(
                cat_predict, ["Prédiction inconnue", "gray"])
        else:
            text_pred, color_pred = "Heure non sélectionnée", "gray"

        return render_template('home.html', graph_json=graph_json, text_pred=color_pred_map[cat_predict][0], color_pred=color_pred_map[cat_predict][1])

    else:
        # méthode GET, appel de l'API et création du graphe
        fig_map = create_figure(data)
        graph_json = fig_map.to_json()  # ERROR oubli parenthèse

        return render_template('home.html', graph_json=graph_json)


if __name__ == '__main__':
    app.run(debug=True)
"""
