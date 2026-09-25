import os
import sys
import src.exception
from ..logger import logging
import pandas as pd

from dataclasses import dataclass


def train_test_split(data, test_size=0.2, random_state=None):
    """Split a DataFrame into training and test sets."""
    shuffled_data = data.sample(frac=1, random_state=random_state)
    test_count = int(len(shuffled_data) * test_size)
    test_set = shuffled_data.iloc[:test_count]
    train_set = shuffled_data.iloc[test_count:]
    return train_set, test_set

class DataIngestionConfig:
    pass

@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv('notebook/data/StudentsPerformance.csv')
            logging.info("Read the dataset as dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise src.exception.CustomException(e, sys)    

if __name__ == "__main__":
    obj = DataIngestion()
    obj.initiate_data_ingestion()
        
