# Intake And Understanding

## Parse Before Asking

Extract every explicit answer from the conversation, attached plan, and stated delegation. Normalize dates, currencies, traveler counts, fixed bookings, and constraints without changing their meaning. Ask only missing questions in one consolidated numbered questionnaire; never repeat a field already answered.

Treat `no preference`, `not needed`, and `decide for me` as understood or delegated only for semantically delegable preferences, such as lodging style, optional dining choices, route shape, or output styling. Do not use them to invent non-delegable facts or safety-critical facts: origin, destination, dates or duration, traveler count and composition, budget ceiling or range, actual mobility or health constraints, citizenship or travel-document jurisdiction and type, country of residence, document expiry, entry-authorization status, driver count, license suitability, driving capacity, mountain-road tolerance, and night-driving limit must come from the traveler or a responsible authority where applicable. Treat nonsensical delegation of such a field as unresolved and blocking. For self-drive, allow delegation of an unbooked vehicle-class preference or loop preference, but require the traveler to state actual or booked vehicle facts and every driver or safety limit. An explicit factual answer such as `no mobility constraints` is valid; `decide my mobility constraints for me` is not. Do not treat silence, urgency, or a broad request to handle everything as delegation. Record conflicting answers and ask the traveler to choose or correct them.

## Use Seven Weighted Groups

Score only applicable atomic fields that are explicit or validly delegated. Resolve an atom only when every material qualifier named by that atom is known; a partial answer receives no credit and remains a follow-up question. For example, a booked flight described only as `morning` or `evening` does not resolve fixed long-distance transport when exact airports or local departure and arrival times materially affect the arrival or departure plan. Calculate each group as `group weight × resolved applicable atomic fields ÷ all applicable atomic fields`. Exclude a conditionally non-applicable field from that group's denominator only after its non-applicability is explicit; do not award credit for the excluded field. Sum the unrounded group scores, then round the total once to the nearest whole percent, with `.5` rounded up. Every group below contains at least one always-applicable field, so its denominator cannot be zero.

| Group | Weight |
| --- | ---: |
| Basics | 25% |
| Travelers | 15% |
| Transport and self-drive | 15% |
| Budget and accommodation | 15% |
| Pace and preferences | 15% |
| Diet, health, and safety | 10% |
| Bookings and output | 5% |
| **Total** | **100%** |

Use exactly these atomic fields within each group. Count each semicolon-separated item as one atom:

- **Basics, 10 base or conditional atoms:** origin; destination; intermediate stops or explicit none; exact dates or duration; date flexibility; trip purpose; and, when the itinerary crosses an international or immigration border, entry identity basis; country of residence when relevant; travel-document expiry; current visa or entry-authorization status. Resolve `entry identity basis` with traveler citizenship or with both travel-document issuing jurisdiction and document type. Never collect the document number. Treat `not applicable`, `not yet obtained`, `pending`, or `approved` as explicit authorization statuses; `not yet obtained` permits requirements research but does not establish entry eligibility.
- **Travelers, 6 base or conditional atoms:** total count; composition; child details when children travel; senior details when seniors travel; mobility and accessibility facts; pregnancy or care facts when applicable.
- **Transport and self-drive, 11 base or conditional atoms:** inbound main transport; outbound main transport; local main transport; self-drive applicability; and, only when self-drive applies, vehicle type; driver count; license suitability; daily driving maximum; loop preference; mountain-road tolerance; night-driving limit.
- **Budget and accommodation, 9 atoms:** budget ceiling or range; currency; total or per-person basis; long-distance transport inclusion; lodging type; nightly range; room arrangement; preferred area; hotel-change tolerance.
- **Pace and preferences, 10 atoms:** pace; usual start time; latest finish time; nightlife preference; walking limit; rest frequency; interests; must-do items; optional items; avoid items.
- **Diet, health, and safety, 11 atoms:** diet preference; dietary restrictions; allergies; health facts; medication facts; altitude constraints; weather constraints; activity constraints; remote-area tolerance; high-risk-activity tolerance; public-safety concerns.
- **Bookings and output, 5 atoms:** fixed long-distance transport; fixed lodging; fixed tickets, reservations, or immovable times; requested output format; AI-image consent.

Treat these fields as critical blockers regardless of score: destination; origin; exact dates or duration; traveler count and composition; main transport; budget ceiling or range; and actual safety or mobility constraints, including an explicit statement that none apply. For international or border-crossing travel, also block on entry identity basis, country of residence when relevant, and travel-document expiry. Require an explicit visa or entry-authorization status before research, but accept `not yet obtained` as a resolved status so research can determine the requirement. When self-drive applies, also block on vehicle type, driver count, license suitability, daily driving maximum, loop preference, mountain-road tolerance, and night-driving limit.

Apply these gates:

- On the first intake, ask every missing field in one numbered questionnaire.
- After a partial reply, recalculate. Below 95%, ask all unresolved applicable fields that materially affect the score or plan, including non-blocking fields needed to reach 95%. Keep them in one consolidated follow-up and never repeat resolved fields.
- With any conflict, identify the conflicting values and wait for clarification.
- At 95% or higher with no blocker or conflict, present the understood-trip summary. Include delegated choices and assumptions explicitly, then wait for affirmative user confirmation before research.

## Numbered Questionnaire

Include only unanswered lines and preserve the seven group headings and numbering.

1. **Basics**
   - Origin:
   - Destination and intermediate stops:
   - Exact departure and return dates, or duration and date flexibility:
   - Main purpose of the trip:
   - For international or border-crossing travel, traveler citizenship or travel-document issuing jurisdiction and document type for each traveler whose details differ (never provide a document number):
   - Country of residence when relevant to entry or transit rules:
   - Travel-document expiry date for each traveler whose details differ (never provide a document number):
   - Current visa or entry-authorization status: not applicable, not yet obtained, pending, or approved:
2. **Travelers**
   - Total traveler count and composition:
   - Children and ages; seniors and relevant needs:
   - Mobility, accessibility, pregnancy, or care requirements:
3. **Transport and self-drive**
   - Main transport to, from, and within the destination:
   - Self-drive, rental car, hired driver, or public transport preference:
   - Vehicle type:
   - Driver count:
   - License suitability for every jurisdiction:
   - Maximum driving time per day:
   - Loop-route preference:
   - Mountain-road tolerance:
   - Night-driving limit:
4. **Budget and accommodation**
   - Total or per-person budget, currency, and whether long-distance transport is included:
   - Lodging type, nightly range, room arrangement, and preferred areas:
   - Hotel-change tolerance:
5. **Pace and preferences**
   - Preferred pace, usual start time, latest finish, and nightlife interest:
   - Walking limit and rest frequency:
   - Interests, must-do items, optional items, and explicit avoids:
6. **Diet, health, and safety**
   - Diet, allergies, and restrictions:
   - Medical, medication, altitude, weather, or activity constraints:
   - Risk tolerance for remote areas, high-risk activities, and public-safety concerns:
7. **Bookings and output**
   - Fixed flights or rail with exact airports or stations and local departure and arrival dates and times; fixed lodging, tickets, reservations, or other immovable times:
   - Requested Markdown, illustrated standalone HTML, or later PDF output:
   - Explicit consent or refusal for AI-generated cover or atmosphere images:

Invite replies by number. Accept concise delegation such as `4. Lodging style: decide for me` only where the field is a preference. Reject invalid delegation of traveler facts or safety limits and ask for the actual value.

## Understood-Trip Summary

Use this field-labeled structure. Omit no critical field and distinguish confirmed facts, delegation, and assumptions.

### Confirmed trip

- Origin:
- Destinations and route scope:
- Dates and duration:
- Travelers and composition:
- Citizenship or travel-document issuing jurisdiction and type:
- Country of residence when relevant:
- Travel-document expiry:
- Visa or entry-authorization status:
- Main transport:
- Self-drive constraints:
- Budget and currency:
- Accommodation requirements:
- Pace, walking, and rest limits:
- Interests, must-do items, and avoids:
- Diet, health, mobility, and safety constraints:
- Fixed bookings and times:
- Requested output:
- AI-image consent:

### Delegated choices

- Agent-decided items:

### Assumptions to verify

- Non-critical working assumptions:

### Understanding result

- Score:
- Critical blockers: none
- Conflicts: none

Ask the traveler to affirm or correct the summary and wait for the response. Start research only after affirmative confirmation. If corrected, update the atomic fields, rescore, present a revised summary when the gates pass, and wait for confirmation again.
