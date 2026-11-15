# ScamShield-India
A Python-based Android application to help users identify suspicious messages and URLs.

import re
import ipaddress
from urllib.parse import urlsplit

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
            padding=20,
            spacing=12
        )

        heading = Label(
            text="[b]SCAMSHIELD INDIA[/b]",
            markup=True,
            font_size=27,
            color=(0.2, 0.8, 1, 1),
            size_hint=(1, 0.12)
        )

        subtitle = Label(
            text="Understand suspicious messages and links",
            font_size=14,
            size_hint=(1, 0.08)
        )

        self.message_input = TextInput(
            hint_text="Paste a message or URL here...",
            multiline=True,
            font_size=16,
            size_hint=(1, 0.30),
            padding=12
        )

        buttons = BoxLayout(
            size_hint=(1, 0.13),
            spacing=10
        )

        analyze_button = Button(
            text="ANALYZE",
            bold=True,
            background_normal="",
            background_color=(0, 0.45, 0.8, 1)
        )

        clear_button = Button(
            text="CLEAR",
            background_normal="",
            background_color=(0.35, 0.35, 0.4, 1)
        )

        analyze_button.bind(
            on_press=self.analyze_message
        )

        clear_button.bind(
            on_press=self.clear_screen
        )

        buttons.add_widget(analyze_button)
        buttons.add_widget(clear_button)

        self.result = TextInput(
            text="Your analysis will appear here.",
            readonly=True,
            multiline=True,
            font_size=14,
            size_hint=(1, 0.37),
            padding=10
        )

        layout.add_widget(heading)
        layout.add_widget(subtitle)
        layout.add_widget(self.message_input)
        layout.add_widget(buttons)
        layout.add_widget(self.result)

        return layout

    def clear_screen(self, instance):
        self.message_input.text = ""
        self.result.text = "Your analysis will appear here."

    def analyze_message(self, instance):

        message = self.message_input.text.lower()

        if not message.strip():
            self.result.text = "Please enter a message first."
            return

        warnings = []

        warning_phrases = [
            "urgent",
            "verify your account",
            "claim your prize",
            "send otp",
            "share otp",
            "account blocked",
            "click here",
            "password",
            "bank details",
            "limited time",
            "account suspended"
        ]

        for phrase in warning_phrases:
            if phrase in message:
                warnings.append(
                    "Suspicious phrase: " + phrase
                )

        urls = re.findall(
            r"(?:https?://|www\.)[^\s]+",
            message,
            re.IGNORECASE
        )

        url_warnings = []

        for url in urls:

            url = url.rstrip(".,!?;:)]}")

            if url.lower().startswith("www."):
                url = "https://" + url

            parsed = urlsplit(url)
            host = parsed.hostname

            if not host:
                url_warnings.append(
                    "Could not properly read a link."
                )
                continue

            if parsed.scheme.lower() != "https":
                url_warnings.append(
                    "Link does not use HTTPS: " + host
                )

            if "@" in parsed.netloc:
                url_warnings.append(
                    "Link contains an unusual @ symbol."
                )

            try:
                ipaddress.ip_address(host)
                url_warnings.append(
                    "Link uses an IP address instead of a domain."
                )
            except ValueError:
                pass

            if any(
                part.startswith("xn--")
                for part in host.lower().split(".")
            ):
                url_warnings.append(
                    "Link contains an encoded domain name."
                )

        output = []

        output.append("SCAMSHIELD ANALYSIS")
        output.append("--------------------------")

        if warnings or url_warnings:

            output.append(
                "RESULT: Suspicious signals detected."
            )

            output.append("")
            output.append("MESSAGE WARNINGS:")

            if warnings:
                output.extend(warnings)
            else:
                output.append("No suspicious phrases found.")

            output.append("")
            output.append("LINK WARNINGS:")

            if url_warnings:
                output.extend(url_warnings)
            elif urls:
                output.append(
                    "No warning signs found by these basic URL checks."
                )
            else:
                output.append("No recognizable URL found.")

        else:

            output.append(
                "RESULT: No warning signals detected."
            )

            output.append(
                "This does NOT guarantee that the message is safe."
            )

            if not urls:
                output.append("No recognizable URL found.")

        output.append("")
        output.append("SAFETY ADVICE:")
        output.append("1. Never share your OTP or password.")
        output.append("2. Do not rush to click unknown links.")
        output.append("3. Verify through the official bank or service app.")
        output.append("4. Contact the organisation using its official contact details.")

        output.append("")
        output.append(
            "IMPORTANT: These are basic warning checks, "
            "not a guarantee of fraud or safety."
        )

        self.result.text = "\n".join(output)


if __name__ == "__main__":
    ScamShieldApp().run()
