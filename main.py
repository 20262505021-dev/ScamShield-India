
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window

Window.clearcolor = (0.06, 0.08, 0.13, 1)


class ScamShieldApp(App):

    def build(self):
        self.title = "ScamShield India"

        layout = BoxLayout(
            orientation="vertical",
            padding=25,
            spacing=18
        )

        heading = Label(
            text="[b]SCAMSHIELD INDIA[/b]",
            markup=True,
            font_size=27,
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.18)
        )

        subtitle = Label(
            text="Your first line of defence against digital scams",
            font_size=14,
            size_hint=(1, 0.10)
        )

        self.message_input = TextInput(
            hint_text="Paste a suspicious message or URL here...",
            multiline=True,
            font_size=16,
            size_hint=(1, 0.35),
            padding=12
        )

        analyze_button = Button(
            text="ANALYZE MESSAGE",
            font_size=18,
            bold=True,
            size_hint=(1, 0.15),
            background_normal="",
            background_color=(0.0, 0.45, 0.8, 1)
        )

        analyze_button.bind(on_press=self.analyze_message)

        self.result = Label(
            text="Your analysis result will appear here.",
            font_size=15,
            size_hint=(1, 0.22)
        )

        layout.add_widget(heading)
        layout.add_widget(subtitle)
        layout.add_widget(self.message_input)
        layout.add_widget(analyze_button)
        layout.add_widget(self.result)

        return layout

    def analyze_message(self, instance):
        message = self.message_input.text.lower()

        if not message.strip():
            self.result.text = "Please enter a message first."
            return

        warning_words = [
            "urgent",
            "verify your account",
            "claim your prize",
            "send otp",
            "account blocked",
            "click here",
            "password"
        ]

        found_words = [
            word for word in warning_words
            if word in message
        ]

        if found_words:
            self.result.text = (
                "WARNING: Suspicious signals found!\n"
                + ", ".join(found_words)
                + "\n\nDo not share OTPs or passwords."
            )
        else:
            self.result.text = (
                "No warning signals found by these basic rules.\n"
                "This does NOT guarantee that the message is safe."
            )


if __name__ == "__main__":
    ScamShieldApp().run()
