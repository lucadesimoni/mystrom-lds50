# ⚠️ IMPORTANT: HACS Validation Requires GitHub Settings

## The Problem

HACS validation is failing with these errors:
- ❌ Repository has no description
- ❌ Repository has no valid topics

**These errors CANNOT be fixed in code files.** They require GitHub repository settings.

## ⚡ Quick Fix (2 minutes)

### Step 1: Add Repository Description

1. Go to: **https://github.com/lucadesimoni/mystrom-lds50**
2. Click the **⚙️ gear icon** next to the "About" section (on the right sidebar)
3. In the "Description" field, paste this:

```
A lightweight, modern Home Assistant integration for MyStrom devices (Switch, Zero, Bulb, Button) with full REST API support.
```

4. Click **Save changes**

### Step 2: Add Repository Topics

Still in the same "About" section:

1. In the "Topics" field, type or paste each topic (press Enter after each):
   - `home-assistant`
   - `home-assistant-integration`
   - `homeassistant`
   - `hacs`
   - `mystrom`
   - `home-automation`
   - `python`
   - `integration`

2. Click **Save changes**

### Step 3: Verify

1. Refresh your repository page
2. You should now see:
   - ✅ Description appears under the repository name
   - ✅ Topics appear as tags below the description

### Step 4: Trigger Validation

After saving, make any small change and push to trigger CI:

```bash
git commit --allow-empty -m "Trigger HACS validation after adding description and topics"
git push
```

## Visual Guide

The settings are located here on your GitHub repository page:

```
┌─────────────────────────────────────────┐
│ Repository: lucadesimoni/mystrom-lds50  │
│                                         │
│ ⚙️ [Click this gear icon to edit]      │ ← About section
│                                         │
│ Description: [Your description]         │ ← Must have text
│ Topics: #home-assistant #hacs ...      │ ← Must have at least one
└─────────────────────────────────────────┘
```

## Why This Happens

HACS validation checks your **GitHub repository metadata** (stored on GitHub's servers), not files in your repository. This is by design - it ensures repositories have proper metadata for discovery and categorization.

## All Code Issues Are Fixed ✅

All code-related validation errors have been resolved:
- ✅ MyPy type checking
- ✅ Pylint warnings
- ✅ Ruff formatting
- ✅ Hassfest validation
- ✅ Markdown linting
- ✅ Services.yaml created

**The ONLY remaining issue is the GitHub repository settings above.**

