---
name: uncodex
description: Enforces high-variation, low-card, non-generic frontend design output for coding agents.
metadata:
  short-description: Make frontend UI look intentionally designed, not AI-template generated
---

# uncodex

Use this skill when the user wants frontend output that does **not** look like generic AI UI.

## Purpose
This skill forces non-generic, high-taste frontend design by enforcing:
- aggressive section variation
- card minimization (especially no nested cards)
- reference-informed composition based on strong modern web patterns
- heavy reuse of `componentry.fun` components where feasible

## Core Rules (Non-Negotiable)

### 1) Section Variation Is Mandatory
Never ship pages where sections repeat the same structure (for example, three equal cards in multiple rows).

Required behaviors:
- every major section must have a distinct composition pattern
- favor asymmetric bento blocks over symmetric 3-up grids
- mix visual densities (quiet section followed by high-information section)
- include at least one spatially layered composition (overlap, stack, collision)
- include at least one motion-led section pattern where the viewport stays anchored while surrounding content transforms (sticky/scroll choreography)

Banned patterns:
- repeated "three cards in a row" sections
- copy-pasted section skeletons with only text changes
- same spacing rhythm and same alignment for all sections

### 2) Keep Cards To A Minimum
Cards are the exception, not the default.

Required behaviors:
- present content directly on the page background/canvas whenever possible
- prioritize typographic blocks, dividing lines, media strips, marquees, timelines, and layered panels over boxed cards
- when a card is required, use the minimum number necessary

Hard bans:
- nested cards
- card-inside-card compositions
- wrapping every paragraph/metric/feature in a separate card

Card budget guidance:
- if the page can work with zero cards, use zero
- default target: no more than 1 carded section per page
- if cards exceed this, justify in a one-line comment in code

### 3) Follow Great Design References + Componentry
Use curated references for direction, then implement with strong component quality.

Reference workflow:
- review relevant examples from `land-book.com` and `curated.design`
- extract layout principles (not visual plagiarism): hierarchy, pacing, whitespace, rhythm, alignment
- prefer references with clear editorial structure and restrained but confident motion (for example, product sites in the quality class of `linear.app`)

Implementation requirement:
- use components and interaction ideas from `https://www.componentry.fun` as much as possible
- adapt those components into the page system, not as disconnected add-ons
- maintain visual consistency after integrating borrowed patterns

## Output Contract
When generating frontend code with this skill, the agent must:
1. State the chosen layout concept in 2-3 lines.
2. List section-by-section variation plan before coding.
3. Explicitly declare card budget and where cards (if any) appear.
4. Implement at least one sticky/scroll transformation section.
5. Confirm there are no nested cards.
6. Provide a short post-build self-audit against this skill.

## Quality Checklist
Use this checklist before finalizing:
- [ ] No repeated section skeletons
- [ ] At least 4 distinct section composition types on a full page
- [ ] No nested cards
- [ ] Card use is minimal and intentional
- [ ] At least one layered/overlap composition
- [ ] At least one sticky/scroll choreography section
- [ ] Typography and whitespace do most of the hierarchy work
- [ ] Componentry-inspired components are integrated

## System Prompt Template
Use or adapt: `templates/system-prompt.md`
