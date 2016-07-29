# Sources: http://praw.readthedocs.io/en/stable/pages/writing_a_bot.html
# https://www.reddit.com/r/redditdev/comments/3gjm58/making_a_comment_chain_to_overcome_reddit_comment/
# https://stackoverflow.com/questions/3540288/how-do-i-read-a-random-line-from-one-file-in-python
# https://stackoverflow.com/questions/3770348/how-to-safely-open-close-files-in-python-2-4

import praw  # Necessary to receive live data from reddit
import random
import time

r = None

password_for_all_test_accs = ""

array_of_login_data = [
    ['C0rvuss', password_for_all_test_accs],
    ['uni_r_test_acc_2', password_for_all_test_accs],
    ['mister_Univerise_MEI', password_for_all_test_accs],
    ['de_dood_of_MEI', password_for_all_test_accs],
    ['muscle_Manager_XXX', password_for_all_test_accs],
    ['AlQaholic_1337', password_for_all_test_accs]
]

amount_of_questions_to_be_asked = 25
currently_selected_acc_data = None
currently_selected_submission = None

questions_to_be_asked = []


def redefine_r_object():
    global r

    r = praw.Reddit(user_agent="Submission variables testing by " +
                               str(chr(random.randrange(97, 97 + 26 + 1))) + str(random.randint(5, 10)))


def get_questions_from_text_file():
    global questions_to_be_asked

    # Opens the textfile and reads in line by line
    read_file = open('Proband_1.txt', 'r')
    lines = read_file.read().splitlines()

    # Try to iterate as often as possible over the randomly picked lines
    try:
        for some_iter in range(9000000):

            randomized_line = random.choice(lines)

            # Whenever the randomly picked line is not within the questions_to_be_asked - array : add it
            if randomized_line not in questions_to_be_asked:
                questions_to_be_asked.append(randomized_line)
            else:
                pass

            # Whenever the amount of questions which are to be asked is reached, break it!
            if len(questions_to_be_asked) >= amount_of_questions_to_be_asked:
                break
            else:
                pass

    finally:
        read_file.close()


def get_random_account():
    global currently_selected_acc_data
    global array_of_login_data

    currently_selected_acc_data = random.choice(array_of_login_data)

    # Makes it possibly, that an account won't be selected for a second time
    # Due to some posting regarding limitations (allowance to only post every 9 minutes...)
    # if currently_selected_acc_data[0] != 'C0rvuss':
    #     array_of_login_data.remove(currently_selected_acc_data)
    # else:
    #     pass


def log_in_with_acc_data():
    r.login(currently_selected_acc_data[0], currently_selected_acc_data[1], disable_warning=True)
    print("Logged in as: " + currently_selected_acc_data[0])


def get_submission():
    global currently_selected_submission

    currently_selected_submission = r.get_submission(submission_id="4v65th")


def post_question():
    random_int = random.randint(1, 21)

    if random_int % 7 != 0:
        currently_selected_submission.add_comment(questions_to_be_asked[0])
        print("I have tried to ask: " + str(questions_to_be_asked[0]))

        # Removes the first question out of the list
        questions_to_be_asked.pop(0)

    else:
        comment = currently_selected_submission.add_comment(questions_to_be_asked[0])
        print("I have tried to ask: " + str(questions_to_be_asked[0]))

        questions_to_be_asked.pop(0)

        # Whenever there are questions left to be asked
        if len(questions_to_be_asked) > 0:
            comment.reply("Und " + questions_to_be_asked[0])
            print("I have tried to respond / ask the following: " + str(questions_to_be_asked[0]))
            questions_to_be_asked.pop(0)
        else:
            pass


def wait_random_amount_of_seconds():
    time_to_sleep = random.randint(10, 30)
    print("Waiting " + str(time_to_sleep) + " seconds")

    time.sleep(time_to_sleep)
    print("-----")


get_questions_from_text_file()

print(str(len(questions_to_be_asked)), questions_to_be_asked)

# for x in range(amount_of_questions_to_be_asked):
#     redefine_r_object()
#     get_random_account()
#     log_in_with_acc_data()
#     get_submission()
#     post_question()
#     wait_random_amount_of_seconds()
