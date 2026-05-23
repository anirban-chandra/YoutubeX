## Enhanced Dashboard for YouTube

An experimental backend service for building an **enhanced analytics and recommendation dashboard for YouTube videos and playlists**.  
It is implemented with **FastAPI** and is structured to be extended with real YouTube Data API integrations, **RRAG-based recommendation pipelines**, and a **creator analytics portal**.

### Features

- **FastAPI backend** with a modular structure (`routes`, `schemas`, `utils`, `config`)
- **Environment-based configuration** using `pydantic-settings`
- Typed **Pydantic models** for video data
- Placeholder endpoints for:
  - Fetching videos by topics
  - Fetching a single video by ID
  - Fetching related videos by ID

### Tech Stack

- **Language**: Python 3.12+
- **Framework**: FastAPI
- **Config**: pydantic-settings
- **Package / env management**: `uv` (via `pyproject.toml` and `uv.lock`)

---

### Project Structure

```text
.
├── main.py                 # Optional entrypoint (can be unused)
├── pyproject.toml          # Project metadata and dependencies
├── src/
│   ├── main.py             # FastAPI app factory and exception handlers
│   ├── routes/
│   │   ├── __init__.py
│   │   └── video_route.py  # Video-related HTTP routes
│   ├── schemas/
│   │   └── video.py        # Pydantic models for video data
│   ├── utils/
│   │   ├── __init__.py
│   │   └── video_functions.py  # Business logic / integration points
│   └── config/
│       ├── __init__.py
│       └── app_config.py   # AppConfig + environment loading
└── .env.example            # Example environment configuration
```

---

### Getting Started

#### 1. Prerequisites

- Python **3.12+**
- `uv` installed (`pip install uv` or see the uv docs)

#### 2. Clone and install dependencies

```bash
git clone https://github.com/<your-username>/Enhanced-Dashboard-For-Youtube.git
cd Enhanced-Dashboard-For-Youtube

uv sync
```

This will install all dependencies defined in `pyproject.toml`.

#### 3. Configure environment variables

Copy `.env.example` to `.env` and set your values:

```bash
cp .env.example .env
```

Then edit `.env`:

```text
YOUTUBE_API_KEY=your_youtube_api_key_here
```

`AppConfig` (`src/config/app_config.py`) reads this value using `pydantic-settings`.

#### 4. Run the development server

Using `uv` and FastAPI's standard runner:

```bash
uv run fastapi dev src/main.py
```

Or with `uvicorn` directly:

```bash
uv run uvicorn src.main:app --reload
```

By default, the API will be available at `http://127.0.0.1:8000`.

You can open the interactive API docs at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

---

### API Overview

All video-related routes are prefixed with `/api/videos`.

- **GET** `/`  
  - Simple health/welcome endpoint. Returns `"Hello"`.

- **GET** `/api/videos`  
  - **Query params**: `topics` (list of strings)  
  - **Response**: `list[Video]`  
  - Uses `get_videos_with_topics` in `utils.video_functions`. Currently returns an empty list (stub for future implementation).

- **GET** `/api/videos/{video_id}`  
  - **Path params**: `video_id` (string)  
  - **Response**: `Video`  
  - Uses `get_video_from_id`. Currently returns a dummy `Video` instance as a placeholder.

- **GET** `/api/videos/related_videos/{video_id}`  
  - **Path params**: `video_id` (string)  
  - **Response**: `list[Video]`  
  - Uses `get_related_videos_from_id`. Currently returns an empty list.

#### Video model (`Video`)

Defined in `src/schemas/video.py`:

- **name**: `str`, required, minimum length 1
- **duration**: `int`, required, must be ≥ 1 (seconds or any unit you choose)

You can extend this model with more fields like `video_id`, `channel_name`, `publish_date`, `views`, etc.

---

### Configuration Details

`AppConfig` in `src/config/app_config.py`:

- Inherits from `BaseSettings` (pydantic-settings)
- Loads environment variables from `.env`
- Currently exposes:
  - `youtube_api_key` (mapped from `YOUTUBE_API_KEY`)

You can safely import `get_config()` from `config.app_config` wherever you need configuration:

```python
from config.app_config import get_config

config = get_config()
print(config.youtube_api_key)
```

---

### Roadmap / TODO

- Implement real YouTube Data API integration in `video_functions.py`
- Add **playlist-related routes** (`playlist_route.py`) and schemas:
  - Fetch playlists for a channel
  - Compute playlist lengths / total watch time
  - Aggregate metrics across multiple playlists
- Implement **RRAG-based recommendation flows** to surface:
  - Best videos and playlists for a given topic/user
  - Personalized content recommendations based on viewing patterns
- Extend `Video` and upcoming `Playlist` schemas with richer metadata
- Add authentication and user-specific dashboards
- Build a **separate portal for content creators**:
  - Creator-level stats (views, watch time, RPM/CPM, engagement)
  - Funnel/retention views across videos and playlists
  - ML-powered suggestions for what kind of content to create next to maximize revenue
- Train and integrate ML models for:
  - Predicting future performance of planned content
  - Recommending optimal topics, formats, and publishing cadence
- Containerize the app with Docker and provide deployment instructions

---

### License

This project is licensed under the terms of the **MIT License**. See `LICENSE` for details.
# YoutubeX
