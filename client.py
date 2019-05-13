
class Client():
    def __init__(self,env,tel_num):
        self.env=env
        self.tel_num=tel_num
        self.line = tuple((env.event() for i in range(5)))

    def receive(self,bell_duration,nohup=True,wait_patience=0,talk_time=0):
        '''
        :param bell_duration:
        :param nohup: 不会挂断电话
        :param talk_time:
        :return:
        '''
        receive_signal, talk_line,start_service_signal,no_wait_patience_signal, finsh_signal=self.line
        yield receive_signal
        yield self.env.timeout(bell_duration) # 响铃中
        if nohup :
            talk_line.succeed("nohup")
            ret=yield start_service_signal | self.env.timeout(wait_patience)
            if start_service_signal in ret:
                yield self.env.timeout(talk_time) # 通话中
                finsh_signal.succeed()  # 完成通话
            else:
                no_wait_patience_signal.succeed()

        else:
            talk_line.succeed("hup")





