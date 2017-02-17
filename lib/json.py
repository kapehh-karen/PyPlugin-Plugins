from org.bukkit.entity import Player
from org.bukkit.inventory import ItemStack
from org.bukkit.util.io import BukkitObjectInputStream
from org.bukkit.util.io import BukkitObjectOutputStream

from java.io import ByteArrayInputStream
from java.io import ByteArrayOutputStream

import json
import binascii


# Bukkit JSON

ITEMSTACK_JSON_NAME = "bukkit::itemstack"


class BukkitJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, ItemStack):
            return None
        byte_array_out = ByteArrayOutputStream()
        bukkit_out = BukkitObjectOutputStream(byte_array_out)
        bukkit_out.writeObject(obj)
        bukkit_out.flush()
        bukkit_out.close()
        raw_bytes = byte_array_out.toByteArray()
        return {ITEMSTACK_JSON_NAME: binascii.hexlify(raw_bytes)}


class BukkitJSONDecoder:
    def from_json(self, json_object):
        if not ITEMSTACK_JSON_NAME in json_object:
            return json_object
        raw_bytes = binascii.unhexlify(json_object[ITEMSTACK_JSON_NAME])
        byte_array_in = ByteArrayInputStream(raw_bytes)
        bukkit_in = BukkitObjectInputStream(byte_array_in)
        bukkit_item = bukkit_in.readObject()
        bukkit_in.close()
        return bukkit_item

    def decode(self, json_string):
        return json.JSONDecoder(object_hook=self.from_json).decode(json_string)


class BukkitJSON:
    encoder = BukkitJSONEncoder()
    decoder = BukkitJSONDecoder()