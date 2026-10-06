"""
memory.py - Session State & Sliding Window Context Management for Apex Car Rental.
"""

import time
from typing import List, Dict, Optional

class SessionState:
    """Stores conversation history and metadata for a single user session."""
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.history: List[Dict[str, str]] = []  # List of {"role": "user"|"assistant", "content": "..."}
        self.last_citations: List[Dict] = []
        self.last_active = time.time()

    def add_user_message(self, message: str):
        self.history.append({"role": "user", "content": message.strip()})
        self.last_active = time.time()

    def add_assistant_message(self, message: str):
        self.history.append({"role": "assistant", "content": message.strip()})
        self.last_active = time.time()

    def get_sliding_window_history(self, max_turns: int = 8) -> List[Dict[str, str]]:
        """
        Returns the last `max_turns` conversation turns (up to max_turns * 2 messages)
        to prevent conversation history from overflowing LLM context memory.
        """
        max_messages = max_turns * 2
        return self.history[-max_messages:]

    def clear(self):
        """Resets conversation history for this session."""
        self.history = []
        self.last_citations = []
        self.last_active = time.time()


class ConversationManager:
    """Manages all active user sessions in memory."""
    def __init__(self, max_turns: int = 8):
        self.sessions: Dict[str, SessionState] = {}
        self.max_turns = max_turns

    def get_or_create_session(self, session_id: str) -> SessionState:
        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(session_id)
        return self.sessions[session_id]

    def reset_session(self, session_id: str):
        if session_id in self.sessions:
            self.sessions[session_id].clear()


# Global singleton instance
memory_manager = ConversationManager()
