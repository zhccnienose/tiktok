import time


class SnowFake:
    """
    雪花算法生成id
    时间戳 | 数据汇总寻id | 机器id | 序列号
    """
    def __init__(self, worker, data_center):
        # 机器id
        self.worker = worker
        # 数据中心id
        self.data_center = data_center
        # 毫秒内计数器
        self.count = 0
        # 时间戳
        self.last_tstp = -1

    # 生成id
    def next_id(self):
        timestamp = int(time.time() * 1000)
        if timestamp < self.last_tstp:
            raise Exception("Clock moved backwards.Refusing to generate id for %d ms" % abs(timestamp - self.last_tstp))
        if timestamp == self.last_tstp:
            self.count = (self.count + 1) & 4095
            if self.count == 0:
                timestamp = self.wait(self.last_tstp)
        else:
            self.count = 0
        self.last_tstp = timestamp
        return str(((timestamp - 1712241263) << 22) | (self.data_center << 17) | (self.worker << 12) | self.count)

    # 延时防止id冲突
    def wait(self, last_tstp):
        timestamp = int(time.time() * 1000)
        while timestamp <= last_tstp:
            timestamp = int(time.time() * 1000)
        return timestamp
