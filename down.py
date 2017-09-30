import digitalocean
import config

manager = digitalocean.Manager(token=config.token)
print([d for d in manager.get_all_droplets() if d.name == "ccdc"])
for d in manager.get_all_droplets():
    if d.name == "ccdc":
        d.destroy()