# Discord Bot Persistence Layer

This document explains how the persistence layer works in the Discord moderation bot.

## Overview

The bot uses a simple file-based persistence system to store server information, moderation actions, and DM history. This ensures that the bot's state is preserved across restarts.

## Components

### 1. FileDB (db.py)

The `FileDB` class in `db.py` handles saving and loading data to/from JSON files:

- `save_messages(messages)`: Serializes the Messages object to JSON files
- `load_messages()`: Loads data from JSON files and creates a Messages object
- `ensure_db_dir()`: Creates the database directory if it doesn't exist

### 2. Messages Class (messages.py)

The `Messages` class has been extended with persistence methods:

- `save()`: Saves the current state to disk using FileDB
- `load()`: Class method that loads state from disk using FileDB
- Automatic saving after moderation actions

### 3. Moderation Class (moderation.py)

The `Moderation` class now:

- Attempts to load messages from disk on initialization
- Falls back to a new Messages instance if loading fails
- Saves changes to disk after updating server rules

### 4. Bot Shutdown Handler (bot.py)

The bot now handles graceful shutdown by:

- Registering signal handlers for SIGINT and SIGTERM
- Saving the messages state before shutting down
- Properly closing the bot connection

## Data Storage

Data is stored in the `db/` directory in two JSON files:

1. `servers.json`: Contains server information, rules, and moderation actions
2. `dm_history.json`: Contains DM message history

## Usage

The persistence layer works automatically:

- Data is loaded when the bot starts
- Changes are saved after moderation actions
- All data is saved when the bot shuts down

No manual intervention is required to manage the persistence.

## Troubleshooting

If you encounter issues with persistence:

1. Check that the `db/` directory exists and is writable
2. Verify that the JSON files are valid
3. Check the logs for any errors during loading or saving

If necessary, you can delete the JSON files to reset the bot's state. 