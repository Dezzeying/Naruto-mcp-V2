from .world_events import (
    get_events_for_year
)


class WorldTick:

    def __init__(
        self,
        timeline,
        memory,
        npc_engine=None,
        jutsu_engine=None
    ):

        self.timeline = timeline

        self.memory = memory

        self.npc_engine = npc_engine

        self.jutsu_engine = jutsu_engine

    def run_day(
        self
    ):

        current = self.timeline.advance_day()

        events = self.check_world_events()

        return {
            "Date": current,
            "Events": events
        }

    # Backwards-compatibility wrapper expected by GameEngine
    def advance(self):
        """
        Compatibility shim: return the current day value (timeline.advance_day)
        """
        return self.timeline.advance_day()

    # Backwards-compatibility wrapper for check_events(day)
    def check_events(self, day=None):
        # day parameter is ignored by the underlying implementation, kept for compatibility
        return self.check_world_events()

    def check_world_events(
        self
    ):

        time = self.timeline.get_time()

        year = time.get(
            "Year",
            0
        )

        events = get_events_for_year(
            year
        )

        triggered = []

        for event in events:

            if self.execute_event(
                event
            ):

                triggered.append(
                    event["Name"]
                )

        return triggered

    def execute_event(
        self,
        event
    ):

        unlocks = event.get(
            "Unlocks",
            []
        )

        for jutsu in unlocks:

            self.unlock_jutsu(
                jutsu
            )

        changes = event.get(
            "NPCChanges",
            {}
        )

        for npc,data in changes.items():

            if self.npc_engine:

                self.npc_engine.update_npc(
                    npc,
                    **data
                )

        return True

    def unlock_jutsu(
        self,
        jutsu
    ):

        if not self.memory:

            return

        data = self.memory.world.read()

        known = data.get(
            "KnownJutsu",
            []
        )

        if jutsu not in known:

            known.append(
                jutsu
            )

        data["KnownJutsu"] = known

        self.memory.world.update(
            **data
        )
