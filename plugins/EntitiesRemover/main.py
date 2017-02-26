from EntitiesRemover.remover import EntityRemover, WorldPoint

def print_to_sender(sender):
    def inner(message):
        sender.sendMessage(message)
    return inner


@pyp_plugin
class MyPlugin(PyPlugin):
    
    @pyp_command_handler("entities")
    def cmd_entities(self, sender, args):
        if len(args) == 0:
            sender.sendMessage("Invalid args!\nHelp: /pyc entities help")
            return

        command = args[0]
        if command == "clear":
            if len(args) < 7:
                sender.sendMessage("Invalid args! Usage: /pyc entities clear x1 y1 z1 x2 y2 z2")
                return
            r = EntityRemover("world", output_callback=print_to_sender(sender))
            pos1 = WorldPoint(x=float(args[1]), y=float(args[2]), z=float(args[3]))
            pos2 = WorldPoint(x=float(args[4]), y=float(args[5]), z=float(args[6]))
            r.clear(pos1, pos2)
            sender.sendMessage("Complete!")
        elif command == "help":
            sender.sendMessage("Hi! This is example usage PyPlugins.\nUsage: /pyc entities clear x1 y1 z1 x2 y2 z2")
        else:
            sender.sendMessage("Nope.")
