#!/usr/bin/python

import json
import man_obj
import pos_arm
import random
import rec_obj
import rospy
import sns_obj
import wgh_obj
import geometry_msgs
import std_msgs
import dep_obj
import numpy

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
bin_a_pose.position.x = 0.30
bin_a_pose.position.y = -1.17
bin_a_pose.position.z = 1.62
bin_a_pose.orientation.w = 0.71
bin_a_pose.orientation.x = 0.00
bin_a_pose.orientation.y = 3.37
bin_a_pose.orientation.z = -0.71

bin_b_pose = geometry_msgs.msg.Pose()
bin_b_pose.position.x = -0.01
bin_b_pose.position.y = -1.17
bin_b_pose.position.z = 1.62
bin_b_pose.orientation.w = 0.71
bin_b_pose.orientation.x = 0.00
bin_b_pose.orientation.y = 5.96
bin_b_pose.orientation.z = -0.71

bin_c_pose = geometry_msgs.msg.Pose()
bin_c_pose.position.x = -0.28
bin_c_pose.position.y = -1.16
bin_c_pose.position.z = 1.62
bin_c_pose.orientation.w = 0.71
bin_c_pose.orientation.x = 0.00
bin_c_pose.orientation.y = 0.00
bin_c_pose.orientation.z = -0.71

bin_d_pose = geometry_msgs.msg.Pose()
bin_d_pose.position.x = 0.30
bin_d_pose.position.y = -1.17
bin_d_pose.position.z = 1.30
bin_d_pose.orientation.w = 0.71
bin_d_pose.orientation.x = 0.00
bin_d_pose.orientation.y = 0.00
bin_d_pose.orientation.z = -0.71

bin_e_pose = geometry_msgs.msg.Pose()
bin_e_pose.position.x = -0.02
bin_e_pose.position.y = -1.22
bin_e_pose.position.z = 1.29
bin_e_pose.orientation.w = 0.72
bin_e_pose.orientation.x = 0.00
bin_e_pose.orientation.y = 4.01
bin_e_pose.orientation.z = -0.69

bin_f_pose = geometry_msgs.msg.Pose()
bin_f_pose.position.x = -0.32
bin_f_pose.position.y = -1.17
bin_f_pose.position.z = 1.29
bin_f_pose.orientation.w = 0.71
bin_f_pose.orientation.x = 0.00
bin_f_pose.orientation.y = 0.00
bin_f_pose.orientation.z = -0.71

bin_g_pose = geometry_msgs.msg.Pose()
bin_g_pose.position.x = 0.30
bin_g_pose.position.y = -1.17
bin_g_pose.position.z = 0.97
bin_g_pose.orientation.w = 0.71
bin_g_pose.orientation.x = 0.00
bin_g_pose.orientation.y = 0.00
bin_g_pose.orientation.z = -0.71

bin_h_pose = geometry_msgs.msg.Pose()
bin_h_pose.position.x = 0.00
bin_h_pose.position.y = -1.17
bin_h_pose.position.z = 0.97
bin_h_pose.orientation.w = 0.71
bin_h_pose.orientation.x = 0.00
bin_h_pose.orientation.y = 0.00
bin_h_pose.orientation.z = 0.71

bin_i_pose = geometry_msgs.msg.Pose()
bin_i_pose.position.x = -0.31
bin_i_pose.position.y = -1.16
bin_i_pose.position.z = 0.97
bin_i_pose.orientation.w = 0.71
bin_i_pose.orientation.x = 0.00
bin_i_pose.orientation.y = 0.00
bin_i_pose.orientation.z = -0.71

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
}

# observe pose

observe_obj_pose = geometry_msgs.msg.Pose()
observe_obj_pose.position.x = 0.79
observe_obj_pose.position.y = 0.11
observe_obj_pose.position.z = 0.75
observe_obj_pose.orientation.w = 0.71
observe_obj_pose.orientation.x = -0.01
observe_obj_pose.orientation.y = 0.70
observe_obj_pose.orientation.z = 0.01

# pick pose

pick_obj_pose = geometry_msgs.msg.Pose()
pick_obj_pose.position.x = 0.80
pick_obj_pose.position.y = 0.11
pick_obj_pose.position.z = 0.15
pick_obj_pose.orientation.w = 0.71
pick_obj_pose.orientation.x = -0.01
pick_obj_pose.orientation.y = 0.70
pick_obj_pose.orientation.z = 0.01

# recognise pose

rec_obj_pose = geometry_msgs.msg.Pose()
rec_obj_pose.position.x = 0.26
rec_obj_pose.position.y = -0.30
rec_obj_pose.position.z = 1.16
rec_obj_pose.orientation.w = 0.57
rec_obj_pose.orientation.x = 0.51
rec_obj_pose.orientation.y = 0.58
rec_obj_pose.orientation.z = -0.41

# weigh pose

weigh_obj_pose = geometry_msgs.msg.Pose()
weigh_obj_pose.position.x = 0.83
weigh_obj_pose.position.y = 0.10
weigh_obj_pose.position.z = 1.50
weigh_obj_pose.orientation.w = 1.00
weigh_obj_pose.orientation.x = 0.00
weigh_obj_pose.orientation.y = 0.00
weigh_obj_pose.orientation.z = 0.02

# object ids

obj_a_id = "dove_beauty_bar"
obj_b_id = "one_with_nature_soap_dead_sea_mud"
obj_c_id = "champion_copper_plus_spark_plug"
obj_d_id = "crayola_64_ct"
obj_e_id = "dr_browns_bottle_brush"
obj_f_id = "elmers_washable_no_run_school_glue"
obj_g_id = "expo_dry_erase_board_eraser"
obj_h_id = "feline_greenies_dental_treats"
obj_i_id = "first_years_take_and_toss_straw_cup"
obj_j_id = "genuine_joe_plastic_stir_sticks"
obj_k_id = "highland_6539_self_stick_notes"
obj_l_id = "kong_air_dog_squeakair_tennis_ball"
obj_m_id = "kong_duck_dog_toy"
obj_n_id = "kong_sitting_frog_dog_toy"
obj_o_id = "kyjen_squeakin_eggs_plush_puppies"
obj_p_id = "laugh_out_loud_joke_book" 
obj_q_id = "mark_twain_huckleberry_finn"     
obj_r_id = "mead_index_cards"
obj_s_id = "mommys_helper_outlet_plugs"
obj_t_id = "munchkin_white_hot_duck_bath_toy"
obj_u_id = "oreo_mega_stuf"
obj_v_id = "paper_mate_12_count_mirado_black_warrior"      
obj_w_id = "rolodex_jumbo_pencil_cup"
obj_x_id = "safety_works_safety_glasses"
obj_y_id = "sharpie_accent_tank_style_highlighters"
obj_z_id = "stanley_66_052"

obj_ids =\
[\
    obj_a_id,\
    obj_b_id,\
    obj_c_id,\
    obj_d_id,\
    obj_e_id,\
    obj_f_id,\
    obj_g_id,\
    obj_h_id,\
    obj_i_id,\
    obj_j_id,\
    obj_k_id,\
    obj_l_id,\
    obj_m_id,\
    obj_n_id,\
    obj_o_id,\
    obj_p_id,\
    obj_q_id,\
    obj_r_id,\
    obj_s_id,\
    obj_t_id,\
    obj_u_id,\
    obj_v_id,\
    obj_w_id,\
    obj_x_id,\
    obj_y_id,\
    obj_z_id,\
]

# object weights

obj_weights =\
{\
    obj_a_id: 473,\
    obj_b_id: 208,\
    obj_c_id:  54,\
    obj_d_id: 374,\
    obj_e_id:  75,\
    obj_f_id: 136,\
    obj_g_id:  19,\
    obj_h_id: 160,\
    obj_i_id: 109,\
    obj_j_id: 279,\
    obj_k_id: 183,\
    obj_l_id:  94,\
    obj_m_id:  22,\
    obj_n_id:  29,\
    obj_o_id:  47,\
    obj_p_id:  82,\
    obj_q_id: 162,\
    obj_r_id: 141,\
    obj_s_id:  80,\
    obj_t_id:  75,\
    obj_u_id: 387,\
    obj_v_id:  72,\
    obj_w_id:  92,\
    obj_x_id:  46,\
    obj_y_id: 107,\
    obj_z_id:  71,\
}

# file dictionary keys

tote_obj_ids_key = "work_order"
bin_obj_ids_key = "bin_contents"

""" Functions """

def get_bin_obj_ids(data, bin_id):
    return data[bin_obj_ids_key][bin_id]

def get_tote_obj_ids(data):
    return data[tote_obj_ids_key]

def init():
    dep_obj.init("dep_obj_srv")
    man_obj.init("man_obj_srv")
    rec_obj.init("rec_obj_srv")
    pos_arm.init("pos_arm_srv")
    sns_obj.init("sns_obj_srv")
    wgh_obj.init("wgh_obj_srv")

    rospy.init_node("tsk_pln_node")

def pick_obj():
    pos_arm.set_pose(observe_obj_pose)
    obj_pos = dep_obj.get_obj_pos()

    temp_observe_obj_pose = geometry_msgs.msg.Pose()
    temp_observe_obj_pose.position.x = observe_obj_pose.position.x
    temp_observe_obj_pose.position.y = observe_obj_pose.position.y
    temp_observe_obj_pose.position.z = observe_obj_pose.position.z
    
    temp_x = 0.0;
    temp_y = 0.0;
    temp_angle = 0.0;
    
    while obj_pos == "":
        # todo: move arm to slightly different position
        temp_x = temp_x + 0.05 * numpy.cos(temp_angle) - 1.0
        temp_y = temp_y + 0.05 * numpy.sin(temp_angle)
        temp_observe_obj_pose.position.x = observe_obj_pose.position.x + temp_x
        temp_observe_obj_pose.position.y = observe_obj_pose.position.y + temp_y
        temp_angle = temp_angle + 0.52
        pos_arm.set_pose(temp_pick_obj_pose)
        obj_pos = dep_obj.get_obj_pos()        

    pos_arm.set_pose(pick_obj_pose)

    coords = obj_pos.split(",")

    # todo: move arm over object
    new_pick_obj_pose = geometry_msgs.msg.Pose()
    new_pick_obj_pose.position.x = temp_pick_obj_pose.position.x - 0.055 * ( coords[1] - 215 )
    new_pick_obj_pose.position.y = temp_pick_obj_pose.position.y - 0.055 * ( coords[0] - 240 )
    new_pick_obj_pose.position.z = temp_pick_obj_pose.position.z
    pos_arm.set_pose(new_pick_obj_pose)
    
    while sns_obj.is_obj_sns() == False:
        # todo: move arm towards object
        new_pick_obj_pose.position.x = new_pick_obj_pose.position.x
        new_pick_obj_pose.position.y = new_pick_obj_pose.position.y
        new_pick_obj_pose.position.z = new_pick_obj_pose.position.z - 0.01
        pos_arm.set_pose(new_pick_obj_pose)
        continue;

    man_obj.grab_obj()

def read_input_file(input_file_path):
    json_data = open(input_file_path)
    return json.load(json_data)

def id_obj(obj_ids):
    pos_arm.set_pose(weigh_obj_pose);
    weight = wgh_obj.get_obj_weight()

    # filter obj ids by weight
    filt_obj_ids = [ ]
    
    for i in range(0, len(obj_ids)):
        obj_id = obj_ids[i]
        obj_weight = obj_weights[obj_id]

        if obj_weight > (weight * 0.8) and obj_weight < (weight * 1.2):
            filt_obj_ids.append(obj_id)
            rospy.loginfo(obj_id)

    if len(filt_obj_ids) == 0:
        return ""

    pos_arm.set_pose(rec_obj_pose)
    return rec_obj.get_obj_id(filt_obj_ids)

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

        rospy.loginfo("object recognised: " + obj_id)

        if obj_id == "":
            # failed to detect object, put it back
            pos_arm.set_pose(pick_obj_pose)
            man_obj.drop_obj()
        else:

            # successful detected object   
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

