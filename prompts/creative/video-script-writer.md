---
title: "Video Script Writer"
shortTitle: "Video Script"
intro: "Create compelling video scripts for YouTube, TikTok, explainer videos, tutorials, and promotional content."
type: "how_to"
difficulty: "intermediate"
audience:
  - "functional-team"
  - "business-analyst"
  - "project-manager"
platforms:
  - "claude"
  - "chatgpt"
  - "github-copilot"
topics:
  - "video-production"
  - "creative"
  - "content-marketing"
author: "Prompts Library Team"
version: "1.0"
date: "2025-11-30"
governance_tags:
  - "PII-safe"
  - "general-use"
dataClassification: "internal"
reviewStatus: "draft"
effectivenessScore: 4.0
---
# Video Script Writer

## Description

Generate professional video scripts tailored to different platforms and formats. This prompt helps content creators, marketers, and video producers create structured scripts with hooks, transitions, and calls-to-action that keep viewers engaged from start to finish.

---

## Use Cases

- YouTube videos (tutorials, vlogs, reviews, educational content)
- TikTok and Instagram Reels short-form content
- Explainer and product demo videos
- Corporate training and onboarding videos
- Promotional and advertisement videos

---

## Prompt

```text
You are an expert video scriptwriter who understands viewer psychology, platform algorithms, and storytelling techniques. Create a compelling video script based on the following details:

**Video Type:** [YOUTUBE/TIKTOK/EXPLAINER/TUTORIAL/PROMOTIONAL/CORPORATE]
**Video Length:** [TARGET DURATION, e.g., 60 seconds, 5 minutes, 10 minutes]
**Topic:** [MAIN SUBJECT OF THE VIDEO]
**Target Audience:** [WHO WILL WATCH THIS]
**Tone:** [CASUAL/PROFESSIONAL/ENERGETIC/EDUCATIONAL/ENTERTAINING]
**Speaker Style:** [ON-CAMERA/VOICEOVER/MULTIPLE SPEAKERS]

**Video Goals:**
- Primary: [EDUCATE/ENTERTAIN/PERSUADE/INFORM/CONVERT]
- Secondary: [SUBSCRIBE/SHARE/CLICK/PURCHASE/LEARN]

**Key Points to Cover:**
1. [MAIN POINT 1]
2. [MAIN POINT 2]
3. [MAIN POINT 3]
4. [MAIN POINT 4 - OPTIONAL]

**Must Include:**
- Hook style: [QUESTION/BOLD STATEMENT/STORY/STATISTIC/CONTROVERSY]
- Call-to-action: [WHAT SHOULD VIEWERS DO?]
- Brand/Channel mention: [YES/NO - NAME?]

**Technical Requirements:**
- B-roll suggestions: [YES/NO]
- On-screen text suggestions: [YES/NO]
- Music/sound cues: [YES/NO]
- Timestamp markers: [YES/NO]

Please create a script that includes:
1. Attention-grabbing hook (first 3-5 seconds)
2. Context/intro that builds curiosity
3. Clear content structure with transitions
4. Engagement prompts throughout
5. Strong conclusion with CTA
6. Visual and audio cues where relevant

Format the script with:
- Timecodes for each section
- [VISUAL] cues for B-roll or graphics
- [AUDIO] cues for music or sound effects
- (Actions) for speaker movements or expressions
```text
## Variables

| Variable | Description |
|----------|-------------|
| `[YOUTUBE/TIKTOK/EXPLAINER/TUTORIAL/PROMOTIONAL/CORPORATE]` | The platform and format for your video |
| `[TARGET DURATION]` | How long the video should be |
| `[MAIN SUBJECT OF THE VIDEO]` | What your video is about |
| `[WHO WILL WATCH THIS]` | Your target viewer demographics |
| `[CASUAL/PROFESSIONAL/ENERGETIC/EDUCATIONAL/ENTERTAINING]` | The overall vibe of the video |
| `[ON-CAMERA/VOICEOVER/MULTIPLE SPEAKERS]` | How the script will be delivered |
| `[EDUCATE/ENTERTAIN/PERSUADE/INFORM/CONVERT]` | Primary purpose of the video |
| `[QUESTION/BOLD STATEMENT/STORY/STATISTIC/CONTROVERSY]` | How you want to start the video |
| `[WHAT SHOULD VIEWERS DO?]` | The action you want viewers to take |

---

## Example Usage

**Input:**

```text
You are an expert video scriptwriter who understands viewer psychology, platform algorithms, and storytelling techniques. Create a compelling video script based on the following details:

**Video Type:** YouTube Tutorial
**Video Length:** 8-10 minutes
**Topic:** How to use Git branches effectively for beginners
**Target Audience:** Junior developers and coding bootcamp students
**Tone:** Friendly, educational, slightly casual
**Speaker Style:** On-camera with screen recordings

**Video Goals:**
- Primary: Educate viewers on Git branching concepts and workflows
- Secondary: Subscribe to channel, try the techniques

**Key Points to Cover:**
1. What branches are and why they matter
2. Creating and switching branches
3. Merging branches and handling basic conflicts
4. Real-world branching strategies (Git flow basics)

**Must Include:**
- Hook style: Question that addresses a common pain point
- Call-to-action: Subscribe and download the Git cheat sheet
- Brand/Channel mention: Yes - "DevPath Academy"

**Technical Requirements:**
- B-roll suggestions: Yes
- On-screen text suggestions: Yes
- Music/sound cues: Yes
- Timestamp markers: Yes

Please create a script that includes:
1. Attention-grabbing hook (first 3-5 seconds)
2. Context/intro that builds curiosity
3. Clear content structure with transitions
4. Engagement prompts throughout
5. Strong conclusion with CTA
6. Visual and audio cues where relevant

Format the script with:
- Timecodes for each section
- [VISUAL] cues for B-roll or graphics
- [AUDIO] cues for music or sound effects
- (Actions) for speaker movements or expressions
```text
**Output:**

```text
# Git Branches for Beginners - Complete Tutorial
## DevPath Academy | ~9 minutes

---

### [0:00-0:15] HOOK

[VISUAL: Quick montage of code conflicts, frustrated developer, then smooth branch merge animation]
[AUDIO: Upbeat intro music, fades under voice]

"Have you ever been terrified to change your code because you might break everything?"

(Lean in, empathetic expression)

"Or maybe you've been working on a feature, your teammate pushed something, and suddenly your code is a disaster zone of conflicts?"

[VISUAL: On-screen text: "Sound familiar?"]

"Git branches solve this. And by the end of this video, you'll never fear experimenting with your code again."

---

### [0:15-0:45] INTRO

[VISUAL: Animated DevPath Academy logo]
[AUDIO: Quick logo sound effect]

"Hey, I'm Sarah from DevPath Academy, where we make developer skills actually make sense."

(Warm smile, conversational)

"Today, we're demystifying Git branches. I'm going to show you exactly what they are, how to use them, and the real-world strategies that professional teams use every single day."

[VISUAL: On-screen chapter list appearing]

"Here's what we'll cover:
- First, what branches actually are—with a simple visual
- Then, creating and switching branches in seconds
- Next, merging your work and handling those scary conflicts
- And finally, a branching strategy you can start using today"

[VISUAL: On-screen text: "Timestamps in description 👇"]

"Timestamps are in the description. Let's dive in."

---

### [0:45-2:30] SECTION 1: What Are Branches?

[VISUAL: Switch to animated diagram of a tree with branches]
[AUDIO: Subtle transition sound]

"Okay, so what exactly is a branch?"

(Use hands to illustrate)

"Think of your code like a tree. The main trunk—usually called 'main' or 'master'—is your stable, working code. The code that's deployed, that works, that you don't want to accidentally break."

[VISUAL: Animation showing main trunk with "main" label]

"Now, when you want to add a feature or fix a bug, you don't carve directly into the trunk. Instead..."

[VISUAL: Animation showing a branch growing from the trunk]

"...you grow a branch. A separate workspace where you can experiment, make changes, even break things—without affecting the main trunk at all."

[VISUAL: Show multiple branches, labeled "feature-login", "bugfix-header", "experiment-ui"]

"This is why branches are powerful:

One—safety. Your main code stays stable.
Two—parallel work. Multiple people can work on different things simultaneously.
Three—experimentation. Try crazy ideas. If they don't work, just delete the branch."

[VISUAL: On-screen text highlighting each point]

(Pause, look at camera)

"Here's the key insight: branches aren't copies of your entire codebase. They're more like... save points in a video game. Git tracks the differences, so branches are fast and lightweight."

[VISUAL: Game controller icon with "Save Point" text]

"Quick knowledge check—drop a comment: Have you used branches before, or is this totally new? I read every comment."

---

### [2:30-4:30] SECTION 2: Creating and Switching Branches

[VISUAL: Transition to screen recording of terminal/VS Code]
[AUDIO: Keyboard typing sound effect]

"Alright, let's get practical. I'll show you the commands, then we'll do it together."

(Energetic, but clear pace)

[VISUAL: Terminal window, commands appearing as spoken]

"To create a new branch, it's just:

`git branch feature-login`

That's it. You've created a branch called 'feature-login'."

[VISUAL: Highlight the command, show branch visualization]

"But here's the catch—you've created it, but you're not ON it yet. You're still on main."

"To switch to your new branch:

`git checkout feature-login`"

[VISUAL: Show the branch switch in visualization]

"Or—and this is my preferred method—do both in one command:

`git checkout -b feature-login`"

[VISUAL: On-screen text: "git checkout -b = create AND switch"]

"The `-b` flag creates the branch and switches to it instantly. I use this probably ten times a day."

[VISUAL: Show demo - create branch, make a small change, show git status]

"Let me show you what this looks like in practice..."

(Walk through demo: create branch, edit a file, git status showing changes only on branch)

"Notice how the main branch is completely unaffected. I could switch back to main right now, and none of these changes would exist there."

[VISUAL: Switch to main, show the file unchanged]

"Mind-blowing when you first see it, right?"

---

### [4:30-6:45] SECTION 3: Merging Branches

[VISUAL: Return to animated branch diagram]
[AUDIO: Transition sound]

"Okay, so you've made your changes on your branch. They work. You're happy. Now what?"

(Build anticipation)

"Now, you merge them back into main. You're basically saying, 'Hey main branch, take all the good work I did over here.'"

[VISUAL: Animation showing branch merging back into trunk]

[VISUAL: Switch to terminal demo]

"Here's how:

First, switch to the branch you want to merge INTO—usually main:

`git checkout main`

Then, merge your feature branch:

`git merge feature-login`"

[VISUAL: Show successful merge message]

"When it works smoothly, you'll see a message like this. Git automatically combines the changes. Beautiful."

(Slight pause, expression changes to 'but wait')

"But sometimes... you get this:"

[VISUAL: Show conflict message in terminal]
[AUDIO: Dramatic dun-dun sound effect]

"The dreaded merge conflict. Don't panic."

[VISUAL: On-screen text: "Merge conflicts aren't scary"]

"A merge conflict just means Git found changes in the same place from different sources, and it needs you to decide which version to keep."

[VISUAL: Show conflict markers in a file]

"When you open the file, you'll see these markers:

The stuff between `<<<<<<< HEAD` and `=======` is what's on main.
The stuff between `=======` and `>>>>>>> feature-login` is what's on your branch."

[VISUAL: Highlight each section clearly]

"Your job: delete the markers, keep the code you want—maybe from both!—and save the file."

[VISUAL: Demo resolving a simple conflict]

"Then:

`git add .`
`git commit -m \"Resolved merge conflict\"`

And you're done."

(Encouraging expression)

"Conflicts sound scary, but they're actually Git being helpful. It's saying, 'Hey, I'm not sure what you want here. You're the human—you decide.'"

---

### [6:45-8:15] SECTION 4: Real-World Branching Strategy

[VISUAL: Professional workflow diagram]
[AUDIO: Subtle background music]

"Now let's talk strategy. How do professional teams actually use branches?"

(Confident, slightly faster pace)

"The most common approach is called Git Flow, or some variation of it. Here's the simplified version you can start using today:"

[VISUAL: Diagram building as points are made]

"**Main branch**: This is production. What users see. Only stable, tested code goes here.

**Develop branch**: This is where active development happens. Features get merged here first.

**Feature branches**: Created from develop, named descriptively—like `feature/user-authentication` or `feature/dark-mode`.

**Hotfix branches**: Emergency fixes that need to go directly to main."

[VISUAL: Show complete flow diagram]

"The workflow looks like:

One—Create a feature branch from develop
Two—Work on your feature, commit often
Three—Open a pull request to merge back to develop
Four—Team reviews, approves, merges
Five—When develop is stable, merge to main for release"

[VISUAL: On-screen text summarizing the 5 steps]

"For solo projects or small teams, you can simplify:

Just main and feature branches. Create a branch for each thing you're working on, merge when it's ready."

[VISUAL: Simplified diagram]

"The principle is the same: never work directly on main. Always branch."

---

### [8:15-9:00] CONCLUSION & CTA

[VISUAL: Return to on-camera, energetic]
[AUDIO: Music builds slightly]

"Alright, let's recap what you learned today:"

[VISUAL: Quick animated recap]

"- Branches are safe workspaces for your code
- `git checkout -b branch-name` creates and switches
- `git merge` brings your changes home
- Conflicts are normal—you've got this
- Professional teams use branching strategies—and now you can too"

(Genuine enthusiasm)

"You now know more about Git branches than I did after six months of professional coding. Seriously."

[VISUAL: Cheat sheet graphic appearing]

"I made a Git commands cheat sheet that covers everything we talked about plus more. Link is in the description—it's free, just download it."

[VISUAL: Subscribe button animation]

"If this helped you, smash that subscribe button. I post new developer tutorials every week, and I don't waste your time."

[VISUAL: Video end screen suggestions appearing]

"If you want to keep learning, this video on Git commit messages will level up your skills even more."

(Wave)

"I'm Sarah from DevPath Academy. Go build something awesome. See you in the next one."

[AUDIO: Outro music]
[VISUAL: End screen with subscribe, suggested videos, cheat sheet link]

---

## VIDEO NOTES

**Thumbnail suggestions:**
- Split image: confused face vs. confident face
- Text overlay: "Git Branches EXPLAINED"
- Branch diagram graphic

**Tags:** git branches, git tutorial, git for beginners, how to use git branches, git merge, git checkout, git workflow, learn git, devpath academy, coding tutorial

**Description first line:** Master Git branches in under 10 minutes! Perfect for beginners who want to stop fearing code changes.
```text
## Tips

- **Hook fast:** You have 3-5 seconds before viewers scroll away—lead with your most compelling point or a relatable pain point
- **Pattern interrupt:** Change visuals, pace, or energy every 30-60 seconds to maintain attention
- **Speak to one person:** Write "you" not "you all" or "everyone"—it feels more personal
- **End screens need setup:** Verbally tee up your end screen recommendations or viewers won't click
- **Script for the edit:** Include visual cues and B-roll suggestions to make editing easier and the final video more engaging
- **Read aloud:** Scripts that look good on paper often sound unnatural—always read your script out loud before recording

---

## Related Prompts

- [Content Marketing Blog Post Generator](content-marketing-blog-post.md)
- [Social Media Content Generator](social-media-content-generator.md)

- [Headline and Tagline Creator](headline-tagline-creator.md)
