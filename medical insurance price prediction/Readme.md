# Medical Insurance Price Prediction using Machine Learning – Python

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Dataset](#dataset)
- [Installation](#installation)
- [Usage](#usage)
- [Model Description](#model-description)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project aims to predict medical insurance costs using machine learning techniques. The prediction is based on various factors such as age, sex, BMI, number of children, smoking status, and region. By leveraging machine learning algorithms, the goal is to provide accurate estimates of insurance premiums, which can be beneficial for both insurance companies and individuals.

## Features
- Data preprocessing and exploration
- Feature engineering
- Model selection and training
- Hyperparameter tuning
- Model evaluation and comparison
- Predictive analytics

## Dataset
The dataset used in this project is a public dataset commonly used for regression tasks in machine learning. It contains the following features:
- `age`: Age of the primary beneficiary
- `sex`: Gender of the primary beneficiary (male/female)
- `bmi`: Body mass index, providing an understanding of the body weight relative to height
- `children`: Number of children/dependents covered by the insurance
- `smoker`: Smoking status of the primary beneficiary (yes/no)
- `region`: Residential area of the beneficiary in the US (northeast, southeast, southwest, northwest)
- `charges`: Medical insurance cost charged by the insurance company (target variable)

## Installation
To get started with this project, clone the repository and install the necessary dependencies:

```bash
git clone https://github.com/yourusername/medical-insurance-prediction.git
cd medical-insurance-prediction
pip install -r requirements.txt
```

## Usage
Once the dependencies are installed, you can run the main script to train the model and make predictions:

```bash
python main.py
```

### Example
To see an example of prediction, you can use the following script:

```python
from prediction import predict_insurance_cost

# Example input
input_data = {
    "age": 29,
    "sex": "female",
    "bmi": 25.3,
    "children": 2,
    "smoker": "no",
    "region": "northwest"
}

# Predict insurance cost
predicted_cost = predict_insurance_cost(input_data)
print(f"Predicted Insurance Cost: ${predicted_cost:.2f}")
```

## Model Description
Several machine learning models are implemented and evaluated in this project, including:
- Linear Regression
- Decision Tree Regressor
- Random Forest Regressor
- Gradient Boosting Regressor

The best performing model is selected based on evaluation metrics such as Mean Absolute Error (MAE), Mean Squared Error (MSE), and R² score.

## Results
The performance of the models is documented in terms of accuracy and error rates. The Random Forest Regressor was found to be the most accurate model with the lowest error rates.

## Contributing
Contributions to this project are welcome. If you have suggestions for improvements or want to add new features, please fork the repository and submit a pull request.

### Steps to Contribute
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add some feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a pull request

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to explore the code, make enhancements, and share your feedback. Happy coding!
