# Quickstart: Goals Management MVP

**Feature**: Goals Management MVP (foundation)
**Date**: 2025-10-04
**Purpose**: Validate implementation against acceptance scenarios from spec.md

## Prerequisites

1. **Docker Compose running**:
   ```bash
   docker-compose up -d postgres
   ```

2. **Backend setup**:
   ```bash
   cd backend
   uv sync
   uv run alembic upgrade head  # Run migrations
   uv run uvicorn ai_life_backend.app:app --reload
   ```

3. **Frontend setup**:
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

4. **Verify services**:
   - Backend: http://localhost:8000/docs (Swagger UI)
   - Frontend: http://localhost:3000
   - PostgreSQL: localhost:5432 (user: postgres, password: postgres, db: ai_life_os)

---

## Acceptance Scenario Validation

### Scenario 1: Create New Goal
**Spec**: _Given I am viewing the goals interface, When I create a new goal with a title, Then the goal appears in my active goals list with creation timestamp and is persisted to the backend_

**Steps**:
1. Open http://localhost:3000
2. Locate the "Create Goal" form
3. Enter title: "Complete project documentation"
4. Click "Create" button
5. **Expected**:
   - Goal appears in the list immediately (optimistic update)
   - Goal shows "Active" status (unchecked checkbox)
   - Goal shows creation timestamp (e.g., "Created: 2 seconds ago")
   - Success message appears: "Goal created successfully"

**API Validation**:
```bash
curl http://localhost:8000/api/goals
# Should return array with the new goal
# Verify: id (UUID), title, is_done=false, date_created, date_updated
```

**Database Validation**:
```sql
SELECT * FROM goals ORDER BY date_created DESC LIMIT 1;
-- Verify: id, title="Complete project documentation", is_done=false
```

---

### Scenario 2 & 2a: View Goals List & Persistence Across Sessions
**Spec**: _Given I have existing goals persisted in the backend, When I view the goals list, Then I see all goals with their titles and completion status. Given I close and reopen my browser, When I view the goals interface, Then my previously created goals are still available._

**Steps**:
1. Create 3 goals via the form:
   - "Complete project documentation"
   - "Review pull requests"
   - "Write unit tests"
2. **Expected**: All 3 goals appear in the list
3. Close the browser tab
4. Open new tab: http://localhost:3000
5. **Expected**: All 3 goals still appear (loaded from backend)

**API Validation**:
```bash
curl http://localhost:8000/api/goals
# Should return array with 3 goals
```

---

### Scenario 3: Edit Goal Title
**Spec**: _Given I have a goal in my list, When I edit its title, Then the goal's title is updated and the update timestamp is refreshed_

**Steps**:
1. Locate goal: "Complete project documentation"
2. Click "Edit" button
3. Change title to: "Complete project documentation and README"
4. Click "Save"
5. **Expected**:
   - Title updates in the list
   - Update timestamp changes (e.g., "Updated: 1 second ago")
   - Success message: "Goal updated successfully"

**API Validation**:
```bash
GOAL_ID="<copy-uuid-from-list>"
curl http://localhost:8000/api/goals/$GOAL_ID
# Verify: title updated, date_updated > date_created
```

---

### Scenario 4: Mark Goal as Done
**Spec**: _Given I have a goal in my list, When I mark it as done, Then the goal's completion status changes and the update timestamp is refreshed_

**Steps**:
1. Locate goal: "Review pull requests"
2. Click checkbox to mark as done
3. **Expected**:
   - Checkbox becomes checked
   - Goal moves to "Done" section (if filtered list is visible)
   - Visual style changes (e.g., strikethrough, different color)
   - Update timestamp refreshes

**API Validation**:
```bash
GOAL_ID="<uuid-of-review-pull-requests>"
curl http://localhost:8000/api/goals/$GOAL_ID
# Verify: is_done=true, date_updated refreshed
```

---

### Scenario 5: Delete Goal
**Spec**: _Given I have a goal in my list, When I delete it, Then the goal is permanently removed from my list_

**Steps**:
1. Locate goal: "Write unit tests"
2. Click "Delete" button
3. Confirm deletion in confirmation dialog
4. **Expected**:
   - Goal disappears from list immediately
   - Success message: "Goal deleted successfully"

**API Validation**:
```bash
GOAL_ID="<uuid-of-write-unit-tests>"
curl -X DELETE http://localhost:8000/api/goals/$GOAL_ID
# Should return 204 No Content

curl http://localhost:8000/api/goals/$GOAL_ID
# Should return 404 Not Found
```

**Database Validation**:
```sql
SELECT * FROM goals WHERE id = '<uuid-of-write-unit-tests>';
-- Should return 0 rows
```

---

### Scenario 6: Filter Active Goals
**Spec**: _Given I have both active and completed goals, When I filter by active goals, Then I see only goals that are not marked as done_

**Setup**:
1. Create 2 goals: "Goal A", "Goal B"
2. Mark "Goal A" as done

**Steps**:
1. Click "Active" filter button
2. **Expected**:
   - Only "Goal B" is visible
   - "Goal A" is hidden

**API Validation**:
```bash
curl http://localhost:8000/api/goals?status=active
# Should return only goals with is_done=false
```

---

### Scenario 7: Filter Completed Goals
**Spec**: _Given I have both active and completed goals, When I filter by completed goals, Then I see only goals that are marked as done_

**Steps**:
1. Click "Done" filter button
2. **Expected**:
   - Only "Goal A" is visible
   - "Goal B" is hidden

**API Validation**:
```bash
curl http://localhost:8000/api/goals?status=done
# Should return only goals with is_done=true
```

---

### Scenario 8: Validation Error - Empty Title
**Spec**: _Given I attempt to create a goal, When I submit without a title, Then I receive a clear validation error message_

**Steps**:
1. Open "Create Goal" form
2. Leave title field empty
3. Click "Create" button
4. **Expected**:
   - Form does NOT submit
   - Error message appears: "Title cannot be empty or whitespace-only"
   - Input field is highlighted as invalid

**API Validation** (bypass frontend validation):
```bash
curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -d '{"title": "   "}'
# Should return 422 with detail: "Title cannot be empty or whitespace-only"
```

---

### Scenario 9: Success Confirmation
**Spec**: _Given I perform any action, When the action succeeds, Then I receive a clear success confirmation_

**Steps**:
1. Create a goal → **Expected**: "Goal created successfully"
2. Edit a goal → **Expected**: "Goal updated successfully"
3. Mark goal as done → **Expected**: "Goal marked as done"
4. Delete a goal → **Expected**: "Goal deleted successfully"

---

### Scenario 10: Error Handling
**Spec**: _Given I perform any action, When the action fails, Then I receive a clear error message explaining what went wrong_

**Steps**:
1. Stop the backend server: `Ctrl+C` in backend terminal
2. Try to create a goal in the frontend
3. **Expected**:
   - Error banner appears: "Cannot connect to server. Please check your connection."
   - All action buttons are disabled (Create, Edit, Delete)
   - Cached goals (if any) are shown with a "stale" indicator

4. Restart the backend: `uv run uvicorn ai_life_backend.app:app --reload`
5. **Expected**:
   - Error banner disappears
   - Action buttons re-enable
   - Goals list revalidates and shows fresh data

---

## Edge Cases

### Edge Case 1: Empty Title (Whitespace-Only)
```bash
curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -d '{"title": "     "}'
# Expected: 422 with "Title cannot be empty or whitespace-only"
```

### Edge Case 2: Concurrent Edits (Last-Write-Wins)
**Setup**:
1. Open http://localhost:3000 in two browser tabs (Tab A, Tab B)
2. Both tabs show goal: "Test Goal"

**Steps**:
1. **Tab A**: Edit title to "Test Goal - Version A", click Save
2. **Tab B** (immediately after): Edit title to "Test Goal - Version B", click Save
3. **Expected**:
   - Tab B's edit overwrites Tab A's edit (last-write-wins)
   - Both tabs show "Test Goal - Version B" after revalidation

### Edge Case 3: Title Exceeds 255 Characters
```bash
curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -d '{"title": "'"$(python3 -c 'print("a" * 256)')"'"}'
# Expected: 422 with "Title cannot exceed 255 characters"
```

### Edge Case 4: Filter with No Matches
**Steps**:
1. Create 1 goal, mark it as done
2. Click "Active" filter
3. **Expected**:
   - Empty state message: "No active goals. Create one to get started!"
   - No error message

### Edge Case 5: No Goals at All
**Steps**:
1. Delete all goals
2. **Expected**:
   - Empty state message: "No goals yet. Create your first goal!"
   - "Create Goal" button is prominent

### Edge Case 6: Backend Unavailable
**Covered in Scenario 10 above**

---

## Performance Validation

### API Response Times
```bash
# List goals (should be <200ms)
time curl http://localhost:8000/api/goals

# Create goal (should be <200ms)
time curl -X POST http://localhost:8000/api/goals \
  -H "Content-Type: application/json" \
  -d '{"title": "Performance Test Goal"}'
```

**Expected**: All responses < 200ms (typically <50ms for simple queries)

### UI Interactions
1. Create goal → **Expected**: <100ms UI feedback (optimistic update)
2. Toggle completion → **Expected**: <100ms UI feedback
3. Filter change → **Expected**: <100ms UI update

---

## Database Verification

### Check Goal Count
```sql
SELECT COUNT(*) FROM goals;
```

### Check Sorting Order
```sql
SELECT title, is_done, date_updated
FROM goals
ORDER BY is_done ASC, date_updated DESC;
-- Verify: Active goals (is_done=false) appear first,
-- within each group, most recently updated first
```

### Check Indexes
```sql
\d goals;
-- Should show indexes: idx_goals_is_done, idx_goals_date_updated
```

---

## Cleanup

### Reset Database
```bash
cd backend
uv run alembic downgrade base
uv run alembic upgrade head
```

### Stop Services
```bash
docker-compose down
# Backend: Ctrl+C in terminal
# Frontend: Ctrl+C in terminal
```

---

## Success Criteria Checklist

- [ ] All 10 acceptance scenarios pass
- [ ] All 6 edge cases handled correctly
- [ ] API response times <200ms
- [ ] UI interactions <100ms
- [ ] Goals persist across browser sessions
- [ ] Backend unavailable error handling works
- [ ] Validation errors are user-friendly
- [ ] Success messages appear for all actions
- [ ] Database schema matches design (UUID, timestamps, indexes)
- [ ] Sorting order correct (active first, then by date_updated DESC)

---

**Quickstart Status**: ✅ READY - All scenarios defined, ready for implementation validation
