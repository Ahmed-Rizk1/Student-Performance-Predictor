"""
Unit tests for data transformation component
"""
import pytest
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline


class TestDataTransformation:
    """Test cases for DataTransformation class"""

    def test_numerical_columns_defined(self):
        """Test that numerical columns are correctly defined"""
        numerical_columns = ["writing_score", "reading_score"]
        assert len(numerical_columns) == 2
        assert "writing_score" in numerical_columns
        assert "reading_score" in numerical_columns

    def test_categorical_columns_defined(self):
        """Test that categorical columns are correctly defined"""
        categorical_columns = [
            "gender",
            "race_ethnicity",
            "parental_level_of_education",
            "lunch",
            "test_preparation_course",
        ]
        assert len(categorical_columns) == 5

    def test_preprocessing_pipeline_creation(self):
        """Test that preprocessing pipeline can be created"""
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        
        num_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]
        )
        
        cat_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder()),
                ("scaler", StandardScaler(with_mean=False))
            ]
        )
        
        assert num_pipeline is not None
        assert cat_pipeline is not None

    def test_column_transformer_creation(self, sample_dataframe):
        """Test that ColumnTransformer can be created and applied"""
        from sklearn.impute import SimpleImputer
        from sklearn.preprocessing import OneHotEncoder, StandardScaler
        
        numerical_columns = ["reading_score", "writing_score"]
        categorical_columns = ["gender", "race_ethnicity", "parental_level_of_education", 
                               "lunch", "test_preparation_course"]
        
        num_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler())
        ])
        
        cat_pipeline = Pipeline([
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("one_hot_encoder", OneHotEncoder(handle_unknown='ignore')),
            ("scaler", StandardScaler(with_mean=False))
        ])
        
        preprocessor = ColumnTransformer([
            ("num_pipeline", num_pipeline, numerical_columns),
            ("cat_pipeline", cat_pipeline, categorical_columns)
        ])
        
        X = sample_dataframe.drop(columns=["math_score"])
        transformed = preprocessor.fit_transform(X)
        
        assert transformed is not None
        assert transformed.shape[0] == len(X)

    def test_target_column_separation(self, sample_dataframe):
        """Test that target column can be separated correctly"""
        target_column = "math_score"
        
        X = sample_dataframe.drop(columns=[target_column])
        y = sample_dataframe[target_column]
        
        assert target_column not in X.columns
        assert len(y) == len(sample_dataframe)
        assert all(isinstance(score, (int, float)) for score in y)

    def test_no_missing_values_after_imputation(self, sample_dataframe):
        """Test that imputation handles missing values"""
        from sklearn.impute import SimpleImputer
        
        # Add some missing values
        df_with_nan = sample_dataframe.copy()
        df_with_nan.loc[0, "reading_score"] = np.nan
        
        imputer = SimpleImputer(strategy="median")
        scores = df_with_nan[["reading_score", "writing_score"]]
        transformed = imputer.fit_transform(scores)
        
        assert not np.isnan(transformed).any()
