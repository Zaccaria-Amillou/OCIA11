# ## 1. Importation

# ### 1.1 Importation des bibliothèques

import pandas as pd
import numpy as np
import io
import os
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras import Model
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, pandas_udf, PandasUDFType, element_at, split
from pyspark.ml.feature import PCA
from pyspark.ml.linalg import Vectors
from pyspark.sql.functions import udf
from pyspark.ml.linalg import VectorUDT

# ### 1.2 Importation des données

PATH = 'storage'
PATH_Data = PATH+'/Test'
PATH_Result = PATH+'/Results'
print('PATH:        '+\
      PATH+'\nPATH_Data:   '+\
      PATH_Data+'\nPATH_Result: '+PATH_Result)

# ## 2. Session Spark


# Lecture des images
images = spark.read.format("binaryFile") \
  .option("pathGlobFilter", "*.jpg") \
  .option("recursiveFileLookup", "true") \
  .load(PATH_Data)

# Extraction des labels des images
images = images.withColumn('label', element_at(split(images['path'], '/'),-2))

# ## 3. Modélisation

# Création du modèle MobileNetV2
model = MobileNetV2(weights='imagenet',
                    include_top=True,
                    input_shape=(224, 224, 3))

# Création d'un nouveau modèle à partir de MobileNetV2 sans la dernière couche
new_model = Model(inputs=model.input,
                  outputs=model.layers[-2].output)

# Diffusion des poids du modèle
brodcast_weights = spark.broadcast(new_model.get_weights())

new_model.summary()

# Fonction pour créer le modèle
def model_fn():
    """
    Renvoie un modèle MobileNetV2 avec la dernière couche supprimée 
    et les poids pré-entraînés diffusés.
    """
    model = MobileNetV2(weights='imagenet',
                        include_top=True,
                        input_shape=(224, 224, 3))
    for layer in model.layers:
        layer.trainable = False
    new_model = Model(inputs=model.input,
                  outputs=model.layers[-2].output)
    new_model.set_weights(brodcast_weights.value)
    return new_model

# Fonction pour prétraiter les images
def preprocess(content):
    """
    Prétraite les bytes d'image brute pour la prédiction.
    """
    img = Image.open(io.BytesIO(content)).resize([224, 224])
    arr = img_to_array(img)
    return preprocess_input(arr)

# Fonction pour extraire les caractéristiques des images
def featurize_series(model, content_series):
    """
    Extraire une pd.Series d'images brutes en utilisant le modèle en entrée.
    :return: une pd.Series de caractéristiques d'image
    """
    input = np.stack(content_series.map(preprocess))
    preds = model.predict(input)
    # Pour certaines couches, les caractéristiques de sortie seront des tenseurs multidimensionnels.
    # Nous aplatissons les tenseurs de caractéristiques en vecteurs pour un stockage plus facile dans les DataFrames Spark.
    output = [p.flatten() for p in preds]
    return pd.Series(output)

# UDF pour extraire les caractéristiques des images
@pandas_udf('array<float>', PandasUDFType.SCALAR_ITER)
def featurize_udf(content_series_iter):
    '''
    Cette méthode est un UDF pandas Scalar Iterator qui enveloppe notre fonction de featurisation.
    Le décorateur spécifie que cela renvoie une colonne de DataFrame Spark de type ArrayType(FloatType).

    :param content_series_iter: Cet argument est un itérateur sur des lots de données, où chaque lot
                              est une série pandas de données d'image.
    '''
    # Avec les UDF pandas Scalar Iterator, nous pouvons charger le modèle une fois et ensuite le réutiliser
    # pour plusieurs lots de données.  Cela amortit le coût de chargement de grands modèles.
    model = model_fn()
    for content_series in content_series_iter:
        yield featurize_series(model, content_series)

# Configuration de Spark
spark.conf.set("spark.sql.execution.arrow.maxRecordsPerBatch", "1024")

# Extraction des caractéristiques des images
features_df = images.repartition(24).select(col("path"),
                                            col("label"),
                                            featurize_udf("content").alias("features")
                                           )

# UDF pour convertir un tableau en vecteur
list_to_vector_udf = udf(lambda l: Vectors.dense(l), VectorUDT())

# Chargement des données
df = spark.read.parquet(PATH_Result)

# Conversion du tableau de flottants en un vecteur
df = df.withColumn("features_vec", list_to_vector_udf(df["features"]))

# Application de PCA
pca = PCA(k=2, inputCol="features_vec", outputCol="pcaFeatures")
model = pca.fit(df)
result = model.transform(df)
result = result.drop('features_vec')
result = result.drop('features')

# Sauvegarde des résultats
result.write.mode("overwrite").parquet(PATH_Result)