from uuid import UUID


class InMemoryTokenStore:
    """In memory token store (Cheap redis clone)."""

    def __init__(self) -> None:
        self.tokens: dict[UUID, str] = {}

    def set(self, user_id: UUID, token: str) -> None:
        """Set the token."""

        self.tokens[user_id] = token

    def get(self, user_id: UUID) -> str | None:
        """Get the token."""
        return self.tokens.get(user_id)

    def pop(self, user_id: UUID) -> str | None:
        """Pop the token."""
        return self.tokens.pop(user_id, None)


token_store = InMemoryTokenStore()
