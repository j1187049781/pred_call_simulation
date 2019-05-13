import simpy

from agents import Agent

if __name__=='__main__':
    env = simpy.Environment()
    agent=Agent(env,1)
    with agent.request() as req:
        print(agent)