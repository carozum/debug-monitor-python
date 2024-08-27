
# Etude des outils de monitoring 
- logging 
- flask monitoring dashboard



# flask monitoring dashboard

## Principe
https://flask-monitoringdashboard.readthedocs.io/en/latest/ 
To monitor a flask APP. 4 principales fonctionnalités : 

- *Surveiller la performance et l'utilisation* : Le tableau de bord vous permet de voir quels endpoints traitent un grand nombre de requêtes et à quelle vitesse. De plus, il fournit des informations sur l'évolution des performances d'un endpoint à travers différentes versions si vous utilisez git.

- *Profilage des requêtes et des endpoints* : Le chemin d'exécution de chaque requête est suivi et stocké dans la base de données. Cela vous permet de comprendre quelles fonctions dans votre code prennent le plus de temps à s'exécuter. Comme toutes les requêtes pour un endpoint sont également regroupées, le tableau de bord offre une vue d'ensemble des fonctions utilisées dans chaque endpoint.

- *Collecte d'informations supplémentaires sur les outliers* : Les cas extrêmes sont des requêtes qui prennent beaucoup plus de temps à traiter que les requêtes régulières. Le tableau de bord détecte automatiquement qu'une requête est un cas extrême et stocke des informations supplémentaires à son sujet (trace de la pile, valeurs de la requête, en-têtes de la requête, environnement de la requête).

- *Collecte d'informations supplémentaires sur votre application Flask* : Supposons que vous ayez une table Utilisateur et que vous souhaitiez savoir combien d'utilisateurs sont enregistrés sur votre application Flask. Vous pouvez alors exécuter la requête suivante : 'SELECT Count(*) FROM USERS;'. Mais c'est ennuyeux à faire régulièrement. Par conséquent, vous pouvez configurer cela dans le Flask-MonitoringDashboard, qui vous fournira cette information par jour (ou autre intervalle de temps).

## installation
pip install flask_monitoringdashboard

## mise en place dans l'app
import flask_monitoringdashboard as dashboard
dashboard.bind(app)

puis lancer l'app : python3 app.py

puis pour accéder au dashboard http://127.0.0.1:5000/dashboard

## configurations avancées
