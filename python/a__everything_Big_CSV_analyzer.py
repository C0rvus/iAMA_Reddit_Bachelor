# Sources used within this class:
# 1. (02.04.2016 @ 18:30) -
# http://www.scipy-lectures.org/packages/statistics/index.html

import pandas                   # Necessary to do statistical calculation

# By looking at all generated csv files we can use the following parameters for calculating various things:
# [some depend on the tier they have been calculated from]
# ----
# Year
# Question ups
# Question answered by iAMA host
# Thread id
# Thread author
# Thread ups
# Thread downs
# Thread creation time stamp
#
# Thread average comment vote score total
# Thread average comment vote score tier 1
# Thread average comment vote score tier x
#
# Thread average question vote score total
# Thread average question vote score tier 1
# Thread average question vote score tier x
#
# Thread num comments total skewed
# Thread num comments total
# Thread num comments tier 1
# Thread num comments tier x
#
# Thread num questions total
# Thread num questions tier 1
# Thread num questions tier x
#
# Thread num questions answered by iama host total
# Thread num questions answered by iama host tier 1
# Thread num questions answered by iama host tier x
#
# Thread num comments answered by iama host total
# Thread num comments answered by iama host tier 1
# Thread num comments answered by iama host tier x
#
# Thread average reaction time between comments total
# Thread average reaction time between comments tier 1
# Thread average reaction time between comments tier x
#
# Thread average reaction time between questions total
# Thread average reaction time between questions tier 1
# Thread average reaction time between questions tier x
#
# Thread average response to question time iama host total
# Thread average response to question time iama host tier 1
# Thread average response to question time iama host tier x
#
# Thread average response to comment time iama host total
# Thread average response to comment time iama host total
# Thread average response to comment time iama host total
#
# Thread life span until last comment
# Thread life span until last question
# ----


thread_information = pandas.read_csv('d_create_Big_CSV_2009_until_2016_BIGDATA_ALL.csv', sep=',', na_values="None")
question_information = pandas.read_csv('a_question_Answered_Yes_No_Tier_Percentage_2009_until_2016_ALL_tier_any.csv',
                                       sep=',', na_values="None", low_memory=False)
# Would replace NaN with zeroes: thread_information.fillna(0, inplace=True)

thread_year = thread_information['Year']
thread_id = thread_information['Thread id']
thread_author = thread_information['Thread author']
thread_ups = thread_information['Thread ups']
thread_downs = thread_information['Thread downs']
thread_creation_time_stamp = thread_information['Thread creation time stamp']

thread_average_comment_vote_score_total = thread_information['Thread average comment vote score total']

thread_average_comment_vote_score_tier_1 = thread_information['Thread average comment vote score tier 1']
thread_average_comment_vote_score_tier_x = thread_information['Thread average comment vote score tier x']

thread_average_question_vote_score_total = thread_information['Thread average question vote score total']
thread_average_question_vote_score_tier_1 = thread_information['Thread average question vote score tier 1']
thread_average_question_vote_score_tier_x = thread_information['Thread average question vote score tier x']

thread_num_comments_total_skewed = thread_information['Thread num comments total skewed']
thread_num_comments_total = thread_information['Thread num comments total']
thread_num_comments_tier_1 = thread_information['Thread num comments tier 1']
thread_num_comments_tier_x = thread_information['Thread num comments tier x']

thread_num_questions_total = thread_information['Thread num questions total']
thread_num_questions_tier_1 = thread_information['Thread num questions tier 1']
thread_num_questions_tier_x = thread_information['Thread num questions tier x']

thread_num_questions_answered_by_iama_host_total = thread_information[
    'Thread num questions answered by iama host total']
thread_num_questions_answered_by_iama_host_tier_1 = thread_information[
    'Thread num questions answered by iama host tier 1']
thread_num_questions_answered_by_iama_host_tier_x = thread_information[
    'Thread num questions answered by iama host tier x']

thread_num_comments_answered_by_iama_host_total = thread_information[
    'Thread num comments answered by iama host total']
thread_num_comments_answered_by_iama_host_tier_1 = thread_information[
    'Thread num comments answered by iama host tier 1']
thread_num_comments_answered_by_iama_host_tier_x = thread_information[
    'Thread num comments answered by iama host tier x']

thread_average_reaction_time_between_comments_total = thread_information[
    'Thread average reaction time between comments total']
thread_average_reaction_time_between_comments_tier_1 = thread_information[
    'Thread average reaction time between comments tier 1']
thread_average_reaction_time_between_comments_tier_x = thread_information[
    'Thread average reaction time between comments tier x']

thread_average_reaction_time_between_questions_total = thread_information[
    'Thread average reaction time between questions total']
thread_average_reaction_time_between_questions_tier_1 = thread_information[
    'Thread average reaction time between questions tier 1']
thread_average_reaction_time_between_questions_tier_x = thread_information[
    'Thread average reaction time between questions tier x']

thread_average_response_to_comment_time_iama_host_total = thread_information[
    'Thread average response to comment time iama host total']
thread_average_response_to_comment_time_iama_host_tier_1 = thread_information[
    'Thread average response to comment time iama host tier 1']
thread_average_response_to_comment_time_iama_host_tier_x = thread_information[
    'Thread average response to comment time iama host tier x']

thread_average_response_to_question_time_iama_host_total = thread_information[
    'Thread average response to question time iama host total']
thread_average_response_to_question_time_iama_host_tier_1 = thread_information[
    'Thread average response to question time iama host tier 1']
thread_average_response_to_question_time_iama_host_tier_x = thread_information[
    'Thread average response to question time iama host tier x']

thread_life_span_until_last_comment = thread_information['Thread life span until last comment']
thread_life_span_until_last_question = thread_information['Thread life span until last question']

question_ups = question_information['Question ups']
question_answered_by_iAMA_host = question_information['Question answered by iAMA host']


# Correlation question upvotes <-> amount of questions answered by the iama host
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
    print("Pearson correlation coefficient: " + str(question_ups.corr(question_answered_by_iAMA_host)))
    print("Kendall correlation coefficient: " + str(question_ups.corr(question_answered_by_iAMA_host,
                                                                      method="kendall")))
    print("Spearman correlation coefficient: " + str(question_ups.corr(question_answered_by_iAMA_host,
                                                                       method="spearman")))
    print("")
    print("----")


# Average means of different values
def average_means_of_values():
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
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_comments_total)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_comments_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_comments_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_comments_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_questions_total)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_questions_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_questions_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(thread_num_questions_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_comments_total)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_comments_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_comments_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_downs' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_comments_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_questions_total)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_questions_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_questions_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_downs' and 'thread_num_questions_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_downs' and 'thread_num_questions_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(thread_num_questions_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_ups.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_ups' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downs.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_comments_tier_x, method="spearman")))
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
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_num_questions_tier_x, method="spearman")))
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
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_comments_tier_x, method="spearman")))
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
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and 'thread_num_comments_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_num_questions_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> iama host repsonse time to comments
def relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread life span (until last comment) <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread life span (until last comment) <-> iama host repsonse time to questions
def relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread life span (until last comment) <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_comment.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> and iama host repsonse time to comments
def relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread life span (until last question) <-> and iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_question' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_question' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread life span (until last question) <-> iama host repsonse time to questions
def relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread life span (until last question) <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_life_span_until_last_comment' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_life_span_until_last_question.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> iama host repsonse time to comments
def relation_thread_reaction_time_comments_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread reaction time between comments <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> iama host repsonse time to questions
def relation_thread_reaction_time_comments_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread reaction time between comments <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> iama host repsonse time to comments
def relation_thread_reaction_time_questions_and_iama_host_response_time_to_comments():
    """Calculation of the correlation thread reaction time between questions <-> iama host repsonse time to comments

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
          " 'thread_average_response_to_comment_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_comment_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_comment_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_comment_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_comment_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
          " 'thread_average_response_to_comment_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_comment_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> iama host repsonse time to questions
def relation_thread_reaction_time_questions_and_iama_host_response_time_to_questions():
    """Calculation of the correlation thread reaction time between questions <-> iama host repsonse time to questions

    Args:
        -
    Returns:
        -
    """

    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
          " 'thread_average_response_to_question_time_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_question_time_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_question_time_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_average_response_to_question_time_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
          " 'thread_average_response_to_question_time_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_average_response_to_question_time_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
          " 'thread_average_response_to_question_time_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_average_response_to_question_time_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> amount of comments the iama host reacted to
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
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
          " 'thread_num_comments_answered_by_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_comments_answered_by_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_comments_answered_by_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_comments_answered_by_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
          " 'thread_num_comments_answered_by_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
          " 'thread_num_comments_answered_by_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between comments <-> amount of questions the iama host reacted to
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
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_total' and"
          " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_questions_answered_by_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_questions_answered_by_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_total.corr(
        thread_num_questions_answered_by_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_1' and"
          " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_comments_tier_x' and"
          " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_comments_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> amount of comments the iama host reacted to
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
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
          " 'thread_num_comments_answered_by_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_comments_answered_by_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_comments_answered_by_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_comments_answered_by_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
          " 'thread_num_comments_answered_by_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_comments_answered_by_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
          " 'thread_num_comments_answered_by_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_comments_answered_by_iama_host_tier_x, method="spearman")))
    print("")
    print("----")


# Correlation thread reaction time between questions <-> amount of questions the iama host reacted to
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
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_total' and"
          " 'thread_num_questions_answered_by_iama_host_total':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_questions_answered_by_iama_host_total)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_questions_answered_by_iama_host_total, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_total.corr(
        thread_num_questions_answered_by_iama_host_total, method="spearman")))
    print("")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_1' and"
          " 'thread_num_questions_answered_by_iama_host_tier_1':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_1.corr(
        thread_num_questions_answered_by_iama_host_tier_1, method="spearman")))
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_reaction_time_between_questions_tier_x' and"
          " 'thread_num_questions_answered_by_iama_host_tier_x':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x)))
    print("Kendall correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_reaction_time_between_questions_tier_x.corr(
        thread_num_questions_answered_by_iama_host_tier_x, method="spearman")))
    print("")
    print("----")

# Start that calculation

relation_question_upvotes_with_amount_of_questions_answered_by_iama_host()

average_means_of_values()

relation_thread_upvotes_with_amount_of_comments()
relation_thread_upvotes_with_amount_of_questions()

relation_thread_downvotes_with_amount_of_comments()
relation_thread_downvotes_with_amount_of_questions()

relation_thread_upvotes_and_iama_host_response_time_comments()
relation_thread_upvotes_and_iama_host_response_time_questions()

relation_thread_downvotes_and_iama_host_response_time_comments()
relation_thread_downvotes_and_iama_host_response_time_questions()

relation_thread_lifespan_to_last_comment_and_amount_of_comments()
relation_thread_lifespan_to_last_comment_and_amount_of_questions()

relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_comments()
relation_thread_lifespan_to_last_comment_and_iama_host_response_time_to_questions()

relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_comments()
relation_thread_lifespan_to_last_question_and_iama_host_response_time_to_questions()

relation_thread_lifespan_to_last_question_and_amount_of_comments()
relation_thread_lifespan_to_last_question_and_amount_of_question()

relation_thread_reaction_time_comments_and_iama_host_response_time_to_comments()
relation_thread_reaction_time_comments_and_iama_host_response_time_to_questions()

relation_thread_reaction_time_questions_and_iama_host_response_time_to_comments()
relation_thread_reaction_time_questions_and_iama_host_response_time_to_questions()

relation_thread_reaction_time_comments_and_amount_of_comments_the_iama_host_answered_to()
relation_thread_reaction_time_comments_and_amount_of_questions_the_iama_host_answered_to()

relation_thread_reaction_time_questions_and_amount_of_comments_the_iama_host_answered_to()
relation_thread_reaction_time_questions_and_amount_of_questions_the_iama_host_answered_to()
