# coding: utf-8
#!/usr/bin/env python
"""
combines the core functions
"""
import numpy as np
import time
import datetime as dt
import sys
import glob
import get_data as gd
import rula_scores as rs


def app_rula(path):
    #path = "../data/rula.csv
    print("===================\n===================")
    print("Starting...")
    print("Importing Data...{%s}" %path)
    # generating the single Scores
    info, header, data = gd.get_data(path)
    upperArm_left, upperArm_right = rs.upperArm_score(header, data)
    lowerArm_left, lowerArm_right = rs.lowerArm_score(header, data)
    wrist_left, wrist_right, suppination_left, suppination_right = rs.wrist_score(header, data)
    neck = rs.neck_score(header, data)
    upperBody = rs.upperBody_score(header, data)
    leg = rs.leg_score()

    # generating the combined scores fromt the RULA tables
    if upperArm_left.shape == upperArm_right.shape == lowerArm_left.shape == lowerArm_right.shape == wrist_left.shape == wrist_right.shape == suppination_left.shape == suppination_right.shape == neck.shape == upperBody.shape:
        final_array = np.zeros((len(upperArm_left), 7)) #[A[l,r,c],B,C[l,r,c]]
        print("Looping for Scores: ")
        # Progressbar
        toolbar_width = 80
        # setup progressbar
        sys.stdout.write("[%s]" % (" " * toolbar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (toolbar_width + 1)) # return to start of line, after '['
        j = 0
        for i in range(len(final_array)):
            j += 1
            if j == int(len(final_array)/toolbar_width):
                j = 0
                sys.stdout.write("#")
                sys.stdout.flush()

            # scores from RULA tables
            final_array[i, 0] = rs.score_table_a(upperArm_left[i], lowerArm_left[i], wrist_left[i], suppination_left[i], i)
            final_array[i, 1] = rs.score_table_a(upperArm_right[i], lowerArm_right[i], wrist_right[i], suppination_right[i], i)
            final_array[i, 2] = np.mean([final_array[i, 0], final_array[i, 1]])
            final_array[i, 3] = rs.score_table_b(neck[i,0], upperBody[i,0], leg)
            final_array[i, 4] = rs.score_table_c(final_array[i, 0], final_array[i, 3])
            final_array[i, 5] = rs.score_table_c(final_array[i, 1], final_array[i, 3])
            final_array[i, 6] = rs.score_table_c(final_array[i, 2], final_array[i, 3])

    else:
        print("inconsistent shapes of matrices")
        print(upperArm_left.shape)
        print(upperArm_right.shape)
        print(lowerArm_left.shape)
        print(lowerArm_right.shape)
        print(wrist_left.shape)
        print(wrist_right.shape)
        print(suppination_left.shape)
        print(suppination_right.shape)
        print(neck.shape)
        print(upperBody.shape)

    output =("""
=========================================================
=========================================================
FINAL MEAN VALUES OF RULA TABLES)
A-left\tA-right\tA-comb\tB\tC-left\tC-right\tC-comb\n
%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f\t%.2f
=========================================================
========================================================="""
    %(np.mean(final_array[:,0]), np.mean(final_array[:,1]), np.mean(final_array[:,2]),
    np.mean(final_array[:,3]), np.mean(final_array[:,4]), np.mean(final_array[:,5]),
    np.mean(final_array[:,6])))

    print(output)
    return output


def write_to_file(filename, output):
    """write results to *.tsv file
    file will be stored in original data folder
    filename = string, output = string
    """
    path = "../data/" + "scored_" + filename + ".tsv"
    fObj = open(path, "w+")
    fObj.write(output)
    fObj.close()


print("""#################################################\n
#                                               #\n
#                                               #\n
#    /////    |   |    |        /////           #\n
#    |   |    |   |    |        |   |           #\n
#    /////    |   |    |        /////           #\n
#    | /      |   |    |        |   |           #\n
#    |  /     /////    /////    |   |     v0.35 #\n
#                                               #\n
#                                               #\n
#################################################
""")
start_time = dt.datetime.now()

mode = input("""Choose Mode:\n
Please make sure all data-files are within the data folder\n
For Batch-processing Mode press b\n
For Single-File Processing press s:\t""")

if mode == "b":
    file_list = glob.glob("../data/*.csv")
    print("%i files were found" %len(file_list))
    for i,item in enumerate(file_list):
        print("\nAnalyzing file %i out of %i\n" %(i, len(file_list)))
        output = app_rula(item)
        f_name = item.split('\\')[-1]
        write_to_file(f_name.split('.')[0], output)

    print("Process finished. Exiting.")

elif mode == "s":
    while True:
        try:
            fObj = input("Please enter filename (without csv-extension): \n\t")
            path = "../data/" + fObj + ".csv"
            print(gd.get_data.__doc__)
            output = app_rula(path)
            write_to_file(fObj, output)
            input("To Exit, press CTRL+C\nTo keep going, press ENTER\n")
        except KeyboardInterrupt:
            sys.exit(0)
        except:
            print("Unexpected error:", sys.exc_info()[0])
            print("Something went wrong. Try again!")
            raise

end_time = dt.datetime.now()
time_delta = end_time - start_time
print("Process Duration: " time_delta.total_seconds())
