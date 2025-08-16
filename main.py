import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from game_tool import roll_dice, generate_event

load_dotenv()
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True)

narrator_agent = Agent(
    name = "NarratorAgent",
    instructions= "You narrate the adventure. Ask the player for choices.",
    model=model
)
monster_agent= Agent(
    name="MonsterAgent",
    instructions= "You handle monster encounters using roll dice and generate_event.",
    model=model,
    tools=[roll_dice, generate_event]
)
item_agent = Agent(
    name = "ItemAgent",
    instructions= "You provide the rewards or item for the player.",
    model=model
)

def main():
    print("\U0001F3AE Welcome to the Fantasy Game\n")
    choice = input(" Do you enter the forest or turn back? ")

    result1 =  Runner.run_sync(narrator_agent, choice, run_config=config)
    print("\n  Story:", result1.final_output)

    result2 =  Runner.run_sync(monster_agent, "Start encounter", run_config=config)
    print("\n  Encounter:", result2.final_output)

    result3 =  Runner.run_sync(item_agent, "Give rewards", run_config=config)
    print("\n  Rewards:", result3.final_output)

if __name__ == "__main__":
    main()


