# Automated Security Incident Management Chatbot

This project implements an automated security incident management system that integrates with Gemini API for alert classification, JIRA for ticketing, and Slack for notifications.

## Features

- AI-powered alert classification using Gemini API
- Automated ticket generation in JIRA
- Real-time notifications via Slack
- RESTful API for alert processing

## Setup

1. Clone the repository
2. Create a `.env` file with your API keys and configuration
3. Install dependencies: `pip install -r requirements.txt`
4. Run the application: `python run.py`

## API Endpoints

- `POST /api/process_alert`: Process a security alert
- `GET /api/alerts/{alert_id}`: Get details of a specific alert

## Components

- FastAPI: Web framework for API endpoints
- Gemini API: AI model for alert classification
- JIRA: Ticketing system for incident management
- Slack: Real-time notifications
