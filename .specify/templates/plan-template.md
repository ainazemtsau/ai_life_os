# Implementation Plan: [FEATURE]

**Branch**: `[BRANCH]` | **Date**: [DATE] | **Spec**: [SPEC_PATH]  
**Input**: Feature specification from [FEATURE_SPEC_ABS]

---

## Purpose
Freeze high-level design for this feature using **contracts-first**. The template is logic-less; the `/plan` runner injects all concrete details.

## Context & Constraints (from spec)
[CONTEXT_SUMMARY]

## Module Map (public surfaces only)
[MODULE_API_MATRIX]

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts
- HTTP contracts (OpenAPI 3.1), if any:  
[HTTP_CONTRACTS_TABLE]
- In-process ports (TS `.d.ts` / Python Protocols), if any:  
[INPROC_PORTS_TABLE]

## Vertical Steps (outline)
[VERTICAL_STEPS]

## Gates
- Registry/manifests/contracts exist and validate.
- No deep imports; consumers use only public surfaces.
- SemVer bump on public surface changes; Conventional Commits.

## Risks/Notes
[NOTES]

## Machine-readable Scope
<!-- TARGET_MODULES:BEGIN
[TBD by /plan runner]
TARGET_MODULES:END -->
<!-- ROUTER_OWNER: [TBD or empty] -->
