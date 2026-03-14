# The project REPORT is where students will document key learnings, challenges, and reflections on their experience using CoPilot for software development. 

# First Impressions - Initial Take on the Project Assignment
## In this section, students will provide their initial thoughts on the project assignment, including their understanding of the requirements, any assumptions they made, points that need clarification, and their overall approach to tackling the project.
## Initial Thoughts
## Assumptions Made
## Points Needing Clarification

# Key Learnings
## Here, students will summarize the most important things they learned while working on the project. This could include computer science related concepts, technical skills, insights about using CoPilot effectively, and any new concepts or tools they encountered
## Computer Science Concepts and Technical Skills
## Insights about Using CoPilot Effectively
## New Concepts or Tools Encountered

# Report on CoPilot Prompting Experience
## Student may pull examples from the JOURNAL.md to illustrate their experience, including specific interactions that were particularly helpful or challenging.
### Types of prompts that worked well
### Types of prompts that did not work well or failed

# Limitations, Hallucinations and Failures
## In this section, students will document any instances where CoPilot provided incorrect or misleading information (hallucinations) or where it failed to provide a useful response. They will analyze why these issues occurred and how they impacted their work on the project.
## For example: Fabricated APIs, Deprecated functions, Subtle logical errors, Confident but wrong explanations, Over-engineered solutions, Under-engineered solutions, overcomplicated code, oversimplified code, etc.
## Examples of Hallucinations or Failures or Misleading Information or Confident but Wrong Explanations, or Over-engineered or Under-engineered Solutions
## Analysis of Why These Issues Occurred
## Impact on the Project

# AI Trust
## When did I trust the AI?
## When did I stop trusting it?
## What signals or situations or patterns indicated low reliability?

# What I Learned
## What did you learn about software development?
## What did you learn about using AI tools?
## When should you trust AI? When should you double-check it?

# Reflection
## Did AI make you faster? Why or why not?
## Did you feel in control of the code?
## Would you use AI the same way next time? What would you change?

**LAB 4**
## First Impressions

At the outset, the project seemed relatively straightforward. However, the constraints (pure function with no loops, separating UI from logic, no string replace) made it more tricky than intially assumed. The requirements forced me to think about the structure and logic so much more. My plan was to design first, implement the core function manually, then use Copilot for the rest.

## Key Learnings

- **State machines**: Using explicit states (START, PLAYING, WON, etc.) made the game loop clean and eliminated messy break conditions.
- **Pure functions**: Writing `update_game_state` without modifying inputs taught me to think about immutability. Using `.copy()` and returning new state prevented bugs.
- **Testing with pytest**: First time using it. Copilot helped generate test cases for duplicates, edge cases, and life clamping.
- **Copilot insights**: Ask mode is great for brainstorming; Agent mode for code generation. But you need to be explicit about constraints.

## Copilot Prompting Experience

**What worked:**
- "Suggest tests for update_game_state": It gave a thorough list including edge cases I missed.
- "Write a game loop with constraints": It produced a clean state machine that respected all rules.
- Code reviews caught real issues like the empty‑string bug (`'' in 'apple'` returns `True`) and negative lives.

**What didn't:**
- Free models sometimes forgot to update the journal.
- Had to remind Copilot about the "no replace" rule a couple times.
- In Ask mode, journal doesn't update automatically at times, which was a massive hurdle as I had to manually trigger it.

## Limitations and Reliability

Copilot isn't perfect. It missed the empty‑string bug initially and occasionally suggested `str.replace` despite the constraint. But with clear prompts and verification through tests, it was mostly reliable. I learned to never trust AI output without a second thought.

## AI Trust

I trusted the AI for generating boilerplate code, suggesting test cases, and providing code reviews after I wrote the core logic, but I stopped trusting it after it missed the empty‑string bug, suggested str.replace despite the explicit "no replace" constraint, and when free models failed to update the journal consistently. Signals that indicated low reliability included over‑complicated solutions, ignoring stated constraints, confident but wrong explanations, and inconsistent adherence to instructions like journaling.

## What I Learned
I learned that designing first with state machines and invariants, using pure functions with immutability, separating logic from UI, and testing thoroughly are essential software development practices. Regarding AI tools, I learned they are useful assistant but not the wherewithal and oftentimes require much more fine-tuning before they could function properly, which demands even more effort than building the logic or documenting the progress myself. Furthermore, precise prompts with explicit constraints yield better results, and all output must be verified, especially for edge cases. Overall, I should trust AI for repetitive code, tests, and certain cases of documentation after quick review, but double‑check core logic, edge cases, and anything with constraints.

## Overall Reflection

Copilot felt like a helpful supporting programmer. It expedited testing and documentation. However, I myself was in charge of building the logical algorithm and retrieving the database. The combination of my design and Copilot's code generation worked well. For future projects, I'll use it the same way: design first, then let AI handle the framework as I verify everything.
