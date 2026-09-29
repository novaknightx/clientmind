# Synthetic client data — seed this into Hindsight at startup

CLIENTS = {
    "priya_sharma": {
        "name": "Priya Sharma",
        "project": "Brand Redesign",
        "avatar": "🎨",
        "history": [
            "Client prefers minimalist design style over complex layouts.",
            "Rejected the blue color palette in session 2. Wants warm earthy tones instead.",
            "Approved the moodboard in session 3. Final asset deadline is this Friday.",
            "Client communicates best over async messages. Prefers bullet points over paragraphs.",
            "Budget is fixed at ₹45,000. No scope for expansion was mentioned."
        ]
    },
    "rahul_mehta": {
        "name": "Rahul Mehta",
        "project": "SaaS Landing Page",
        "avatar": "💻",
        "history": [
            "Client wants the landing page to convert developers, not managers.",
            "He strongly dislikes stock photos. Wants code snippets and terminal screenshots instead.",
            "Pricing section caused confusion in last review. Needs a complete rework.",
            "Client is technical and gives very detailed feedback. Expects same level of detail back.",
            "Launch deadline is end of month. He mentioned investor demo is dependent on this."
        ]
    },
    "ananya_iyer": {
        "name": "Ananya Iyer",
        "project": "Social Media Strategy",
        "avatar": "📱",
        "history": [
            "Client runs a sustainable fashion brand targeting Gen Z women in metro cities.",
            "Previous agency used too many hashtags. She wants a cleaner, editorial feel.",
            "Instagram is the primary channel. LinkedIn is secondary.",
            "She approved the content calendar for October in the last session.",
            "Client is very responsive on WhatsApp but slow on email."
        ]
    }
}

def seed_client_memories():
    """Call this once at startup to load all client history into Hindsight."""
    from memory import retain
    for client_id, data in CLIENTS.items():
        for memory in data["history"]:
            retain(client_id, memory)
    print("✅ Client memories seeded into Hindsight.")