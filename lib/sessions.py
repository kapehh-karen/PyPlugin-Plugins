from org.bukkit.entity import Player
from org.bukkit import Bukkit

import os

from .bukkitjson import BukkitJSON

# PyPlugin Sessions


class PlayerSession:
    MAX_CACHE_THRESHOLD = 150
    session_dir = "sessions"
    sessions = {}

    @staticmethod
    def set_path(*args):
        PlayerSession.session_dir = os.path.join(*args)

    @staticmethod
    def clean_sessions():
        players = [str(x.getUniqueId().toString()) for x in Bukkit.getOnlinePlayers()]
        for k, v in PlayerSession.sessions.iteritems():
            if k not in players:
                del PlayerSession.sessions[k]

    @staticmethod
    def get(player, force_read=False):
        if not isinstance(player, Player):
            raise Exception('Support only for <Player>')

        filename = str(player.getUniqueId().toString())
        if (not force_read) and (filename in PlayerSession.sessions):
            return PlayerSession.sessions[filename]

        if len(PlayerSession.sessions) > PlayerSession.MAX_CACHE_THRESHOLD:
            PlayerSession.clean_sessions()

        full_name = os.path.join(PlayerSession.session_dir, filename + ".json")
        if not os.path.isfile(full_name):
            empty_obj = {
                'name': player.getName()
            }
            PlayerSession.sessions[filename] = empty_obj
            return empty_obj

        with open(full_name, 'r') as content_file:
            content = content_file.read()
            json_obj = BukkitJSON.decode(content)
            PlayerSession.sessions[filename] = json_obj
            return json_obj

    @staticmethod
    def save(player):
        if not isinstance(player, Player):
            raise Exception('Support only for <Player>')

        filename = str(player.getUniqueId().toString())
        if filename not in PlayerSession.sessions:
            return None

        if not os.path.exists(PlayerSession.session_dir):
            os.mkdir(PlayerSession.session_dir)

        full_name = os.path.join(PlayerSession.session_dir, filename + ".json")
        with open(full_name, 'w') as content_file:
            json_string = BukkitJSON.encode(PlayerSession.sessions[filename])
            content_file.write(json_string)
            return json_string
