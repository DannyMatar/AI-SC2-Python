import sc2
from sc2 import run_game, maps, Race, Difficulty
from sc2.player import Bot, Computer
from sc2.constants import NEXUS, PROBE, PYLON


class SC2Bot(sc2.BotAI):
	async def on_step(self, iteration):
		# Actions to be done for every step
		await self.distribute_workers() # Located in sc2/bot_ai.py
		await self.build_workers()
		await self.build_pylons()

	async def build_workers(self):
		for nexus in self.units(NEXUS).ready.noqueue:
			if self.can_afford(PROBE):	
				await self.do(nexus.train(PROBE))

	async def build_pylons(self):
		if self.supply_left < 5 and self.already_pending(PYLON):
			nexuses = self.units(NEXUS).ready
			if nexuses.exists:
				if self.can_afford(PYLON):
					await self.build(PYLON, near=nexuses.first)

run_game(maps.get("AbyssalReefLE"), [
	Bot(Race.Protoss, SC2Bot()), 
	Computer(Race.Terran, Difficulty.Easy)
	], realtime=True)