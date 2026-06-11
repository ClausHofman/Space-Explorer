# CSS and Form UI Guide

This project uses one shared stylesheet in `templates/base.html`.
Most form and action-panel behavior depends on these shared classes, so reuse them exactly.

## 1) Where styles and behavior live

- Shared CSS: `templates/base.html` inside the `<style>` block.
- Shared action-panel JavaScript: `templates/base.html` at the bottom `<script>` block.
- Reusable action panel partial: `templates/galaxy/_action_panel.html`.

If a new form should look like existing forms, do not add one-off inline styles in the form template.
Use the shared classes below.

## 2) Form action classes (Save/Cancel/Delete)

Use these classes for all form action rows:

- `.form-actions`
  - Horizontal row for action controls.
  - Adds spacing and alignment.
- `.button-link`
  - Makes an `<a>` look like a button.
  - Use this for Cancel links.
- `.btn-secondary`
  - Secondary style (Cancel).
- `.btn-primary`
  - Primary style (Save/Create).
- `.btn-danger`
  - Destructive primary style (Delete confirmations).

## 3) Recommended form template structure

Use this structure for new forms:

```html
<form method="post">
    {% csrf_token %}
    <input type="hidden" name="next" value="{{ cancel_url }}">
    {{ form.as_p }}

    <div class="form-actions">
        <a href="{{ cancel_url }}" class="button-link btn-secondary">Cancel</a>
        <button type="submit" class="btn-primary">Save</button>
    </div>
</form>
```

For destructive confirmations:

```html
<div class="form-actions">
    <a href="{{ cancel_url }}" class="button-link btn-secondary">Cancel</a>
    <button type="submit" class="btn-danger">Yes, delete</button>
</div>
```

## 4) Action panel classes and hooks

Action panel relies on class-based hooks. Keep these class names unchanged:

- `.action-toggle`
- `.toggle-arrow`
- `.action-panel`
- `.add-menu`
- `.add-button`
- `.add-dropdown`

These are used by the shared JavaScript for sliding and dropdown logic.

### Action panel markup pattern

```html
<div class="action-toggle">
    <span class="toggle-arrow">▶</span>
</div>

<div class="action-panel">
    <!-- action buttons -->

    <div class="add-menu">
        <button type="button" class="add-button">Add...</button>

        <div class="add-dropdown">
            <!-- dropdown links -->
        </div>
    </div>
</div>
```

## 5) Do and do not rules

Do:

- Reuse shared classes from `base.html`.
- Keep action/dropdown hooks class-based.
- Use `<a class="button-link ...">Cancel</a>` for cancel navigation.
- Keep primary action as a real submit `<button type="submit">`.

Do not:

- Do not use duplicate IDs for reusable UI parts.
- Do not wrap `<button>` inside `<a>`.
- Do not rename hook classes unless you also update shared JS.
- Do not remove `.action-panel.open { overflow: visible; }` (dropdown can get clipped).

## 6) Creating a new form checklist

1. Add/confirm the Django view and pass `cancel_url` in context.
2. Add `{% csrf_token %}` and hidden `next` input.
3. Render fields (`{{ form.as_p }}` or explicit fields).
4. Add `.form-actions` row.
5. Add Cancel as `.button-link.btn-secondary`.
6. Add submit as `.btn-primary` (or `.btn-danger` for delete).
7. Run checks: `python manage.py check`.
8. Manually verify button sizes/order and cancel navigation.

## 7) Quick troubleshooting

- Cancel looks bigger than Save:
  - Ensure Cancel uses `.button-link` and Save uses `.btn-primary`.
  - Ensure both are inside `.form-actions`.
- Dropdown does not appear:
  - Ensure `.add-dropdown` gets class `open` on click.
  - Ensure parent `.action-panel` opens and keeps `overflow: visible`.
- Only one panel works on page:
  - Check for duplicate IDs; use classes only.
