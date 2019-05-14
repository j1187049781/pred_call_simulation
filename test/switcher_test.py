import simpy

from agents import Agent
from switcher import Switcher
from client import Client

def set_lambda(env,switcher,num):
    yield env.timeout(3)
    switcher.dialing_lines.set_lambda_parm(num)
if __name__=='__main__':
    env = simpy.Environment()
    sw=Switcher(env,3)
    # sw.dialing_lines.set_lambda_parm(1)
    agent=Agent(env,3)

    # env.process(set_lambda(env, sw, 1))
    # talk_line=env.event()
    # finsh_sigal=env.event()
    # start_sigal=env.event()
    # env.process(cl.receive(start_sigal,talk_line,finsh_sigal,2,True,1))
    # env.process(sw.dial(start_sigal,talk_line,finsh_sigal,"1",3))
    #
    # talk_line=env.event()
    # finsh_sigal=env.event()
    # start_sigal = env.event()
    # env.process(cl.receive(start_sigal,talk_line,finsh_sigal,5,True,1))
    # env.process(sw.dial(start_sigal,talk_line,finsh_sigal,"12",3))
    #
    # talk_line=env.event()
    # finsh_sigal=env.event()
    # start_sigal = env.event()
    # env.process(cl.receive(start_sigal,talk_line,finsh_sigal,2,False,1))
    # env.process(sw.dial(start_sigal,talk_line,finsh_sigal,"123",3))

    for i in range(10):
        cl = Client(env, "{}".format(i))
        env.process(cl.receive( 0, True, 1,2))
        env.process(sw.dial(cl, 3,agent))

        cl = Client(env, "{}.{}".format(i,i))
        env.process(cl.receive( 2, True, 1,2))
        env.process(sw.dial(cl, 1,agent))
    env.process(set_lambda(env,sw,1))
    env.run()


