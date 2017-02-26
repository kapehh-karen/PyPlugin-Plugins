from org.bukkit import Location
from org.bukkit import Bukkit
from org.bukkit.entity import Monster, Animals


class WorldPoint:
    def __init__(self, **kwargs):
        self.x = kwargs.get("x")
        self.y = kwargs.get("y")
        self.z = kwargs.get("z")

    def __str__(self):
        return "[X={}; Y={}; Z={}]".format(self.x, self.y, self.z)


class EntityRemover:
    def __init__(self, name, output_callback=None):
        self.output_callback = output_callback
        self.world = Bukkit.getWorld(name)

    def _get_bukkit_location(self, pos):
        return Location(self.world, pos.x, pos.y, pos.z)

    def _remove_entities(self, chunk):
        removed = 0

        for entity in chunk.getEntities():
            # Check Java interface of entity
            if isinstance(entity, Monster) or isinstance(entity, Animals):
                entity.remove()
                removed += 1

        if self.output_callback:
            self.output_callback(
                "Chunk [{}, {}] cleared! Removed {} mobs.".format(
                    chunk.getX(),
                    chunk.getZ(),
                    removed))

    def set_output_callback(callback):
        self.output_callback = callback

    def clear(self, pos1, pos2):
        loc1 = self._get_bukkit_location(pos1)
        loc2 = self._get_bukkit_location(pos2)
        chunk1 = self.world.getChunkAt(loc1)
        chunk2 = self.world.getChunkAt(loc2)

        # If equals chunk
        if chunk1.getX() == chunk2.getX() and chunk1.getZ() == chunk2.getZ():
            self._remove_entities(chunk1)
            return

        minX, minZ = min(chunk1.getX(), chunk2.getX()), max(chunk1.getX(), chunk2.getX())
        maxX, maxZ = min(chunk1.getZ(), chunk2.getZ()), max(chunk1.getZ(), chunk2.getZ())
        for x in xrange(minX, maxX + 1):
            for z in xrange(minZ, maxZ + 1):
                chunk = self.world.getChunkAt(x, z)
                self._remove_entities(chunk)
