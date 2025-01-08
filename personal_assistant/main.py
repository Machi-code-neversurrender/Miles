import logging
from src.agent import PersonalAssistantAgent

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

def main():
    # Set up logging
    setup_logging()

    # Initialize the agent
    agent = PersonalAssistantAgent()

    # Run the agent
    agent.run()

if __name__ == "__main__":
    main()