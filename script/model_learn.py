import warnings

warnings.filterwarnings("ignore")
import os
import glob
from datetime import datetime
import io
import pandas as pd
import numpy as np

import statsmodels.api as sm


from itertools import product
from tqdm import tqdm

import asyncio

# data_h_df = pd.read_csv('./temp_data.csv', index_col='dt', parse_dates=['dt'])


async def sarima_learn(data_h_df):
    print("sarima_learn 잘 돌고 있니?")
    p, q = range(0, 3), range(0, 3)
    d = range(0, 1)
    P, Q = range(0, 3), range(0, 3)
    D = range(0, 1)
    m = 24
    trend_pdq = list(product(p, d, q))
    seasonal_pdq = [
        (candi[0], candi[1], candi[2], m) for candi in list(product(P, D, Q))
    ]

    # all_list = data_h_df.TABLE_INDEX.unique()
    # ld_nm_list=all_list[:]
    # ld_nm_list=all_list[5:15]

    file_list = []

    # print('부하명 : ', ld_nm)
    ## 최소학습
    # train_df = data_h_df['DIS'][len(data_h_df[data_h_df['TABLE_INDEX'] == ld_nm]) - (24*60):len(data_h_df[data_h_df['TABLE_INDEX'] == ld_nm]) - (24*30)]
    # test_df = data_h_df['DIS'][len(data_h_df[data_h_df['TABLE_INDEX'] == ld_nm]) - (24*30):]
    cut_idx = round(len(data_h_df["val"]) * 0.8)

    train_df = data_h_df["val"][:cut_idx]
    test_df = data_h_df["val"][cut_idx:]
    print(train_df)

    train_df = train_df.asfreq("H", method="ffill")
    test_df = test_df.asfreq("H", method="ffill")
    Y_train_feR = train_df.copy()
    Y_test_feR = test_df.copy()
    Y_train_feR = Y_train_feR + 0.00000000000000000001
    Y_test_feR = Y_test_feR + 0.00000000000000000001

    try:
        ##  AUTO SARIMAX (최적파라미터)
        AIC = []
        SARIMAX_order = []
        for trend_param in tqdm(trend_pdq):
            for seasonal_params in seasonal_pdq:
                try:
                    result = sm.tsa.SARIMAX(
                        Y_train_feR,
                        trend="c",
                        order=trend_param,
                        seasonal_order=seasonal_params,
                    ).fit()
                    print(
                        "Fit SARIMAX: trend_order={} seasonal_order={} AIC={}, BIC={}".format(
                            trend_param,
                            seasonal_params,
                            result.aic,
                            result.bic,
                            end="\r",
                        )
                    )
                    AIC.append(result.aic)
                    SARIMAX_order.append([trend_param, seasonal_params])
                except:
                    continue
        ## Parameter Selection
        print(
            "The smallest AIC is {} for model SARIMAX{}x{}".format(
                min(AIC),
                SARIMAX_order[AIC.index(min(AIC))][0],
                SARIMAX_order[AIC.index(min(AIC))][1],
            )
        )

        fit_ts_sarimax = sm.tsa.SARIMAX(
            Y_train_feR,
            trend="c",
            order=SARIMAX_order[AIC.index(min(AIC))][0],
            seasonal_order=SARIMAX_order[AIC.index(min(AIC))][1],
        ).fit()

        ## Prediction
        pred_tr_ts_sarimax = fit_ts_sarimax.predict()
        pred_te_ts_sarimax = fit_ts_sarimax.get_forecast(
            steps=len(Y_test_feR)
        ).predicted_mean
        pred_te_ts_sarimax_ci = fit_ts_sarimax.get_forecast(
            steps=len(Y_test_feR)
        ).conf_int()

        def forecast_one_step():
            pred = fit_ts_sarimax.get_forecast(1)
            return pred.predicted_mean, pred.conf_int()

        result_df = pd.DataFrame()
        res = pd.DataFrame()
        for values in Y_test_feR.val.values:
            pred, ci = forecast_one_step()
            result_df = pd.concat([pd.DataFrame({"predict": pred}), ci], axis=1)
            res = pd.concat([res, result_df])
            fit_ts_sarimax = fit_ts_sarimax.extend(np.array([values]))

        val_df = pd.concat([pd.DataFrame(res.predict), Y_test_feR], axis=1)
        val_df["dif"] = (val_df.predict - val_df.val).abs()
        val_df["dif/val"] = (val_df["dif"] / val_df["val"] * 100).abs()

        file_list.append(
            [
                "test",
                SARIMAX_order[AIC.index(min(AIC))][0],
                SARIMAX_order[AIC.index(min(AIC))][1],
                100 - val_df["dif/val"].mean(),
            ]
        )
        fit_ts_sarimax.save("./ld_sarima_" + ".pkl")

        one_list = []
        one_list.append(
            [
                "test",
                SARIMAX_order[AIC.index(min(AIC))][0],
                SARIMAX_order[AIC.index(min(AIC))][1],
                100 - val_df["dif/val"].mean(),
            ]
        )
        with open("./prameter.csv", "a") as f:
            for param in one_list:
                print(str(param))
                f.writelines("%s\n" % str(param))
        one_list = []

    except:
        print("예외발생")
        file_list.append(["test", "예외발생"])


# sarima_learn(data_h_df)
