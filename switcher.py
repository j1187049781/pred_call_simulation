import simpy

from queue import Queue, Empty, Full

import simpy

class DialingLine(simpy.PriorityResource):
    def __init__(self, env,capacity):
        super().__init__(env,capacity)
        self.request_close_buff=Queue(capacity) # 关闭线路的资源句柄存放buffer,lambda_parm值减小1，关闭一个
        self.lambda_parm=capacity
    def set_lambda_parm(self,lambda_parm):
        lambda_parm =0 if lambda_parm<0 else lambda_parm
        lambda_parm = self.capacity if lambda_parm > self.capacity  else lambda_parm
        self.lambda_parm = lambda_parm

        close_num=(self.capacity - lambda_parm)
        closing_num=close_num-self.request_close_buff.qsize()
        if closing_num>0:
            self.increase_close_lines(closing_num)
        elif closing_num<0:
            self.decrease_close_lines(-closing_num)
    def decrease_close_lines(self,num):
        assert self.capacity-num>=0
        if not self.request_close_buff.empty():
            for i in range(num):
                req=self.request_close_buff.get_nowait()
                self.release(req)

    def increase_close_lines(self,num):
        for i in range(num):
            req=self.request(priority=-1)
            self.request_close_buff.put_nowait(req)
    def get_available_lines(self):
        return self.capacity-self.count-self.request_close_buff.qsize()

class Switcher():
    def __init__(self, env, max_concurrent_dialing):
        '''

        :param env:
        :param max_concurrent_dialing: 交换机的最大同时拨号数
        '''
        self.env=env
        self.max_concurrent_dialing=max_concurrent_dialing
        self.dialing_lines = DialingLine(env, max_concurrent_dialing) #lambda_parm: 同时拨号数
    def dial(self,client,conn_patience,agent):
        '''
        拨打一个电话号
        :param tel_num: 电话号
        :param conn_patience: 未接通超时挂断
        :return: (tel_num,patience,status,talk_time,agent_id)
        '''
        output_info=""
        start_signal, talk_line, start_service_signal,no_wait_patience_signal, finsh_signal=client.line
        with self.dialing_lines.request(priority=0) as req:
            yield req
            output_info+="{} 拨打电话号: {} ...\t".format(self.env.now,client.tel_num)
            print("{} 拨打电话号: {} ...\t ,usable {}".format(self.env.now, client.tel_num,self.dialing_lines.get_available_lines()))
            start_signal.succeed()
            respone_timeout=self.env.timeout(conn_patience)
            ret=yield  talk_line | respone_timeout

            if talk_line in ret:
                if ret[talk_line]=="nohup":
                    output_info+="{} 连接成功,加入连接客服队列\t".format(self.env.now)
                    with agent.request() as req:
                       conn_agent_ret=yield req  | no_wait_patience_signal
                       if req in conn_agent_ret:
                           start_service_signal.succeed()
                           output_info+="{} 连接到客服... ".format(self.env.now)
                           yield finsh_signal
                           output_info+="{} 完成服务，断开连接\t".format(self.env.now)
                       else:
                           output_info+="{} 客户离开客服队列\n".format(self.env.now)
                else:
                    output_info+="{} 客户 {} 挂断\n".format(self.env.now)
            else:
                output_info+="{} 超过拨号等待时间，交换机挂断\n".format(self.env.now)
            print(output_info)