---
title: Product_Principles
version: v4.0
status: Final
owner: YB
document_type: Product Constitution
product: YB Knowledge Factory Operating System
last_updated: 2026-07-28
---

# Product Constitution

> **The Constitution of YB Knowledge Factory**
>
> This document defines the immutable principles that guide every product decision, architecture, workflow, user experience, and AI capability within YB Knowledge Factory.
>
> These principles are technology-independent, model-independent, and version-independent.
>
> Every future feature must comply with this constitution before implementation.

---

# Principle Zero

## Knowledge is the Product

> **Knowledge is the product.**
>
> Everything else exists to create, preserve, discover, and reuse knowledge.

Users are not purchasing:

- AI
- Browser Extension
- Transcript
- Study Note
- Markdown

These are implementation mechanisms.

The real product is the user's continuously growing knowledge base.

Whenever a design decision is made, ask:

> **Does this feature help users build better knowledge?**

If the answer is **No**, the feature should be redesigned or removed.

---

# Mission

Transform fragmented information into reusable knowledge.

YB Knowledge Factory exists to help people continuously accumulate knowledge instead of repeatedly consuming information.

Our mission is to make knowledge capture effortless, knowledge processing automatic, and knowledge reuse natural.

---

# Vision

Build an AI-powered Knowledge Operating System that enables anyone to collect, organize, refine, and reuse knowledge across every stage of learning.

Knowledge should become a permanent personal asset rather than a temporary reading experience.

---

# Knowledge Flywheel

Knowledge is not a linear process.

It is a continuous cycle.

```
Capture

↓

Understand

↓

Organize

↓

Create

↓

Reuse

↓

Share

↓

Capture
```

Every completed cycle increases the long-term value of the user's knowledge base.

Every new feature should strengthen this flywheel.

---

# Product Identity

YB Knowledge Factory is **not**:

- YouTube Downloader
- Transcript Tool
- AI Summary Tool
- Markdown Generator
- Note-taking App

YB Knowledge Factory is:

> **An AI Knowledge Operating System**

Its purpose is to manage the complete lifecycle of knowledge.

---

# Product Architecture

The system is organized into capability layers.

```
Knowledge Capture

↓

Learning Queue

↓

AI Processing

↓

Knowledge Assets

↓

Knowledge Retrieval

↓

Knowledge Reuse
```

Every future capability should belong to one of these layers.

---

# Core Workflow

```
Capture

↓

Queue

↓

Transcript

↓

Study Note

↓

Knowledge Assets

↓

Retrieval

↓

Reuse
```

Capture and Processing are intentionally separated.

---

# Design Principles

## Principle 1 — Capture First

The easiest action should always be capturing.

Target:

Complete capture within three seconds.

---

## Principle 2 — Process Later

AI processing should never block users.

Background processing is the default architecture.

---

## Principle 3 — Homepage is an Inbox

The homepage exists only for:

- Capture
- Queue Management

It is not:

- an editor
- a reader
- a document viewer

---

## Principle 4 — Queue is Temporary

Queue represents pending work.

Knowledge represents permanent value.

Queue can be cleared.

Knowledge remains.

---

## Principle 5 — Markdown is the Source of Truth

Every knowledge asset must exist independently as Markdown.

This guarantees:

- portability
- longevity
- interoperability

Applications may change.

Knowledge must not.

---

## Principle 6 — Knowledge Before Content

The system manages knowledge.

Not media.

Content sources are interchangeable.

Knowledge is permanent.

---

## Principle 7 — Automation by Default

Every repetitive action should be automated whenever practical.

Automation should reduce user effort rather than introduce additional configuration.

---

## Principle 8 — AI is Invisible

Users should experience completed knowledge rather than AI models.

The interface should emphasize outcomes, not implementation details.

---

## Principle 9 — Mobile First

The primary usage scenario is fragmented time.

The product should optimize for quick interactions and low cognitive load.

---

## Principle 10 — Simplicity Wins

Every feature increases complexity.

Complexity must be justified by meaningful value.

Simple solutions are preferred over feature-rich solutions.

---

## Principle 11 — Modular by Design

Every capability should be implemented as an independent module.

Modules communicate through clearly defined inputs and outputs.

This allows the system to evolve without unnecessary coupling.

---

## Principle 12 — Knowledge Compounds

Knowledge should become more valuable over time.

Each new Transcript, Study Note, Knowledge Card, SOP, Prompt, or Agent should strengthen the entire knowledge system rather than exist as isolated documents.

---

# Product Modules

```
YB Knowledge Factory

├── Learning Inbox
│     Capture
│     Queue
│
├── Transcript Engine
│
├── Study Note Engine
│
├── Knowledge Assets
│     Transcript
│     Study Notes
│     Knowledge Cards
│     SOPs
│     Prompt Library
│
├── Knowledge Retrieval
│     Search
│     Tags
│     Related Knowledge
│
└── Knowledge Automation
      Agents
      Workflows
      Integrations
```

---

# Decision Hierarchy

When multiple design options exist, follow this order:

1. Principle Zero
2. Simplicity
3. Capture Speed
4. Automation
5. Knowledge Quality
6. Extensibility
7. Additional Features

Higher priorities always override lower priorities.

---

# Decision Checklist

Before implementing any feature:

□ Does it support Principle Zero?

□ Does it improve knowledge creation?

□ Does it reduce capture effort?

□ Can it run in the background?

□ Does it belong to an existing module?

□ Does it preserve Markdown as the source of truth?

□ Does it simplify the user experience?

If three or more answers are **No**, redesign the feature.

---

# Success Metrics

The success of YB Knowledge Factory is measured by knowledge growth.

Primary indicators include:

- Knowledge Sources Captured
- Queue Completion Rate
- Transcript Generation Rate
- Study Note Completion Rate
- Knowledge Assets Created
- Knowledge Reuse Frequency
- Knowledge Network Growth

AI usage metrics are secondary.

Knowledge accumulation is primary.

---

# Product Promise

Every valuable piece of information should become permanent, searchable, and reusable knowledge with the least possible effort.

---

# Final Principle

Whenever uncertainty arises, ask one question:

> **Will this decision help users build a stronger personal knowledge system?**

If the answer is **No**, it should not become part of YB Knowledge Factory.

---

# Closing Statement

Technology will evolve.

AI models will change.

User interfaces will be redesigned.

Workflows will continue to improve.

However, these principles remain constant.

YB Knowledge Factory exists for one purpose:

> **To transform information into lasting knowledge and knowledge into long-term personal value.**