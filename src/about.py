import tkinter as tk

class AboutTab:

    def __init__(self, frame):
        self.frame = frame
        self.build_ui()

    def build_ui(self):

        # Background
        self.frame.configure(bg="#f8f5ef")

        # ================= HEADER =================

        header = tk.Frame(
            self.frame,
            bg="#f8f5ef"
        )
        header.pack(
            fill=tk.X,
            pady=(35, 10)
        )

        # App name
        tk.Label(
            header,
            text="GoldPOS",
            font=("Segoe UI", 26, "bold"),
            bg="#f8f5ef",
            fg="#222222"
        ).pack()

        # Tagline
        tk.Label(
            header,
            text="Jewellery Management Software",
            font=("Segoe UI", 11),
            bg="#f8f5ef",
            fg="#666666"
        ).pack(pady=(4, 0))

        # ================= DIVIDER =================

        tk.Frame(
            self.frame,
            height=1,
            bg="#d6d2ca"
        ).pack(
            fill=tk.X,
            padx=100,
            pady=(15, 25)
        )

        # ================= DESCRIPTION CARD =================

        description_card = tk.Frame(
            self.frame,
            bg="white",
            bd=1,
            relief=tk.SOLID
        )
        description_card.pack(
            padx=100,
            fill=tk.X
        )

        tk.Label(
            description_card,
            text="About GoldPOS",
            font=("Segoe UI", 13, "bold"),
            bg="white",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=20,
            pady=(18, 8)
        )

        tk.Label(
            description_card,
            text=(
                "GoldPOS is a simple and reliable solution designed "
                "for jewellery shops.\n\n"
                "It helps with gold exchange calculations, purity "
                "calculations and receipt printing."
            ),
            font=("Segoe UI", 10),
            bg="white",
            fg="#555555",
            justify="left",
            anchor="w"
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # ================= FEATURES =================

        tk.Label(
            self.frame,
            text="Features",
            font=("Segoe UI", 13, "bold"),
            bg="#f8f5ef",
            fg="#222222"
        ).pack(
            anchor="w",
            padx=100,
            pady=(25, 10)
        )

        features_frame = tk.Frame(
            self.frame,
            bg="#f8f5ef"
        )
        features_frame.pack(
            padx=100,
            fill=tk.X
        )

        features = [
            "Gold Exchange Calculation",
            "Purity & Net Gold Calculation",
            "Receipt Generation",
            "Receipt Printing",
            "Daily Sales Summary"
        ]

        for feature in features:

            row = tk.Frame(
                features_frame,
                bg="#f8f5ef"
            )
            row.pack(
                fill=tk.X,
                pady=3
            )

            tk.Label(
                row,
                text="✓",
                font=("Segoe UI", 11, "bold"),
                bg="#f8f5ef",
                fg="#0a8f08",
                width=3
            ).pack(
                side=tk.LEFT
            )

            tk.Label(
                row,
                text=feature,
                font=("Segoe UI", 10),
                bg="#f8f5ef",
                fg="#444444"
            ).pack(
                side=tk.LEFT
            )

        # ================= VERSION =================

        version_frame = tk.Frame(
            self.frame,
            bg="#f8f5ef"
        )
        version_frame.pack(
            pady=(25, 10)
        )

        tk.Label(
            version_frame,
            text="VERSION",
            font=("Segoe UI", 8, "bold"),
            bg="#f8f5ef",
            fg="#888888"
        ).pack()

        tk.Label(
            version_frame,
            text="0.1.7",
            font=("Segoe UI", 12, "bold"),
            bg="#f8f5ef",
            fg="#222222"
        ).pack(
            pady=(2, 0)
        )

        # ================= FOOTER =================

        footer = tk.Frame(
            self.frame,
            bg="#f8f5ef"
        )
        footer.pack(
            side=tk.BOTTOM,
            pady=15
        )

        tk.Label(
            footer,
            text="GoldPOS",
            font=("Segoe UI", 9, "bold"),
            bg="#f8f5ef",
            fg="#555555"
        ).pack()

        tk.Label(
            footer,
            text="© 2026  •  All Rights Reserved",
            font=("Segoe UI", 8),
            bg="#f8f5ef",
            fg="#888888"
        ).pack(
            pady=(2, 0)
        )