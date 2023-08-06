import argparse
import glob
import json
import logging
import re
from datetime import datetime
from enum import Enum
from os.path import exists, basename, abspath
from typing import Dict, Optional

from dateutil.parser import parse as parse_iso_date

from .bwapi import supported_versions, versions_md5s
from .error import PlayerException
from .utils import md5_file

logger = logging.getLogger(__name__)

SC_BOT_DIR = abspath("bots")


class PlayerRace(Enum):
    PROTOSS = 'P'
    ZERG = 'Z'
    TERRAN = 'T'
    RANDOM = 'R'


class Player:
    name = "noname"
    race = PlayerRace.RANDOM

    def __str__(self):
        return f"{self.__class__.__name__}:{self.name}:{self.race.value}"


class HumanPlayer(Player):
    name = "human"


class BotType(Enum):
    AI_MODULE = "dll"
    EXE = "exe"
    JAVA = "jar"
    JYTHON = "jython"


class BotJsonMeta:
    # required fields:
    name: str
    race: PlayerRace
    botType: BotType

    # optional fields
    description: Optional[str] = None
    update: Optional[datetime] = None  # last updated
    botBinary: Optional[str] = None  # link to website
    bwapiDLL: Optional[str] = None  # link to website
    botProfileURL: Optional[str] = None  # link to website
    javaDebugPort: Optional[int] = None  # optionally allow attaching debugger


class BotPlayer(Player):
    """
    Each bot has following structure in the bots directory:
    - bot.json        bot JSON config file
    - BWAPI.dll       BWAPI.dll to inject into game
    - AI/             bot binaries (as from SSCAIT).
                      In its root must be some executable - EXE, JAR, DLL
    - read/*          all read files that will be mounted

    At the time of creating instance it must have the file system structure satisfied.
    """

    def __init__(self, bot_dir: str):
        self.bot_dir = bot_dir

        self._check_structure()
        self.meta = self._read_meta()
        self.name = self.meta.name
        self.race = self.meta.race
        self.bot_type = self.meta.botType
        self.bot_filename = self._find_bot_filename(self.meta.botType)
        self.bwapi_version = self._find_bwapi_version()

    def _read_meta(self) -> BotJsonMeta:
        with open(f"{self.bot_dir}/bot.json", "r") as f:
            json_spec = json.load(f)

        return self.parse_meta(json_spec)

    def _find_bot_filename(self, bot_type: BotType) -> str:
        expr = f"{self.ai_dir}/*.{bot_type.value}"
        candidate_files = [file for file in glob.glob(expr)
                           if "BWAPI" not in file]

        if len(candidate_files) == 1:
            return list(candidate_files)[0]
        elif len(candidate_files) > 1:
            raise Exception(f"Too many files found as candidates for bot launcher, "
                            f"launcher searched for files {expr}")
        else:
            raise Exception(f"Cannot find bot binary, launcher searched for {expr}")

    @property
    def bot_basefilename(self) -> str:
        return basename(self.bot_filename)

    @property
    def bwapi_dll_file(self):
        return f"{self.bot_dir}/BWAPI.dll"

    @property
    def bot_json_file(self):
        return f"{self.bot_dir}/bot.json"

    @property
    def ai_dir(self):
        return f"{self.bot_dir}/AI"

    @property
    def read_dir(self):
        return f"{self.bot_dir}/read"

    @property
    def write_dir(self):
        return f"{self.bot_dir}/write"

    def _check_structure(self):
        if not exists(f"{self.bot_dir}"):
            raise PlayerException(f"Bot cannot be found in {self.bot_dir}")
        if not exists(self.bot_json_file):
            raise PlayerException(f"Bot JSON config cannot be found in {self.bot_json_file}")
        if not exists(self.bwapi_dll_file):
            raise PlayerException(f"BWAPI.dll cannot be found in {self.bwapi_dll_file}")
        if not exists(f"{self.ai_dir}"):
            raise PlayerException(f"AI folder cannot be found in {self.ai_dir}")
        if not exists(f"{self.read_dir}"):
            raise PlayerException(f"read folder cannot be found in {self.read_dir}")
        if not exists(f"{self.write_dir}"):
            raise PlayerException(f"write folder cannot be found in {self.write_dir}")

    @staticmethod
    def parse_meta(json_spec: Dict) -> BotJsonMeta:
        meta = BotJsonMeta()
        meta.name = json_spec['name']
        meta.race = PlayerRace[json_spec['race'].upper()]
        bot_type = json_spec['botType']
        if bot_type == "JAVA_JNI" or bot_type == "JAVA_MIRROR":
            bot_type = "JAVA"
        meta.botType = BotType[bot_type]

        meta.description = json_spec['description'] if 'description' in json_spec else None
        meta.update = parse_iso_date(json_spec['update']) if 'update' in json_spec else None
        meta.botBinary = json_spec['botBinary'] if 'botBinary' in json_spec else None
        meta.bwapiDLL = json_spec['bwapiDLL'] if 'bwapiDLL' in json_spec else None
        meta.botProfileURL = json_spec['botProfileURL'] if 'botProfileURL' in json_spec else None
        meta.javaDebugPort = json_spec['javaDebugPort'] if 'javaDebugPort' in json_spec else None

        return meta

    def _find_bwapi_version(self):
        bwapi_md5_hash = md5_file(self.bwapi_dll_file)
        if bwapi_md5_hash not in versions_md5s.values():
            raise PlayerException(f"Bot uses unrecognized version of BWAPI, "
                                  f"with md5 hash {bwapi_md5_hash} . Supported versions are: "
                                  f"{', '.join(supported_versions)}")

        version = [version for version, bwapi_hash in versions_md5s.items()
                   if bwapi_hash == bwapi_md5_hash][0]
        if version not in supported_versions:
            raise PlayerException(f"Bot uses unsupported version of BWAPI: {version}. "
                                  f"Supported versions are: "
                                  f"{', '.join(supported_versions)}")
        return version


_races = "|".join([race.value for race in PlayerRace])
_expr = re.compile("^[a-zA-Z0-9_][a-zA-Z0-9_. -]{0,40}"
                   "(\:(" + _races + "))?$")


def bot_regex(bot: str):
    if not _expr.match(bot):
        raise argparse.ArgumentTypeError(
            f"Bot specification '{bot}' is not valid, should match {_expr.pattern}")
    return bot


def check_bot_exists(bot: str, bot_dir: str):
    # this will raise exception if bot doesn't exist
    # or doesn't have proper structure
    BotPlayer(f"{bot_dir}/{bot}")
