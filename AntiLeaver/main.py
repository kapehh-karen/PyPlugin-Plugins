# -*- coding: utf-8 -*-
from org.bukkit.entity import Player
from org.bukkit import Material
from org.bukkit import Bukkit
from com.herocraftonline.heroes.api.events import HeroLeaveCombatEvent
from com.herocraftonline.heroes.characters.effects import CombatEffect
from org.bukkit import ChatColor
from me.kapehh.main.pluginmanager.vault import PluginVault

PermEx = None
PERM_NO_DROP = "cfactory.leaver.nodrop"

@BukkitListener
class Keks(PyListener):
        
    @PyEventHandler(HeroLeaveCombatEvent)
    def heroleavecombat(self, event):
        
        # Если причина лива - логаут
        if event.getReason() == CombatEffect.LeaveCombatReason.LOGOUT:
            player = event.getHero().getPlayer()
            
            # Если у игрока есть права, то при ливе нет дропа
            if (PermEx is not None) and PermEx.has(None, player.getName(), PERM_NO_DROP):
                return
            
            # Если хп выше 80 процентов, то нет дропа
            healthPercent = int((float(player.getHealth()) / float(player.getMaxHealth())) * 100)
            if healthPercent > 80:
                return
            
            # В цикле проверяем тех, кто в бою с игроком был. Если есть другие игроки, то надо дропать вещи.
            inCombatWithPlayers = False
            for key, value in event.getCombatants().iteritems():
                if isinstance(key, Player):
                    key.sendMessage(u"%sИгрок %s вышел из игры во время боя." % (ChatColor.YELLOW, player.getName()))
                    inCombatWithPlayers = True
            
            if inCombatWithPlayers:
                worldPlayer = player.getWorld()
                locationPlayer = player.getLocation()
                
                # Дропаем инвентарь игрока
                for itemStack in player.getInventory().getContents():
                    if (itemStack is None) or (itemStack.getType() == Material.AIR):
                        continue
                    worldPlayer.dropItem(locationPlayer, itemStack);
                    
                # Дропаем снаряжение игрока
                for itemStack in player.getInventory().getArmorContents():
                    if (itemStack is None) or (itemStack.getType() == Material.AIR):
                        continue
                    worldPlayer.dropItem(locationPlayer, itemStack);
                
                # Очищаем инвентарь игрока
                player.getInventory().setArmorContents([None] * 4) # Шлем, Нагрудник, Штаны, Ботинки
                player.getInventory().clear() # Предметы

@BukkitPlugin
class Plug(PyPlugin):
    def onEnable(self):
        global PermEx
        PermEx = PluginVault.setupPermissions()
        if PermEx is None:
            print "Vault not found!"
