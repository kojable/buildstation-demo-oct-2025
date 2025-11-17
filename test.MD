Trace the bug causing the error: "APIError: User email is required" during workflow update.

## Goal
Identify why the user email is missing when saving workflow responses, and where the failure occurs in the backend or frontend flow.

## Context
- The error appears in the frontend console:  
  `Error saving workflow state to S3, falling back to sessionStorage: Error: Failed to update workflow`
- The JS trace points to `main.c02ed7ce.js:2`
- Backend flow involves:
  - `save_workflow_responses(workflow_id)` in `workflow.py`
  - `process_new_workflow(email, workflow_id, workflow_data)` in `dashboard_aggregation_service.py`
- Data is saved to:  
  `backend/data_storage/users/{email_hash}/responses/{workflow_id}_responses.json`

## Source
Refer to:
- `DATA_STORAGE_QUICK_REFERENCE.md` for file paths and save logic
- `DATA_FLOW_SUMMARY.md` for full architecture and flow
- Error trace from `main.c02ed7ce.js`

## Expectations
- Identify where the email is expected but missing
- Suggest possible causes (e.g. frontend not sending it, backend not extracting it)
- Recommend fixes or logging improvements to trace the issue
