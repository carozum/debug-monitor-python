import plotly.express as px
import numpy as np
import logging
logger = logging.getLogger(__name__)


def create_figure(data):
    try:
        fig_map = px.scatter_mapbox(
            data,
            title="Traffic en temps réel",
            color="traffic",
            lat="lat",
            lon="lon",
            color_discrete_map={
                'freeFlow': 'green',
                'heavy': 'orange',
                'congested': 'red'},
            zoom=10,
            height=500,
            mapbox_style="carto-positron"
        )
        logger.debug("Carte créée avec succès")
        return fig_map
    except Exception as e:
        logger.error(f"Erreur lors de la création de la carte: {e}")
        raise


def prediction_from_model(model, hour_to_predict):
    try:
        input_pred = np.array([0]*24)
        input_pred[int(hour_to_predict)] = 1

        cat_predict = np.argmax(model.predict(np.array([input_pred])))
        logger.debug(f"Prediction faite avec succès : {cat_predict}")
        return cat_predict
    except Exception as e:
        logger.error(f"Erreur de génération de la prédiction : {e}")
        raise


"""import plotly.express as px
import numpy as np

# crée un graphique de carte avec les données de trafic et configure les couleurs


def create_figure(data):

    fig_map = px.scatter_mapbox(
        data,
        title="Traffic en temps réel",
        color="traffic",
        lat="lat",
        lon="lon",
        color_discrete_map={
            'freeFlow': 'green',
            'heavy': 'orange',
            'congested': 'red'},
        zoom=10,  # ERROR corrected
        height=500,
        mapbox_style="carto-positron"
    )

    return fig_map


def prediction_from_model(model, hour_to_predict):
    # Prend en entrée une heure et crée un vecteur d'entrée pour le modèle. Prédît la catégorie du trafic en utilisant le modèle et renvoie l'indice de la catégorie la plus probable.
    input_pred = np.array([0]*25)
    input_pred[int(hour_to_predict)] = 1

    cat_predict = np.argmax(model.predict(np.array([input_pred])))

    return cat_predict
"""
