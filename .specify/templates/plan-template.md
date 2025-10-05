# Implementation Plan: [FEATURE]

**Branch**: `[BRANCH]` | **Date**: [DATE] | **Spec**: [SPEC_PATH]  
**Input**: Feature specification from [FEATURE_SPEC_ABS]

---

## Purpose
Freeze high-level design for this feature using **contracts-first**. Keep template logic-less: all module/data details are injected by the /plan runner.

## Context & Constraints (from spec)
[CONTEXT_SUMMARY]

## Module Map (auto-generated)
[MODULE_API_MATRIX]

> Only surfaces listed above are public. Everything else is private implementation.

## Contracts
- HTTP contracts (OpenAPI 3.1) for modules that expose HTTP:  
[HTTP_CONTRACTS_TABLE]
- In-process ports (typed DTO/functions) for same-process consumption:  
[INPROC_PORTS_TABLE]

## Vertical Steps (outline)
[VERTICAL_STEPS]

## Gates
- Registry/manifests/contracts exist and validate.
- No deep imports; consumers use only public surfaces.
- SemVer bump on public surface changes; Conventional Commits.

## Risks/Notes
[NOTES]
