#!/usr/bin/python

import json
import man_obj
import pos_arm
import random
import rec_obj
import rospy
import sns_obj
import geometry_msgs
import std_msgs

""" Definitions """

# bin ids

bin_a_id = "bin_A"
bin_b_id = "bin_B"
bin_c_id = "bin_C"
bin_d_id = "bin_D"
bin_e_id = "bin_E"
bin_f_id = "bin_F"
bin_g_id = "bin_G"
bin_h_id = "bin_H"
bin_i_id = "bin_I"
bin_j_id = "bin_J"
bin_k_id = "bin_K"
bin_l_id = "bin_L"

bin_ids =\
[\
    bin_a_id,\
    bin_b_id,\
    bin_c_id,\
    bin_d_id,\
    bin_e_id,\
    bin_f_id,\
    bin_g_id,\
    bin_h_id,\
    bin_i_id,\
    bin_j_id,\
    bin_k_id,\
    bin_l_id,\
]

# bin selection probabilities

bin_probs =\
{\
     0:   3.125,\
     1:   6.25 ,\
     2:  12.5  ,\
     3:  25.0  ,\
     4:  50.0  ,\
     5: 100.0  ,\
     6:  50.0  ,\
     7:  25.0  ,\
     8:  12.5  ,\
     9:   6.25 ,\
    10:   3.125,\
}

# bin poses

bin_a_pose = geometry_msgs.msg.Pose()
bin_a_pose.position.x = 1
bin_a_pose.position.y = 2
bin_a_pose.position.z = 3
bin_a_pose.orientation.w = 4
bin_a_pose.orientation.x = 5
bin_a_pose.orientation.y = 6
bin_a_pose.orientation.z = 7

bin_b_pose = geometry_msgs.msg.Pose()
bin_b_pose.position.x = 1
bin_b_pose.position.y = 2
bin_b_pose.position.z = 3
bin_b_pose.orientation.w = 4
bin_b_pose.orientation.x = 5
bin_b_pose.orientation.y = 6
bin_b_pose.orientation.z = 7

bin_c_pose = geometry_msgs.msg.Pose()
bin_c_pose.position.x = 1
bin_c_pose.position.y = 2
bin_c_pose.position.z = 3
bin_c_pose.orientation.w = 4
bin_c_pose.orientation.x = 5
bin_c_pose.orientation.y = 6
bin_c_pose.orientation.z = 7

bin_d_pose = geometry_msgs.msg.Pose()
bin_d_pose.position.x = 1
bin_d_pose.position.y = 2
bin_d_pose.position.z = 3
bin_d_pose.orientation.w = 4
bin_d_pose.orientation.x = 5
bin_d_pose.orientation.y = 6
bin_d_pose.orientation.z = 7

bin_e_pose = geometry_msgs.msg.Pose()
bin_e_pose.position.x = 1
bin_e_pose.position.y = 2
bin_e_pose.position.z = 3
bin_e_pose.orientation.w = 4
bin_e_pose.orientation.x = 5
bin_e_pose.orientation.y = 6
bin_e_pose.orientation.z = 7

bin_f_pose = geometry_msgs.msg.Pose()
bin_f_pose.position.x = 1
bin_f_pose.position.y = 2
bin_f_pose.position.z = 3
bin_f_pose.orientation.w = 4
bin_f_pose.orientation.x = 5
bin_f_pose.orientation.y = 6
bin_f_pose.orientation.z = 7

bin_g_pose = geometry_msgs.msg.Pose()
bin_g_pose.position.x = 1
bin_g_pose.position.y = 2
bin_g_pose.position.z = 3
bin_g_pose.orientation.w = 4
bin_g_pose.orientation.x = 5
bin_g_pose.orientation.y = 6
bin_g_pose.orientation.z = 7

bin_h_pose = geometry_msgs.msg.Pose()
bin_h_pose.position.x = 1
bin_h_pose.position.y = 2
bin_h_pose.position.z = 3
bin_h_pose.orientation.w = 4
bin_h_pose.orientation.x = 5
bin_h_pose.orientation.y = 6
bin_h_pose.orientation.z = 7

bin_i_pose = geometry_msgs.msg.Pose()
bin_i_pose.position.x = 1
bin_i_pose.position.y = 2
bin_i_pose.position.z = 3
bin_i_pose.orientation.w = 4
bin_i_pose.orientation.x = 5
bin_i_pose.orientation.y = 6
bin_i_pose.orientation.z = 7

bin_j_pose = geometry_msgs.msg.Pose()
bin_j_pose.position.x = 1
bin_j_pose.position.y = 2
bin_j_pose.position.z = 3
bin_j_pose.orientation.w = 4
bin_j_pose.orientation.x = 5
bin_j_pose.orientation.y = 6
bin_j_pose.orientation.z = 7

bin_k_pose = geometry_msgs.msg.Pose()
bin_k_pose.position.x = 1
bin_k_pose.position.y = 2
bin_k_pose.position.z = 3
bin_k_pose.orientation.w = 4
bin_k_pose.orientation.x = 5
bin_k_pose.orientation.y = 6
bin_k_pose.orientation.z = 7

bin_l_pose = geometry_msgs.msg.Pose()
bin_l_pose.position.x = 1
bin_l_pose.position.y = 2
bin_l_pose.position.z = 3
bin_l_pose.orientation.w = 4
bin_l_pose.orientation.x = 5
bin_l_pose.orientation.y = 6
bin_l_pose.orientation.z = 7

bin_poses =\
{\
    bin_a_id: bin_a_pose,\
    bin_b_id: bin_b_pose,\
    bin_c_id: bin_c_pose,\
    bin_d_id: bin_d_pose,\
    bin_e_id: bin_e_pose,\
    bin_f_id: bin_f_pose,\
    bin_g_id: bin_g_pose,\
    bin_h_id: bin_h_pose,\
    bin_i_id: bin_i_pose,\
    bin_j_id: bin_j_pose,\
    bin_k_id: bin_k_pose,\
    bin_l_id: bin_l_pose,\
}

# pick pose

pick_obj_pose = geometry_msgs.msg.Pose()
pick_obj_pose.position.x = 1
pick_obj_pose.position.y = 2
pick_obj_pose.position.z = 3
pick_obj_pose.orientation.w = 4
pick_obj_pose.orientation.x = 5
pick_obj_pose.orientation.y = 6
pick_obj_pose.orientation.z = 7

# recognise pose

rec_obj_pose = geometry_msgs.msg.Pose()
rec_obj_pose.position.x = 1
rec_obj_pose.position.y = 2
rec_obj_pose.position.z = 3
rec_obj_pose.orientation.w = 4
rec_obj_pose.orientation.x = 5
rec_obj_pose.orientation.y = 6
rec_obj_pose.orientation.z = 7

# file dictionary keys

tote_obj_ids_key = "work_order"
bin_obj_ids_key = "bin_contents"

""" Functions """

def get_bin_obj_ids(data, bin_id):
    return data[bin_obj_ids_key][bin_id]

def get_tote_obj_ids(data):
    return data[tote_obj_ids_key]

def init():
    man_obj.init("man_obj_srv")
    rec_obj.init("rec_obj_srv")
    pos_arm.init("pos_arm_srv")
    sns_obj.init("sns_obj_srv")

    rospy.init_node("tsk_pln_node")

def pick_obj():
    pos_arm.set_pose(pick_obj_pose)

    # TODO lots of work needed here

    while sns_obj.is_obj_sns() == False:
        continue;

    man_obj.grab_obj()

def read_input_file(input_file_path):
    json_data = open(input_file_path)
    return json.load(json_data)

def id_obj(obj_ids):
    pos_arm.set_pose(rec_obj_pose)
    return rec_obj.get_obj_id(obj_ids)

def sel_bin(data):
    bins = { }

    tot_bin_prob = 0;

    for i in range(0, len(bin_ids)):
        bin_id = bin_ids[i]
        bin_obj_ids = get_bin_obj_ids(data, bin_id)
        len_bin_obj_ids = len(bin_obj_ids)
        bin_prob = 0
        if len_bin_obj_ids in bin_probs:
            bin_prob = bin_probs[len_bin_obj_ids]
        else:
            bin_prob = 0

        bins[bin_id] = bin_prob
        tot_bin_prob = tot_bin_prob + bin_prob

    # normalize bin selection probabilities

    for i in range(0, len(bin_ids)):
        bin_id = bin_ids[i]
        bins[bin_id] = bins[bin_id] / tot_bin_prob        

    # use roulette wheel to select bin

    x = random.random()

    for i in range(0, len(bin_ids)):
        bin_id = bin_ids[i]
        x = x - bins[bin_id]
        if x < 0:
           return bin_id

    # should never get here
    raise Exception("roulette wheel selection")

def stow_obj(bin_id):
    pos_arm.set_pose(bin_poses[bin_id])    
    man_obj.drop_obj()

def write_output_file(output_file_path, data):
    with open(output_file_path, 'w') as outfile:
        json.dump(data, outfile)

""" Entry Point """

if __name__ == "__main__":
    init()

    input_file_path = rospy.get_param("input_file_path", "stow.json")
    output_file_path = rospy.get_param("output_file_path", "task.json")

    data = read_input_file(input_file_path)
    tote_obj_ids = get_tote_obj_ids(data)

    # stow items in tote
    while len(tote_obj_ids) > 0:
        pick_obj()
        obj_id = id_obj(tote_obj_ids)
        #TODO need to check if object id returned is present in tote, if not, adjust arm, then try again    
        bin_id = sel_bin(data)
        stow_obj(bin_id)
             
        # update data

        bin_obj_ids = get_bin_obj_ids(data, bin_id)
        bin_obj_ids.append(obj_id)
        tote_obj_ids.remove(obj_id)

    write_output_file(output_file_path, data)

# alternative sel_bin implementation, seeks to maximise points scored
"""
# better to specify a limit i.e. 5
def sel_bin(data):
    bins = { }
    any_bin_has_5_or_more_items = False

    for i in range(0, len(bin_ids)):
        bin_id = bin_ids[i]
        bin_cont = getBinContents(data, bin_id)
        len_bin_cont = len(bin_cont)
        bins[bin_id] = len_bin_cont
        if len_bin_cont > 4:
            any_bin_has_5_or_more_items = True

    print bins
    print any_bin_has_5_or_more_items

    if any_bin_has_5_or_more_items: 
        # return least populated bin with 5 or more items

        for i in range(0, len(bin_ids)):
            bin_id = bin_ids[i]
            if bins[bin_id] < 5:
               # bin contains fewer than 5 items, exclude it from the search
               bins[bin_id] = 999 

        min_len_bin_id = bin_ids[0]
        
        for i in range(1, len(bin_ids)):
            bin_id = bin_ids[i]
            if bins[bin_id] < bins[min_len_bin_id]:
                min_len_bin_id = bin_id

        return min_len_bin_id
    else: 
        # return most populated bin
        max_len_bin_id = bin_ids[0]

        for i in range(1, len(bin_ids)):
            bin_id = bin_ids[i]
            if bins[bin_id] > bins[max_len_bin_id]:
                max_len_bin_id = bin_id

        return max_len_bin_id
"""

