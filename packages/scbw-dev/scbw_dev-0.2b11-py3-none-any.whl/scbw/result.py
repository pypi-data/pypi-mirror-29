import json
import logging
from typing import List, Optional

from .logs import find_logs, find_frames, find_replays, find_results
from .player import Player

logger = logging.getLogger(__name__)


class ScoreResult:
    def __init__(self,
                 is_winner: bool,
                 is_crashed: bool,
                 building_score: int,
                 kill_score: int,
                 razing_score: int,
                 unit_score: int,
                 ):
        self.is_winner = is_winner
        self.is_crashed = is_crashed
        self.building_score = building_score
        self.kill_score = kill_score
        self.razing_score = razing_score
        self.unit_score = unit_score

    @staticmethod
    def load_result(result_file: str):
        with open(result_file, "r") as f:
            v = json.load(f)

        return ScoreResult(
            v['is_winner'],
            v['is_crashed'],
            v['building_score'],
            v['kill_score'],
            v['razing_score'],
            v['unit_score'],
        )


class GameResult:
    def __init__(self,
                 game_name: str,
                 players: List[Player],
                 game_time: float,
                 is_realtime_outed: bool,
                 map_dir: str,
                 log_dir: str):
        #
        self.game_name = game_name
        self.game_time = game_time
        self.players = players

        self.map_dir = map_dir
        self.log_dir = log_dir

        self._is_crashed = None
        self._is_gametime_outed = None
        self.is_realtime_outed = is_realtime_outed

        self._winner_player = None
        self._nth_winner_player = None
        self._loser_player = None
        self._nth_loser_player = None

        self._log_files = None
        self._replay_files = None
        self._frame_files = None
        self._result_files = None

        self.score_results = []

        self._is_processed = False

    def _process_files(self):
        # this whole processing assumes 1v1 bot vs bot games
        if self._is_processed:
            return

        self._is_processed = True

        if self.is_realtime_outed:
            return

        num_players = len(self.players)

        if len(self.result_files) != num_players:
            logger.warning(f"Not all result files have been recorded for game '{self.game_name}'")
            logger.warning(f"Expected {num_players} result files, got {len(self.result_files)}")
            logger.warning("Assuming a crash happened.")
            self._is_crashed = True
            return

        results = {result_file: ScoreResult.load_result(result_file)
                   for result_file in sorted(self.result_files)}
        if any(result.is_crashed for result in results.values()):
            logger.warning(f"Some of the players crashed in game '{self.game_name}'")
            self._is_crashed = True
            return

        if not any(result.is_winner for result in results.values()):
            logger.warning(f"No winner found in game '{self.game_name}'")
            logger.warning("Assuming a crash happened.")
            self._is_crashed = True
            return

        if sum(int(result.is_winner) for result in results.values()) > 1:
            logger.warning(f"There are multiple winners of a game '{self.game_name}'")
            logger.warning("This can indicates possible game result corruption!")
            logger.warning("Assuming a crash happened.")
            self._is_crashed = True
            return

        winner_result_file = [file for file, result in results.items() if result.is_winner][0]
        nth_player = int(winner_result_file.replace("_results.json", "").split("_")[-1])

        self._nth_winner_player = nth_player
        self._nth_loser_player = 1 - nth_player
        self._winner_player = self.players[self._nth_winner_player]
        self._loser_player = self.players[self._nth_loser_player]
        self._is_crashed = False
        # todo: implement, maybe according to SSCAIT rules?
        self._is_gametime_outed = False
        self.score_results = results

    @property
    def replay_files(self) -> List[str]:
        if self._replay_files is None:
            self._replay_files = find_replays(self.map_dir, self.game_name)
        return self._replay_files

    @property
    def log_files(self) -> List[str]:
        if self._log_files is None:
            self._log_files = find_logs(self.log_dir, self.game_name)
        return self._log_files

    @property
    def frame_files(self) -> List[str]:
        if self._frame_files is None:
            self._frame_files = find_frames(self.log_dir, self.game_name)
        return self._frame_files

    @property
    def result_files(self) -> List[str]:
        if self._result_files is None:
            self._result_files = find_results(self.log_dir, self.game_name)
        return self._result_files

    # Bunch of getters
    @property
    def is_valid(self) -> bool:
        self._process_files()
        return not self.is_crashed and \
               not self.is_gametime_outed and \
               not self.is_realtime_outed

    @property
    def is_crashed(self) -> bool:
        self._process_files()
        return self._is_crashed

    @property
    def is_gametime_outed(self) -> bool:
        self._process_files()
        return self._is_gametime_outed

    @property
    def winner_player(self) -> Optional[Player]:
        self._process_files()
        return self._winner_player

    @property
    def nth_winner_player(self) -> Optional[int]:
        self._process_files()
        return self._nth_winner_player

    @property
    def loser_player(self) -> Optional[Player]:
        self._process_files()
        return self._loser_player

    @property
    def nth_loser_player(self) -> Optional[int]:
        self._process_files()
        return self._nth_loser_player
