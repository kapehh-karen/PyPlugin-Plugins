# -*- coding: utf-8 -*-

from org.bukkit.entity import Player
from org.bukkit.event.player import PlayerJoinEvent
from org.bukkit.event.player import PlayerQuitEvent
from org.bukkit.event.player import PlayerCommandPreprocessEvent
from org.bukkit.event.entity import PlayerDeathEvent
from org.bukkit import ChatColor
from org.bukkit import Bukkit
from me.kapehh.main.pluginmanager.vault import PluginVault

import re


LINKS_TEXT = u"""{2}{3}========== [ Ц-Фактори 2 (Ссылки) ] =========={1}
Официальный сайт: {0}http://c-factory2.pw{1}
Правила сервера: {0}http://c-factory2.pw/rules{1}
Гайд для начинающих: {0}https://vk.com/topic-29987531_34308374{1}
Классы Героев: {0}https://vk.com/topic-29987531_34131838{1}
Классы Изгоев: {0}https://vk.com/topic-29987531_34131951{1}
Основные команды сервера: {0}https://vk.com/topic-29987531_34245639{1}
{2}{3}=============================================={1}""".format(ChatColor.AQUA, ChatColor.RESET, ChatColor.GOLD, ChatColor.BOLD)


@BukkitListener
class Listnr(PyListener):


    @PyEventHandler(PlayerJoinEvent)
    def join(self, event):
        event.setJoinMessage("")


    @PyEventHandler(PlayerQuitEvent)
    def quit(self, event):
        event.setQuitMessage("")


    @PyEventHandler(PlayerCommandPreprocessEvent)
    def cmd(self, event):
        if event.isCancelled():
            return

        cmdName = event.getMessage()
        player = event.getPlayer()

        if cmdName == "/kill":
            player.setHealth(0)
            event.setCancelled(True)

        elif cmdName == "/links":
            player.sendMessage(LINKS_TEXT)
            event.setCancelled(True)

        elif cmdName == "/spawn":
            isHero = player.hasPermission("cfactoryfractions.fraction.heroes")
            isOutcast = player.hasPermission("cfactoryfractions.fraction.outcast")
            if not (isHero == isOutcast):
                event.setCancelled(True) # Отменяем команду /spawn
                if isHero:
                    player.sendMessage(u"Ожидайте телепорт на спаун фракции %sГероев%s!" % (ChatColor.YELLOW, ChatColor.RESET))
                    player.chat("/t spawn Cradle") # Выполняем команду
                elif isOutcast:
                    player.sendMessage(u"Ожидайте телепорт на спаун фракции %sИзгоев%s!" % (ChatColor.RED, ChatColor.RESET))
                    player.chat("/t spawn Ark") # Выполняем команду

        elif cmdName.startswith("/t new ") or cmdName.startswith("/town new "):
            if not re.match(r'^/(t|town) new [A-Za-z0-9_]+$', unicode(cmdName)):
                event.setCancelled(True)
                player.sendMessage(u"%sВ имени города можно использовать только буквы латинского алфавита, цифры или знак подчеркивания!" % ChatColor.RED)


@BukkitPlugin
class Plug(PyPlugin):
    iconomy = None
    pheroes = None


    def onEnable(self):
        try:
            self.pheroes = Bukkit.getServer().getPluginManager().getPlugin("Heroes")
        except:
            print "Heroes plugin ploblems!"

        self.iconomy = PluginVault.setupEconomy()
        if self.iconomy is None:
            print "Vault not found!"


    @PyCommandHandler("iteminfo")
    def onItemInfo(self, sender, args):
        if not isinstance(sender, Player):
            sender.sendMessage("You not player!")
            return
            
        item = sender.getItemInHand()
        sender.sendMessage("Item: %s" % item)


    @PyCommandHandler("paygem")
    def onPayGem(self, sender, args):
        if self.iconomy is None:
            sender.sendMessage("Vault not found!")
            return

        if not sender.isOp():
            sender.sendMessage("Only for OP!")
            return

        if len(args) < 3:
            sender.sendMessage("Usage: paygem <player> <cost> <gemname>")
            return

        namePlayer = args[0]
        cost = float(args[1])
        nameGem = args[2]

        player = Bukkit.getPlayer(namePlayer)

        if not self.iconomy.has(namePlayer, cost):
            player.sendMessage(u"%sНе хватает денег на покупку. Требуется %d голд." % (ChatColor.RED, cost))
            return

        self.iconomy.withdrawPlayer(namePlayer, cost)
        server = Bukkit.getServer()
        server.dispatchCommand(server.getConsoleSender(), "md gem %s -a 1 -g %s" % (namePlayer, nameGem))


    @PyCommandHandler("getexp")
    def onGetExp(self, sender, args):
        if self.pheroes is None:
            sender.sendMessage("Heroes not found!")
            return

        if not sender.isOp():
            sender.sendMessage("Only for OP!")
            return

        if len(args) < 2:
            sender.sendMessage("Usage: getexp <player> <exp>")
            return

        namePlayer = args[0]
        exp = int(args[1])

        player = Bukkit.getPlayer(namePlayer)
        if player is None:
            sender.sendMessage("%sPlayer not found!" % ChatColor.RED)
            return

        hero = self.pheroes.getCharacterManager().getHero(player)
        if hero is None:
            sender.sendMessage("%sHero not found!" % ChatColor.RED)
            return

        heroClass = hero.getHeroClass()
        heroLevel = hero.getLevel(heroClass)
        if heroLevel >= heroClass.getMaxLevel():
            player.sendMessage(u"%sУ вас уже максимальный уровень." % ChatColor.RED)
        else:
            hero.addExp(exp, heroClass, player.getLocation())
            player.sendMessage(u"%sПолучено %d опыта." % (ChatColor.GREEN, exp))
