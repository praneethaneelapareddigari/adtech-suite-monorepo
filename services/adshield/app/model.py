import numpy as np
from sklearn.linear_model import LogisticRegression

class ToyFraudModel:
    def __init__(self):
        X = []
        y = []
        # synthetic training: higher bids or bad IP indicate fraud
        for i in range(500):
            bid = np.random.exponential(0.5)
            ip_bad = np.random.rand() < 0.05
            feat = [bid, int(ip_bad)]
            label = 1 if bid > 1.2 or ip_bad else 0
            X.append(feat); y.append(label)
        self.clf = LogisticRegression().fit(np.array(X), np.array(y))

    def predict_proba(self, bid: float, ip_bad: int):
        p = self.clf.predict_proba(np.array([[bid, ip_bad]]))[0,1]
        return float(p)