from ai.deepseek_engine import DeepSeekEngine
from ai.game_controller import GameController


from engine.base_memory import BaseMemory
from engine.memory_engine import MemoryEngine

from engine.npc_engine import NPCEngine
from engine.clan_engine import ClanEngine

from engine.relationship_engine import RelationshipEngine
from engine.world_state import WorldState

from engine.mission_engine import MissionEngine
from engine.rank_system import RankSystem

from engine.jutsu_engine import JutsuEngine
from engine.ability_system import AbilitySystem
from engine.ability_progression import AbilityProgression

from engine.dojutsu_system import DojutsuSystem
from engine.dojutsu_ability_system import DojutsuAbilitySystem

from engine.training_engine import TrainingEngine

from engine.npc_simulator import NPCSimulator
from engine.game_engine import GameEngine

# Added imports for AI orchestration
from ai.context_manager import ContextManager
from ai.prompt_builder import PromptBuilder
from ai.response_parser import ResponseParser
from lore.naruto_lore import NarutoLore


class NarutoRPG:


    def __init__(self):


        print(
            "Naruto RPG AI başlatılıyor..."
        )


        # ======================
        # AI
        # ======================


        self.ai = DeepSeekEngine()


        # ======================
        # MEMORY
        # ======================


        self.base_memory = BaseMemory()


        self.memory_engine = MemoryEngine(

            self.base_memory

        )


        # ======================
        # NPC
        # ======================


        self.npc_engine = NPCEngine(

            self.base_memory

        )


        # ======================
        # CLAN
        # ======================


        self.clan_engine = ClanEngine(

            self.npc_engine

        )


        self.npc_engine.connect_clan_engine(

            self.clan_engine

        )


        # ======================
        # JUTSU
        # ======================


        self.jutsu_engine = JutsuEngine(

            self.npc_engine

        )


        # ======================
        # ABILITY
        # ======================


        self.ability_system = AbilitySystem(

            self.npc_engine

        )


        self.ability_progression = AbilityProgression(

            self.npc_engine,

            self.ability_system

        )


        # ======================
        # DOJUTSU
        # ======================


        self.dojutsu_system = DojutsuSystem(

            self.npc_engine,

            self.ability_system

        )


        self.dojutsu_ability_system = DojutsuAbilitySystem(

            self.npc_engine

        )


        # ======================
        # TRAINING
        # ======================


        self.training_engine = TrainingEngine(

            self.npc_engine,

            self.jutsu_engine

        )


        # ======================
        # RELATIONSHIP
        # ======================


        self.relationship_engine = RelationshipEngine(

            self.npc_engine

        )


        # ======================
        # WORLD
        # ======================


        self.world_state = WorldState(

            self.base_memory

        )


        # ======================
        # MISSION
        # ======================


        self.mission_engine = MissionEngine(

            self.npc_engine,

            self.world_state,

            self.relationship_engine

        )


        # ======================
        # RANK
        # ======================


        self.rank_system = RankSystem(

            self.npc_engine

        )


        # ======================
        # NPC SIMULATION
        # ======================


        self.npc_simulator = None


        # ======================
        # GAME ENGINE
        # ======================


        self.game_engine = GameEngine(

            None,

            self.npc_engine,

            self.training_engine,

            self.npc_simulator,

            self.mission_engine,

            self.relationship_engine,

            self.memory_engine

        )


        # ======================
        # CONTROLLER
        # ======================

        # Build AI-related helper objects so GameController receives the expected types
        self.ai_context = ContextManager()
        self.lore = NarutoLore()
        self.prompt_builder = PromptBuilder(self.ai_context, self.lore)
        self.response_parser = ResponseParser()

        self.controller = GameController(

            # GameController expects: memory, prompt_builder, deepseek_engine, response_parser=None, validator=None
            self.ai_context,
            self.prompt_builder,
            self.ai,
            self.response_parser,
            None

        )


        self.player = None


    def create_player(self):


        print(
            "\n=== Yeni Ninja ===\n"
        )


        name = input(
            "Ninja adı: "
        )


        clan = input(
            "Clan: "
        )


        village = input(
            "Köy: "
        )


        npc = self.npc_engine.create_npc_with_clan(

            name,

            clan,

            Village=village,

            Rank="Academy Student"

        )


        self.player = self.npc_engine.get_npc(

            name

        )


        print(
            "\nKarakter oluşturuldu!"
        )


        print(
            self.player
        )


    def start(self):


        self.create_player()


        while True:


            print(
                """

====================

1 - Hikaye devam

2 - Durum göster

3 - Görev oluştur

4 - Rütbe kontrol

5 - Gün ilerlet

6 - Çıkış

====================

"""
            )

            choice = input(
                "Seçim: "
            )

            if choice == "1":

                action = input(
                    "\nNe yapmak istiyorsun:\n> "
                )

                result = self.controller.process_action(

                    self.player,

                    action.get("location") if isinstance(action, dict) else self.player.get("Village", "Konohagakure"),

                    action if isinstance(action, str) else str(action)

                )

                print(result)

            elif choice == "2":

                current = self.npc_engine.get_npc(

                    self.player["Name"]

                )

                print(current)

            elif choice == "3":

                mission = self.mission_engine.generate_mission(

                    self.player

                )

                print(mission)

            elif choice == "4":

                current = self.npc_engine.get_npc(

                    self.player["Name"]

                )

                print(

                    self.rank_system.check_promotion(

                        current

                    )

                )

            elif choice == "5":

                print(

                    self.game_engine.run_day()

                )

            elif choice == "6":

                print(
                    "Oyun kapatıldı."
                )

                break

            else:

                print(
                    "Geçersiz seçim."
                )


if __name__ == "__main__":

    game = NarutoRPG()

    game.start()
