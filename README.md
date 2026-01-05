# H2H Matchup Dashboard with Score-based Glicko-2 Rating Model for Fencing

This project presents a **Head-to-Head (H2H) analytics dashboard** for the **Philippine Fencing Association (PFA) National Rankings**, covering **all three weapons in each category (Men’s and Women’s Épée, Foil, and Sabre)**.

The system combines **web-scraped bout-level data**, a **score-based Glicko-2 rating model**, and an **interactive Streamlit dashboard** to enable direct comparisons between any two fencers. Unlike traditional win/loss rating systems, this implementation incorporates **margin of victory** to better reflect match dominance and competitive intensity, particularly important in fencing where score differentials carry meaningful information.

The dashboard allows users to:
- Compare two fencers’ pool and DE performance
- View separate Glicko-2 ratings for Pools and Direct Elimination
- Examine head-to-head history
- Generate probabilistic match predictions based on rating uncertainty

---

## Data Sources

This project uses official tournament data from the **Philippine Fencing Association (PFA) National Rankings**, scraped directly from **FencingTimeLive**.

Each dataset corresponds to **five legs of a national ranking season per weapon**.

Example data sources:
- [FencingTimeLive – PFA National Rankings](https://www.fencingtimelive.com/)

Separate datasets were collected for:
- Pool bouts
- Direct Elimination (DE) tableau bouts

---

### Data Collection

All match data were collected via **automated web scraping** using **Selenium (Python)**.

Two dedicated scrapers were developed:
- **Pool Matches Scraper**
- **Direct Elimination (DE) Scraper**

Key features of the scraping process:
- Iterates across all tournament legs
- Extracts fencer names, scores, round information, and winners
- Handles multi-round DE tableaux with dynamic spacing logic
- Outputs consolidated CSV files per weapon

Relevant scripts:
- `web scrape (pools).py`
- `web scrape (DE).py`

---

### Data Cleaning

Raw scraped data were cleaned and standardized to produce a unified bout-level dataset.

Cleaning steps included:
- Parsing score formats (e.g., `V5`, `15-12`)
- Removing bye rounds and invalid DE entries
- Standardizing fencer name formats
- Separating Pools and DE matches
- Merging all tournament legs into a single dataset

Computed fields added:
- **Margin of Victory (MOV)**
- **Binary Outcome** (win/loss)
- **Scaled Outcome**, defined as:

\[
\text{Scaled Outcome} = 0.5 + \frac{\text{Margin of Victory}}{2 \times \text{Winning Score}}
\]

This transformation allows the Glicko-2 model to account for **how decisively a match was won**, not just whether it was won.

Relevant script:
- `data_cleaning.py`

---

## Building Process

### Exploratory Data Analysis

Initial analysis focused on:
- Distribution of score margins across pools and DE
- Frequency of repeated head-to-head matchups
- Comparison of pool vs DE volatility
- Identification of sparse match histories and uncertainty sources

These insights informed the decision to:
- Separate pool and DE rating systems
- Retain rating deviation (RD) explicitly in predictions
- Use margin-aware outcomes instead of binary results

---

### Model Building

A **custom score-based Glicko-2 rating model** was implemented from first principles in Python.

Key characteristics:
- Based on the official Glicko-2 formulation
- Uses **scaled outcomes** instead of binary wins
- Processes matches in **rating periods aligned to tournament legs**
- Maintains player-level:
  - Rating
  - Rating Deviation (RD)
  - Volatility

Two independent rating systems were computed:
- **Pool Glicko-2 Ratings**
- **Direct Elimination Glicko-2 Ratings**

This separation reflects structural differences between pool bouts (shorter, round-robin) and DE matches (longer, elimination-based).

Relevant script:
- `glicko2_model.py`

---

### Dashboard Building

The dashboard was built using **Streamlit** with **Plotly** for interactive visualizations.

Key features:
- Weapon-specific pages
- Two-fencer selection interface
- Side-by-side statistical comparison
- Head-to-head records with last match context
- Probabilistic match outcome visualization
- Rating uncertainty explicitly displayed via RD

Prediction logic:
- Glicko-2 expected score function
- Ratings scaled to Glicko-2 space
- Probabilities computed separately for Pools and DE matches

Relevant components:
- `Home.py`
- Weapon-specific pages (e.g., `Women's_Epee.py`)
- Shared utility functions (footer, styling)

---

## Results and Evaluation

The score-based Glicko-2 model:
- Produces more stable rankings than win/loss models
- Differentiates dominant wins from narrow victories
- Reflects uncertainty for low-activity fencers via higher RD
- Aligns well with observed competitive outcomes

The separation of pool and DE ratings reveals meaningful performance differences, highlighting fencers who:
- Perform consistently in pools but struggle in DE
- Peak in elimination bouts despite average pool results

The dashboard successfully translates complex rating mechanics into an interpretable, user-friendly interface.

---

## Future Work

Planned extensions include:
- Cross-weapon normalization for broader comparisons
- Time-decay weighting for recent performances
- Incorporation of seeding effects
- Tournament-level prediction simulations
- Deployment of a public online dashboard
- Validation against international ranking systems

---

## Acknowledgments / References

- Philippine Fencing Association (PFA)
- FencingTimeLive for tournament data access
- Glickman, M. E. (2012). *Example of the Glicko-2 system*
- Streamlit and Plotly open-source communities
