# encoding: utf-8
from org.bukkit.entity import Player
from org.bukkit import ChatColor
from org.bukkit import Material
from org.bukkit.enchantments import Enchantment

PERM_SET_CUSTOM_NAME = "cfactory.custom.item"

@pyp_plugin
class Plug(PyPlugin):

    def check_setitem(self, sender, argv):
        if not isinstance(sender, Player):
            sender.sendMessage("You not player!")
            return False

        player = sender
        if not player.hasPermission(PERM_SET_CUSTOM_NAME):
            player.sendMessage("%sYou don't has permission!" % ChatColor.RED)
            return False

        itemStack = player.getItemInHand()
        if (itemStack is None) or (itemStack.getType() == Material.AIR):
            player.sendMessage("%sPlease, take item in hand!" % ChatColor.GOLD)
            return False

        return True

    @pyp_command_handler("setitemname")
    def cmdSetItemName(self, sender, argv):
        if not self.check_setitem(sender, argv):
            return

        player = sender
        if len(argv) < 1:
            player.sendMessage("%sPlease, enter new name! Usage: setitemname <newname>" % ChatColor.GOLD)
            return

        argv = [x for x in argv]
        itemName = ChatColor.translateAlternateColorCodes('&', ' '.join(argv))

        itemStack = player.getItemInHand()
        itemMeta = itemStack.getItemMeta()
        itemMeta.setDisplayName(unicode(ChatColor.RESET) + itemName);
        itemStack.setItemMeta(itemMeta);
        player.sendMessage("%sComplete!" % (ChatColor.GREEN))

    @pyp_command_handler("setitemlore")
    def cmdSetItemLore(self, sender, argv):
        if not self.check_setitem(sender, argv):
            return

        player = sender
        if len(argv) < 1:
            player.sendMessage("%sPlease, enter new lore! Usage: setitemlore <lore>" % ChatColor.GOLD)
            return

        argv = [x for x in argv]
        itemLore = ChatColor.translateAlternateColorCodes('&', ' '.join(argv)).split("\\n")

        itemStack = player.getItemInHand()
        itemMeta = itemStack.getItemMeta()
        lore = [(unicode(ChatColor.RESET) + x) for x in itemLore]
        itemMeta.setLore(lore);
        itemStack.setItemMeta(itemMeta);
        player.sendMessage("%sComplete!" % (ChatColor.GREEN))

    @pyp_command_handler("setitemench")
    def cmdSetItemEnch(self, sender, argv):
        if not self.check_setitem(sender, argv):
            return

        player = sender
        if len(argv) < 2:
            player.sendMessage("%sPlease, enter new enchant! Usage: setitemench <ench_name_or_id> <ench_level>" % ChatColor.GOLD)
            return

        enchObj = Enchantment.getByName(argv[0])
        enchLvl = int(argv[1])

        if enchObj is None:
            player.sendMessage("%sInvalid enchantment name!" % ChatColor.RED)
            return

        if enchLvl < 0:
            player.sendMessage("%sInvalid enchantment level!" % ChatColor.RED)
            return

        itemStack = player.getItemInHand()
        itemMeta = itemStack.getItemMeta()
        if enchLvl > 0:
            itemMeta.addEnchant(enchObj, enchLvl, True)
        elif enchLvl == 0:
            itemMeta.removeEnchant(enchObj)
        itemStack.setItemMeta(itemMeta);
        player.sendMessage("%sComplete!" % (ChatColor.GREEN))
