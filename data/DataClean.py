import numpy as np


class DataClean:
    def __init__(self, datafr):
        self.df = datafr

    def clean_na(self):
        self.df.replace('', np.nan)
        # self.df.dropna(subset=[self.df.columns[0]]) # the first column has the primary key
        # print(self.df)
        return self.df

    def drop_columns(self, to_drop_columns):
        self.df.drop(columns=to_drop_columns, axis=1, inplace=True)
        return self.df

    def check_unique_values(self):
        for cols in self.df:
            print("Unique values in " + cols + "=" + str(self.df[cols].nunique()))
        print('\n')

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
        print("IN remove_bad_char")
        # if self.df.columns.any() == col_to_remove_char:
        for col_name in self.df.columns:
            if col_name == col_to_remove_char:
                self.df[col_to_remove_char] = self.df[col_to_remove_char].str.replace(char_to_rm, "")
        return self.df

    def replace_nan(self, column_with_nan):
        self.df[column_with_nan].astype(str)
        # for row in self.df.ISBN:
        #     self.df[each_colm].fillna(self.df[each_colm].interpolate(method='linear'),inplace=True)
        self.df[column_with_nan] = self.df[column_with_nan].interpolate(method='linear').ffill().bfill()
        return self.df

    # This created to aggregate the logic running all at once for each dataset.
    # to covert the case of many new data comming as batches or streams. Also,
    # this saves multiple method calls and code repetition.
    # Of course each dataset has different data and requires different analysis
    # for the scope of this project we can use this.

    def execute_pipeline_cleaning(self, to_drop_columns, numeric_col_to_nan):
        self.clean_na()
        self.drop_columns(to_drop_columns)
        self.check_unique_values()
        self.remove_bad_char()
        self.check_numerical_and_set_nan(numeric_col_to_nan)
        print(self.df)
        # self.replace_nan(numeric_col_to_nan)
