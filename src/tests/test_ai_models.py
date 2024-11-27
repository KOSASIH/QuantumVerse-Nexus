import unittest
import numpy as np
from model import IrisClassifier

class TestIrisClassifier(unittest.TestCase):
    def setUp(self):
        self.classifier = IrisClassifier()

    def test_initialization(self):
        """Test that the model is initialized correctly."""
        self.assertIsInstance(self.classifier.model, RandomForestClassifier)
        self.assertFalse(self.classifier.is_trained)

    def test_train(self):
        """Test the training process."""
        self.classifier.train()
        self.assertTrue(self.classifier.is_trained)

    def test_predict_before_training(self):
        """Test that prediction raises an exception if the model is not trained."""
        with self.assertRaises(Exception) as context:
            self.classifier.predict(np.array([[5.1, 3.5, 1.4, 0.2]]))
        self.assertTrue("Model must be trained before predictions can be made." in str(context.exception))

    def test_predict_after_training(self):
        """Test that prediction works after training."""
        self.classifier.train()
        prediction = self.classifier.predict(np.array([[5.1, 3.5, 1.4, 0.2]]))
        self.assertIn(prediction[0], [0, 1, 2])  # Since Iris dataset has 3 classes

    def test_save_and_load_model(self):
        """Test saving and loading the model."""
        self.classifier.train()
        self.classifier.save_model('test_model.joblib')
        
        new_classifier = IrisClassifier()
        new_classifier.load_model('test_model.joblib')
        prediction = new_classifier.predict(np.array([[5.1, 3.5, 1.4, 0.2]]))
        self.assertIn(prediction[0], [0, 1, 2])  # Check if the loaded model can predict

if __name__ == '__main__':
    unittest.main()
