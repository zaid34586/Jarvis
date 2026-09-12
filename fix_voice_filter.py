import os

voice_fix_code = '''# Filter logic for Speech Synthesis
def clean_text_for_speech(raw_text):
    # If text contains code block, speak only summary line before code
    if "```" in raw_text:
        summary_line = raw_text.split("```")[0].strip()
        if len(summary_line) > 0:
            return summary_line
        return "I have updated the code on your screen."
    
    # Trim long responses for voice output (max 200 chars)
    if len(raw_text) > 200:
        return raw_text[:180] + "... Check screen for complete output."
        
    return raw_text
'''

print("[SUCCESS] Voice Filter Logic Ready!")