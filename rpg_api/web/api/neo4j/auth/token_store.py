class InMemoryTokenStore:
    """In memory token store (Cheap redis clone)."""

    def __init__(self) -> None:
        self.tokens: dict[int, str] = {}

    def set(self, user_id: int, token: str) -> None:
        """Set the token."""

        self.tokens[user_id] = token

    def get(self, user_id: int) -> str | None:
        """Get the token."""
        return self.tokens.get(user_id)

    def pop(self, user_id: int) -> str | None:
        """Pop the token."""
        return self.tokens.pop(user_id, None)


token_store = InMemoryTokenStore()
