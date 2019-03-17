import process
import fp
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import pandas as pd

DIAGNOSIS_COL = 'DIAGNOSIS_SHORT_1'
DIAGNOSIS_CAT_COL = DIAGNOSIS_COL + "_CAT"
KEEP_COLS = ['VISIT_REASON_1', 'DIAGNOSIS_SHORT_1']
DUMMY_COLS = [c for c in KEEP_COLS if c != DIAGNOSIS_COL]
PREFIX_COLS = [s[:2] for s in DUMMY_COLS]
TEST_SIZE = 0.2
RANDOM_STATE = 1

class SymptomTree:
    def __init__(self):
        self.model = DecisionTreeClassifier()
        self.diagnosis_dict = {}
        self.rev_diagnosis_dict = {}
        self.data = None
        self.x_train = None
        self.y_train = None
        self.test_data_x = None
        self.test_data_y = None
        self.y_pred = None

    def train(self,x_data, y_data):
        self.x_train, self.test_data_x, \
        self.y_train, self.test_data_y = fp.split_data(x_data, y_data)

        self.trained_model = self.model.fit(self.x_train, self.y_train)

    def predict(self, param):
        # pass none to set testing data predictions
        if param is None:
            self.y_pred = self.trained_model.predict(self.test_data_x)
            return None
        else:
            pass

    def get_diagnosis_string(self, code):
        try:
            diagnosis = self.rev_diagnosis_dict[code]
            return diagnosis
        except:
            return None

    def get_diagnosis_code(self, string):
        try:
            code = self.diagnosis_dict[string]
            return code
        except:
            return None

    @property
    def accuracy(self):
        score = accuracy_score(self.test_data_y, self.y_pred)
        print("Accuracy:", score)
        return score

    @property
    def predictor_set_size(self):
        return len(self.x_train.columns) - 1

def get_data(path):
    # need to add param to fp
    df = process.read_and_process_data(path)
    df = df.loc[:, KEEP_COLS]
    df2 = df.copy()
    df2, d_map, d_r = fp.encode_diagnoses(df2, DIAGNOSIS_COL, 
        DIAGNOSIS_CAT_COL)
    df2 = pd.get_dummies(df2, columns=DUMMY_COLS, prefix=PREFIX_COLS)

    return (df2, d_map, d_r)


def go(raw_path):
    st = SymptomTree()
    st.data, st.diagnosis_dict, st.rev_diagnosis_dict = get_data(raw_path)
    x, y = fp.split_attributes(st.data)

    st.train(x,y)
    st.predict(None)

    return st


if __name__ == "__main__":
    path = 'data/d_small.csv'
    go(path)