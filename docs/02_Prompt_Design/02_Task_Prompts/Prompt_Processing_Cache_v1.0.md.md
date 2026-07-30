# Feature: Processing Cache

## Objective

Implement a processing cache to avoid reprocessing the same YouTube video.

Reuse existing outputs whenever possible.

---

## Requirements

Before processing a video, check whether previous outputs already exist.

### If Transcript and Study Note exist

- Skip processing.
- Enable download immediately.

### If only Transcript exists

- Reuse the existing Transcript.
- Generate the Study Note only.

### Otherwise

- Run the normal processing workflow.

---

## Regeneration

When the user selects **Regenerate Study Note**:

- Reuse the existing Transcript.
- Regenerate the Study Note only.

---

## Future Compatibility

Design the cache mechanism to support future generated outputs.

Generate only missing outputs.

---

## Constraints

Do NOT:

- Reprocess existing outputs.
- Redownload the same video unnecessarily.
- Redesign the UI.
- Modify the existing workflow.
- Modify unrelated code.

Modify only the files required for this feature.

Start implementing.