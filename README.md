

<h1>Fruits! - Prototype de Classification d'Images de Fruits</h1>
<div class='img'>
  <img src='https://plus.unsplash.com/premium_photo-1671379086168-a5d018d583cf?q=80&w=1887&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D', alt='some fruits on a table'>
</div>  
<p>Mise en place d'une architecture Big Data pour une application mobile de reconnaissance de fruits</p>


<h2>Introduction</h2>
<p>Fruits! est une start-up de l'AgriTech qui développe des solutions innovantes pour la récolte de fruits. Notre objectif est de préserver la biodiversité des fruits en utilisant des robots cueilleurs intelligents.</p>
<p>Ce projet vise à créer un prototype d'application mobile permettant aux utilisateurs d'identifier des fruits en les prenant en photo. Ce prototype servira également à tester notre moteur de classification d'images et à mettre en place une architecture Big Data évolutive.</p>


<h2>Architecture Big Data</h2>
<p>Nous utiliserons une architecture Big Data hybride, combinant les services AWS et Azure, pour traiter les données d'images de fruits. Cette approche nous permet de tirer parti des forces de chaque plateforme et d'assurer une scalabilité optimale pour gérer des volumes de données croissants.</p>

<h3>Services AWS</h3>
    <ul>
        <li>**EMR (Elastic MapReduce):** Cluster Hadoop géré pour exécuter des tâches de traitement de données distribuées avec PySpark.</li>
        <li>**S3 (Simple Storage Service):** Stockage objet pour les données d'images brutes et les modèles entraînés.</li>
        <li>**IAM (Identity and Access Management):** Gestion des accès et des permissions pour sécuriser les ressources AWS.</li>
    </ul>

<h3>Services Azure</h3>
    <ul>
        <li>**Azure Blob Storage:** Stockage objet pour les données intermédiaires et les résultats de traitement.</li>
        <li>**Databricks (Optionnel):** Plateforme d'analyse de données basée sur Apache Spark, offrant une alternative à EMR pour le traitement distribué.</li>
    </ul>

<h2>Traitement des Données avec PySpark</h2>
<p>Nous utiliserons PySpark pour développer des scripts de traitement de données distribués sur le cluster EMR. Nous compléterons le notebook existant en ajoutant les étapes suivantes :</p>
    <ul>
        <li>**Diffusion des poids du modèle (Broadcast):** Permet de partager efficacement les poids du modèle TensorFlow entre les nœuds du cluster.</li>
        <li>**Réduction de dimension (PCA):** Réduit la dimensionnalité des données pour améliorer les performances et la visualisation.</li>
    </ul>

### Livrables
1. EDA : [Notebook](https://github.com/Zaccaria-Amillou/OCIA11/blob/main/Notebook/1.%20Analyse.ipynb)
2. Modélisation en local : [notebook](https://github.com/Zaccaria-Amillou/OCIA11/blob/main/Notebook/2.%20Modelisation%20en%20Local.ipynb)
3. Script AWS : [Script](https://github.com/Zaccaria-Amillou/OCIA11/blob/main/Notebook/3.%20Script%20AWS%20EMR.py)
4. Notebook DataBricks : [Notebook](https://github.com/Zaccaria-Amillou/OCIA11/blob/main/Notebook/4.%20Modelisation%20Databricks.ipynb)
5. Présentation : [PDF](https://github.com/Zaccaria-Amillou/OCIA11/blob/main/Presentation.pdf)
