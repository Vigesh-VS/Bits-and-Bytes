# Integration contract

## Trust model

The React client must call the Role 2 trusted backend first. That backend verifies Firebase Auth and any doctor share authorization, then invokes this service with a server-derived scope and authorized file bytes. Do not forward browser-supplied patient IDs, roles, or share token state. Replace the demo `authorized_patient` dependency with this adapter before deployment.

Suggested adapter input: `{subject_id, permitted_patient_id, permitted_record_ids, share_expires_at, share_revoked}`. Reject expired/revoked shares before invoking retrieval or processing. Pass only records in `permitted_record_ids`; doctor access must not default to the full history.

## Example responses

`POST /api/v1/medicines/reconcile` accepts `{ "medications": [{"record_id":"r1","original_name":"Glucophage","strength":"500 mg"}] }`. It returns normalized medicines and review alerts, never treatment instructions.

`POST /api/v1/chat/query` accepts `{ "question":"What is my HbA1c?", "record_ids":["r1"] }`; response contains `answer`, citation objects (`record_id`, title, date, page, excerpt), evidence state, limitations and follow-ups. Citations are constructed only from retrieved permitted records.

`POST /api/v1/process-document` is multipart with `file`. Send bytes only after Storage authorization. Its response contains a reviewable record, proposed medicines/labs, and `manual_entry_required`; persist user corrections in the Role 2 owned store.
