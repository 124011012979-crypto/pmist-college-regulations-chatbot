# pmist-college-regulations-chatbot
AI-powered PMIST College Regulations Chatbot

## Deploy on Render

1. Push or merge this branch into your deployment branch.
2. In Render, choose **New → Blueprint** and connect this GitHub repository. Render reads the root `render.yaml` to configure the web service.
3. When prompted, enter your provider key as the `API_KEY` environment variable. Do not commit the key to the repository.
4. Deploy the service. Render will install dependencies from `requirements.txt` and start the Flask app with Gunicorn.

`API_URL` and `MODEL` are optional environment variables; the app has defaults for both. The static page is served from `sstatic/`.
