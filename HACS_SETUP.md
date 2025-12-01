# HACS Setup Instructions

To pass HACS validation, you need to configure the following in your GitHub repository settings:

## Required Steps

### 1. Add Repository Description

1. Go to your GitHub repository: https://github.com/lucadesimoni/mystrom-lds50
2. Click on the **⚙️ Settings** tab
3. Scroll down to the **Features** section
4. Or simply click the **⚙️ gear icon** next to the "About" section on the repository homepage
5. Add a description, for example:

   ```text
   A lightweight, modern Home Assistant integration for MyStrom devices (Switch, Zero, Bulb, Button) with full REST API support.
   ```

### 2. Add Repository Topics

1. On your repository homepage, click the **⚙️ gear icon** next to the "About" section
2. In the "Topics" field, add the following topics:

   - `home-assistant`
   - `home-assistant-integration`
   - `homeassistant`
   - `hacs`
   - `mystrom`
   - `home-automation`
   - `python`
   - `integration`

These topics help HACS and users discover your integration.

## Verification

After adding the description and topics, the HACS validation should pass on your next commit/push.

## Note

These settings are **GitHub repository metadata** and cannot be configured through code. They must be set manually in the GitHub repository settings.
