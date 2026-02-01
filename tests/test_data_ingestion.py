"""
Unit tests for data ingestion component
"""
import pytest
import os
import pandas as pd


class TestDataIngestion:
    """Test cases for DataIngestion class"""

    def test_data_file_exists(self):
        """Test that the source data file exists"""
        data_path = os.path.join("notebook", "data", "stud.csv")
        assert os.path.exists(data_path), f"Data file not found at {data_path}"

    def test_data_file_readable(self):
        """Test that the data file can be read as DataFrame"""
        data_path = os.path.join("notebook", "data", "stud.csv")
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            assert isinstance(df, pd.DataFrame)
            assert len(df) > 0

    def test_data_columns_present(self):
        """Test that all required columns are present"""
        data_path = os.path.join("notebook", "data", "stud.csv")
        required_columns = [
            "gender", "race/ethnicity", "parental level of education",
            "lunch", "test preparation course", 
            "math score", "reading score", "writing score"
        ]
        
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            for col in required_columns:
                assert col in df.columns, f"Column {col} not found"

    def test_artifacts_directory_creation(self, artifacts_dir):
        """Test that artifacts directory can be created"""
        assert artifacts_dir.exists()
        assert artifacts_dir.is_dir()

    def test_train_test_split_ratio(self, sample_dataframe):
        """Test that train/test split maintains correct ratio"""
        from sklearn.model_selection import train_test_split
        
        train, test = train_test_split(sample_dataframe, test_size=0.2, random_state=42)
        
        total = len(sample_dataframe)
        assert len(train) == int(total * 0.8) or len(train) == round(total * 0.8)
        assert len(test) == total - len(train)
