# Team Agreements & Collaboration Guidelines

**Team:** Student Performance Prediction Project  
**Members:** Pratik, Emmanuel, Yugant, Hamza  
**Date Established:** February 11, 2026  
**Last Updated:** February 24, 2026  

---

## Purpose

This document outlines our team's agreements for working together effectively throughout the project. By establishing clear expectations and processes upfront, we aim to minimize conflicts and maximize collaboration.

---

## Team Structure & Roles

### Team Lead: Pratik
**Responsibilities:**
- Facilitate Stand-up Meetings
- Review and merge Pull Requests
- Monitor overall project progress
- Coordinate with instructor/TAs
- Resolve conflicts if they arise
- Ensure balanced workload distribution

**Authority:**
- Final say on merging code to master
- Can reassign tasks if someone is overloaded
- Decides priority when timeline pressures occur

### All Members (Including Lead)
**Shared Responsibilities:**
- Attend all Stand-up Meetings
- Complete assigned tasks on time
- Communicate proactively about issues
- Review teammates' code when requested
- Help others when they're stuck
- Maintain professional, respectful communication

---

## Communication Guidelines

### Primary Channels

**1. Group Chat (WhatsApp/Discord)**
- **Purpose:** Daily quick questions, updates, casual discussion
- **Response Time:** Within 6 hours during weekdays
- **Best for:** "Hey, can you check my PR?", "I'm stuck on this error", "Meeting time change"

**2. GitHub Issues & Pull Requests**
- **Purpose:** Technical discussions, task tracking, code reviews
- **When to use:** 
  - Creating new tasks
  - Reporting bugs
  - Discussing implementation approaches
  - Requesting code review

**3. Stand-up Meetings (In-Class)**
- **Purpose:** Weekly progress sync, planning, problem-solving
- **Duration:** 10 minutes maximum
- **Required:** All members attend

**4. Video Calls (As Needed)**
- **Purpose:** Complex discussions, pair programming, debugging sessions
- **When to schedule:** When async communication isn't enough
- **Platform:** Zoom/Google Meet

### Communication Expectations

✅ **DO:**
- Respond to direct messages within 6 hours (weekdays)
- Give a heads up if you'll be unavailable
- Ask for help when stuck (don't struggle alone for days)
- Provide constructive feedback on others' work
- Use clear, specific language in messages
- Tag relevant people in GitHub Issues/comments

❌ **DON'T:**
- Ghost the team for 24+ hours
- Criticize work without offering solutions
- Make major decisions without team input
- Complain without trying to solve the problem first
- Force-push to master branch

---

## Meeting Schedule

### Stand-up Meetings (Weekly)
**When:** Every Wednesday at start of class  
**Duration:** 30 minutes  
**Format:** Each person answers 3 questions:
1. What I completed since last week
2. Current roadblocks/issues
3. What I plan to complete before next week

### Additional Meetings (As Needed)
**Weekly Meetings:** Saturdays 4:00 PM  
**TA Check-ins:** Scheduled individually as required

### Meeting Etiquette
- Be on time (or notify if late)
- Come prepared (know your update)
- Stay focused (no lengthy tangents)
- Document decisions (in group chat or GitHub)
- Respect everyone's time (keep it efficient)

---

## Git Workflow & Guidelines

### Branch Strategy

**Branch Naming Convention:**
- Format: `yourname-feature` (e.g., `pratik-home-page`, `yugant-model-training`)
- Keep names short and descriptive
- Use hyphens, not underscores or spaces

**Branch Rules:**
1. **Never commit directly to `master`** (except team lead in emergencies)
2. Everyone works on their own branch
3. Merge to master only via Pull Request
4. Delete branch after merging (optional)

### Daily Git Workflow

**Every time you start work:**
```bash
# 1. Switch to your branch
git checkout your-branch

# 2. Get latest changes from master
git pull origin master

# 3. Merge master into your branch
git merge master

# 4. Do your work
# ... code, test, save ...

# 5. Stage and commit
git add .
git commit -m "Clear, specific message"

# 6. Push to your branch
git push origin your-branch
```

### Pull Request Process

**Creating a PR:**
1. Push your branch to GitHub
2. Go to repository on GitHub.com
3. Click "Compare & pull request"
4. Write clear description of changes
5. Tag Pratik for review
6. Link related GitHub Issue (if applicable)

**PR Description Template:**
```
## What Changed
Brief summary of what this PR does

## Tasks Completed
- [x] Task 1
- [x] Task 2
- [ ] Task 3 (in progress)

## Testing Done
How you verified this works

## Related Issue
Closes #12 (if applicable)
```

**Reviewing PRs (Pratik):**
- Review within 24 hours
- Check code works (pull and run locally)
- Leave at least 1 comment (positive or constructive)
- Approve or request changes
- Merge when ready

**PR Merge Rules:**
- Minimum 1 approval required (from Pratik)
- No merge conflicts
- Code follows project style
- All files in correct folders

### Commit Message Guidelines

**Good commit messages:**
✅ `Add correlation heatmap for demographic features`  
✅ `Fix bug in data encoding for categorical variables`  
✅ `Implement Random Forest model with hyperparameter tuning`  
✅ `Update README with Week 3 progress`  

**Bad commit messages:**
❌ `Update`  
❌ `Changes`  
❌ `Fix stuff`  
❌ `asdfasdf`  

**Format:** Start with verb, be specific, keep under 72 characters

### Merge Conflict Resolution

**If you get a merge conflict:**
1. Don't panic! It's normal in collaborative work
2. Post in group chat: "I have a merge conflict in [file]"
3. Open the file in VS Code
4. Look for conflict markers (`<<<<<<`, `======`, `>>>>>>`)
5. Choose which version to keep (or combine both)
6. Delete the conflict markers
7. Save, commit, push
8. If stuck, ask Pratik or do video call

**Prevention:**
- Pull from master frequently (at least daily)
- Communicate before editing shared files
- Keep changes focused and small

---

## Work Distribution & Fairness

### Guiding Principles
1. **Everyone contributes to all aspects** (EDA, modeling, visualization, app)
2. **Commit history should be roughly balanced** (no 80/20 splits)
3. **Distribute work by interest and strength** (but also by learning goals)
4. **No one person owns a component** (knowledge sharing is important)

### Weekly Task Assignment
- Tasks assigned in Stand-up Meeting
- Each person gets 1-2 main tasks per week
- Expected: 2-4 commits per week per person
- If someone is overloaded, speak up early!

### Handling Uneven Workload

**If you're struggling:**
- Tell the team ASAP (not the day before deadline)
- Explain what's blocking you
- Ask for specific help or reassignment

**If someone isn't contributing:**
- Team lead talks to them privately first
- Document the conversation
- Set clear expectations and deadline
- Escalate to instructor if pattern continues

**If someone is doing too much:**
- Team appreciates the enthusiasm!
- But ensure others get opportunities too
- Redistribute tasks to balance learning

---

## Code Standards & Best Practices

### Python Code Style
- **Follow PEP 8** (use a linter if possible)
- **Meaningful variable names:** `student_age` not `sa`
- **Add docstrings** to functions
- **Comment complex logic** (but code should be self-explanatory)
- **Remove commented-out code** before committing

### Notebook Standards
- **Clear structure:** Import → Load → Analyze → Visualize → Conclude
- **Markdown cells** to explain what you're doing
- **Restart & Run All** before committing (ensure it works end-to-end)
- **Clear outputs** if notebook is large (File → Clear All Outputs)

### File Organization
- **Data files:** `data/` or `data/processed/`
- **Notebooks:** `notebooks/` with numbered prefixes (`01_`, `02_`)
- **Models:** `models/` (saved as `.pkl` files)
- **App pages:** `pages/` with numbered prefixes
- **Documentation:** `docs/`

### Naming Conventions
- **Files:** lowercase with underscores (`student_analysis.ipynb`)
- **Functions:** lowercase with underscores (`calculate_average()`)
- **Classes:** PascalCase (`StudentModel`)
- **Constants:** UPPERCASE (`MAX_GRADE = 20`)

---

## Conflict Resolution

### Types of Conflicts

**1. Technical Disagreements**
- Example: "Should we use Decision Tree or Random Forest?"
- **Resolution:** Present evidence (accuracy scores, interpretability), team vote, defer to ML expert (Yugant)

**2. Workload Disputes**
- Example: "I feel like I'm doing more work than others"
- **Resolution:** Review commit history objectively, redistribute tasks if imbalanced, team lead mediates

**3. Code Quality Issues**
- Example: "Your code has bugs / isn't following standards"
- **Resolution:** Point to specific issues, offer help to fix, pair program if needed

**4. Communication Problems**
- Example: "Someone isn't responding to messages"
- **Resolution:** Private message first, team lead follows up, set clear response time expectations

### Resolution Process
1. **Address directly first** (message the person involved)
2. **Assume good intent** (maybe they didn't understand, were busy, etc.)
3. **Involve team lead** if direct approach doesn't work
4. **Document the issue** (what happened, what was agreed)
5. **Escalate to instructor** only if serious and unresolved

### Non-Negotiables
These behaviors are unacceptable and will be escalated immediately:
- Plagiarism or academic dishonesty
- Personal attacks or harassment
- Deliberately sabotaging others' work
- Ghosting the team for extended periods without communication

---

## Quality Standards

### Definition of "Done"
A task is only complete when:
- [ ] Code works (tested locally)
- [ ] Code is committed to branch
- [ ] PR created and approved
- [ ] Merged to master
- [ ] Documented (README updated if needed)

### Code Review Checklist
When reviewing a PR, check:
- [ ] Code runs without errors
- [ ] Follows naming conventions
- [ ] Includes comments/docstrings where needed
- [ ] No unnecessary files committed (e.g., `.DS_Store`, `__pycache__`)
- [ ] Commit messages are clear

### Testing Standards
Before committing:
- [ ] Run the code locally (ensure no errors)
- [ ] Test edge cases (empty inputs, max values, etc.)
- [ ] If modifying app, run `streamlit run app.py` and click through pages
- [ ] If modifying notebooks, restart kernel and run all cells

---

## Emergency Protocols

### If Team Lead is Unavailable
**Backup:** Emmanuel acts as temporary lead
- Can approve urgent PRs
- Facilitates Stand-up Meeting
- Communicates with instructor if needed

### If Someone Has a Personal Emergency
**Process:**
1. Notify team ASAP (even if brief: "Family emergency, can't work this week")
2. Team lead redistributes urgent tasks
3. No judgment or pressure - emergencies happen
4. Team member catches up when able

### If We're Falling Behind Schedule
**Response:**
1. Team meeting to assess status
2. Identify critical path items
3. Cut optional features if needed
4. Redistribute work
5. Consult instructor for guidance

---

## Success Metrics

### Team Health Indicators
✅ **Healthy Team:**
- Everyone commits regularly (2-4 per week)
- PRs reviewed within 24 hours
- Stand-up Meetings are productive (under 10 min)
- Group chat is active and positive
- Conflicts resolved quickly and respectfully

⚠️ **Warning Signs:**
- Someone hasn't committed in 2+ weeks
- PRs sitting unreviewed for days
- Stand-ups feel tense or awkward
- Group chat is silent
- Same person always doing the work

### Project Quality Indicators
✅ **Good Quality:**
- Code is well-documented
- Notebooks have clear explanations
- App pages are polished
- GitHub Issues are used to track work
- README stays up to date

⚠️ **Needs Improvement:**
- Code has no comments
- Notebooks are messy or unclear
- App has obvious bugs
- No task tracking system
- README is outdated

---

## Amendments to This Document

This is a living document. If something isn't working, we can change it.

**Process to Update:**
1. Anyone can propose a change (post in group chat)
2. Team discusses (async or in meeting)
3. If 3+ members agree, change is made
4. Pratik updates the document
5. Notify team of change

**Change History:**
- Feb 11, 2026: Initial version created
- Feb 24, 2026: Added Git workflow details based on Week 2-3 experience

---

## Sign-Off

By participating in this project, all team members agree to follow these guidelines.

**Team Members:**
- ✅ Pratik (Team Lead)
- ✅ Emmanuel
- ✅ Yugant  
- ✅ Hamza

---

## Quick Reference

### Key Links
- **Repository:** https://github.com/pratikkmane/student-performance
- **Group Chat:** [WhatsApp/Discord link]
- **Project Board:** GitHub Issues tab

### Important Commands
```bash
# Start your work session
git checkout your-branch
git pull origin master
git merge master

# End your work session  
git add .
git commit -m "Your clear message"
git push origin your-branch
```

### Need Help?
1. Check this document first
2. Ask in group chat
3. Schedule a video call
4. Contact Pratik (team lead)
5. Go to TA office hours

---

**Remember:** We're all learning. Mistakes will happen. Communicate, be patient with each other, and we'll build something great together! 🚀
