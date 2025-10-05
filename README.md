# 🧠 Reinforcement Learning Tic Tac Toe

Dieses Projekt ist eine Implementierung des Spiels **Tic Tac Toe**, bei dem ein **Q-Learning-Agent** lernt, optimal gegen einen menschlichen Spieler zu spielen.

Das Spiel läuft in einer **Tkinter-GUI**, in der du gegen einen vortrainierten Agenten antrittst. Der Agent nutzt eine **Q-Tabelle**, die zuvor durch selbstständiges Training gegen einen zufälligen Gegner gelernt wurde.

---

## 📂 Projektstruktur
TicTacToe/
├── game.py               → GUI-Spiel (Tkinter)
├── q_agent.py            → Q-Learning Agent
├── tictactoe_env.py      → Spielumgebung
├── train_q_agent.py      → Trainings-Skript für Agent
├── q_table.pkl           → Vortrainierte Q-Tabelle
├── test_env.py           → Umgebung testen (optional)
└── README.md             → Projektdokumentation

---

## ▶️ Spiel starten

```bash
python game.py

🏋️‍♂️ Agent selbst trainieren

Wenn du willst, kannst du den Agenten neu trainieren:
python train_q_agent.py

	•	Das Training läuft über mehrere tausend Episoden
	•	Der Agent lernt gegen einen zufälligen Gegner
	•	Die Q-Tabelle wird in q_table.pkl gespeichert

💡 Je mehr Episoden, desto besser wird der Agent! (z.Bsp. 500000)

⸻

💡 Wie funktioniert Q-Learning?
	•	Das Spiel wird als Markov Decision Process modelliert
	•	Jeder Zustand des Spielfelds ist ein Tupel aus 9 Zahlen (-1, 0, 1)
	•	Die Q-Tabelle enthält die Bewertungen möglicher Züge für jeden Zustand
	•	Der Agent lernt mit der Formel:
	Q(s, a) ← Q(s, a) + α * [r + γ * max(Q(s', a')) - Q(s, a)]

	🛠️ Voraussetzungen
	•	Python 3.8+
	•	Module:
	•	tkinter (Standard)
	•	pickle (Standard)

⸻

👨‍💻 Autor

Josip Jukic

Projekt zur Übung von Reinforcement Learning und Python GUI-Programmierung.

⸻

📜 Lizenz

MIT License – frei verwendbar für Lern- und Forschungszwecke.
