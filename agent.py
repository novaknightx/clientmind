from groq import Groq
from memory import retain, recall
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_opening_brief(client_id: str, client_name: str, project: str) -> str:
    """Generate a memory-powered brief before the conversation starts."""
    
    # Recall everything about this client
    memories = recall(client_id, f"summary of all work and preferences for {client_name}")
    memory_text = "\n".join([m.get("content", "") for m in memories.get("results", [])])
    
    system_prompt = f"""You are a smart assistant helping a freelancer manage their client relationships.
You have access to the complete history of interactions with this client.

Client: {client_name}
Project: {project}

Here is everything you remember about this client:
{memory_text}

Generate a short, warm briefing (3-4 sentences) for the freelancer before they start this session.
Mention: what was last discussed, any pending items, and one preference to keep in mind.
Speak directly to the freelancer. Start with "Welcome back."
Do not make up details. Only use what's in the memory above."""

    response = client.chat.completions.create(
        model="qwen/qwen3-32b",
        messages=[{"role": "user", "content": "Give me the client brief."}],
        temperature=0.7,
    )
    
    # Handle potential function calling errors from Groq
    try:
        return response.choices[0].message.content
    except Exception:
        return f"Welcome back. Here's what I remember about {client_name}: {memory_text[:300]}..."

def chat_with_client(client_id: str, client_name: str, project: str, 
                     conversation_history: list, user_message: str) -> str:
    """Handle a conversation turn, with memory context injected."""
    
    # Recall relevant memories for this specific message
    memories = recall(client_id, user_message)
    memory_text = "\n".join([m.get("content", "") for m in memories.get("results", [])])
    
    system_prompt = f"""You are helping a freelancer communicate with their client {client_name} 
about the project: {project}.

Relevant memories about this client:
{memory_text}

Use this context naturally in your response. 
Be professional, concise, and reference past interactions when relevant."""

    messages = [{"role": "system", "content": system_prompt}] + conversation_history
    messages.append({"role": "user", "content": user_message})
    
    try:
        response = client.chat.completions.create(
            model="qwen/qwen3-32b",
            messages=messages,
            temperature=0.7,
        )
        assistant_reply = response.choices[0].message.content
    except Exception as e:
        assistant_reply = f"I encountered an issue: {str(e)}. Please try again."
    
    # Retain this new interaction as a memory
    retain(client_id, f"Freelancer said: {user_message}. Agent responded: {assistant_reply[:200]}")
    
    return assistant_reply