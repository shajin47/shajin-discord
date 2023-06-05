from superagi.tools.thinking.tools import LlmThinkingTool
import os

def handle_response(message) -> str:
    p_message = message.lower()
    if p_message != '' and p_message != None:
        if p_message[:4] == "ask/":
            obj_llm = LlmThinkingTool()
            return obj_llm._execute(p_message)

    #  return 'Yeah, I don\'t know. Try typing "!help".'