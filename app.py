from flask import Flask
import pandas as pd
import numpy as np
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import json

app = Flask(__name__)

@app.route("/")
def homepage():
    boston_data = load_boston()
    df = pd.DataFrame(boston_data.data,columns=boston_data.feature_names)

    # Sets the target column
    df['target'] = pd.Series(boston_data.target)
    df.rename({'target': 'MEDV'}, axis=1, inplace=True)
    df['MEDV'] = df['MEDV'] * 1000

    # Separate training from testing data
    X = df.drop('MEDV',axis=1)
    y = df['MEDV']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=101)

    # Create and train the model
    lm = LinearRegression()
    lm.fit(X_train, y_train)

    df = pd.DataFrame(lm.coef_, X.columns, columns=['Coeff'])

    df_str = df.to_html()

    html_str = """\
    <html>
      <head></head>
      <body>
        <p>Here are the coefficients for a linear regression model:
            To understand what the coefficients are doing, they read like this:

                "For one unit of (CRIM), the value of the house (MEDV) 'increases' by ≈ -77"
                "For one unit of (CHAS), the value of the house (MEDV) increases by ≈ 4133"

           {df_str}
        </p>
      </body>
    </html>
    """.format(df_str=df_str)

    return html_str

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
    

