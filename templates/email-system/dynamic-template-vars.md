# Dynamic Email HTML Templates — Variable Contract

These templates are modular and intentionally not fixed copy.

## Templates
- `templates/email-system/debt-relief-v2.dynamic.html`
- `templates/email-system/personal-loan-cross-sell-v2.dynamic.html`

## Required Variables
- `email_subject`
- `preheader_text`
- `brand_name`
- `brand_primary_color`
- `headline`
- `intro_line`
- `primary_cta_label`
- `primary_cta_url`
- `signoff_line`
- `signature_name`
- `compliance_disclosure`
- `physical_address`
- `unsubscribe_url`

## Optional Variables
- `hero_kicker`
- `body_line_1`
- `body_line_2`
- `helper_text`
- `proof_points_html` (debt relief template)
- `comparison_points_html` (personal loan template)

## Conditional Sections
Any block wrapped in:
- `{{#if variable_name}} ... {{/if}}`

is rendered only when the variable is present and non-empty.

## Compliance Note
- Keep one primary CTA.
- Footer compliance text must remain present in all production sends.
