import math
import pandas as pd
from util import is_csv
from cuz_error import NotCsvException

CONST_A = 0.0018
CONST_B = 0.138
CONST_THETA = 40
CONST_OUTPUT_COLS = ('soil_results',)


class WaterCloudModel:
    def __init__(self, input_path, output_path, alpha, const_a=CONST_A, const_b=CONST_B, theta=CONST_THETA,
                 output_cols=CONST_OUTPUT_COLS):
        self.file_path = input_path
        self.output_path = output_path
        self.alpha = alpha
        self.A = const_a
        self.B = const_b
        self.theta = math.pi * theta / 180
        self.output_cols = output_cols

    @staticmethod
    def read_data(file_path: str) -> pd.DataFrame:
        if not is_csv(file_path):
            raise NotCsvException(file_path)
        return pd.read_csv(file_path, sep=r'\s*,\s*')

    def write_to_csv(self, df: pd.DataFrame):
        df.to_csv(self.output_path, header=True)

    def get_double_decay_factor(self, mv: float) -> float:
        if math.cos(self.theta)==0:
            raise ZeroDivisionError
        tmp = -2 * self.B * mv / math.cos(self.theta)
        return math.exp(tmp)

    def compute_canopy(self, mv: float) -> float:
        return self.A * mv * math.cos(self.theta) * self.get_double_decay_factor(mv)

    def compute_soil(self):
        df = self.read_data(self.file_path)
        rows = df.shape[0]
        new_df = pd.DataFrame(columns=self.output_cols)
        for row in range(0, rows):
            mv = df.at[row, 'mv']
            total = df.at[row, 'total']
            decay_factor = self.get_double_decay_factor(mv)
            if decay_factor == 0:
                print("zero decay_factor found")
                continue
            canopy = self.compute_canopy(mv)
            soil = (total - canopy*(1-math.exp(-self.alpha))) / decay_factor
            new_df = new_df.append({self.output_cols[0]: soil}, ignore_index=True)
        return new_df

    def compute_and_write_soil(self):
        df = self.compute_soil()
        self.write_to_csv(df)
