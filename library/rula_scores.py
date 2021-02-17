# coding: utf-8
#!/usr/bin/env python
"""
module for generation of scores due to rula ergonomic concept
"""
import numpy as np
import re

#==============================================================================
# RULA PART I
#==============================================================================
def upperArm_score(header, data):
    """returns rula score for upper Arm

    takes all three anatomical angles for shoulder provided by MR3s myoMOTION
    """
    # No. 1 of RULA protocol
    angle_limits = [[-20, 20], [-20, 20, 45], [45, 90], [90]] # rula definition
    angle_abdu = 30 # own definition/limit

    shoulder_flex = np.zeros((len(data), 2)) # [0,1 == left, right]
    shoulder_abdu = np.zeros((len(data), 2)) # [0,1 == left, right]
    shoulder_flex[:, 0] = data[:, np.where(header=="Schulter Flexion LT,Grad")[0][0]]
    shoulder_flex[:, 1] = data[:, np.where(header=="Schulter Flexion RT,Grad")[0][0]]
    shoulder_abdu[:, 0] = data[:, np.where(header=="Schulter Abduktion LT,Grad")[0][0]]
    shoulder_abdu[:, 1] = data[:, np.where(header=="Schulter Abduktion RT,Grad")[0][0]]


    score_left = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]
    score_right = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]

    for a in range(len(data)):
        # scoring for left side
        if shoulder_flex[a, 0] > angle_limits[0][0] and shoulder_flex[a, 0] <= angle_limits[0][1]:
            score_left[a, 0] = 1
        elif shoulder_flex[a, 0] < angle_limits[1][0]:
            score_left[a, 0] = 2
        elif shoulder_flex[a, 0] > angle_limits[1][1] and shoulder_flex[a, 0] <= angle_limits[1][2]:
            score_left[a, 0] = 2
        elif shoulder_flex[a, 0] > angle_limits[2][0] and shoulder_flex[a, 0] <= angle_limits[2][1]:
            score_left[a, 0] = 3
        elif shoulder_flex[a, 0] > angle_limits[3][0]:
            score_left[a, 0] = 4

        # scoring for right side
    for b in range(len(data)):
        if shoulder_flex[b, 1] > angle_limits[0][0] and shoulder_flex[a, 0] <= angle_limits[0][1]:
            score_right[b, 0] = 1
        elif shoulder_flex[b, 1] < angle_limits[1][0]:
            score_right[b, 0] = 2
        elif shoulder_flex[b, 1] > angle_limits[1][1] and shoulder_flex[a, 0] <= angle_limits[1][2]:
            score_right[b, 0] = 2
        elif shoulder_flex[b, 1] > angle_limits[2][0] and shoulder_flex[a, 0] <= angle_limits[2][1]:
            score_right[b, 0] = 3
        elif shoulder_flex[b, 1] > angle_limits[3][0]:
            score_right[b, 0] = 4


    abucted_arm_left = np.where(shoulder_abdu[:,0] > angle_abdu)[0]
    abucted_arm_right = np.where(shoulder_abdu[:,1] > angle_abdu)[0]

    score_left[abucted_arm_left,0] += 1
    score_right[abucted_arm_right,0] += 1

    print("\n???????????????\nQUESTION\n???????????????")
    while True:
        try:
            a = int(input("Wie lange ist die Person angelehnt ODER\n der Arm unterstützt?\n [Angabe in % relativ zur Gesamtdauer des Vorgangs]\n\n\t"))
            a = a/100
            break
        except ValueError:
            print("Oppsidaysi! That wasn't  an integer Value. Try again!")


    print('upper Arm:')
    print(np.mean(score_left[:,0]))
    print(np.mean(score_right[:,0]))

    return score_left, score_right



def lowerArm_score(header, data):
    """returns rula score for lower Arm

    takes the one anatomical angle for ellbow provided by MR3s myoMOTION
    """
    # No. 2 of RULA protocol
    angle_limits = [[60, 100], [0, 60, 100]] # rula definition
    outer_rotation = 15 # own definition

    lowerArm_flex = np.zeros((len(data), 2)) # [0,1 == left, right]
    shoulder_rota = np.zeros((len(data), 2)) # [0,1 == left, right]
    lowerArm_flex[:, 0] = data[:, np.where(header=="Ellbogen Flexion LT,Grad")[0][0]]
    lowerArm_flex[:, 1] = data[:, np.where(header=="Ellbogen Flexion RT,Grad")[0][0]]
    shoulder_rota[:, 0] = data[:, np.where(header=="Schulter Rotation - out LT,Grad")[0][0]]
    shoulder_rota[:, 1] = data[:, np.where(header=="Schulter Rotation - out RT,Grad")[0][0]]

    score_left = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]
    score_right = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]

    # scoring for left side
    for a in range(len(data)):
        if lowerArm_flex[a, 0] > angle_limits[0][0] and lowerArm_flex[a, 0] < angle_limits[0][1]:
            score_left[a, 0] = 1
        elif lowerArm_flex[a ,0] > angle_limits[1][0] and lowerArm_flex[a, 0] <= angle_limits[1][1]:
            score_left[a, 0] = 2
        elif lowerArm_flex[a, 0] >= angle_limits[1][2]:
            score_left[a, 0] = 2

    # scoring for right side
    for b in range(len(data)):
        if lowerArm_flex[b, 1] > angle_limits[0][0] and lowerArm_flex[b, 1] < angle_limits[0][1]:
            score_right[b, 0] = 1
        elif lowerArm_flex[b ,1] > angle_limits[1][0] and lowerArm_flex[b, 1] <= angle_limits[1][1]:
            score_right[b, 0] = 2
        elif lowerArm_flex[b, 1] >= angle_limits[1][2]:
            score_right[b, 0] = 2

    # abduction: might need improvement
    outer_rotation_left = np.where(shoulder_rota[:, 0] > outer_rotation)[0]
    outer_rotation_right = np.where(shoulder_rota[:, 1] > outer_rotation)[0]

    score_left[outer_rotation_left, 0] += 1
    score_right[outer_rotation_right, 0] += 1

    print("lower Arm:")
    print(np.mean(score_left[:,0]))
    print(np.mean(score_right[:,0]))

    return score_left, score_right



def wrist_score(header, data):
    """returns rula score for wrist

    takes all three anatomical angles for wrist provided by MR3s myoMOTION
    """
    # No. 3 of RULA protocol
    angle_limits = [[-1, 1], [-15, -1, 1, 15], [-15, 15]] # rula definition
    angle_abdu = 10 # own definition/limit
    angle_around = [-5, 5] # own definition/limit

    wrist_ext = np.zeros((len(data), 2)) # [0,1 == left, right]
    wrist_abdu = np.zeros((len(data), 2)) # [0,1 == left, right]
    wrist_around = np.zeros((len(data), 2)) # [0,1 == left, right]
    wrist_ext[:, 0] = data[:, np.where(header=="Handgelenk Dorsalextension LT,Grad")[0][0]]
    wrist_ext[:, 1] = data[:, np.where(header=="Handgelenk Dorsalextension RT,Grad")[0][0]]
    wrist_abdu[:, 0] = data[:, np.where(header=="Handgelenk Radialabduktion LT,Grad")[0][0]]
    wrist_abdu[:, 1] = data[:, np.where(header=="Handgelenk Radialabduktion RT,Grad")[0][0]]
    wrist_around[:, 0] = data[:, np.where(header=="Wrist Supination LT,Grad")[0][0]]
    wrist_around[:, 1] = data[:, np.where(header=="Wrist Supination RT,Grad")[0][0]]

    score_left = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]
    score_right = np.zeros((len(data), 1)) # [0,1 == angleScore, additional]
    score_suppination = np.zeros((len(data), 2)) # [0,1 == left, right]

    # scoring for left side
    for a in range(len(data)):
        if wrist_ext[a, 0] > angle_limits[0][0] and wrist_ext[a, 0] < angle_limits[0][1]:
            score_left[a, 0] = 1
        elif wrist_ext[a ,0] > angle_limits[1][0] and wrist_ext[a, 0] <= angle_limits[1][1]:
            score_left[a, 0] = 2
        elif wrist_ext[a ,0] >= angle_limits[1][2] and wrist_ext[a, 0] < angle_limits[1][3]:
            score_left[a, 0] = 2
        elif wrist_ext[a, 0] <= angle_limits[2][0] or wrist_ext[a, 0] >= angle_limits[2][1]:
            score_left[a, 0] = 3

    # scoring for right side
    for b in range(len(data)):
        if wrist_ext[b, 1] > angle_limits[0][0] and wrist_ext[b, 1] < angle_limits[0][1]:
            score_right[b, 0] = 1
        elif wrist_ext[b ,1] > angle_limits[1][0] and wrist_ext[b, 1] <= angle_limits[1][1]:
            score_right[b, 0] = 2
        elif wrist_ext[b ,1] >= angle_limits[1][2] and wrist_ext[b, 1] < angle_limits[1][3]:
            score_right[b, 0] = 2
        elif wrist_ext[b, 1] <= angle_limits[2][0] or wrist_ext[b, 1] >= angle_limits[2][1]:
            score_right[b, 0] = 3


    rad_abdu_left = np.where(wrist_abdu[:, 0] > angle_abdu)
    rad_abdu_right = np.where(wrist_abdu[:, 1] > angle_abdu)
    score_left[rad_abdu_left,0] += 1
    score_right[rad_abdu_right,0] += 1

    # No. 4 of RULA protocol
    # scoring for left suppination value
    for c in range(len(data)):
        if wrist_around[c, 0] > angle_around[0] and wrist_around[c, 0] < angle_around[1]:
            score_suppination[c, 0] = 1
        else:
            score_suppination[c, 0] = 2

    # scoring for rigt suppination value
    for d in range(len(data)):
        if wrist_around[d, 1] > angle_around[0] and wrist_around[d, 1] < angle_around[1]:
            score_suppination[d, 1] = 1
        else:
            score_suppination[d, 1] = 2


    print("wrist:")
    print(np.mean(score_left[:,0]))
    print(np.mean(score_right[:,0]))
    print("suppination:")
    print(np.mean(score_suppination[:, 0]))
    print(np.mean(score_suppination[:, 1]))

    return score_left, score_right, score_suppination[:,0].reshape(len(score_suppination), 1), score_suppination[:,1].reshape(len(score_suppination), 1)

#==============================================================================
# RULA PART II
#==============================================================================
def neck_score(header, data):
    """returns rula score for neck

    takes all three anatomical angles for neck provided by MR3s myoMOTION
    """
    # No. 6 of RULA protocol
    angle_limits = [[0, 10], [10, 20], [20], [0]] # rula definition
    angle_rota = [-5, 5] # own definition/limit
    angle_tilt = [-5, 5] # own definition/limit

    neck_flex = np.zeros((len(data), 1))
    neck_rota = np.zeros((len(data), 1))
    neck_tilt = np.zeros((len(data), 1))
    neck_flex[:, 0] = data[:, np.where(header=="Halswirbel Flexion,Grad")[0][0]]
    neck_rota[:, 0] = data[:, np.where(header=="Halswirbel Axial - RT,Grad")[0][0]]
    neck_tilt[:, 0] = data[:, np.where(header=="Halswirbel Lateral - RT,Grad")[0][0]]

    score_neck = np.zeros((len(data), 1))

    # scoring for neck movement
    for a in range(len(data)):
        if neck_flex[a, 0] >= angle_limits[0][0] and neck_flex[a, 0] <= angle_limits[0][1]:
            score_neck[a, 0] = 1
        elif neck_flex[a ,0] > angle_limits[1][0] and neck_flex[a, 0] <= angle_limits[1][1]:
            score_neck[a, 0] = 2
        elif neck_flex[a ,0] > angle_limits[2][0]:
            score_neck[a, 0] = 3
        elif neck_flex[a, 0] < angle_limits[3][0]:
            score_neck[a, 0] = 4

    # adding +1 for rotation limit
    for b in range(len(data)):
        if neck_rota[b, 0] < angle_rota[0] or neck_rota[b, 0] > angle_rota[1]:
            score_neck[b, 0] += 1

    # adding +1 for tilt limit
    for c in range(len(data)):
        if neck_tilt[c, 0] < angle_tilt[0] or neck_tilt[c, 0] > angle_tilt[1]:
            score_neck[c, 0] += 1

    print("neck:")
    print(np.mean(score_neck[:, 0]))

    return score_neck


def upperBody_score(header, data):
    """returns rula score for upper Body

    takes two planar thoracal and lower spine anatomical angles of back sensors provided by MR3s myoMOTION
    """
    # No. 7 of RULA protocol
    angle_limits = [[-20, 0], [0, 20], [20, 60], [60]] # rula definition
    angle_rota = [-5, 5] # own definition/limit
    angle_tilt = [-5, 5] # own definition/limit

    body_flex = np.zeros((len(data), 1))
    body_rota = np.zeros((len(data), 1))
    body_tilt = np.zeros((len(data), 1))
    body_flex[:, 0] = data[:, np.where(header=="Lendenwirbelsäule Flexion,Grad")[0][0]]
    body_rota[:, 0] = data[:, np.where(header=="Thorax Axial - RT,Grad")[0][0]]
    body_tilt[:, 0] = data[:, np.where(header=="Thorax Lateral - RT,Grad")[0][0]]

    score_body = np.zeros((len(data), 1))

    # scoring for upper body movement
    for a in range(len(data)):
        if body_flex[a, 0] > angle_limits[0][0] and body_flex[a, 0] <= angle_limits[0][1]:
            score_body[a, 0] = 1
        elif body_flex[a ,0] > angle_limits[1][0] and body_flex[a, 0] <= angle_limits[1][1]:
            score_body[a, 0] = 2
        elif body_flex[a ,0] > angle_limits[2][0] and body_flex[a, 0] <= angle_limits[2][1]:
            score_body[a, 0] = 3
        elif body_flex[a, 0] > angle_limits[3][0]:
            score_body[a, 0] = 4

    # adding +1 for rotation limit
    for b in range(len(data)):
        if body_rota[b, 0] < angle_rota[0] or body_rota[b, 0] > angle_rota[1]:
            score_body[b, 0] += 1

    # adding +1 for tilt limit
    for c in range(len(data)):
        if body_tilt[c, 0] < angle_tilt[0] or body_tilt[c, 0] > angle_tilt[1]:
            score_body[c, 0] += 1

    print("Upper Body:")
    print(np.mean(score_body[:, 0]))

    return score_body


def leg_score():
    """returns rula score for leg position

    takes all ? anatomical angles for ? provided by MR3s myoMOTION
    """
    # No. 8 of RULA rotocol
    print("\n???????????????\nQUESTION\n???????????????")
    while True:
        try:
            a = str(input("Sind Beide Beine belastet? (yes=y/no=n)\n\n\t"))
            if a == 'y':
                score_leg = 1
                break
            elif a == 'n':
                score_leg = 2
                break
            else:
                print("Oppsidaysi! That wasn't 'yes' or 'no'. Try again!")
        except ValueError:
            print("Oppsidaysi! We call this a ValueError. It occured.")

    print("Leg:")
    print(score_leg)

    return score_leg


#==============================================================================
# RULA PART III
#==============================================================================
def score_table_a(upperArm_score, lowerArm_score, wrist_score, suppination, i):
    """
    generates the table based RULA score for upper body
    """
    scores = np.round([upperArm_score, lowerArm_score, wrist_score, suppination])
    scores = scores.astype(int)

    table = np.genfromtxt("../tableA.csv", delimiter=',', dtype=np.int)

    error_path = "../errorX.txt"

    # generating x-coordinate
    if scores[0] == 1  and scores[1] == 1:
        x = 0
    elif scores[0] == 1 and scores[1] == 2:
        x = 1
    elif scores[0] == 1 and scores[1] == 3:
        x = 2
    elif scores[0] == 2 and scores[1] == 1:
        x = 3
    elif scores[0] == 2 and scores[1] == 2:
        x = 4
    elif scores[0] == 2 and scores[1] == 3:
        x = 5
    elif scores[0] == 3 and scores[1] == 1:
        x = 6
    elif scores[0] == 3 and scores[1] == 2:
        x = 7
    elif scores[0] == 3 and scores[1] == 3:
        x = 8
    elif scores[0] == 4 and scores[1] == 1:
        x = 9
    elif scores[0] == 4 and scores[1] == 2:
        x = 10
    elif scores[0] == 4 and scores[1] == 3:
        x = 11
    elif scores[0] == 5 and scores[1] == 1:
        x = 12
    elif scores[0] == 5 and scores[1] == 2:
        x = 13
    elif scores[0] == 5 and scores[1] == 3:
        x = 14
    elif scores[0] == 6 and scores[1] == 1:
        x = 15
    elif scores[0] == 6 and scores[1] == 2:
        x = 16
    elif scores[0] == 6 and scores[1] == 3:
        x = 17
    else:
        x = 0
        with open(error_path, "a") as errors:
            errors.write("x-score Error: at " + str(i) + "\n")

    # generating y-coordinate
    if scores[2] == 1 and scores[3] == 1:
        y = 0
    elif scores[2] == 1 and scores[3] == 2:
        y = 1
    elif scores[2] == 2 and scores[3] == 1:
        y = 2
    elif scores[2] == 2 and scores[3] == 2:
        y = 3
    elif scores[2] == 3 and scores[3] == 1:
        y = 4
    elif scores[2] == 3 and scores[3] == 2:
        y = 5
    elif scores[2] == 4 and scores[3] == 1:
        y = 6
    elif scores[2] == 4 and scores[3] == 2:
        y = 7

    #print("Score Tabelle A:")
    #print("x: " + str(x) + "; y: " + str(y))
    #print(str(table[x, y]))
    return table[x, y]


def score_table_b(neck_score, upperBody_score, leg_score):
    """
    generates the table based RULA score for lower body
    """
    scores = np.round([neck_score, upperBody_score, leg_score])
    scores = scores.astype(int)

    table = np.genfromtxt("../tableB.csv", delimiter=',', dtype=np.int)

    # generating x-coordinates
    if scores[0] == 1:
        x = 0
    elif scores[0] == 2:
        x = 1
    elif scores[0] == 3:
        x = 2
    elif scores[0] == 4:
        x = 3
    elif scores[0] == 5:
        x = 4
    elif scores[0] == 6:
        x = 5

    # generating y-coordinate
    if scores[1] == 1 and scores[2] == 1:
        y = 0
    elif scores[1] == 1 and scores[2] == 2:
        y = 1
    elif scores[1] == 2 and scores[2] == 1:
        y = 2
    elif scores[1] == 2 and scores[2] == 2:
        y = 3
    elif scores[1] == 3 and scores[2] == 1:
        y = 4
    elif scores[1] == 3 and scores[2] == 2:
        y = 5
    elif scores[1] == 4 and scores[2] == 1:
        y = 6
    elif scores[1] == 4 and scores[2] == 2:
        y = 7
    elif scores[1] == 5 and scores[2] == 1:
        y = 8
    elif scores[1] == 5 and scores[2] == 2:
        y = 9
    elif scores[1] == 6 and scores[2] == 1:
        y = 10
    elif scores[1] == 6 and scores[2] == 2:
        y = 11


    #print("Score Tabelle B:")
    #print("x: " + str(x) + "; y: " + str(y))
    #print(str(table[x, y]))
    return table[x, y]


def score_table_c(A, B):
    """
    generates the final Rula Score based, on values of upper_table and lower_table
    """
    scores = np.round([A, B])
    scores = scores.astype(int)

    table = np.genfromtxt("../tableC.csv", delimiter=',', dtype=np.int)

    # generating x-coordinate
    if scores[0] == 1:
        x = 0
    elif scores[0] == 2:
        x = 1
    elif scores[0] == 3:
        x = 2
    elif scores[0] == 4:
        x = 3
    elif scores[0] == 5:
        x = 4
    elif scores[0] == 6:
        x = 5
    elif scores[0] == 7:
        x = 6
    elif scores[0] >= 8:
        x = 7

    # generating y-coordinate
    if scores[1] == 1:
        y = 0
    elif scores[1] == 2:
        y = 1
    elif scores[1] == 3:
        y = 2
    elif scores[1] == 4:
        y = 3
    elif scores[1] == 5:
        y = 4
    elif scores[1] == 6:
        y = 5
    elif scores[1] >= 7:
        y = 6


    #print("Score Tabelle C:")
    #print("x: " + str(x) + "; y: " + str(y))
    #print("==============")
    #print("FINAL SCORE:")
    #print("\t" + str(table[x, y]))
    #print("==============")
    return table[x, y]
