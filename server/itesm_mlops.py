"""Main module."""
from load.load_data import DataRetriever
from train.train_data import StrokeDataPipeline
import pandas as pd
from sklearn.model_selection import train_test_split
import joblib
import os
from sklearn.metrics import accuracy_score, roc_auc_score

DATASETS_DIR = './data/'
URL = 'C:/Users/gcsanchez/Documents/GitHub/mlops_mod3/module-3/datasets/healthcare-dataset-stroke-data.csv'
DROP_COLS = ['id']
RETRIEVED_DATA = 'raw-data-stroke.csv'


SEED_SPLIT = 404
TRAIN_DATA_FILE = DATASETS_DIR + 'train.csv'
TEST_DATA_FILE  = DATASETS_DIR + 'test.csv'


TARGET = 'stroke'
FEATURES = ['gender','age','hypertension','heart_disease','ever_married','work_type','Residence_type','avg_glucose_level','bmi','smoking_status']
NUMERICAL_VARS = ['age','avg_glucose_level', 'bmi']
CATEGORICAL_VARS = ['gender','hypertension','heart_disease','ever_married','work_type','Residence_type','smoking_status']


NUMERICAL_VARS_WITH_NA = ['bmi']
CATEGORICAL_VARS_WITH_NA = []
NUMERICAL_NA_NOT_ALLOWED = [var for var in NUMERICAL_VARS if var not in NUMERICAL_VARS_WITH_NA]
CATEGORICAL_NA_NOT_ALLOWED = [var for var in CATEGORICAL_VARS if var not in CATEGORICAL_VARS_WITH_NA]


SEED_MODEL = 404

SELECTED_FEATURES = ['gender','age','hypertension','heart_disease','ever_married','work_type',
       'Residence_type','avg_glucose_level','bmi','smoking_status']

TRAINED_MODEL_DIR = './models/'
PIPELINE_NAME = 'logistic_regression'
PIPELINE_SAVE_FILE = f'{PIPELINE_NAME}_output.pkl'


if __name__ == "__main__":
    
    print(os.getcwd())
    os.chdir('C:/Users/gcsanchez/Documents/GitHub/mlops_mod3/itesm_mlops/itesm_mlops')
    # Retrieve data
    data_retriever = DataRetriever(URL, DATASETS_DIR)
    result = data_retriever.retrieve_data()
    print(result)
    
    # Instantiate the strokeDataPipeline class
    stroke_data_pipeline = StrokeDataPipeline(seed_model=SEED_MODEL,
                                                numerical_vars=NUMERICAL_VARS, 
                                                categorical_vars_with_na=CATEGORICAL_VARS_WITH_NA,
                                                numerical_vars_with_na=NUMERICAL_VARS_WITH_NA,
                                                categorical_vars=CATEGORICAL_VARS,
                                                selected_features=SELECTED_FEATURES)
    
    # Read data
    df = pd.read_csv(DATASETS_DIR + RETRIEVED_DATA)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
                                                        df.drop(TARGET, axis=1),
                                                        df[TARGET],
                                                        test_size=0.2,
                                                        random_state=404
                                                   )
    
    logistic_regression_model = stroke_data_pipeline.fit_logistic_regression(X_train, y_train)
    
    X_test = stroke_data_pipeline.PIPELINE.fit_transform(X_test)
    
    X_test2 = X_test.drop(['gender','ever_married','work_type','Residence_type','smoking_status'], axis=1)
    y_pred = logistic_regression_model.predict(X_test2)
    
    class_pred = logistic_regression_model.predict(X_test2)
    proba_pred = logistic_regression_model.predict_proba(X_test2)[:,1]
    print(f'test roc-auc : {roc_auc_score(y_test, proba_pred)}')
    print(f'test accuracy: {accuracy_score(y_test, class_pred)}')
    
    # # Save the model using joblib
    save_path = TRAINED_MODEL_DIR + PIPELINE_SAVE_FILE
    joblib.dump(logistic_regression_model, save_path)
    print(f"Model saved in {save_path}")