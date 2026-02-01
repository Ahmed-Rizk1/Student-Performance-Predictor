"""
Unit tests for prediction pipeline
"""
import pytest
import pandas as pd
import os


class TestCustomData:
    """Test cases for CustomData class"""

    def test_custom_data_initialization(self, sample_student_data):
        """Test that CustomData can be initialized with valid data"""
        from src.pipeline.predict_pipeline import CustomData
        
        data = CustomData(**sample_student_data)
        
        assert data.gender == sample_student_data["gender"]
        assert data.race_ethnicity == sample_student_data["race_ethnicity"]
        assert data.reading_score == sample_student_data["reading_score"]
        assert data.writing_score == sample_student_data["writing_score"]

    def test_get_data_as_dataframe(self, sample_student_data):
        """Test that CustomData returns correct DataFrame"""
        from src.pipeline.predict_pipeline import CustomData
        
        data = CustomData(**sample_student_data)
        df = data.get_data_as_data_frame()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        assert "gender" in df.columns
        assert "reading_score" in df.columns
        assert "writing_score" in df.columns

    def test_dataframe_column_order(self, sample_student_data):
        """Test that DataFrame has correct column order"""
        from src.pipeline.predict_pipeline import CustomData
        
        expected_columns = [
            "gender", "race_ethnicity", "parental_level_of_education",
            "lunch", "test_preparation_course", "reading_score", "writing_score"
        ]
        
        data = CustomData(**sample_student_data)
        df = data.get_data_as_data_frame()
        
        assert list(df.columns) == expected_columns

    def test_score_values_preserved(self, sample_student_data):
        """Test that score values are correctly preserved in DataFrame"""
        from src.pipeline.predict_pipeline import CustomData
        
        data = CustomData(**sample_student_data)
        df = data.get_data_as_data_frame()
        
        assert df["reading_score"].iloc[0] == sample_student_data["reading_score"]
        assert df["writing_score"].iloc[0] == sample_student_data["writing_score"]


class TestPredictPipeline:
    """Test cases for PredictPipeline class"""

    def test_model_artifact_path(self):
        """Test that model artifact path is correctly formed"""
        model_path = os.path.join("artifacts", "model.pkl")
        assert model_path == "artifacts\\model.pkl" or model_path == "artifacts/model.pkl"

    def test_preprocessor_artifact_path(self):
        """Test that preprocessor artifact path is correctly formed"""
        preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
        assert "artifacts" in preprocessor_path
        assert "preprocessor.pkl" in preprocessor_path

    def test_prediction_pipeline_initialization(self):
        """Test that PredictPipeline can be initialized"""
        from src.pipeline.predict_pipeline import PredictPipeline
        
        pipeline = PredictPipeline()
        assert pipeline is not None


class TestFlaskApp:
    """Test cases for Flask application routes"""

    def test_app_import(self):
        """Test that Flask app can be imported"""
        from app import app
        assert app is not None

    def test_index_route_exists(self):
        """Test that index route is registered"""
        from app import app
        
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert "/" in rules

    def test_predict_route_exists(self):
        """Test that predict route is registered"""
        from app import app
        
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        assert "/predictdata" in rules
