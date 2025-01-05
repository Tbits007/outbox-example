from app.application.interfaces.link_creator_interface import LinkCreator


class SimpleLinkCreator(LinkCreator):
    def create_verification_link(self, token: str) -> str:
        return f"https://localhost:8000/verify-email?token={token}"

    def create_password_reset_link(self, token: str) -> str:
        return f"https://localhost:8000/reset-password?token={token}"
