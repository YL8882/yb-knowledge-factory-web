---
Version: v2.0
Status: Final
Owner: YB
Document: CLAUDE
Category: AI Coding Agent Guide
Purpose: Claude Code Project Entry Point
Priority: Critical
Last Updated: 2026-07-29
---

# CLAUDE.md

---

# Project

YB Knowledge Factory MVP

---

# Mission

Build a maintainable AI product based on approved product requirements.

Implement features according to the approved specifications.

Do not change product decisions without confirmation.

---

# Project Startup

This project follows the **AI Product Factory Development Operating System**.

Before starting **any** implementation task, you must complete the following startup process.

## Step 1

Read:

> docs/00_Project_Management/Development_Operating_System.md

This document defines the project's:

- Development workflow
- AI responsibilities
- Token Economy principles
- Decision governance
- Architecture governance

This is the highest development specification.

---

## Step 2

Read the relevant Product Requirement Document (PRD).

---

## Step 3

Read the related Workflow Specification.

---

## Step 4

Read the corresponding Prompt Specification (if applicable).

---

## Step 5

Confirm the current Milestone.

Implement **only** the current Milestone.

---

## Important Rules

Never:

- Skip the startup process.
- Modify approved architecture.
- Implement future features.
- Assume missing requirements.
- Continue when specifications are unclear.

When specifications are incomplete,

STOP.

Explain what information is missing.

Wait for confirmation.

---

# Development Principles

- Product First
- Workflow First
- Specification First
- Simple MVP
- Incremental Development
- Modular Design
- Single Responsibility

---

# Engineering Rules

- Reuse existing modules whenever possible.
- Keep functions small.
- Keep files focused.
- Write readable code.
- Handle errors explicitly.
- Avoid duplicate logic.
- Prefer configuration over hard-coded values.

---

# Architecture

The system architecture follows this structure.

Frontend

↓

Backend API

↓

AI Services

↓

Runtime

↓

Storage

Maintain loose coupling between modules.

---

# Folder Rules

- Follow the existing folder structure.
- Do not create new top-level folders unless necessary.
- Place new files in the appropriate module.
- Respect the Documentation Standard.

---

# Coding Standards

- Use clear naming.
- Keep functions focused.
- Write maintainable code.
- Add logging where appropriate.
- Avoid unnecessary complexity.

---

# Development Workflow

Understand

↓

Plan

↓

Implement

↓

Test

↓

Refactor

↓

Commit

---

# Milestone Rules

Implement only **one Milestone** at a time.

After completing the Milestone:

1. Verify functionality.
2. Review changed files.
3. Prepare for Git Commit.
4. Stop.

Wait for the next instruction.

Do not continue implementing additional features.

---

# Before Coding Checklist

Before writing any code, confirm that you have read:

- Development_Operating_System.md
- Product Requirement Document (PRD)
- Workflow Specification
- Prompt Specification (if applicable)
- Current Milestone

If any required document is missing,

stop and report it.

---

# References

docs/

- 00_Project_Management/
- 01_Product_Requirements/
- 02_Prompt_Design/
- 03_Workflows/
- 04_Templates/
- 05_UI_UX/
- 06_Google_AI_Studio/
- 99_Milestones/

---

# Expected AI Behavior

Claude Code should:

- Follow specifications before implementation.
- Ask questions instead of making assumptions.
- Complete one Milestone at a time.
- Minimize unnecessary token usage.
- Keep commits small and focused.
- Respect the approved product architecture.