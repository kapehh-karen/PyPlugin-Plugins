# encoding: utf-8

from com.palmergames.bukkit.towny.event import TownAddResidentEvent
from org.bukkit import Bukkit
from org.bukkit import ChatColor
from org.bukkit.event.entity import PlayerDeathEvent
from org.bukkit.event.player import PlayerRespawnEvent
from com.palmergames.bukkit.towny.object import TownyUniverse


PERM_HEROES = "cfactoryfractions.fraction.heroes"
PERM_OUTCAST = "cfactoryfractions.fraction.outcast"
PERM_NEWBIE = "cfactoryfractions.fraction.newbie"
PERM_ADMIN = "cfactoryfractions.admin"

WORLD_HEROES = None
WORLD_OUTCAST = None


@BukkitPlugin
class CFFractions(PyPlugin):


    def onEnable(self):
        global WORLD_HEROES
        global WORLD_OUTCAST

        WORLD_HEROES = Bukkit.getWorld("Overworld")
        WORLD_OUTCAST = Bukkit.getWorld("DeepWorld")

        if WORLD_HEROES is None:
            WORLD_HEROES = Bukkit.getWorlds().get(0)

        if WORLD_OUTCAST is None:
            WORLD_OUTCAST = Bukkit.getWorlds().get(0)


@BukkitListener
class TownyListeners(PyListener):


    @PyEventHandler(PlayerDeathEvent)
    def event_player_death(self, event):
        player = event.getEntity()
        if player.hasPermission(PERM_NEWBIE) or player.hasPermission(PERM_ADMIN):
            event.setKeepInventory(True)


    @PyEventHandler(PlayerRespawnEvent)
    def event_respawn(self, event):
        player = event.getPlayer()

        playerIsHero = player.hasPermission(PERM_HEROES)
        playerIsOutcast = player.hasPermission(PERM_OUTCAST)
        playerWithoutTown = True

        try:
            resident = TownyUniverse.getDataSource().getResident(player.getName())
            if (resident is not None) and (not resident.isNPC()):
                playerWithoutTown = not resident.hasTown()
        except:
            pass

        if playerWithoutTown:

            if playerIsHero:
                event.setRespawnLocation(WORLD_HEROES.getSpawnLocation())
            elif playerIsOutcast:
                event.setRespawnLocation(WORLD_OUTCAST.getSpawnLocation())


    @PyEventHandler(TownAddResidentEvent)
    def event_resident_add(self, event):

        residentJoined = event.getResident()
        if residentJoined is None:
            return

        town = event.getTown()
        if town is None:
            return

        player = Bukkit.getPlayer(residentJoined.getName())
        if (player is None) or (not player.isOnline()):
            return

        hasResidentsInTown = False
        findedResident = False
        playerInTown = None
        for resTown in town.getResidents():
            if (resTown == residentJoined):
                continue

            hasResidentsInTown = True

            if resTown.isNPC():
                continue

            playerInTown = Bukkit.getPlayer(resTown.getName())
            if (playerInTown is None) or (not playerInTown.isOnline()) or (playerInTown.hasPermission(PERM_ADMIN)):
                # Если игрок не в сети, или этот игрок Админ, тогда продолжаем поиск.
                # Из-за админа мы не можем заинвайтить игрока в город, ибо может начаться каша в городе!
                continue

            findedResident = True
            break

        # Если событие вызывается когда игрок создает город,
        # то надо игнорировать все проверки и просто ничего не делать
        if not hasResidentsInTown:
            return

        needRemove = False
        if findedResident:
            isTownHero = playerInTown.hasPermission(PERM_HEROES)
            isTownOutcast = playerInTown.hasPermission(PERM_OUTCAST)
            isResHero = player.hasPermission(PERM_HEROES)
            isResOutcast = player.hasPermission(PERM_OUTCAST)
            isResAdmin = player.hasPermission(PERM_ADMIN)

            # print "isTownHero: %s, isTownOutcast: %s, isResHero: %s, isResOutcast: %s, isResAdmin: %s" % (isTownHero, isTownOutcast, isResHero, isResOutcast, isResAdmin)

            isCorrect = isResAdmin or (isTownHero and isResHero) or (isTownOutcast and isResOutcast)

            if not isCorrect:
                needRemove = True
                player.sendMessage(u"%sВы не можете вступить в город противоположной фракции." % ChatColor.RED)

        else:
            needRemove = True
            player.sendMessage(u"%sВ данный момент в городе нет игроков в онлайн! Подождите пока кто-нибудь появится онлайн." % ChatColor.RED)

        if needRemove:
            try:
                town.removeResident(residentJoined)
            except:
                pass