import simpy

class Agent(simpy.Resource):
    def __init__(self,env,capacity):
        super().__init__(env,capacity)

    def get_usage_precent(self):
        return self.count/self.capacity



