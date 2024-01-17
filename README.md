# Odoo Discuss with Gemini

## Overview

Odoo Discuss-with-Gemini is a powerful module that integrates Gemini AI into Odoo's Discuss app, enhancing communication and content creation within the Odoo ecosystem.

## Features

- **Seamless Integration:** Connects Gemini AI seamlessly with Odoo Discuss.
- **Text => Text**
- **Text + Image => Text**
- **Text + multiple images => Text**

## Installation & Setup

Follow these steps to install and configure the Odoo Discuss with Gemini module:

1. **Get your free Gemini API key:** Visit [Gemini API Key](https://makersuite.google.com/app/apikey) to obtain your API key.

2. **Docker Compose:**
just run the following command then the project will run on port 8007
```
docker compose up
```

3. **Install google-generativeai:** 
```
pip install google-generativeai
```

4. **Install the module in your Odoo instance:** Use the provided module files and place them in the appropriate Odoo addons directory.

5. **Configure the Gemini API key:** Update the module settings with your Gemini API key.

6. **Start chatting with Gemini in Discuss:** Open Odoo Discuss and experience the power of AI-driven insights and content generation.

## Requirements

- Odoo version: 17.0
- Python libraries: `google-generativeai`
- Free Gemini API key with limits (60 queries/minute).

## Support & Customization

For any customization or support needs, please contact at [https://engelias.website](https://engelias.website).
