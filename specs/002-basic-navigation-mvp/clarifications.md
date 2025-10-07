# Clarifications

**Feature**: Basic Navigation MVP
**Date**: 2025-10-06

## Context (summary)
- Dashboard-centric navigation with dark theme as default
- Frontend-only MVP with no backend changes
- Establishes foundation for future complex navigation features

## Questions & Answers

1. **Q:** What MUST the greeting message say on the Dashboard?
   **A:** "Welcome to AI Life OS" - fixed text, no personalization in this MVP. _(updated 2025-10-06)_

2. **Q:** What specific "placeholder information" MUST be displayed on the Dashboard (FR-003)?
   **A:** "Your personal productivity companion" - single descriptive line. Future features will replace this with actual content (recent activity, stats, etc.). _(updated 2025-10-06)_

3. **Q:** MUST the Goals navigation element be a button or a link? Where SHOULD it be placed?
   **A:** MUST be a button component from the design system. SHOULD be prominently placed in the main content area of the Dashboard, clearly labeled "Go to Goals" or "View Goals". Exact placement is implementation detail, but it MUST be visible without scrolling. _(updated 2025-10-06)_

4. **Q:** What are the performance requirements for page load and navigation?
   **A:** For this MVP: navigation between Dashboard and Goals SHOULD complete within 500ms on modern broadband connections. No hard performance gates for MVP, but perceivable lag would fail acceptance. _(updated 2025-10-06)_

5. **Q:** Are there accessibility requirements for the dark theme (contrast ratios, WCAG compliance)?
   **A:** Dark theme SHOULD meet WCAG 2.1 Level AA contrast requirements (4.5:1 for normal text, 3:1 for large text). Since design system already exists, assume it follows these standards. No additional A11Y audit required for MVP. _(updated 2025-10-06)_

6. **Q:** What browsers MUST be supported?
   **A:** Modern evergreen browsers (Chrome, Firefox, Safari, Edge - latest 2 versions). No IE11 or legacy browser support required. _(updated 2025-10-06)_

7. **Q:** Does the Dashboard need to persist any state (scroll position, user preferences)?
   **A:** No. Dashboard is stateless in this MVP. Browser back/forward MUST work correctly, but no state persistence beyond URL routing. _(updated 2025-10-06)_

8. **Q:** What happens if a user navigates directly to an unknown route (e.g., "/unknown")?
   **A:** Out of scope for this MVP. Current behavior (404 or fallback) MAY remain unchanged. Future navigation features will handle error routes. _(updated 2025-10-06)_

## Open Items

_None. All clarifications resolved._

## Notes
- All answers use RFC 2119 terms (MUST/SHOULD/MAY) for testable requirements.
- Greeting and placeholder content are intentionally simple for MVP - they establish the pattern that future features will enhance.
- Navigation button placement is deliberately left flexible (visible without scrolling is the key constraint).

## Next

- **No design spikes needed** - straightforward implementation using existing patterns
- **No ADRs needed** - routing strategy already documented in plan.md (Next.js App Router + app-shell module)
- Ready to proceed to `/tasks` after plan approval
