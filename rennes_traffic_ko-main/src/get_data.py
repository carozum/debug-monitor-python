import pandas as pd
import requests
import logging

logger = logging.getLogger(__name__)


class GetData(object):

    def __init__(self, url) -> None:
        self.url = url
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            self.data = response.json()
            logger.debug("Données récupérées de l'API.")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise
        except ValueError as e:
            logger.error(f"Failed to parse JSON: {e}")
            raise

    def processing_one_point(self, data_dict: dict):
        try:
            temp = pd.DataFrame({key: [data_dict[key]] for key in [
                                'datetime', 'geo_point_2d', 'averagevehiclespeed', 'traveltime', 'trafficstatus']})  # err

            temp = temp.rename(columns={'trafficstatus': 'traffic'})  # err
            temp['lat'] = temp.geo_point_2d.map(lambda x: x['lat'])  # err
            temp['lon'] = temp.geo_point_2d.map(lambda x: x['lon'])  # err
            del temp['geo_point_2d']
            logger.debug("Processed one data point successfully.")
            return temp
        except KeyError as e:
            logger.error(f"Key not found: {e}")
            raise
        except Exception as e:
            logger.error(f"Error while processing one point: {e}")
            raise

    def __call__(self):
        try:
            res_df = pd.DataFrame({})

            for data_dict in self.data:
                temp_df = self.processing_one_point(data_dict)
                res_df = pd.concat([res_df, temp_df])  # err

            res_df = res_df[res_df.traffic != 'unknown']
            logger.debug("Données récupérées avec succès")
            return res_df
        except Exception as e:
            logger.error(f"Error while processing data : {e}")


"""import pandas as pd
import requests


class GetData(object):

    def __init__(self, url) -> None:
        # rrécupére les données de l'API en format JSON
        self.url = url
        response = requests.get(self.url)
        self.data = response.json()

    def processing_one_point(self, data_dict: dict):
        # transforme un dictionnaire en dataframe
        temp = pd.DataFrame({key: [data_dict[key]] for key in [
                            'datetime', 'traffic_status', 'geo_point_2d', 'averagevehiclespeed', 'traveltime', 'trafficstatus']})
        temp = temp.rename(columns={'traffic_status': 'traffic'})
        temp['lat'] = temp.geo_point_2d.map(lambda x: x['lattitude'])
        temp['lon'] = temp.geo_point_2d.map(lambda x: x['longitude'])
        del temp['geo_point_2d']

        return temp

    def __call__(self):
        # Récupère toutes les données, les transforme en DataFrame, et filtre les entrées dont le statut de trafic est inconnu.
        res_df = pd.DataFrame({})

        for data_dict in self.data:
            # ERROR correction indentation (voir si indentation 2 lignes ?)
            temp_df = self.processing_one_point(data_dict)
            res_df = pd.concat([res_df, temp_df])

        # ERROR adding closing square brackets ]
        res_df = res_df[res_df.traffic != 'unknown']

        return res_df
"""
