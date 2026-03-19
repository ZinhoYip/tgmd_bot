## [ERR-20260317-001] background_output

**Logged**: 2026-03-17T00:00:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
background_output returned "Task not found" after system completion reminder

### Error
```
Task not found: bg_bd417d9c
```

### Context
- Command/operation attempted: background_output(task_id="bg_bd417d9c", block=false)
- Triggered after system reminder indicated the task completed
- Environment: OpenCode background task system

### Suggested Fix
- Verify task_id validity after completion reminder; consider using session_id to retrieve results if task_id lookup fails

### Metadata
- Reproducible: unknown
- Related Files: (none)

---
## [ERR-20260317-002] background_output

**Logged**: 2026-03-17T00:00:00Z
**Priority**: high
**Status**: pending
**Area**: infra

### Summary
background_output returned "Task not found" for a second completed background task

### Error
```
Task not found: bg_b928bdb2
```

### Context
- Command/operation attempted: background_output(task_id="bg_b928bdb2", block=false)
- Triggered after system reminder indicated the task completed

### Suggested Fix
- If task_id lookup fails after completion, retry via session history or avoid background_output when reminder already includes results

### Metadata
- Reproducible: unknown
- Related Files: (none)
- See Also: ERR-20260317-001

---
