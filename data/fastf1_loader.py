import fastf1
import pandas as pd


class FastF1Loader:

    def __init__(self, cache_dir="cache"):
        fastf1.Cache.enable_cache(cache_dir)

    def load_session(
        self,
        year: int,
        event: str,
        session_type: str = "R"
    ):
        """
        session_type:
            R = Race
            Q = Qualifying
            FP1/FP2/FP3
        """

        session = fastf1.get_session(
            year,
            event,
            session_type
        )

        session.load()

        return session

    def get_laps(
        self,
        year,
        event,
        session_type="R"
    ):

        session = self.load_session(
            year,
            event,
            session_type
        )

        laps = session.laps.copy()

        laps["LapTimeSeconds"] = (
            laps["LapTime"]
            .dt.total_seconds()
        )

        return laps

    def get_weather(
        self,
        year,
        event,
        session_type="R"
    ):

        session = self.load_session(
            year,
            event,
            session_type
        )

        return session.weather_data

    def get_results(
        self,
        year,
        event,
        session_type="Q"
    ):

        session = self.load_session(
            year,
            event,
            session_type
        )

        return session.results