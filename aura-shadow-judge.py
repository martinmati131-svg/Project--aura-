# aura_shadow_judge.py
def shadow_validate(user_reply, ai_tag):
    """
    Shadow Test: Verifies if the AI correctly tagged a user goal.
    """
    # Example: User says "I want to grow my business"
    # AI should tag as: 'Professional_Growth'
    valid_tags = ['Health', 'Professional_Growth', 'Zen_Flow', 'Technical']
    
    if ai_tag in valid_tags:
        return "PASS"
    else:
        return f"FAIL: Unknown tag '{ai_tag}' detected in Shadow Run."
