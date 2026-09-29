\# ClientMind 🧠

\### An AI agent that never forgets your clients.



Freelancers lose hours every week re-reading old emails and 

notes before client calls. ClientMind uses Hindsight memory 

to retain every interaction, preference, and deadline — 

and briefs you automatically before every session.



\## What Makes It Different

Without memory: "Hi, how can I help you today?"  

With memory: "Welcome back. Priya flagged the color palette 

last week — she wants warmer tones. Friday deadline still on track."



\## Tech Stack

\- \*\*Memory:\*\* Hindsight (vectorize.io)

\- \*\*LLM:\*\* Groq (qwen/qwen3-32b)

\- \*\*Frontend:\*\* Streamlit

\- \*\*Language:\*\* Python



\## Setup

1\. Clone this repo

2\. Create a `.env` file with your API keys

3\. `pip install -r requirements.txt`

4\. `streamlit run app.py`



\## How Hindsight Is Used

\- `retain()` — saves every interaction and new client detail

\- `recall()` — fetches relevant memories before each response

\- Memory panel — shows stored memories live in the UI



\## Links

\- Hindsight: https://hindsight.vectorize.io

\- Hindsight GitHub: https://github.com/vectorize-io/hindsight

