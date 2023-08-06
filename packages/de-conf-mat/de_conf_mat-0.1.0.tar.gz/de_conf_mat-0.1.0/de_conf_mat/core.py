class DeConfMat:
    def __init__(self, conf_mat):
        self.conf_mat = conf_mat

    def deconf(self):
        labels_row = []
        labels_col = []

        for i_row, row in enumerate(self.conf_mat):
            for i_col, value in enumerate(row):
                labels_row += [i_row] * value
                labels_col += [i_col] * value

        truth = labels_row
        predicted = labels_col

        return truth, predicted

def de_conf_mat(cm):
    dc = DeConfMat(cm)
    truth, predicted = dc.deconf()

    return truth, predicted
