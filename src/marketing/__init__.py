#!/usr/bin/env python3

from src.marketing.agent import MarketingAgent


def main():
    agent = MarketingAgent()
    print(agent.summary())


if __name__ == "__main__":
    main()
