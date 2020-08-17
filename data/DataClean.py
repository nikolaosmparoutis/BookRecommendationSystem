import numpy as np
from configurations.LoggerCls import LoggerCls


class DataClean:
    formatter = '%(name)s - %(levelname)s - Line No. : %(lineno)d - %(message)s'
    logData = LoggerCls("DataClean logger", "DataLogger.log", "w", formatter, "INFO")

    def __init__(self, datafr):
        self.df = datafr

    def clean_na(self):
        self.df.replace('', np.nan)
        # self.df.dropna(subset=[self.df.columns[0]]) # the first column has the primary key
        return self.df

    def drop_columns(self, to_drop_columns):
        self.df.drop(columns=to_drop_columns, axis=1, inplace=True)
        return self.df

    def check_unique_values(self):
        for cols in self.df:
            DataClean.logData.info("Unique values in " + cols + "=" + str(self.df[cols].nunique()))

    def check_numerical_and_set_nan(self, cols_to_nan):
        for each_colm in cols_to_nan:
            counter = 0
            for each_row in self.df[each_colm]:
                if type(each_row) is str:
                    if each_row.isdigit() is False:
                        self.df.loc[counter, each_colm] = np.nan
                counter += 1
        return self.df

    def remove_bad_char(self, col_to_remove_char="ISBN", char_to_rm="X"):
        for col_name in self.df.columns:
            if col_name == col_to_remove_char:
                self.df[col_to_remove_char] = self.df[col_to_remove_char].str.replace(char_to_rm, "")
        return self.df

    def replace_nan(self, columns_with_nan):
        for each_column in columns_with_nan:
            self.df[each_column].astype(str)
            self.df[each_column] = self.df[each_column].interpolate(method='linear').ffill().bfill()
        return self.df

    # This created to aggregate the logic running all at once for each dataset.
    # this saves multiple method calls, unreadable code and code repetition.
    # Of course each dataset has different data and requires different analysis.
    def execute_pipeline_cleaning(self, to_drop_columns, numeric_col_to_nan):
        import pandas as pd
        self.clean_na()
        self.drop_columns(to_drop_columns)
        self.check_unique_values()
        self.remove_bad_char()
        self.check_numerical_and_set_nan(numeric_col_to_nan)
        clean_df = pd.DataFrame(self.replace_nan(numeric_col_to_nan))
        return clean_df
