import os
import asyncio
from termcolor import cprint
from deepseek_handler import call_deepseek

# Configuration
MAX_HISTORY = 5
REASONING_COLOR = 'yellow'
ANSWER_COLOR = 'cyan'
PROMPT_COLOR = 'green'

async def main():
    conversation_history = []
    
    try:
        cprint("\n🛠️  Initializing Interactive Reasoning Explorer...", 'magenta', attrs=['bold'])
        cprint("🔗 DeepSeek R1 Model: Chain-of-Thought Enabled\n", 'blue')
        
        while True:
            # Get user question with history context
            user_query = input(f"\n{'-'*40}\n🎯 Your question (q to quit): \n> ").strip()
            if user_query.lower() in ['q', 'exit']:
                break

            # Call DeepSeek with streaming
            response = await call_deepseek(user_query)
            if not response:
                cprint("\n⚠️ Failed to get valid response", 'red')
                continue

            # Store conversation context
            conversation_entry = {
                'question': user_query,
                'reasoning': response['reasoning'],
                'answer': response['content']
            }
            conversation_history = ([conversation_entry] + conversation_history)[:MAX_HISTORY]

            # Continue showing options until user starts new topic or exits
            while True:
                # Show interaction options
                cprint("\n🔍 How would you like to proceed?", 'magenta')
                cprint("1. Ask follow-up question")
                cprint("2. Explain reasoning in more detail")
                cprint("3. Show me examples")
                cprint("4. Start new topic")
                cprint("5. Exit")
                
                choice = input("\n⏩ Your choice (1-5): ").strip()
                
                if choice == '5':
                    return  # Exit the program
                elif choice == '4':
                    conversation_history = []
                    cprint("\n🧹 Starting fresh conversation...\n", 'yellow')
                    break  # Break inner loop to get new topic
                elif choice in ['2', '3']:
                    # Build follow-up prompt based on reasoning
                    follow_up_prompt = f"Regarding this reasoning:\n{response['reasoning']}\n\n"
                    if choice == '2':
                        follow_up_prompt += "Explain this thought process in more detail."
                    else:
                        follow_up_prompt += "Provide concrete examples to support this reasoning."
                    
                    # Get clarification
                    clarification = await call_deepseek(follow_up_prompt)
                    if clarification:
                        cprint("\n📚 Expanded Explanation:", 'magenta')
                        cprint(clarification['content'], ANSWER_COLOR)
                        # Update the response for future follow-ups
                        response = clarification
                elif choice == '1':
                    break  # Break inner loop to ask follow-up
                else:
                    cprint("\n⚠️ Invalid choice, please try again", 'red')

    except Exception as e:
        cprint(f"\n🚨 Critical error: {str(e)}", 'red', attrs=['bold'])
    finally:
        cprint("\n🔚 Session ended. Goodbye! 👋\n", 'magenta', attrs=['bold'])

if __name__ == "__main__":
    asyncio.run(main()) 