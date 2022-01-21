import pandas as pd
import os
import numpy as np

econOneLinerCV1H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\economicOneLinerCV1H.csv"
)
econOneLinerCV2H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\economicOneLinerCV2H.csv"
)
econOneLinerPshigoda = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\economicOneLinerPshigoda1H.csv"
)

econOneLinerIrvin = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\economicOneLinerIrvinSisters1H.csv"
)

monthlyCashFlowIrvinSisters1H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowRollupFinal2022IrvinSisters1HForecast.csv"
)

monthlyCashFlowPshigoda1H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowRollupFinal2022Pshigoda1HForecast.csv"
)

monthlyCashFlowCV1H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowRollupFinal2022CV1HForecast.csv"
)

monthlyCashFlowCV2H = pd.read_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowRollupFinal2022CV2HForecast.csv"
)


econLinerRollUp = pd.DataFrame()
monthlyCashFlowCombine = pd.DataFrame()

monthlyCashFlowCombine = monthlyCashFlowPshigoda1H.copy()
monthlyCashFlowCombine = monthlyCashFlowCombine.append(
    monthlyCashFlowIrvinSisters1H, ignore_index=True
)
monthlyCashFlowCombine = monthlyCashFlowCombine.append(
    monthlyCashFlowCV1H, ignore_index=True
)
monthlyCashFlowCombine = monthlyCashFlowCombine.append(
    monthlyCashFlowCV2H, ignore_index=True
)

econOneLinerCV1H["Name"] = "Cotton Valley 1H"
econOneLinerCV2H["Name"] = "Cotton Valley 2H"
econOneLinerIrvin["Name"] = "Irvin Sister 1H"
econOneLinerPshigoda["Name"] = "Pshigoda 1H"

econOneLinerCV1H.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\testCV.csv"
)

econLinerRollUp = econOneLinerCV1H.copy()
econLinerRollUp = econLinerRollUp.append(econOneLinerCV2H, ignore_index=True)
econLinerRollUp = econLinerRollUp.append(econOneLinerIrvin, ignore_index=True)
econLinerRollUp = econLinerRollUp.append(econOneLinerPshigoda, ignore_index=True)

econLinerRollUp.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\rollupEconOneLiner2022.csv",
    index=False,
)

monthlyCashFlowCombine.to_csv(
    r"C:\Users\MichaelTanner\Documents\code_doc\king\data\monthlyCashFlowCombine2022Forecast.csv",
    index=False,
)

print("yay")
