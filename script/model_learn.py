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

import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib import font_manager, rc
import seaborn as sns
from forecast.models import FileList

# 라인 그래프
def savefig_lineplot(dates, real_value, pred_value, folder_name):
    sns.set(style="whitegrid", palette="pastel")
    plt.figure(figsize=(10, 6))
    print("dates:", dates[-48:])
    print("real_value:", real_value[-48:])
    print("pred_value:", pred_value[-48:-25]+real_value[-24]+pred_value[-24:])
    sns.lineplot(x=dates[-48:], y=real_value[-48:], label="Actual", color="red")
    sns.lineplot(x=dates[-48:], y=pred_value[-48:], label="Prediction", color="blue")
    plt.xlabel("Date")
    plt.ylabel("Value")
    # plt.title("line Plot of Prediction vs. Actual")
    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    plt.savefig(folder_name + "/lineplot.png")
    plt.close()


# 산점도 그래프
def savefig_scatter(dates, real_value, pred_value, folder_name):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(
        x=dates, y=real_value, label="Actual", color="red", marker="x", s=100
    )
    sns.scatterplot(
        x=dates, y=pred_value, label="Prediction", color="blue", marker="o", s=100
    )
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.title("Scatter Plot of Prediction vs. Actual")
    plt.legend()
    plt.xticks(rotation=45)  # Rotate x-axis labels
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    plt.savefig(folder_name + "/scatter.png")
    plt.close()


# 히스토그램 그래프
def savefig_histogram(dates, real_value2, pred_value2, folder_name):
    plt.figure(figsize=(10, 6))

    sns.histplot(real_value2, label="Actual", color="red", kde=True)
    sns.histplot(pred_value2, label="Prediction", color="blue", kde=True)

    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Prediction vs. Actual")

    plt.legend()

    plt.savefig(folder_name + "/histogram.png")
    plt.close()


# 박스 플롯 그래프
def savefig_boxplot(dates, real_value2, pred_value2, folder_name):
    plt.figure(figsize=(10, 6))

    sns.boxplot(data=[real_value2, pred_value2], palette=["red", "blue"])

    plt.ylabel("Value")
    plt.title("Box Plot of Prediction vs. Actual")

    plt.xticks([0, 1], ["Actual", "Prediction"])
    plt.savefig(folder_name + "/boxplot.png")
    plt.close()


# 바이올린 플롯 그래프
def savefig_violinplot(dates, real_value2, pred_value2, folder_name):
    plt.figure(figsize=(10, 6))

    sns.violinplot(data=[real_value2, pred_value2], palette=["red", "blue"])

    plt.ylabel("Value")
    plt.title("Violin Plot of Prediction vs. Actual")

    plt.xticks([0, 1], ["Actual", "Prediction"])

    plt.savefig(folder_name + "/violinplot.png")
    plt.close()


def sarima_learn(data_h_df, file_id):
    file_instance = FileList.objects.get(id=file_id)
    file_path = file_instance.파일
    folder_name = "media/" + os.path.dirname(str(file_path))
    p, q = range(0, 2), range(0, 2)
    d = range(0, 1)
    P, Q = range(0, 2), range(0, 2)
    D = range(0, 1)
    m = 24
    trend_pdq = list(product(p, d, q))
    seasonal_pdq = [
        (candi[0], candi[1], candi[2], m) for candi in list(product(P, D, Q))
    ]

    file_list = []

    cut_idx = round(len(data_h_df["val"]) * 0.8)

    # train_df = data_h_df["val"][:cut_idx]
    # test_df = data_h_df["val"][cut_idx:]
    train_df = data_h_df[:cut_idx]
    test_df = data_h_df[cut_idx:]

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
                    AIC.append(result.aic)
                    SARIMAX_order.append([trend_param, seasonal_params])
                except:
                    continue

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

        fit_ts_sarimax.save("./ld_sarima_" + file_id + ".pkl")

        one_list = []
        one_list.append(
            [
                "test",
                SARIMAX_order[AIC.index(min(AIC))][0],
                SARIMAX_order[AIC.index(min(AIC))][1],
                100 - val_df["dif/val"].mean(),
            ]
        )

        one_list = []
        print("모델수행 완료")

        ## 24 시간 예측
        def forecast_24_step(model):
            pred = model.get_forecast(24)
            return pred.predicted_mean, pred.conf_int()

        # ## df 만들기
        pred, ci = forecast_24_step(fit_ts_sarimax)
        actual_df = data_h_df.copy()
        actual_df.columns = ["real_value"]
        pred.to_frame(name="val").index.name = "dt"
        pred_df = pred.to_frame(name="pred_value")
        df = pd.concat([actual_df, pred_df])
        # df.to_csv("./file_id.csv")
        dates = df.index
        pred_value = df.pred_value
        real_value = df.real_value
        pred_value2 = pred_value.copy()
        real_value2 = real_value.copy()
        real_value2 = [x for x in real_value2 if x != "null"]
        pred_value2 = [x for x in pred_value2 if x != "null"]


        # 이미지 저장
        savefig_lineplot(dates, real_value, pred_value, folder_name)
        savefig_scatter(dates, real_value, pred_value, folder_name)
        savefig_histogram(dates, real_value, pred_value, folder_name)
        savefig_boxplot(dates, real_value, pred_value, folder_name)
        savefig_violinplot(dates, real_value, pred_value, folder_name)
    except Exception as e:
        print("예외발생")
        print(e)
        file_list.append(["test", "예외발생"])


# sarima_learn(data_h_df)
