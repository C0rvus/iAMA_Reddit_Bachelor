# Sources used within this class:
# 1. (02.04.2016 @ 18:30) -
# http://www.scipy-lectures.org/packages/statistics/index.html
# 2. (10.04.2016 @ 12:37) -
# https://stackoverflow.com/questions/20235401/remove-nan-from-pandas-series
# 3. (10.04.2016 @ 13:04) -
# https://stackoverflow.com/questions/13413590/how-to-drop-rows-of-pandas-dataframe-whose-value-of-certain-column-is-nan
# 4. (10.04.2016 @ 13:47) -
# http://docs.scipy.org/doc/scipy/reference/stats.html
# 5. (10.04.2016 @ 18:04) -
# http://www.eecs.qmul.ac.uk/~norman/blog_articles/p_values.pdf
# 6. (23.04.2016 @ 18:19) -
# https://stackoverflow.com/questions/12838993/scipy-normaltest-how-is-it-used
# 7. (16.07.2016 @ 15:34) -
# https://stackoverflow.com/a/17171819
# 8. (23.07.2016 @ 18:42) -
# https://stackoverflow.com/questions/13404468/t-test-in-pandas-python

import copy  # Necessary to copy value of the starting year - needed for correct csv file name
import pandas  # Necessary to do statistical calculation
import numpy as np  # Necessary to do statistical calculations
from scipy.stats import pearsonr  # Necessary to calculate pearson correlation
from scipy.stats import spearmanr  # Necessary to calculate spearman correlation
from scipy.stats import kendalltau  # Necessary to calculate kendall correlation
from scipy.stats import ttest_ind   # Necessary to do some t tests

# By looking at all generated csv files we can use the following parameters for calculating various things:
# [some depend on the tier they have been calculated from]
# ----
# Year
# Thread id
# Thread author
# Thread ups
# Thread downs
# Thread creation time stamp
# Thread average comment vote score total
# Thread average comment vote score tier 1
# Thread average comment vote score tier x
# Thread average question vote score total
# Thread average question vote score tier 1
# Thread average question vote score tier x
# Thread num comments total skewed
# Thread num comments total
# Thread num comments tier 1
# Thread num comments tier x
# Thread num questions total
# Thread num questions tier 1
# Thread num questions tier x
# Thread num questions answered by iama host total
# Thread num questions answered by iama host tier 1
# Thread num questions answered by iama host tier x
# Thread num comments answered by iama host total
# Thread num comments answered by iama host tier 1
# Thread num comments answered by iama host tier x
# Thread average reaction time between comments total
# Thread average reaction time between comments tier 1
# Thread average reaction time between comments tier x
# Thread average reaction time between questions total
# Thread average reaction time between questions tier 1
# Thread average reaction time between questions tier x
# Thread average response to question time iama host total
# Thread average response to question time iama host tier 1
# Thread average response to question time iama host tier x
# Thread average response to comment time iama host total
# Thread average response to comment time iama host tier 1
# Thread average response to comment time iama host tier x
# Thread amount of questioners total
# Thread amount of questioners tier 1
# Thread amount of questioners tier x
# Thread amount of commentators total
# Thread amount of commentators tier 1
# Thread amount of commentators tier x
# Thread life span until last comment
# Thread life span until last question
# ----

# Reads the .csv file containing information about all 'iAMA' authors to the given database date
author_information_iama = pandas.read_csv(
    'a_author_information_iama.csv',
    sep=',',
    na_values="None")

# Randomly picks a given amount of rows from the dataset
author_information_iama_sampleset_randomized = author_information_iama.ix[np.random.choice
(author_information_iama.index.values, 10000)]



# Reads the .csv file containing information about all, randomly chosen authors to the given database date
author_information_random = pandas.read_csv(
    'a_author_Information_random.csv',
    sep=',',
    na_values="None")

# Randomly picks a given amount of rows from the dataset
author_information_random_sampleset_randomized = author_information_random.ix[np.random.choice
(author_information_random.index.values, 10000)]





# Reads the .csv file which will contain information about all iAMA threads posted
thread_information = pandas.read_csv(
    'd_create_Big_CSV_2009_until_2016_BIGDATA_ALL.csv',
    sep=',',
    na_values="None")

# Reads the .csv file which will contain all information about all questions asked
question_information = pandas.read_csv(
    'a_question_Answered_Yes_No_Tier_Percentage_2009_until_2016_ALL_tier_any.csv',
    sep=',',
    na_values="None",
    low_memory=False)

# Would replace NaN with zeroes:
# thread_information.fillna(0, inplace=True)
# thread_information.dropna(0, inplace=True)
# question_information.fillna(0, inplace=True)

# Skips NaN-Values here which is necessary for correct t-test (significance) calculation
# NaN-Values for authors won't be skipped here, because there are many authors who only create one iAMA thread
# and nothing else.. Therefore some values (i.E. author_thread_creation_every_x_sec) can be NaN. But dropping them
# would skew the author calculation.
# for column in copy.copy(thread_information):
#     thread_information = thread_information[
#         pandas.notnull(thread_information['' + str(column)])]
#
# for column in copy.copy(question_information):
#     question_information = question_information[
#         pandas.notnull(question_information['' + str(column)])]

# Variables regarding 'iAMA' authors are defined here
author_amount_creation_iama_threads = author_information_iama ['amount_creation_iama_threads']
author_amount_creation_other_threads = author_information_iama ['amount_creation_other_threads']
author_amount_of_comments_except_iama = author_information_iama ['amount_of_comments_except_iama']
author_amount_of_comments_iama = author_information_iama ['amount_of_comments_iama']
author_author_birth_date = author_information_iama ['author_birth_date']
author_author_comment_karma_amount = author_information_iama ['author_comment_karma_amount']
author_author_link_karma_amount = author_information_iama ['author_link_karma_amount']
author_author_name = author_information_iama ['author_name']
author_comment_creation_every_x_sec = author_information_iama ['comment_creation_every_x_sec']
author_thread_creation_every_x_sec = author_information_iama ['thread_creation_every_x_sec']
author_time_acc_birth_first_iama_thread = author_information_iama ['time_acc_birth_first_iama_thread']
author_time_diff_acc_creation_n_first_comment = author_information_iama ['time_diff_acc_creation_n_first_comment']
author_time_diff_acc_creation_n_first_thread = author_information_iama ['time_diff_acc_creation_n_first_thread']

# Variables regarding 'iAMA' authors are defined here (randomized!!)
author_amount_creation_iama_threads_randomized = author_information_iama_sampleset_randomized['amount_creation_iama_threads']
author_amount_creation_other_threads_randomized = author_information_iama_sampleset_randomized['amount_creation_other_threads']
author_amount_of_comments_except_iama_randomized = author_information_iama_sampleset_randomized['amount_of_comments_except_iama']
author_amount_of_comments_iama_randomized = author_information_iama_sampleset_randomized['amount_of_comments_iama']
author_author_birth_date_randomized = author_information_iama_sampleset_randomized['author_birth_date']
author_author_comment_karma_amount_randomized = author_information_iama_sampleset_randomized['author_comment_karma_amount']
author_author_link_karma_amount_randomized = author_information_iama_sampleset_randomized['author_link_karma_amount']
author_author_name_randomized = author_information_iama_sampleset_randomized['author_name']
author_comment_creation_every_x_sec_randomized = author_information_iama_sampleset_randomized['comment_creation_every_x_sec']
author_thread_creation_every_x_sec_randomized = author_information_iama_sampleset_randomized['thread_creation_every_x_sec']
author_time_acc_birth_first_iama_thread_randomized = author_information_iama_sampleset_randomized['time_acc_birth_first_iama_thread']
author_time_diff_acc_creation_n_first_comment_randomized = author_information_iama_sampleset_randomized['time_diff_acc_creation_n_first_comment']
author_time_diff_acc_creation_n_first_thread_randomized = author_information_iama_sampleset_randomized['time_diff_acc_creation_n_first_thread']

# Variables regarding all random authors, who are not involved in 'iAMA' posts are made here
random_author_amount_creation_iama_threads = author_information_random ['amount_creation_iama_threads']
random_author_amount_creation_other_threads = author_information_random ['amount_creation_other_threads']
random_author_amount_of_comments_except_iama = author_information_random ['amount_of_comments_except_iama']
random_author_amount_of_comments_iama = author_information_random ['amount_of_comments_iama']
random_author_author_birth_date = author_information_random ['author_birth_date']
random_author_author_comment_karma_amount = author_information_random ['author_comment_karma_amount']
random_author_author_link_karma_amount = author_information_random ['author_link_karma_amount']
random_author_author_name = author_information_random ['author_name']
random_author_comment_creation_every_x_sec = author_information_random ['comment_creation_every_x_sec']
random_author_thread_creation_every_x_sec = author_information_random ['thread_creation_every_x_sec']
random_author_time_acc_birth_first_iama_thread = author_information_random ['time_acc_birth_first_iama_thread']
random_author_time_diff_acc_creation_n_first_comment = \
    author_information_random ['time_diff_acc_creation_n_first_comment']
random_author_time_diff_acc_creation_n_first_thread = author_information_random [
    'time_diff_acc_creation_n_first_thread']


# Variables regarding all random authors, who are not involved in 'iAMA' posts are made here (randomized!!)
random_author_amount_creation_iama_threads_randomized = author_information_random_sampleset_randomized['amount_creation_iama_threads']
random_author_amount_creation_other_threads_randomized = author_information_random_sampleset_randomized['amount_creation_other_threads']
random_author_amount_of_comments_except_iama_randomized = author_information_random_sampleset_randomized['amount_of_comments_except_iama']
random_author_amount_of_comments_iama_randomized = author_information_random_sampleset_randomized['amount_of_comments_iama']
random_author_author_birth_date_randomized = author_information_random_sampleset_randomized['author_birth_date']
random_author_author_comment_karma_amount_randomized = author_information_random_sampleset_randomized['author_comment_karma_amount']
random_author_author_link_karma_amount_randomized = author_information_random_sampleset_randomized['author_link_karma_amount']
random_author_author_name_randomized = author_information_random_sampleset_randomized['author_name']
random_author_comment_creation_every_x_sec_randomized = author_information_random_sampleset_randomized['comment_creation_every_x_sec']
random_author_thread_creation_every_x_sec_randomized = author_information_random_sampleset_randomized['thread_creation_every_x_sec']
random_author_time_acc_birth_first_iama_thread_randomized = author_information_random_sampleset_randomized['time_acc_birth_first_iama_thread']
random_author_time_diff_acc_creation_n_first_comment_randomized = \
    author_information_random_sampleset_randomized['time_diff_acc_creation_n_first_comment']
random_author_time_diff_acc_creation_n_first_thread_randomized = author_information_random_sampleset_randomized[
    'time_diff_acc_creation_n_first_thread']



# Variables regarding all 'iAMA' threads are defined here
# thread_year = thread_information['Year']
# thread_id = thread_information['Thread id']
# thread_author = thread_information['Thread author']
# thread_ups = thread_information['Thread ups']
# thread_downs = thread_information['Thread downs']
# thread_creation_time_stamp = thread_information['Thread creation time stamp']
#
# thread_average_comment_vote_score_total = thread_information[
#     'Thread average comment vote score total']
#
# thread_average_comment_vote_score_tier_1 = thread_information[
#     'Thread average comment vote score tier 1']
# thread_average_comment_vote_score_tier_x = thread_information[
#     'Thread average comment vote score tier x']
#
# thread_average_question_vote_score_total = thread_information[
#     'Thread average question vote score total']
# thread_average_question_vote_score_tier_1 = thread_information[
#     'Thread average question vote score tier 1']
# thread_average_question_vote_score_tier_x = thread_information[
#     'Thread average question vote score tier x']
#
# thread_num_comments_total_skewed = thread_information[
#     'Thread num comments total skewed']
# thread_num_comments_total = thread_information['Thread num comments total']
# thread_num_comments_tier_1 = thread_information['Thread num comments tier 1']
# thread_num_comments_tier_x = thread_information['Thread num comments tier x']
#
# thread_num_questions_total = thread_information['Thread num questions total']
# thread_num_questions_tier_1 = thread_information['Thread num questions tier 1']
# thread_num_questions_tier_x = thread_information['Thread num questions tier x']
#
# thread_num_questions_answered_by_iama_host_total = thread_information[
#     'Thread num questions answered by iama host total']
# thread_num_questions_answered_by_iama_host_tier_1 = thread_information[
#     'Thread num questions answered by iama host tier 1']
# thread_num_questions_answered_by_iama_host_tier_x = thread_information[
#     'Thread num questions answered by iama host tier x']
#
# thread_num_comments_answered_by_iama_host_total = thread_information[
#     'Thread num comments answered by iama host total']
# thread_num_comments_answered_by_iama_host_tier_1 = thread_information[
#     'Thread num comments answered by iama host tier 1']
# thread_num_comments_answered_by_iama_host_tier_x = thread_information[
#     'Thread num comments answered by iama host tier x']
#
# thread_average_reaction_time_between_comments_total = thread_information[
#     'Thread average reaction time between comments total']
# thread_average_reaction_time_between_comments_tier_1 = thread_information[
#     'Thread average reaction time between comments tier 1']
# thread_average_reaction_time_between_comments_tier_x = thread_information[
#     'Thread average reaction time between comments tier x']
#
# thread_average_reaction_time_between_questions_total = thread_information[
#     'Thread average reaction time between questions total']
# thread_average_reaction_time_between_questions_tier_1 = thread_information[
#     'Thread average reaction time between questions tier 1']
# thread_average_reaction_time_between_questions_tier_x = thread_information[
#     'Thread average reaction time between questions tier x']
#
# thread_average_response_to_comment_time_iama_host_total = thread_information[
#     'Thread average response to comment time iama host total']
# thread_average_response_to_comment_time_iama_host_tier_1 = thread_information[
#     'Thread average response to comment time iama host tier 1']
# thread_average_response_to_comment_time_iama_host_tier_x = thread_information[
#     'Thread average response to comment time iama host tier x']
#
# thread_average_response_to_question_time_iama_host_total = thread_information[
#     'Thread average response to question time iama host total']
# thread_average_response_to_question_time_iama_host_tier_1 = thread_information[
#     'Thread average response to question time iama host tier 1']
# thread_average_response_to_question_time_iama_host_tier_x = thread_information[
#     'Thread average response to question time iama host tier x']
#
# thread_amount_of_questioners_total = thread_information[
#     'Thread amount of questioners total']
# thread_amount_of_questioners_tier_1 = thread_information[
#     'Thread amount of questioners tier 1']
# thread_amount_of_questioners_tier_x = thread_information[
#     'Thread amount of questioners tier x']
#
# thread_amount_of_commentators_total = thread_information[
#     'Thread amount of commentators total']
# thread_amount_of_commentators_tier_1 = thread_information[
#     'Thread amount of commentators tier 1']
# thread_amount_of_commentators_tier_x = thread_information[
#     'Thread amount of commentators tier x']
#
#
# thread_life_span_until_last_comment = thread_information[
#     'Thread life span until last comment']
# thread_life_span_until_last_question = thread_information[
#     'Thread life span until last question']
#
# # Variables regarding all 'iAMA' questions are defined here
# question_ups = question_information['Question ups']
# question_answered_by_iAMA_host = question_information[
#     'Question answered by iAMA host']


# Correlation question upvotes <-> amount of questions answered by the
# iama host
def relation_question_upvotes_with_amount_of_questions_answered_by_iama_host():
    """Calculation of the correlation question upvotes <-> amount of questions answered by the iama host

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'question_ups' and 'question_answered_by_iAMA_host':")
    print("")

    print("Pearson correlation coefficient: " +
          str(pearsonr(question_ups, question_answered_by_iAMA_host) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(question_ups, question_answered_by_iAMA_host) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(question_ups, question_answered_by_iAMA_host) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(question_ups, question_answered_by_iAMA_host) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(question_ups, question_answered_by_iAMA_host) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(question_ups, question_answered_by_iAMA_host) [1]))

    print("")
    print("----")


# Average means of different values
def average_means_of_values_f_threads():
    """Calculation of the average means of different values

    Args:
        -
    Returns:
        -
    """

    print("----")
    print("Calculating arithmetic average means here")
    print("")
    print("Average arithmetic mean - thread upvotes: " + str(thread_ups.mean()))
    print("Average arithmetic mean - thread downvotes: " + str(thread_downs.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL : comment vote score: " +
          str(thread_average_comment_vote_score_total.mean()))
    print("Average arithmetic mean - Tier 1 : comment vote score: " +
          str(thread_average_comment_vote_score_tier_1.mean()))
    print("Average arithmetic mean - Tier X : comment vote score: " +
          str(thread_average_comment_vote_score_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL : question vote score: " +
          str(thread_average_question_vote_score_total.mean()))
    print("Average arithmetic mean - Tier 1 : question vote score: " +
          str(thread_average_question_vote_score_tier_1.mean()))
    print("Average arithmetic mean - Tier X : question vote score: " +
          str(thread_average_question_vote_score_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Thread amount of comments (skewed): " +
          str(thread_num_comments_total_skewed.mean()))
    print("Average arithmetic mean - Tier ALL: Thread amount of comments (real): " +
          str(thread_num_comments_total.mean()))
    print("Average arithmetic mean - Tier 1: Thread amount of comments (real): " +
          str(thread_num_comments_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Thread amount of comments (real): " +
          str(thread_num_comments_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Thread amount of questions (real): " +
          str(thread_num_questions_total.mean()))
    print("Average arithmetic mean - Tier 1: Thread amount of questions (real): " +
          str(thread_num_questions_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Thread amount of questions (real): " +
          str(thread_num_questions_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Amount of questions answered by iama host: " +
          str(thread_num_questions_answered_by_iama_host_total.mean()))
    print("Average arithmetic mean - Tier 1: Amount of questions answered by iama host: " +
          str(thread_num_questions_answered_by_iama_host_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Amount of questions answered by iama host: " +
          str(thread_num_questions_answered_by_iama_host_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Amount of comments answered by iama host: " +
          str(thread_num_comments_answered_by_iama_host_total.mean()))
    print("Average arithmetic mean - Tier 1: Amount of comments answered by iama host: " +
          str(thread_num_comments_answered_by_iama_host_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Amount of comments answered by iama host: " +
          str(thread_num_comments_answered_by_iama_host_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Reaction time between comments (sec): " +
          str(thread_average_reaction_time_between_comments_total.mean()))
    print("Average arithmetic mean - Tier 1: Reaction time between comments (sec): " +
          str(thread_average_reaction_time_between_comments_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Reaction time between comments (sec): " +
          str(thread_average_reaction_time_between_comments_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Reaction time between questions (sec): " +
          str(thread_average_reaction_time_between_questions_total.mean()))
    print("Average arithmetic mean - Tier 1: Reaction time between questions (sec): " +
          str(thread_average_reaction_time_between_questions_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Reaction time between questions (sec): " +
          str(thread_average_reaction_time_between_questions_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Response time to comments by iAMA host (sec): " +
          str(thread_average_response_to_comment_time_iama_host_total.mean()))
    print("Average arithmetic mean - Tier 1: Response time to comments by iAMA host (sec): " +
          str(thread_average_response_to_comment_time_iama_host_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Response time to comments by iAMA host (sec): " +
          str(thread_average_response_to_comment_time_iama_host_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Response time to questions by iAMA host (sec): " +
          str(thread_average_response_to_question_time_iama_host_total.mean()))
    print("Average arithmetic mean - Tier 1: Response time to questions by iAMA host (sec): " +
          str(thread_average_response_to_question_time_iama_host_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Response time to questions by iAMA host (sec): " +
          str(thread_average_response_to_question_time_iama_host_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Thread life span until last questions: " +
          str(thread_life_span_until_last_comment.mean()))
    print("Average arithmetic mean - Tier ALL: Thread life span until last comment: " +
          str(thread_life_span_until_last_question.mean()))

    print("--")
    print("Average arithmetic mean - Tier ALL: Thread amount of commentators: " +
          str(thread_amount_of_commentators_total.mean()))
    print("Average arithmetic mean - Tier 1: Thread amount of commentators: " +
          str(thread_amount_of_commentators_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Thread amount of commentators: " +
          str(thread_amount_of_commentators_tier_x.mean()))
    print("--")
    print("Average arithmetic mean - Tier ALL: Thread amount of questioners: " +
          str(thread_amount_of_questioners_total.mean()))
    print("Average arithmetic mean - Tier 1: Thread amount of questioners: " +
          str(thread_amount_of_questioners_tier_1.mean()))
    print("Average arithmetic mean - Tier X: Thread amount of questioners: " +
          str(thread_amount_of_questioners_tier_x.mean()))
    print("----")


# Correlation thread upvotes <-> amount of comments
def relation_thread_upvotes_with_amount_of_comments():
    """Calculation of the correlation thread upvotes <-> amount of comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")

    print("Calculating correlation between 'thread_ups' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_comments_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_comments_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_comments_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_comments_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_comments_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_comments_total) [1]))
    print("")
    print("Calculating correlation between 'thread_ups' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_comments_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_comments_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_comments_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_comments_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_comments_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_comments_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_comments_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_comments_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_comments_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_comments_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_comments_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_comments_tier_x) [1]))
    print("")
    print("----")


# Correlation thread upvotes <-> amount of questions
def relation_thread_upvotes_with_amount_of_questions():
    """Calculation of the correlation thread upvotes <-> amount of questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and 'thread_num_questions_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_questions_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_questions_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_questions_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_questions_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_questions_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_questions_total) [1]))
    print("")
    print("Calculating correlation between 'thread_ups' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_questions_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_questions_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_questions_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_questions_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_questions_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_questions_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_ups, thread_num_questions_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_ups, thread_num_questions_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_num_questions_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_num_questions_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_num_questions_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_num_questions_tier_x) [1]))
    print("")
    print("----")


# Correlation thread downvotes <-> amount of comments
def relation_thread_downvotes_with_amount_of_comments():
    """Calculation of the correlation thread downvotes <-> amount of comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_comments_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_comments_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_comments_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_comments_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_comments_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_comments_total) [1]))
    print("")
    print("Calculating correlation between 'thread_downs' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_comments_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_comments_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_comments_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_comments_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_comments_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_comments_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_comments_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_comments_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_comments_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_comments_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_comments_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_comments_tier_x) [1]))
    print("")
    print("----")


# Correlation thread downvotes <-> amount of questions
def relation_thread_downvotes_with_amount_of_questions():
    """Calculation of the correlation thread downvotes <-> amount of questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_questions_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_questions_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_questions_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_questions_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_questions_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_questions_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_questions_total) [1]))
    print("")
    print("Calculating correlation between 'thread_downs' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_questions_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_questions_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_questions_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_questions_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_questions_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_questions_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_num_questions_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_num_questions_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_num_questions_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_num_questions_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_num_questions_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_num_questions_tier_x) [1]))
    print("")
    print("----")


# Correlation thread upvotes <-> iama host repsonse time to comments
def relation_thread_upvotes_and_iama_host_response_time_comments():
    """Calculation of the correlation thread upvotes <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_comment_time_iama_host_total)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_comment_time_iama_host_total) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_ups,
                                                               thread_average_response_to_comment_time_iama_host_total)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_ups,
                                                           thread_average_response_to_comment_time_iama_host_total) [
                                                    1]))

    print("Spearman correlation coefficient: " + str(spearmanr(thread_ups,
                                                               thread_average_response_to_comment_time_iama_host_total)
                                                     [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_ups,
                                                           thread_average_response_to_comment_time_iama_host_total) [
                                                     1]))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_comment_time_iama_host_tier_1)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_ups,
                                                               thread_average_response_to_comment_time_iama_host_tier_1)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_ups,
                                                           thread_average_response_to_comment_time_iama_host_tier_1)
                                                [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_ups,
                                                           thread_average_response_to_comment_time_iama_host_tier_1)
                                                 [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_comment_time_iama_host_tier_x)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_ups,
                                                               thread_average_response_to_comment_time_iama_host_tier_x)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_ups,
                                                           thread_average_response_to_comment_time_iama_host_tier_x)
                                                [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_average_response_to_comment_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread upvotes <-> iama host repsonse time to questions
def relation_thread_upvotes_and_iama_host_response_time_questions():
    """Calculation of the correlation thread upvotes <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_question_time_iama_host_total)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_question_time_iama_host_total) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_ups,
                                                               thread_average_response_to_question_time_iama_host_total)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_ups,
                                                           thread_average_response_to_question_time_iama_host_total)
                                                [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_average_response_to_question_time_iama_host_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_ups, thread_average_response_to_question_time_iama_host_total)
              [1]))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_question_time_iama_host_tier_1)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_question_time_iama_host_tier_1)
                                                [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_average_response_to_question_time_iama_host_tier_1)
              [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_ups,
                                                           thread_average_response_to_question_time_iama_host_tier_1)
                                                [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_average_response_to_question_time_iama_host_tier_1)
              [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_ups,
                                                           thread_average_response_to_question_time_iama_host_tier_1)
                                                 [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_ups,
                                                             thread_average_response_to_question_time_iama_host_tier_x)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_ups,
                                                         thread_average_response_to_question_time_iama_host_tier_x)
                                                [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_ups, thread_average_response_to_question_time_iama_host_tier_x)
              [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_ups, thread_average_response_to_question_time_iama_host_tier_x)
              [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_ups, thread_average_response_to_question_time_iama_host_tier_x)
              [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_ups,
                                                           thread_average_response_to_question_time_iama_host_tier_x)
                                                 [1]))
    print("")
    print("----")


# Correlation thread downvotes <-> iama host repsonse time to comments
def relation_thread_downvotes_and_iama_host_response_time_comments():
    """Calculation of the correlation thread downvotes <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_downs,
                                                             thread_average_response_to_comment_time_iama_host_total)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_downs,
                                                         thread_average_response_to_comment_time_iama_host_total) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_total)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_total) [
                                                    1]))

    print("Spearman correlation coefficient: " + str(spearmanr(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_total)
                                                     [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_total) [
                                                     1]))
    print("")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_downs,
                                                             thread_average_response_to_comment_time_iama_host_tier_1)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_downs,
                                                         thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_tier_1)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_tier_1)
                                                [1]))

    print("Spearman correlation coefficient: " + str(spearmanr(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_tier_1)
                                                     [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_tier_1)
                                                 [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_downs,
                                                             thread_average_response_to_comment_time_iama_host_tier_x)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_downs,
                                                         thread_average_response_to_comment_time_iama_host_tier_x)
                                                [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_tier_x)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_tier_x)
                                                [1]))

    print("Spearman correlation coefficient: " + str(spearmanr(thread_downs,
                                                               thread_average_response_to_comment_time_iama_host_tier_x)
                                                     [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_downs,
                                                           thread_average_response_to_comment_time_iama_host_tier_x)
                                                 [1]))
    print("")
    print("----")


# Correlation thread downvotes <-> iama host repsonse time to questions
def relation_thread_downvotes_and_iama_host_response_time_questions():
    """Calculation of the correlation thread downvotes <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_downs,
                                                             thread_average_response_to_question_time_iama_host_total)
                                                    [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_downs,
                                                         thread_average_response_to_question_time_iama_host_total)
                                                [1]))

    print("Kendall correlation coefficient: " + str(kendalltau(thread_downs,
                                                               thread_average_response_to_question_time_iama_host_total)
                                                    [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_downs,
                                                           thread_average_response_to_question_time_iama_host_total)
                                                [1]))

    print("Spearman correlation coefficient: " + str(spearmanr(thread_downs,
                                                               thread_average_response_to_question_time_iama_host_total)
                                                     [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_downs,
                                                           thread_average_response_to_question_time_iama_host_total)
                                                 [1]))
    print("")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_downs, thread_average_response_to_question_time_iama_host_tier_1)
              [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(pearsonr(thread_downs,
                                                             thread_average_response_to_question_time_iama_host_tier_x)
                                                    [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_downs, thread_average_response_to_question_time_iama_host_tier_x)
              [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_downs, thread_average_response_to_question_time_iama_host_tier_x)
              [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_downs, thread_average_response_to_question_time_iama_host_tier_x)
              [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_downs, thread_average_response_to_question_time_iama_host_tier_x)
              [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_downs,
                                                           thread_average_response_to_question_time_iama_host_tier_x)
                                                 [1]))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> amount of comments
def relation_thread_lifespan_to_last_comment_and_amount_of_comments():
    """Calculation of the correlation thread life span (until last comment) <-> amount of comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_total) [1]))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_comments_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_comments_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_comments_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> amount of questions
def relation_thread_lifespan_to_last_comment_and_amount_of_questions():
    """Calculation of the correlation thread life span (until last comment) <-> amount of questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_questions_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_total) [1]))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_comment, thread_num_questions_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_comment, thread_num_questions_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_comment, thread_num_questions_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> amount of comments
def relation_thread_lifespan_to_last_question_and_amount_of_comments():
    """Calculation of the correlation thread life span (until last question) <-> amount of comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_total) [1]))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_tier_1) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_comments_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_tier_x) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_comments_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_comments_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> amount of question
def relation_thread_lifespan_to_last_question_and_amount_of_question():
    """Calculation of the correlation thread life span (until last question) <-> amount of question

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_questions_total':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_total) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_total) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_questions_total) [0]))
    print("Kendall correlation p-value: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_questions_total) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_total) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_total) [1]))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_tier_1) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_tier_1) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_questions_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_num_questions_tier_1) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_tier_1) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_tier_x) [0]))
    print("Pearson correlation p-value: " +
          str(pearsonr(thread_life_span_until_last_question, thread_num_questions_tier_x) [1]))

    print("Kendall correlation coefficient: " +
          str(kendalltau(thread_life_span_until_last_question, thread_num_questions_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_num_questions_tier_x) [1]))

    print("Spearman correlation coefficient: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_tier_x) [0]))
    print("Spearman correlation p-value: " +
          str(spearmanr(thread_life_span_until_last_question, thread_num_questions_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> iama host repsonse
# time to comments
def relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread life span (until last comment) <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> iama host repsonse
# time to questions
def relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread life span (until last comment) <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> and iama host
# repsonse time to comments
def relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread life span (until last question) <-> and iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_question' and"
        " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_life_span_until_last_question' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_question' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_question,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> iama host
# repsonse time to questions
def relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread life span (until last question) <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_life_span_until_last_comment' and"
        " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_life_span_until_last_comment,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> iama host repsonse
# time to comments
def relation_thread_reaction_time_comments_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread reaction time between comments <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
        " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> iama host repsonse
# time to questions
def relation_thread_reaction_time_comments_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread reaction time between comments <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
        " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_average_response_to_question_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
        " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
        " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> iama host
# repsonse time to comments
def relation_thread_reaction_time_questions_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread reaction time between questions <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
        " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_comment_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_comment_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
        " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_comment_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> iama host
# repsonse time to questions
def relation_thread_reaction_time_questions_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread reaction time between questions <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
        " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_average_response_to_question_time_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
        " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_average_response_to_question_time_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
        " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_average_response_to_question_time_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> amount of comments
# the iama host reacted to
def relation_thread_reaction_time_comments_and_amount_of_comments_the_iama_host_answered_to():
    """Calculation of the correlation thread reaction time between comments <-> amount of comments the iama host
        reacted to

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
        " 'thread_num_comments_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_num_comments_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
        " 'thread_num_comments_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
        " 'thread_num_comments_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> amount of
# questions the iama host reacted to
def relation_thread_reaction_time_comments_and_amount_of_questions_the_iama_host_answered_to():
    """Calculation of the correlation thread reaction time between comments <-> amount of questions the
        iama host reacted to

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
        " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_total,
                thread_num_questions_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
        " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
        " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_comments_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> amount of
# comments the iama host reacted to
def relation_thread_reaction_time_questions_and_amount_of_comments_the_iama_host_answered_to():
    """Calculation of the correlation thread reaction time between questions <-> amount of comments the
        iama host reacted to

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
        " 'thread_num_comments_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_num_comments_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
        " 'thread_num_comments_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
        " 'thread_num_comments_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> amount of
# questions the iama host reacted to
def relation_thread_reaction_time_questions_and_amount_of_questions_the_iama_host_answered_to():
    """Calculation of the correlation thread reaction time between questions <-> amount of questions the iama
        host reacted to

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
        " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_total,
                thread_num_questions_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
        " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
        " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_average_reaction_time_between_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation amount of questioners per thread <-> amount of questions
# answered by iama host
def relation_thread_amount_of_questioners_total_and_num_questions_answered_by_iama_host():
    """Calculation of the correlation amount of questioners per thread <-> amount of questions answered by iama host

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_amount_of_questioners_total' and"
        " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_questioners_total,
                thread_num_questions_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_amount_of_questioners_tier_1' and"
        " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_questioners_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_amount_of_questioners_tier_x' and"
        " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_questioners_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation amount of commentators per thread <-> amount of questions
# answered by iama host
def realation_thread_amount_of_commentators_total_and_num_comments_answered_by_iama_host():
    """Calculation of the correlation amount of commentators per thread <-> amount of questions answered by iama host

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_amount_of_commentators_total' and"
        " 'thread_num_comments_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_commentators_total,
                thread_num_comments_answered_by_iama_host_total) [1]))
    print("")
    print(
        "Calculating correlation between 'thread_amount_of_commentators_tier_1' and"
        " 'thread_num_comments_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_commentators_tier_1,
                thread_num_comments_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print(
        "Calculating correlation between 'thread_amount_of_commentators_tier_x' and"
        " 'thread_num_comments_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Pearson correlation p-value: " + str(
            pearsonr(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Kendall correlation p-value: " + str(
            kendalltau(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [0]))
    print(
        "Spearman correlation p-value: " + str(
            spearmanr(
                thread_amount_of_commentators_tier_x,
                thread_num_comments_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation amount of questions ansked <-> amount of questions answered
# by iama host
def relation_thread_amount_of_questions_and_amount_questions_answered_by_iama_host():
    """Calculation of the amount of questions ansked <-> amount of questions answered by iama host

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_num_questions_total' and"
          " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_num_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_num_questions_total,
                                                         thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_num_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_num_questions_total,
                                                           thread_num_questions_answered_by_iama_host_total) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_num_questions_total,
                thread_num_questions_answered_by_iama_host_total) [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_num_questions_total,
                                                           thread_num_questions_answered_by_iama_host_total) [1]))
    print("")
    print("Calculating correlation between 'thread_num_questions_tier_1' and"
          " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_num_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_num_questions_tier_1,
                                                         thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_num_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_num_questions_tier_1,
                                                           thread_num_questions_answered_by_iama_host_tier_1) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_num_questions_tier_1,
                thread_num_questions_answered_by_iama_host_tier_1) [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_num_questions_tier_1,
                                                           thread_num_questions_answered_by_iama_host_tier_1) [1]))
    print("")
    print("----")
    print("Calculating correlation between 'thread_num_questions_tier_x' and"
          " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print(
        "Pearson correlation coefficient: " + str(
            pearsonr(
                thread_num_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print("Pearson correlation p-value: " + str(pearsonr(thread_num_questions_tier_x,
                                                         thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Kendall correlation coefficient: " + str(
            kendalltau(
                thread_num_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print("Kendall correlation p-value: " + str(kendalltau(thread_num_questions_tier_x,
                                                           thread_num_questions_answered_by_iama_host_tier_x) [1]))

    print(
        "Spearman correlation coefficient: " + str(
            spearmanr(
                thread_num_questions_tier_x,
                thread_num_questions_answered_by_iama_host_tier_x) [0]))
    print("Spearman correlation p-value: " + str(spearmanr(thread_num_questions_tier_x,
                                                           thread_num_questions_answered_by_iama_host_tier_x) [1]))
    print("")
    print("----")


# Correlation of every column with every column
def thread_overall_correlation():
    """Calculation of the correlation of every column with every column for the threads

    Args:
        -
    Returns:
        -
    """
    print(str(thread_information.corr()))


# Correlation of every column with every column
def question_overall_correlation():
    """Calculation of the correlation of every column with every column for the questions

    Args:
        -
    Returns:
        -
    """
    print(str(question_information.corr()))


# Calculates various arithmetic means for author data
def average_means_of_values_f_authors():
    """Calculation of the average means of different values for author data
    
    Args:
        -
    Returns:
        -
    """

    global author_information_iama, author_information_random
    
    print("----")
    print("Calculating arithmetic average means for 'iAMA' author here")
    print("")

    print("Average arithmetic mean - author_amount_creation_iama_threads: " + str(
        author_amount_creation_iama_threads.mean()))

    print("Average arithmetic mean - author_amount_creation_other_threads: " + str(
        author_amount_creation_other_threads.mean()))

    print("Average arithmetic mean - author_amount_of_comments_except_iama: " + str(
        author_amount_of_comments_except_iama.mean()))

    print("Average arithmetic mean - author_amount_of_comments_iama: " + str(
        author_amount_of_comments_iama.mean()))

    print("Average arithmetic mean - author_author_comment_karma_amount: " + str(
        author_author_comment_karma_amount.mean()))

    print("Average arithmetic mean - author_author_link_karma_amount: " + str(
        author_author_link_karma_amount.mean()))

    print("Average arithmetic mean - author_time_acc_birth_first_iama_thread: " + str(
        author_time_acc_birth_first_iama_thread.mean()))

    print("----")
    print("Calculating arithmetic medians for the 'iAMA' author here")
    print("")
    print("Median - author_amount_creation_iama_threads: " + str(
        author_amount_creation_iama_threads.median()))

    print("Median - author_amount_creation_other_threads: " + str(
        author_amount_creation_other_threads.median()))

    print("Median - author_amount_of_comments_except_iama: " + str(
        author_amount_of_comments_except_iama.median()))

    print("Median - author_amount_of_comments_iama: " + str(
        author_amount_of_comments_iama.median()))

    print("Median - author_author_comment_karma_amount: " + str(
        author_author_comment_karma_amount.median()))

    print("Median - author_author_link_karma_amount: " + str(
        author_author_link_karma_amount.median()))

    print("Median - author_time_acc_birth_first_iama_thread: " + str(
        author_time_acc_birth_first_iama_thread.median()))

    print("----")
    print("Skipping all NaN values here and calculating the remaining data means")
    print("----")

    # Dropping all NaN values here
    for values in copy.copy(author_information_iama):
        author_information_iama = author_information_iama [
            pandas.notnull(author_information_iama ['' + str(values)])]

    print("Average arithmetic mean - author_comment_creation_every_x_sec: " + str(
        author_comment_creation_every_x_sec.mean()))

    print("Average arithmetic mean - author_thread_creation_every_x_sec: " + str(
        author_thread_creation_every_x_sec.mean()))

    print("Average arithmetic mean - author_time_diff_acc_creation_n_first_comment: " + str(
        author_time_diff_acc_creation_n_first_comment.mean()))

    print("Average arithmetic mean - author_time_diff_acc_creation_n_first_thread: " + str(
        author_time_diff_acc_creation_n_first_thread.mean()))

    print("----")
    print("!! Calculating data for random reddit users here !!")
    print("----")

    print("Average arithmetic mean - random_author_amount_creation_iama_threads: " + str(
        random_author_amount_creation_iama_threads.mean()))

    print("Average arithmetic mean - random_author_amount_creation_other_threads: " + str(
        random_author_amount_creation_other_threads.mean()))

    print("Average arithmetic mean - random_author_amount_of_comments_except_iama: " + str(
        random_author_amount_of_comments_except_iama.mean()))

    print("Average arithmetic mean - random_author_amount_of_comments_iama: " + str(
        random_author_amount_of_comments_iama.mean()))

    print("Average arithmetic mean - random_author_author_comment_karma_amount: " + str(
        random_author_author_comment_karma_amount.mean()))

    print("Average arithmetic mean - random_author_author_link_karma_amount: " + str(
        random_author_author_link_karma_amount.mean()))

    print("Average arithmetic mean - random_author_time_acc_birth_first_iama_thread: " + str(
        random_author_time_acc_birth_first_iama_thread.mean()))

    print("----")
    print("Calculating arithmetic medians for the 'iAMA' author here")
    print("")
    print("Median - random_author_amount_creation_iama_threads: " + str(
        random_author_amount_creation_iama_threads.median()))

    print("Median - random_author_amount_creation_other_threads: " + str(
        random_author_amount_creation_other_threads.median()))

    print("Median - random_author_amount_of_comments_except_iama: " + str(
        random_author_amount_of_comments_except_iama.median()))

    print("Median - random_author_amount_of_comments_iama: " + str(
        random_author_amount_of_comments_iama.median()))

    print("Median - random_author_author_comment_karma_amount: " + str(
        random_author_author_comment_karma_amount.median()))

    print("Median - random_author_author_link_karma_amount: " + str(
        random_author_author_link_karma_amount.median()))

    print("Median - random_author_time_acc_birth_first_iama_thread: " + str(
        random_author_time_acc_birth_first_iama_thread.median()))

    print("----")
    print("Skipping all NaN values here and calculating the remaining data means")
    print("----")

    # Dropping all NaN values here
    for values in copy.copy(author_information_random):
        author_information_random = author_information_random [
            pandas.notnull(author_information_random ['' + str(values)])]

        # print("Average arithmetic mean - random_author_comment_creation_every_x_sec: " + str(
        #     random_author_comment_creation_every_x_sec.mean()))
        #
        # print("Average arithmetic mean - random_author_thread_creation_every_x_sec: " + str(
        #     random_author_thread_creation_every_x_sec.mean()))
        #
        # print("Average arithmetic mean - random_author_time_diff_acc_creation_n_first_comment: " + str(
        #     random_author_time_diff_acc_creation_n_first_comment.mean()))
        #
        # print("Average arithmetic mean - random_author_time_diff_acc_creation_n_first_thread: " + str(
        #     random_author_time_diff_acc_creation_n_first_thread.mean()))


# Start that calculation

# relation_question_upvotes_with_amount_of_questions_answered_by_iama_host()
#
# average_means_of_values_f_threads()
#
# average_means_of_values_f_authors()
#
#
# relation_thread_upvotes_with_amount_of_comments()
# relation_thread_upvotes_with_amount_of_questions()
# relation_thread_downvotes_with_amount_of_comments()
# relation_thread_downvotes_with_amount_of_questions()
#
# relation_thread_upvotes_and_iama_host_response_time_comments()
# relation_thread_upvotes_and_iama_host_response_time_questions()
# relation_thread_downvotes_and_iama_host_response_time_comments()
# relation_thread_downvotes_and_iama_host_response_time_questions()
#
# relation_thread_lifespan_to_last_comment_and_amount_of_comments()
# relation_thread_lifespan_to_last_comment_and_amount_of_questions()
# relation_thread_lifespan_to_last_question_and_amount_of_comments()
# relation_thread_lifespan_to_last_question_and_amount_of_question()
#
# relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_comments()
# relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_questions()
# relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_comments()
# relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_questions()
#
# relation_thread_reaction_time_comments_and_iama_host_response_time_to_comments()
# relation_thread_reaction_time_comments_and_iama_host_response_time_to_questions()
# relation_thread_reaction_time_questions_and_iama_host_response_time_to_comments()
# relation_thread_reaction_time_questions_and_iama_host_response_time_to_questions()
#
# relation_thread_reaction_time_comments_and_amount_of_comments_the_iama_host_answered_to()
# relation_thread_reaction_time_comments_and_amount_of_questions_the_iama_host_answered_to()
# relation_thread_reaction_time_questions_and_amount_of_comments_the_iama_host_answered_to()
# relation_thread_reaction_time_questions_and_amount_of_questions_the_iama_host_answered_to()
#
# relation_thread_amount_of_questioners_total_and_num_questions_answered_by_iama_host()
#
# relation_thread_amount_of_questions_and_amount_questions_answered_by_iama_host()
#
# thread_overall_correlation()
# question_overall_correlation()


def median_of_values_f_authors():
    print("----")
    print("Calculating arithmetic medians for the 'iAMA' author here (randomized!!)")
    print("")
    print("Median - author_amount_creation_iama_threads: " + str(
        author_amount_creation_iama_threads_randomized.median()))

    print("(std derivation): Median - author_amount_creation_iama_threads: " + str(
        np.std(author_amount_creation_iama_threads_randomized)))

    print("Median - author_amount_creation_other_threads: " + str(
        author_amount_creation_other_threads_randomized.median()))

    print("(std derivation): Median - author_amount_creation_other_threads: " + str(
        np.std(author_amount_creation_other_threads_randomized)))

    print("Median - author_amount_of_comments_except_iama: " + str(
        author_amount_of_comments_except_iama_randomized.median()))

    print("(std derivation): Median - author_amount_of_comments_except_iama: " + str(
        np.std(author_amount_of_comments_except_iama_randomized)))

    print("Median - author_amount_of_comments_iama: " + str(
        author_amount_of_comments_iama_randomized.median()))

    print("(std derivation): Median - author_amount_of_comments_iama: " + str(
        np.std(author_amount_of_comments_iama_randomized)))

    print("Median - author_author_comment_karma_amount: " + str(
        author_author_comment_karma_amount_randomized.median()))

    print("(std derivation): Median - author_author_comment_karma_amount: " + str(
        np.std(author_author_comment_karma_amount_randomized)))

    print("Median - author_author_link_karma_amount: " + str(
        author_author_link_karma_amount_randomized.median()))

    print("(std derivation): Median - author_author_link_karma_amount: " + str(
        np.std(author_author_link_karma_amount_randomized)))

    print("----")
    print("-- 1st thread stories")
    print("----")

    print("Median - author_time_acc_birth_first_iama_thread_randomized: " + str(
        author_time_acc_birth_first_iama_thread_randomized.median()))

    print("Arr. Mean - author_time_acc_birth_first_iama_thread_randomized: " + str(
        author_time_acc_birth_first_iama_thread_randomized.mean()))

    print("Median - author_time_diff_acc_creation_n_first_thread_randomized: " + str(
        author_time_diff_acc_creation_n_first_thread_randomized.median()))

    print("Arr. Mean - author_time_diff_acc_creation_n_first_thread_randomized: " + str(
        author_time_diff_acc_creation_n_first_thread_randomized.mean()))
    print("----")
    print("----")
    print("----")
    print("Median - random_author_amount_creation_iama_threads: " + str(
        random_author_amount_creation_iama_threads_randomized.median()))

    print("(std derivation) Median - random_author_amount_creation_iama_threads: " + str(
        random_author_amount_creation_iama_threads_randomized.median()))

    print(" Median - random_author_amount_creation_other_threads: " + str(
        random_author_amount_creation_other_threads_randomized.median()))

    print("(std derivation): Median - random_author_amount_creation_other_threads: " + str(
        np.std(random_author_amount_creation_other_threads_randomized)))

    print("Median - random_author_amount_of_comments_except_iama: " + str(
        random_author_amount_of_comments_except_iama_randomized.median()))

    print("(std derivation): Median - random_author_amount_of_comments_except_iama: " + str(
        np.std(random_author_amount_of_comments_except_iama_randomized)))

    print("Median - random_author_amount_of_comments_iama: " + str(
        random_author_amount_of_comments_iama_randomized.median()))

    print("(std derivation): Median - random_author_amount_of_comments_iama: " + str(
        np.std(random_author_amount_of_comments_iama_randomized)))

    print("Median - random_author_author_comment_karma_amount: " + str(
        random_author_author_comment_karma_amount_randomized.median()))

    print("(std derivation) Median - random_author_author_comment_karma_amount: " + str(
        np.std(random_author_author_comment_karma_amount_randomized)))

    print("Median - random_author_author_link_karma_amount: " + str(
        random_author_author_link_karma_amount_randomized.median()))

    print("(std derivation): Median - random_author_author_link_karma_amount: " + str(
        np.std(random_author_author_link_karma_amount_randomized)))

    print("----")
    print("-- 1st thread stories")
    print("----")

    print("Median - random_author_time_acc_birth_first_iama_thread_randomized: " + str(
        random_author_time_acc_birth_first_iama_thread_randomized.median()))

    print("Arr. Mean - random_author_time_acc_birth_first_iama_thread_randomized: " + str(
        random_author_time_acc_birth_first_iama_thread_randomized.mean()))

    print("Median - random_author_time_diff_acc_creation_n_first_thread_randomized: " + str(
        random_author_time_diff_acc_creation_n_first_thread_randomized.median()))

    print("Arr. Mean - random_author_time_diff_acc_creation_n_first_thread_randomized: " + str(
        random_author_time_diff_acc_creation_n_first_thread_randomized.mean()))


def calculate_t_tests_of_author_values():
    print("calculating t-tests")

    author_information_iama_sampleset_randomized_2 = author_information_iama.ix[np.random.choice(author_information_iama.index.values, 10000)]
    author_information_random_sampleset_randomized_2 = author_information_random.ix[np.random.choice(author_information_random.index.values, 10000)]

    # Variables regarding 'iAMA' authors are defined here (randomized!!)
    author_amount_creation_iama_threads_randomized_2 = author_information_iama_sampleset_randomized_2['amount_creation_iama_threads']
    author_amount_creation_other_threads_randomized_2 = author_information_iama_sampleset_randomized_2['amount_creation_other_threads']
    author_amount_of_comments_except_iama_randomized_2 = author_information_iama_sampleset_randomized_2['amount_of_comments_except_iama']
    author_amount_of_comments_iama_randomized_2 = author_information_iama_sampleset_randomized_2['amount_of_comments_iama']
    author_author_birth_date_randomized_2 = author_information_iama_sampleset_randomized_2['author_birth_date']
    author_author_comment_karma_amount_randomized_2 = author_information_iama_sampleset_randomized_2['author_comment_karma_amount']
    author_author_link_karma_amount_randomized_2 = author_information_iama_sampleset_randomized_2['author_link_karma_amount']
    author_author_name_randomized_2 = author_information_iama_sampleset_randomized_2['author_name']
    author_comment_creation_every_x_sec_randomized_2 = author_information_iama_sampleset_randomized_2['comment_creation_every_x_sec']
    author_thread_creation_every_x_sec_randomized_2 = author_information_iama_sampleset_randomized_2['thread_creation_every_x_sec']
    author_time_acc_birth_first_iama_thread_randomized_2 = author_information_iama_sampleset_randomized_2['time_acc_birth_first_iama_thread']
    author_time_diff_acc_creation_n_first_comment_randomized_2 = author_information_iama_sampleset_randomized_2['time_diff_acc_creation_n_first_comment']
    author_time_diff_acc_creation_n_first_thread_randomized_2 = author_information_iama_sampleset_randomized_2['time_diff_acc_creation_n_first_thread']

    # Variables regarding all random authors, who are not involved in 'iAMA' posts are made here (randomized!!)
    random_author_amount_creation_iama_threads_randomized_2 = author_information_random_sampleset_randomized_2['amount_creation_iama_threads']
    random_author_amount_creation_other_threads_randomized_2 = author_information_random_sampleset_randomized_2['amount_creation_other_threads']
    random_author_amount_of_comments_except_iama_randomized_2 = author_information_random_sampleset_randomized_2['amount_of_comments_except_iama']
    random_author_amount_of_comments_iama_randomized_2 = author_information_random_sampleset_randomized_2['amount_of_comments_iama']
    random_author_author_birth_date_randomized_2 = author_information_random_sampleset_randomized_2['author_birth_date']
    random_author_author_comment_karma_amount_randomized_2 = author_information_random_sampleset_randomized_2['author_comment_karma_amount']
    random_author_author_link_karma_amount_randomized_2 = author_information_random_sampleset_randomized_2['author_link_karma_amount']
    random_author_author_name_randomized_2 = author_information_random_sampleset_randomized_2['author_name']
    random_author_comment_creation_every_x_sec_randomized_2 = author_information_random_sampleset_randomized_2['comment_creation_every_x_sec']
    random_author_thread_creation_every_x_sec_randomized_2 = author_information_random_sampleset_randomized_2['thread_creation_every_x_sec']
    random_author_time_acc_birth_first_iama_thread_randomized_2 = author_information_random_sampleset_randomized_2['time_acc_birth_first_iama_thread']
    random_author_time_diff_acc_creation_n_first_comment_randomized_2 = author_information_random_sampleset_randomized_2['time_diff_acc_creation_n_first_comment']
    random_author_time_diff_acc_creation_n_first_thread_randomized_2 = author_information_random_sampleset_randomized_2['time_diff_acc_creation_n_first_thread']

    print("T-Test iAMA-Authors (randomized) : amount creation of iama threads", str(ttest_ind(author_amount_creation_iama_threads_randomized, author_amount_creation_iama_threads_randomized_2)))
    print("T-Test iAMA-Authors (randomized) : amount creation of other threads", str(ttest_ind(author_amount_creation_other_threads_randomized, author_amount_creation_other_threads_randomized_2)))

    print("T-Test iAMA-Authors (randomized) : amount of comments in iama threads", str(ttest_ind(author_amount_of_comments_iama_randomized, author_amount_of_comments_iama_randomized_2)))
    print("T-Test iAMA-Authors (randomized) : amount of comments in other threads", str(ttest_ind(author_amount_of_comments_except_iama_randomized, author_amount_of_comments_except_iama_randomized_2)))

    print("T-Test iAMA-Authors (randomized) : amount comment carma", str(ttest_ind(author_author_comment_karma_amount_randomized, author_author_comment_karma_amount_randomized_2)))

    print("T-Test iAMA-Authors (randomized) : amount link karma", str(ttest_ind(author_author_link_karma_amount_randomized, author_author_link_karma_amount_randomized_2)))


# median_of_values_f_authors()
calculate_t_tests_of_author_values()