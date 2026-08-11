---
name: photo-restoration
description: Restore vintage, blurry, faded, scratched, or damaged photographs with a preservation-first workflow. Use when the user asks to repair an old photo, remove scratches or stains, recover faded detail, sharpen a blurry picture, colorize a black-and-white photo, or give a restored photo a modern look.
---

# Photo Restoration

Restore old photographs with ImageGen while protecting the information that makes the original photograph recognizable and historically meaningful.

## Choose A Mode

Use **faithful restoration** by default. Repair scratches, folds, stains, film grain, fading, exposure problems, and recoverable blur. Keep the original black-and-white, sepia, or color state.

Use **modern enhancement** only when the user explicitly asks for a modern look, colorization, cinematic lighting, or similar changes. Enhancement may improve clarity, light, and local detail, but it still must preserve the subject, identity, pose, composition, and scene.

Do not apply a fixed 85mm lens look, shallow depth of field, cinematic lighting, or skin beautification unless the user explicitly requests that style. Do not claim that the built-in tool produced an actual 8K pixel file; describe 8K as a high-detail target only.

## Workflow

1. Confirm that an edit target is available. If the user has not supplied a photograph, ask them to upload one instead of generating a replacement image.
2. If the target exists only as a local file, load it with `view_image` first so it is visible in the conversation context. Treat it as the edit target, not merely a style reference.
3. Inspect the photograph for people, composition, era markers, text, and damage. Separate recoverable defects from missing areas that would require speculation.
4. Select faithful restoration unless the user explicitly requests modern enhancement. For a people-focused photograph use the `identity-preserve` edit taxonomy; for a person-free photograph or localized repair use `precise-object-edit`.
5. Build an ImageGen edit prompt with the structure below. State the requested repair first, then list every invariant and avoid item.
6. Use the built-in image editing tool by default. Use a CLI or explicit model path only after the user asks for it or explicitly approves the fallback and its API key requirement.
7. Inspect the result against the source. Check identity, facial proportions, age, expression, hair, pose, clothing, person count, subject placement, crop, aspect ratio, background, text, and historical details.
8. If identity or scene content drifted, discard that result and retry once with a single targeted constraint. Do not add new beautification requirements during the retry.
9. Save a new version by default and never overwrite the original unless the user explicitly requests replacement. Report the saved path, mode, and main repairs.

## Prompt Template

Use this labeled structure and fill only the details supported by the source image and user request:

```text
Use case: identity-preserve or precise-object-edit
Asset type: restored photograph
Primary request: <faithful restoration or explicitly requested modern enhancement>
Input images: Image 1 is the edit target
Restoration: <scratches, folds, stains, blur, fading, exposure, or noise to address>
Constraints: preserve identity, facial proportions, age, expression, hair, pose, clothing, person count, composition, crop, aspect ratio, background, text, and era details
Avoid: new people or objects, face changes, age changes, skin smoothing, composition changes, invented large details, text, watermark
```

For faithful restoration, add: `Keep the original monochrome, sepia, or color state. Change only the listed damage and quality defects.`

For modern enhancement, add only the requested style changes and repeat: `Keep the original identity, pose, composition, person count, and scene content unchanged.`

For colorization, state that color is the only intentional global change and preserve the original lighting, clothing, facial features, and composition.

## Guardrails

- Do not invent a face, person, object, or large missing area without telling the user that the result is speculative and obtaining confirmation.
- Do not alter identity, facial geometry, age, expression, pose, clothing, person count, or historical context.
- Do not colorize, modernize, glamorize, or change the era unless the user asks for it.
- Do not deliver an output with obvious identity drift, added people, changed framing, or a different scene.
- If the input is too damaged to preserve a critical area, explain the limitation before editing.
- If the built-in tool is unavailable, explain the CLI fallback and API key requirement; do not switch silently.
- Keep the source file untouched by default.

## Scope

Use this Skill for restoration and optional enhancement of old photographs. Route pure resizing or format conversion, background removal, background replacement, object replacement, and unrelated compositing to the general image editing workflow. This Skill does not provide batch restoration, deterministic traditional image algorithms, face recognition, manual mask authoring, or a standalone upscaler.
