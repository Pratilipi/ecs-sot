import threading
import Queue
import time
import boto3
import json
import config

# threads config
NO_OF_READ_THREADS = config.NO_OF_READ_THREADS
NO_OF_PROCESS_THREADS = config.NO_OF_PROCESS_THREADS

# sqs config
SQS_CLIENT = boto3.resource('sqs')
SQS_QUEUE = SQS_CLIENT.get_queue_by_name(QueueName=config.SQS_NAME)
INTERNAL_QUEUE = Queue.Queue()

# get data from sqs
class SourceData(threading.Thread):
    def __init__(self, local_queue):
        threading.Thread.__init__(self)
        self.local_queue = local_queue

    def run(self):
        while True:
            try:
                msgs = SQS_QUEUE.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=5)
                if msgs == None:
                    print "sqs empty"
                for msg in msgs:
                    self.local_queue.put(msg)
                    msg.delete()
                    print "new task added to internal queue sz:{}".format(self.local_queue.qsize())
            except Exception as err:
                print "error:: while receiving data from sqs, {}".format(err)

# process msg
class ProcessMsgs(threading.Thread):
    def __init__(self, local_queue):
        threading.Thread.__init__(self)
        self.local_queue = local_queue

    def run(self):
        while True:
            msg = self.local_queue.get()
            try:
                if msg != "":
                    data = json.loads(msg.body)
            except Exception as err:
                print "error:: parsing, {} ".format(e)
            finally:
                self.local_queue.task_done()

def main():
    for i in range(NO_OF_READ_THREADS):
        source_msg_thread = SourceData(INTERNAL_QUEUE)
        source_msg_thread.start()

    for j in range(NO_OF_PROCESS_THREADS):
        parse_thread = ProcessMsgs(INTERNAL_QUEUE)
        parse_thread.start()

    # wait till all threads processing is completed
    INTERNAL_QUEUE.join()

if __name__ == '__main__':
    main()

