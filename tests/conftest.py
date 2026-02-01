"""
Pytest fixtures for Student Performance Predictor tests
"""
import pytest
import pandas as pd
import numpy as np
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return {
        "gender": "male",
        "race_ethnicity": "group B",
        "parental_level_of_education": "bachelor's degree",
        "lunch": "standard",
        "test_preparation_course": "completed",
        "reading_score": 75,
        "writing_score": 78
    }


@pytest.fixture
def sample_dataframe():
    """Sample DataFrame for testing transformations"""
    return pd.DataFrame({
        "gender": ["male", "female", "male"],
        "race_ethnicity": ["group A", "group B", "group C"],
        "parental_level_of_education": ["bachelor's degree", "some college", "master's degree"],
        "lunch": ["standard", "free/reduced", "standard"],
        "test_preparation_course": ["completed", "none", "completed"],
        "reading_score": [72, 65, 88],
        "writing_score": [74, 68, 90],
        "math_score": [70, 62, 85]
    })


@pytest.fixture
def sample_train_array():
    """Sample training array for model testing"""
    np.random.seed(42)
    X = np.random.rand(100, 7)
    y = np.random.rand(100) * 100  # Scores 0-100
    return np.column_stack([X, y])


@pytest.fixture
def sample_test_array():
    """Sample test array for model testing"""
    np.random.seed(24)
    X = np.random.rand(20, 7)
    y = np.random.rand(20) * 100
    return np.column_stack([X, y])


@pytest.fixture
def artifacts_dir(tmp_path):
    """Temporary artifacts directory for testing"""
    artifacts = tmp_path / "artifacts"
    artifacts.mkdir()
    return artifacts
