# SCRAPBOUND — 2-Player Online Competitive Tower Defense

Built with **Godot 4** for the Telecom Hackathon.

SCRAPBOUND is a fast-paced, two-player competitive tower defense survival game where two players defend their respective towers against relentless monster swarms while competing for the highest score.

---

## 🎮 How to Play

### Online / LAN Multiplayer (Two Computers):
1. **Player 1 (Host):**
   * Launch the game.
   * Click **HOST GAME (P1)** on port `7777`.
2. **Player 2 (Client):**
   * Launch the game on the second computer.
   * Enter Player 1's local IP address (e.g. `192.168.1.50`).
   * Click **JOIN GAME (P2)**.
3. Once Player 2 connects, Player 1 clicks **START MATCH**!

### Local Testing (Single Computer):

**On Linux:**
* Run `./start_two_players.sh` (or from repo root `./start_two_players.sh`) to launch two game windows side-by-side.
* Or run `./run_game.sh` to launch a single game instance.
* In Window 1, click **HOST GAME (P1)**.
* In Window 2, click **JOIN GAME (P2)**.
* Click **START MATCH** on Window 1!

**On Windows:**
* Double-click `START_TWO_PLAYERS.bat` to launch two game windows side-by-side.
* In Window 1, click **HOST GAME (P1)**.
* In Window 2, click **JOIN GAME (P2)**.
* Click **START MATCH** on Window 1!

---

## 🕹️ Controls (Independent on each computer)

| Action | Keys |
| :--- | :--- |
| **Movement** | `W, A, S, D` or `Arrow Keys` |
| **Shoot Weapon** | `SPACE` or `K` or `ENTER` |
| **Recycle Scrap** | `E` or `L` *(when near Recycler)* |
| **Quick Craft** | `E` or `L` *(outside Recycler)* |
| **Build Barrier** | `Q` or `O` *(costs 2 building materials)* |

---

## ⚙️ Core Game Rules

* **Two Opposing Towers:**
  * Player 1 Tower (West / Cyan) vs Player 2 Tower (East / Orange).
  * Towers start at $1000\text{ HP}$. Monsters attack towers and players.
* **Match Duration:** $120\text{ seconds}$ (2 minutes).
* **Death & Respawn Scaling:**
  $$\text{Respawn Time} = \text{Death Count} \times 5.0\text{ seconds}$$
  * 1st Death: $5\text{s}$ | 2nd Death: $10\text{s}$ | 3rd Death: $15\text{s}$.
* **Recycling Machine:**
  * Deposit $15\text{ Scrap}$ to produce 1 of 5 items:
    1. **Battery** *(Rare special resource)*
    2. **Material A**
    3. **Material B**
    4. **Material C**
    5. **Material D**
* **Configurable Crafting:**
  * `Material A + Material B` = **Rapid-Fire Weapon** (high fire rate).
  * `Material A + Material C` = **High-Damage Weapon** ($60\text{ DMG}$, piercing).
* **Building System:**
  * Monsters drop Wood, Plastic, and Iron.
  * Use 2 materials to place a **Defensive Barrier Wall** ($150\text{ HP}$) that diverts monster movement and shields your tower.
* **Scoring & Victory:**
  * Killing monsters awards $+100\text{ points}$.
  * Final score calculation:
    $$\text{Final Score} = \text{Kill Score} + (\text{Remaining Tower HP} \times 2)$$

---

## 🌐 Network Architecture

* **Networking Library:** Godot 4 high-level multiplayer (`ENetMultiplayerPeer`).
* **Server Authority:** The host machine is fully authoritative over:
  * Monster AI, pathfinding, and attack calculations.
  * Bullet collisions and damage validation.
  * Scrap drops and player pickup validation.
  * Recycler random table rolls and material crafting.
  * Match clock, scoring, and victory conditions.
* **Client Prediction:** Local player movement is simulated instantly for zero-latency responsive controls, with delta synchronization to the remote puppet.
