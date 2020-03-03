from CustomLinearRegression import CustomLinearRegression
from DBConnectionManager import DBConnectionManager
from WikiTable import WikiTable
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd


def main():
    dbConnectionManager = DBConnectionManager()

    museumsTable = WikiTable.load("Museums", dbConnectionManager.getDBConnection())
    citiesTable = WikiTable.load("Cities", dbConnectionManager.getDBConnection())

    mergedTable = pd.merge(museumsTable, citiesTable, left_on='City', right_on='City')

    print(mergedTable)

    attendance = mergedTable["VisitorsPerYear"].to_numpy()
    population = mergedTable["Population"].to_numpy()

    attendance = attendance.reshape(-1, 1)
    population = population.reshape(-1, 1)
    population = np.divide(population, 1000000)
    attendance = np.divide(attendance, 1000000)

    regr = CustomLinearRegression()

    regr.fit(population, attendance)
    print(regr.score(population, attendance))

    x_pred = [min(population), max(population)]
    y_pred = regr.predict(x_pred)
    plt.scatter(population, attendance, color='b')
    plt.plot(x_pred, y_pred, color='k')

    plt.title("Number of visitors with respect to city population")
    plt.xlabel("City population (millions)")
    plt.ylabel("Museum attendance (millions)")

    plt.show()


if __name__ == '__main__':
    main()
