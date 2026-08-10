import os
import json


class MemoryFile:

    def __init__(self, path):

        self.path = path

        directory = os.path.dirname(self.path)

        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

        if not os.path.exists(self.path):

            with open(
                self.path,
                "w",
                encoding="utf-8"
            ) as f:

                json.dump(
                    {},
                    f,
                    ensure_ascii=False,
                    indent=4
                )


    def read(self):

        with open(
            self.path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)


    def update(
        self,
        **data
    ):

        with open(
            self.path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                data,
                f,
                ensure_ascii=False,
                indent=4
            )


class BaseMemory:

    def __init__(self):

        self.npcs = MemoryFile(

            "memory/npcs.json"

        )


        self.memories = MemoryFile(

            "memory/memories.json"

        )


        self.player = MemoryFile(

            "memory/player.json"

        )

        # Added world memory file to satisfy world-related code expecting memory.world
        self.world = MemoryFile(

            "memory/world.json"

        )
