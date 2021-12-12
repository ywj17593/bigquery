import numpy as np
from service_migration import dataset_query, env, graph
import matplotlib.pyplot as plt
import networkx as nx

#####################  hyper parameters  ####################
BS_NUMBER = 5
THRESHOLD = 10000
MAX_STEP = 5


# create environment

# function


# init request
class Request:
    def __init__(self, edge_id, job_id):
        # id
        self.edge_id = edge_id
        self.job_id = job_id
        self.edge_loc = 0
        # state
        self.state = 2  # 2: not connect
        self.pre_state = 2
        # transmission size
        self.u2e_size = 0
        self.process_size = 0
        self.e2u_size = 0
        # edge state
        self.resource = 0
        self.mig_size = 0
        # task type
        self.task_type = TaskType()
        self.last_migration = 0
        # timer
        self.timer = 0


# feature of the task
class TaskType:
    def __init__(self):
        self


class Policy:
    @staticmethod
    def generate_policy(connection):
        return connection

    @staticmethod
    def resource_update(R, E, U):
        for edge in E:
            # count the number of the connection user
            connect_num = 0
            for user_id in edge.user_group:
                if U[user_id].req.state != 5 and U[user_id].req.state != 6:
                    connect_num += 1
            # dispatch the resource to the connection user
            for user_id in edge.user_group:
                # no need to provide resource to the disconnecting users
                if U[user_id].req.state == 5 or U[user_id].req.state == 6:
                    R[user_id] = 0
                # provide resource to connecting users
                else:
                    R[user_id] = edge.capability / (
                            connect_num + 2)  # reserve the resource to those want to migration
        return R

    @staticmethod
    def bandwidth_update(M, table, B, U, E):
        for user in U:
            share_number = 1
            ini_edge = int(user.req.edge_id)
            target_edge = int(M[user.req.user_id])
            # no need to migrate
            if ini_edge == target_edge:
                B[user.req.user_id] = 0
            # provide bandwidth to migrate
            else:
                # share bandwidth with user from migration edge
                for user_id in E[target_edge].user_group:
                    if O[user_id] == ini_edge:
                        share_number += 1
                # share bandwidth with the user from the original edge to migration edge
                for ini_user_id in E[ini_edge].user_group:
                    if ini_user_id != user.req.user_id and M[ini_user_id] == target_edge:
                        share_number += 1
                # allocate the bandwidth
                B[user.req.user_id] = table[min(ini_edge, target_edge)][max(ini_edge, target_edge)] / (
                        share_number + 2)

        return B


class Env:
    def __init__(self):
        self.time = 0
        # define environment object
        self.edge_num = 0
        self.step = 0
        self.reward_all = []
        self.cost = []
        self.connection = []
        self.rewards = 0
        self.job_list = []
        self.job = []
        self.R = 0
        self.M = 0
        self.B = 0
        self.edge_server = []
        self.model = 0
        self.policy = []

    def reset(self):
        # reset time
        self.time = 0
        # reward
        self.reward_all = []
        # graph
        self.edge_num, self.step, self.cost, self.connection, self.job_list, self.edge_server = graph.create_graph()
        # task
        self.job = self.job_list.sample()
        print(self.job)
        # Resource
        self.R = 0
        # Migration
        self.M = 0
        print(self.connection)
        # bandwidth
        self.B = 0
        # bandwidth table
        print(self.cost)
        # server
        print(self.edge_server)
        # model
        self.model = Policy()
        # initialize the request
        self.policy = self.model.generate_policy(self.connection)
        self.M = self.model.indicate_edge(self.O, self.U)
        # for user in self.U:
        #    user.generate_request(self.O[user.user_id])
        # return generate_state(self.table, self.U, self.E, self.x_min, self.y_min)


class Reward:




env = Env
env.reset(env)
