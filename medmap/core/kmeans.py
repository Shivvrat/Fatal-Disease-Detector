import os

from sklearn.cluster import KMeans
import numpy as np

from config import LOG_DIR
from logger import setup_logger

ml_logger = setup_logger(__name__, log_file=os.path.join(LOG_DIR, 'server_log'), level="DEBUG")
ml_logger.propagate = False


def get_center_from_data(df, disease):
    try:
        kmeans = KMeans(n_clusters=8)
        data = df[df.DISEASE == disease]
        if data.shape[0] == 0:
            return (), ()
        data = data.dropna()
        array = data[['GEO_LAT', 'GEO_LONG']].values
        if array.shape[0] >= 8:
            kmeans.fit(array)
            cent = kmeans.cluster_centers_
            count_list = [len(np.where(kmeans.labels_ == i)[0]) for i in range(kmeans.n_clusters)]
            return cent.tolist(), count_list
    except ValueError:
        ml_logger.exception("Error occured while clustering.")
    return [], []
