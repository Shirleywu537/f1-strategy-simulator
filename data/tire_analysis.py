import numpy as np
import pandas as pd


class TireAnalyzer:

    def __init__(self, laps_df):
        self.laps = laps_df

    def fit_degradation(
        self,
        compound
    ):
        """
        Returns:
            slope (sec/lap)
        """

        df = self.laps.copy()

        df = df[
            df["Compound"] == compound
        ]

        df = df.dropna(
            subset=[
                "TyreLife",
                "LapTimeSeconds"
            ]
        )

        if len(df) < 10:
            return None

        x = df["TyreLife"]
        y = df["LapTimeSeconds"]

        slope, intercept = np.polyfit(
            x,
            y,
            1
        )

        return {
            "compound": compound,
            "degradation_rate": slope,
            "base_time": intercept
        }

    def analyze_all(self):

        compounds = [
            "SOFT",
            "MEDIUM",
            "HARD"
        ]

        results = {}

        for compound in compounds:

            result = self.fit_degradation(
                compound
            )

            if result:
                results[compound] = result

        return results