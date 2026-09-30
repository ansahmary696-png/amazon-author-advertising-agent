services:
  - type: web
    name: daniel-author-agent
    plan: free
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --bind 0.0.0.0:$PORT
    envVars:
      - key: SECRET_KEY
        value: change_this_secret
      - key: ADMIN_USERNAME
        value: daniel
      - key: ADMIN_PASSWORD
        value: author123
