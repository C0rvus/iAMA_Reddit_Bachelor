# Sources used:
# 1. (02.04.2016 @ 18:30) -
# http://www.scipy-lectures.org/packages/statistics/index.html
#
# http://stackoverflow.com/questions/15392730/in-python-is-it-possible-to-escape-newline-characters-when-printing-a-string


# By looking at all generated csv files we can use the following parameters for calculating various things:
# [some depend on the tier they have been calculated from]
# ----
# Question answered by iAMA host (bool),
# Question author,
# Question birth time since thread started, (only available at top / worst 1000 calculation)
# Question creation time stamp,
# Question id,
# Question parents id
# Question text,
# Question tier (1 or other)
# Question ups,
# Thread amount of comments,
# Thread amount of questions,
# Thread amount questions answered by iAMA host,
# Thread author,
# Thread average comment reaction time (sec),
# Thread average response time from iAMA host (sec),
# Thread downs,
# Thread id,
# Thread life span (sec),
# Thread text,
# Thread ups,
# Year
# ----


#
# What csv data do we need ?
# How do we have to prepare them ?
# Threads:
# Questions: We merge them by hand
import pandas


thread_information = pandas.read_csv(
    'd_create_Big_CSV_2009_until_2016_BIGDATA_ALL'
    , sep=',', na_values=".")

thread_average_lifespan = thread_information['Thread life span (sec)']
thread_average_mean_comment_reaction_time = thread_information['Thread average comment reaction time (sec)']
thread_upvotes = thread_information['Thread ups']
thread_downvotes = thread_information['Thread downs']
thread_num_comments = thread_information['Thread comments']



def average_means_of_values():
    print("----")
    print("Calculating arithmetic average means here")
    print("")
    print("Average arithmetic mean - thread upvotes: " + str(thread_upvotes.mean()))
    print("Average arithmetic mean - thread downvotes: " + str(thread_downvotes.mean()))
    print("Average arithmetic mean - thread life span in seconds: " + str(thread_average_lifespan.mean()))
    print("Average arithmetic mean - comments per thread: " + str(thread_num_comments.mean()))
    print("Average arithmetic mean - comment reaction time of everybody: " +
          str(thread_average_mean_comment_reaction_time.mean()))
    print("----")


def relation_thread_upvotes_with_amount_of_comments():
    print("")
    print("----")
    print("Calculating correlation between 'thread_upvotes' and 'amount_of_comments':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_upvotes.corr(thread_num_comments)))
    print("Kendall correlation coefficient: " + str(thread_upvotes.corr(thread_num_comments, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_upvotes.corr(thread_num_comments, method="spearman")))
    print("----")


def relation_thread_downvotes_with_amount_of_comments():
    print("")
    print("----")
    print("Calculating correlation between 'thread_downvotes' and 'amount_of_comments':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments)))
    print("Kendall correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments, method="spearman")))
    print("----")
    print("")
    print("----")
    print("Calculating correlation between 'thread_downvotes' and 'amount_of_comments':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments)))
    print("Kendall correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_downvotes.corr(thread_num_comments, method="spearman")))
    print("----")


def relation_thread_average_reaction_time_with_thread_life_span():
    print("")
    print("----")
    print("Calculating correlation between 'thread_average_mean_comment_reaction_time' and 'thread_average_lifespan':")
    print("")
    print("Pearson correlation coefficient: " + str(thread_average_mean_comment_reaction_time.corr
                                                    (thread_average_lifespan)))
    print("Kendall correlation coefficient: " + str(thread_average_mean_comment_reaction_time.corr
                                                    (thread_average_lifespan, method="kendall")))
    print("Spearman correlation coefficient: " + str(thread_average_mean_comment_reaction_time.corr
                                                     (thread_average_lifespan, method="spearman")))
    print("----")



# average_means_of_values()
# relation_thread_upvotes_with_amount_of_comments()
# relation_thread_downvotes_with_amount_of_comments()
relation_thread_average_reaction_time_with_thread_life_span()
# relation_question_upvotes_with_question_tier()
