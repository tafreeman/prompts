# MCP Memory integration logic


class MCPMemory:
    def __init__(self):
        self.store = {}

    def upsert(self, key, value):
        # Logic to upsert memory
        self.store[key] = value

    def get(self, key):
        # Logic to retrieve memory
        return self.store.get(key)

    def list_all(self):
        # Logic to list all memory entries
        return self.store.items()
