---
name: web-clone
description: URL-driven website cloning with visual and functional verification
---

# Web Clone

Clone a live webpage into working code with strong visual similarity and basic interaction parity.

## Purpose

This is a workflow skill, not a browser driver. Use it to structure the cloning job. For live extraction, screenshots, snapshots, and UI interaction, use the existing `playwright` skill.

## When To Use

- The user gives a URL and wants the page replicated in code
- The task is mostly frontend structure, styling, and basic interaction behavior
- Single-page fidelity matters more than backend parity

## When Not To Use

- The user only has screenshots
  Use `visual-verdict` instead.
- The task requires auth flows, payments, or backend API parity
- The user wants a redesign, not a faithful clone
- The target is a large multi-page site and deep route graph cloning is expected

## Scope

Included:
- page structure
- typography, spacing, colors, borders, and layout
- basic interactions such as links, buttons, menus, modals, forms, and toggles
- responsive behavior when it can be reasonably inferred

Excluded:
- backend integration
- protected content
- dynamic personalized behavior
- third-party widget parity
- copyright-protected asset replication beyond placeholders

## Required Companion Skill

Use the `playwright` skill for browser automation:
- open the target URL
- take snapshots and screenshots
- inspect visible structure and interactions
- verify the local clone after implementation

If Playwright cannot run in the environment, stop and report that the clone workflow is blocked.

## Workflow

### 1. Extract with Playwright

Use the `playwright` skill to:
- open the target page
- take a full-page screenshot
- collect one or more snapshots of the rendered structure
- inspect key interactive elements
- capture additional screenshots after major UI state changes when needed

Keep extraction focused. Do not over-collect.

### 2. Build a Clone Plan

From the extracted page, identify:
- major sections
- repeated patterns and components
- design tokens such as colors, spacing, typography, radius, and shadows
- key interactions worth recreating

Write a component and file plan before coding if the page is non-trivial.

### 3. Implement the Clone

Build the page in the current project stack.

Rules:
- match the visible structure first
- then match layout and spacing
- then typography and color
- then interactions
- use placeholders for external assets when necessary

### 4. Verify

Use the `playwright` skill to open the clone locally and capture screenshots.

Then compare the clone against the reference with `visual-verdict`.

Also do a small functional check on the most important interactions:
- navigation
- menu or modal toggles
- form entry

### 5. Iterate

Fix the highest-impact mismatches first:
- layout
- missing landmarks
- broken interactions
- spacing
- typography
- colors

Repeat verification until the result is good enough for the requested fidelity.

## Deliverable

Report:
- what was cloned
- what was intentionally approximated
- what still differs
- what was verified visually and functionally

## Legal Reminder

Only clone sites you own or have permission to replicate. Respect copyright, trademarks, and terms of service.
