# PyPlugin Sessions


class PlayerSession:
    sessions = {}

    @staticmethod
    def get(player, force_read=False):
        if not isinstance(player, Player):
            raise Exception('Support only for <Player>')

        filename = str(player.getUniqueId().toString())
        if (not force_read) and (filename in PlayerSession.sessions):
            return PlayerSession.sessions[filename]

        full_name = os.path.join(__internal_data__["sessiondir"], filename + ".json")
        if not os.path.isfile(full_name):
            empty_obj = {
                'name': player.getName()
            }
            PlayerSession.sessions[filename] = empty_obj
            return empty_obj

        with open(full_name, 'r') as content_file:
            content = content_file.read()
            json_obj = BukkitJSON.decoder.decode(content)
            PlayerSession.sessions[filename] = json_obj
            return json_obj

    @staticmethod
    def save(player):
        if not isinstance(player, Player):
            raise Exception('Support only for <Player>')

        filename = str(player.getUniqueId().toString())
        if filename not in PlayerSession.sessions:
            return None

        if not os.path.exists(__internal_data__["sessiondir"]):
            os.mkdir(__internal_data__["sessiondir"])

        full_name = os.path.join(__internal_data__["sessiondir"], filename + ".json")
        with open(full_name, 'w') as content_file:
            json_string = BukkitJSON.encoder.encode(PlayerSession.sessions[filename])
            content_file.write(json_string)
            return json_string
