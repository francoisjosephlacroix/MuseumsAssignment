class CustomLinearRegression():

    def __init__(self, learning_rate=0.005, maxNbIterations=500, epsilon=0.001):
        self.learning_rate = learning_rate
        self.maxNbIterations = maxNbIterations
        self.epsilon = epsilon

    def fit(self, X, Y):
        self.coeff = 0
        self.intercept = 0

        self.loss = self.score(X, Y)

        for i in range(self.maxNbIterations):
            print("Iteration: {}".format(i))

            Y_preds = self.predict(X)

            d_coeff = 0
            d_intercept = 0

            for j in range(len(X)):
                x = X[j]
                y = Y[j]
                y_pred = Y_preds[j]

                d_coeff -= x * (y - y_pred)
                d_intercept -= (y - y_pred)

            d_coeff = (-2 / len(X)) * d_coeff
            d_intercept = (-2 / len(X)) * d_intercept

            self.coeff += d_coeff * self.learning_rate
            self.intercept += d_intercept * self.learning_rate

            print("Coefficient derivative: {}".format(d_coeff))
            print("Intercept derivative: {}".format(d_intercept))
            print("Coefficient: {}".format(self.coeff))
            print("Intercept: {}".format(self.intercept))

            currentLoss = self.score(X, Y)
            print("Loss: {}".format(currentLoss))

            if (abs(self.loss - currentLoss) < self.epsilon):
                break

            self.loss = currentLoss

        return self.loss

    def predict(self, X):
        y = []
        for x in X:
            y_pred = self.coeff * x + self.intercept
            y.append(y_pred)

        return y

    def score(self, X, Y):
        loss = 0

        for i in range(len(X)):
            x = X[i]
            y = Y[i]
            y_pred = self.predict(x)[0]

            loss += (y - y_pred) ** 2

        loss /= len(X)
        return loss
