from dataclasses import dataclass
import json

@dataclass
class ThemeState:
    name: str = "darkly"
    emoji: str = "🌙"
    font_family: str = "Segoe UI"

    def toggle(self):
        if self.name in ("darkly", "cyborg", "superhero"):
            self.name = "flatly"
            self.emoji = "☀️"
            self.font_family = "Calibri"
        else:
            self.name = "darkly"
            self.emoji = "🌙"
            self.font_family = "Segoe UI"