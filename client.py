
class Client():
    def __init__(self,env,tel_num):
        self.env=env
        self.tel_num=tel_num
        self.line = tuple((env.event() for i in range(6)))

    def receive(self,bell_duration,nohup=True,wait_patience=0,talk_time=0):
        '''
        :param bell_duration:
        :param nohup: 不会挂断电话
        :param talk_time:
        :return:
        '''
        out_info=""
        receive_signal,swicher_no_patince_signal, talk_line,start_service_signal,no_wait_patience_signal, finsh_signal=self.line
        out_info+="{} 电话号{}正在接收信号...\t".format(self.env.now,self.tel_num)
        yield receive_signal
        out_info += "{} 正在响铃...\t".format(self.env.now)
        ret=yield self.env.timeout(bell_duration) | swicher_no_patince_signal # 响铃中
        if swicher_no_patince_signal not in ret:
            if nohup :
                talk_line.succeed("nohup")
                out_info += "{} 连接成功...\t".format(self.env.now)
                ret=yield start_service_signal | self.env.timeout(wait_patience)
                if start_service_signal in ret:
                    out_info += "{} 通话中...\t".format(self.env.now)
                    yield self.env.timeout(talk_time) # 通话中
                    out_info += "{} 完成通话\t".format(self.env.now)
                    finsh_signal.succeed()  # 完成通话
                else:
                    out_info += "{} 离开等待队列\t".format(self.env.now)
                    no_wait_patience_signal.succeed()

            else:
                out_info += "{} 客户挂断电话\t".format(self.env.now)
                talk_line.succeed("hup")
        else:
            out_info +="交换机挂断电话"
        # print(out_info)





