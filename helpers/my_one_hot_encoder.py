from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np
import pandas as pd


class MyOneHotEncoder(object):
    def labelEncodeColumn(self, col, le=LabelEncoder()):
        le.fit(col)  # note that duplicates does not seem to matter here, so no need to call unique beforehand
        # print auto_full_edit['make']
        return le.transform(col)

    @staticmethod
    def createNewPanda(arr, col_name):
        assert len(arr.shape) > 1
        return pd.DataFrame(arr, columns=[col_name + "_{}".format(col_ind) for col_ind in range(arr.shape[1])])

    def encodePandasColAndMerge(self, data_frame, col_name):
        one_hot_encoded = MyOneHotEncoder().encodePandasColumn(data_frame=data_frame, col_name=col_name)
        return pd.concat((data_frame, one_hot_encoded), axis=1).drop(labels=[col_name], axis=1)

    def encodePandasColumn(self, data_frame, col_name):
        # df = data_frame[:]
        dataf = data_frame.copy()

        le = LabelEncoder()

        le.fit(data_frame[col_name])

        dataf[col_name] = le.transform(dataf[col_name])  # .astype(np.float)
        # The categorical attributes must be gone and replaced by numbers

        encoder = OneHotEncoder()

        transformation = encoder.fit_transform(dataf[col_name].to_frame())

        # Dummy variable trap
        # Because of the dummy variable  trap we need to drop one of the columns for each category
        arr = transformation.toarray()[:, 1:]

        return self.createNewPanda(arr=arr, col_name=col_name)

    def encodePandasColumn_old(self, data_frame, col_name):
        # df = data_frame[:]
        dataf = data_frame.copy()

        le = LabelEncoder()

        le.fit(data_frame[col_name])

        dataf[col_name] = le.transform(dataf[col_name])  # .astype(np.float)
        # The categorical attributes must be gone and replaced by numbers
        print(dataf[col_name].dtype)

        assert np.all(dataf[col_name] >= 0)
        assert np.all(dataf[col_name] < 100)

        mask = dataf.dtypes
        mask[:] = False
        mask[col_name] = True
        print(mask)

        encoder = OneHotEncoder(categorical_features=mask)  # mask needs to be of type Series

        transformation = encoder.fit_transform(dataf)

        print(encoder.feature_indices_)

        # return transformation.toarray()
