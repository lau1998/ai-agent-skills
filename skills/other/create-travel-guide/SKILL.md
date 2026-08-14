---
name: create-travel-guide
description: Use when planning a domestic or international trip, road trip, multi-city itinerary, family vacation, or revising an existing travel plan that needs traveler-specific research, routing, budgeting, transport, accommodation, safety, or Markdown, illustrated HTML, and PDF guide output.
---

# Create Travel Guide

Understand first, verify second, plan last. Treat a plausible itinerary as incomplete until traveler constraints and current facts support it.

## Route References

- Read [references/intake.md](references/intake.md) before collecting or scoring trip details.
- Read [references/research-verification.md](references/research-verification.md) before any online research.
- Read [references/itinerary-quality.md](references/itinerary-quality.md) before constructing or revising an itinerary.
- Read [references/output-formats.md](references/output-formats.md) before choosing a format, sourcing images, generating images, or exporting a PDF.

## Follow The Seven States

1. **Collect information:** Parse every supplied answer. Ask all missing questions once in a consolidated numbered questionnaire.
2. **Wait for details:** Incorporate answers, ask every unresolved field that materially affects the score or plan, and surface conflicts instead of resolving them silently. Never repeat a resolved field.
3. **Confirm understanding:** At 95% or higher with every critical field resolved, present the understood-trip summary and wait for affirmative user confirmation. Apply corrections, rescore, and gate again; do not research before confirmation.
4. **Online research:** Verify date-specific facts through current sources and preserve citations.
5. **Build itinerary:** Construct a feasible route, schedule, lodging strategy, transport plan, and budget from confirmed constraints.
6. **Quality check:** Replan every route, time, budget, fatigue, mobility, or safety conflict. Do not leave an impossible plan in place with a warning.
7. **Delivery:** Deliver only verified, internally consistent output in the requested supported format.

## Enforce Hard Gates

- Do not research when understanding is below 95%, any critical field is missing, or answers conflict.
- Do not infer critical answers from stereotypes, popular routes, urgency, or a request to "just decide." Accept explicit delegation only for semantically delegable preferences; never invent or delegate away traveler facts or safety-critical facts.
- For international or border-crossing travel, require the travel-document type plus either traveler citizenship or travel-document issuing jurisdiction, country of residence when relevant, travel-document expiry, and explicit current visa or entry-authorization status. These facts are non-delegable. Never request a passport or document number. Do not build or deliver a final plan until the qualifiers are collected and the responsible authority verifies the consequential entry requirements; `not yet obtained` is a valid status for starting that verification, not proof of eligibility.
- Do not present a pseudo-complete guide when the network is unavailable or a current critical fact cannot be verified. State the unverified scope and offer only verified alternatives.
- Keep source traceability in the final guide or its appendix. Do not hide sources because an output is client-facing or because the user prioritizes appearance.

## Handle Narrow Queries

For a single-fact request such as one attraction's hours, one transport segment, one visa rule, or one price, skip the full questionnaire. Before research, collect only the missing qualifiers required to answer that exact fact, such as travel-document type plus citizenship or issuing jurisdiction, document expiry, residence when relevant, and travel purpose for a visa, or exact date, route, travelers, and occupancy for transport or price. Never request a passport or document number. Then verify online, check the applicable date, and cite the source and verification date. Refuse to convert model memory into a current answer when verification is unavailable.

## Prevent Silent Assumptions

- Never invent dates, duration, arrival or departure gateways, route direction, traveler count, fitness, transport mode, driving status, budget, season, vehicle, lodging standard, citizenship, travel-document jurisdiction or type, residence, document expiry, entry-authorization status, or dynamic prices to make a guide look directly deliverable.
- For self-drive trips, treat vehicle type, driver count, license suitability, daily driving maximum, loop preference, mountain-road tolerance, and night-driving limit as conditional blockers. Knowing these inputs does not make late or night driving safe. Replan whenever confirmed limits, daylight, fatigue guidance, weather, road conditions, or official safety advice would be violated.
- Require explicit prior consent for AI images. Never disguise them as real or remove the required `AI 生成示意图` label. Preserve source traceability for real images and all current facts despite user pressure.

## Respect Operation And Privacy Limits

- Do not book, pay, purchase, cancel, or submit personal, identity, payment, contact, or health data to third parties.
- Do not claim to replace legal, medical, visa, consular, public-safety, or emergency authorities. Link to the responsible current authority for consequential requirements.
- Refuse unsafe or unlawful itinerary elements and provide a verified safer alternative.
