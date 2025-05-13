# EDA
import pandas as pd
client_data = pd.read_csv("client_data.csv")
print("Client data shape", client_data.shape)
client_data.head()

deposit_data = pd.read_csv("deposit_data.csv")
print("Deposit data shape", deposit_data.shape)
deposit_data.head()

calendar_data = pd.read_csv("calendar_data.csv")
print("Calendar data shape", calendar_data.shape)
calendar_data.head()

# step 1.
df = client_data.merge(deposit_data, on="client_id")
# step 2.
df = df.merge(calendar_data, left_on="deposit_date", right_on="gregorian_date", copy=False)
print(df)

df.drop(columns="gregorian_date", inplace=True)
df

df["client_geographical_region"].value_counts()
df["client_residence_status"].value_counts()
df["client_age"].describe()
_ = client_data[["client_age"]].plot(kind="hist")
calendar_data["month_name"].value_counts()
df["deposit_date"].min(), df["deposit_date"].max()
df["deposit_type"].value_counts()
df["deposit_cadence"].value_counts()
# convert the date column type to a datetime object
df["deposit_date"] = pd.to_datetime(df["deposit_date"])

from matplotlib import pyplot as plt

plt.rcParams["figure.figsize"] = (10, 7)
deposit_amount_by_month = df.groupby(by=df["month_name"])["deposit_amount"].sum()

print(deposit_amount_by_month)

_ = plt.plot(deposit_amount_by_month)
_ = plt.title("Deposit amount per month")
_ = plt.ylabel("Deposit amount")
_ = plt.xlabel("Month")

number_of_deposits_by_month = df.groupby(by=df["month_name"]).size()

_ = plt.plot(number_of_deposits_by_month)

_ = plt.title("Number of deposits per month")
_ = plt.ylabel("Number of deposits")
_ = plt.xlabel("Month")

deposit_amount_by_type = df.groupby(by=df["deposit_type"])["deposit_amount"].sum()


_ = plt.bar(deposit_amount_by_type.index, deposit_amount_by_type)

_ = plt.title("Deposit amount by type")
_ = plt.ylabel("Deposit amount")
_ = plt.xlabel("Deposit type")

deposit_amount_by_cadence = df.groupby(by=df["deposit_cadence"])["deposit_amount"].sum()


_ = plt.bar(deposit_amount_by_cadence.index, deposit_amount_by_cadence)

_ = plt.title("Deposit amount by cadence")
_ = plt.ylabel("Deposit amount")
_ = plt.xlabel("Deposit cadence")

tmp_df = df.groupby(by=[df["deposit_cadence"], df["month_name"]])["deposit_amount"].sum()

ax = tmp_df.unstack(level=0).plot(kind='line')

ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and cadence")
plt.tight_layout()

tmp_df = df.groupby(by=[df["client_geographical_region"], df["month_name"]])["deposit_amount"].sum()

ax = tmp_df.unstack(level=0).plot(kind='line')

ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and region")
plt.tight_layout()

tmp_df = df.groupby(by=[df["client_residence_status"], df["month_name"]])["deposit_amount"].sum()

ax = tmp_df.unstack(level=0).plot(kind='line')

ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and cadence")
plt.tight_layout()

'''
Question 1
Provide a quantitative assessment of whether the marketing campaign was successful. How and why did you choose your specific success metric(s)?

This question can already be answered from the plots in the previous sections, especially the ones that show the deposit amount per month. We know that the ad campaign was running during the 3rd month of our data set (which is Month 8 in the current year, i.e., August). A huge spike can be noticed in the line plot titled "Deposit amount per month" between months 7 & 8, i.e., while the campaign was running. Since then, the deposit amount has been slowly decreasing but has remained at very higher levels than before the campaign. To put this into numbers:

During the month the campaign was running, Freedom Debt Relief received almost $10 million dollars increase in deposit amounts than previous months

In the months following the campaign, the total deposit amount starts to slowly decrease, but is still at higher levels than before the ad campaign: $8.5 million in the month immediately following the campaign, and $8 million in the last month of the data

The cost of the campaign was $5 million, and the incurred deposit amount increased by a total of $26.5 million. A quick Google search for "freedom debt relief pricing" reveals an 18-25% fee incurred by the company for its services. We would assume that this is based on the residence status and the deposit cadence, but neither the data nor the task description provide any estimate or hint to this. Assuming the lowest, 18% fee for all clients, we observe an increase in profits to $4.77 million (26.5M * 18%). While this looks like a loss of $230K for the campaign, it is important to note that the trend shows this would have been much higher without the campaign, and it is very unlikely that the minimum fee is applied to all clients, so this number should be treated as the most pessimistic estimate.
Another quantitative assessment that we can make is to see the number of new clients that were brought in during and after the market campaign.
'''
clients_before_campaign = df[(df["month_name"] == "Month 1")
                           | (df["month_name"] == "Month 2")]["client_id"].unique()
clients_before_campaign.shape

clients_before_campaign = df[(df["month_name"] == "Month 1")
                           | (df["month_name"] == "Month 2")]["client_id"].unique()
clients_before_campaign.shape

clients_after_campaign = df[(df["month_name"] == "Month 4")
                          | (df["month_name"] == "Month 5")]["client_id"].unique()
clients_after_campaign.shape

'''
Question: How many new clients were acquired while the ad campaign was running?

A new client is one that has made his first deposit while the campaign was running.
'''

#len(set(clients_during_campaign).difference(set(clients_before_campaign)))

#Question: How many after the campaign?

#len(
#    set(clients_after_campaign).difference(set(clients_before_campaign).union(set(clients_during_campaign)))
#)

temp_df = df.groupby(by=[df["deposit_type"], df["month_name"]])["deposit_type"].count()

ax = temp_df.unstack(level=0).plot(kind='line')

ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and type")
plt.tight_layout()

'''
As expected, this plot very closely matches the distributions of the plots in the analysis section. During the ad campaign, the number of actual and scheduled deposits increases for 25%, or 10K transactions, and while it gradually decreases in the next two months, it still remains very high, at above 50K deposits per type each, while the pre-campaign levels were at around 40K.

Question 2
Based on the provided data, how would you recommend campaign strategy be adjusted in the future to improve performance?

Almost all of the plots show similar patterns through time and it is difficult to make any suggestions.

One thing that could be explored more is targeted marketing. We notice that most of the people in the data are middle-aged (40-60 years) and most of them are home owners. We can observe this in the age histogram and the count per residence status in the EDA section.

In the next plot, we will show the deposit amount changing through time and age group (age divided by 10).
'''


def discretize_age(row):
    return int(row.client_age / 10)

dff = df.copy(deep=True)
dff["age_group"] = dff.apply(discretize_age, axis=1)
dff

tmp_df = dff.groupby(by=[dff["age_group"], dff["month_name"]]).size()

ax = tmp_df.unstack(level=0).plot(kind='line')

ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and age-group")
plt.tight_layout()

'''
We observe big increase in middle-aged customers and little to no increase in very young or very old customers. In the following analysis, we focus on the middle-aged sub-group of customers. We think that better engagement with them could result in more deposits.

'''


df_q2 = df[(df["client_residence_status"] == "Own") 
         & (df["client_age"] <= 60) 
         & (df["client_age"] >= 40)]
df_q2.shape

temp_df = df_q2.groupby(by=[df_q2["deposit_type"], df_q2["month_name"]])["deposit_type"].count()

ax = temp_df.unstack(level=0).plot(kind='line')
ax.set_xlabel("Month")
ax.set_ylabel("Deposit amount")
ax.set_title("Deposit amount per month and type")
plt.tight_layout()

extra_deposit_df_q2 = df_q2[df_q2["deposit_cadence"] == "Extra"]["deposit_amount"].sum()
extra_deposit_df = df[df["deposit_cadence"] == "Extra"]["deposit_amount"].sum()

extra_deposit_df_q2 / extra_deposit_df

df_q2.shape[0] / df.shape[0]

df[df["deposit_cadence"] == "Extra"]["client_geographical_region"].value_counts()

df[df["deposit_cadence"] == "Extra"]["client_residence_status"].value_counts()

df[df["deposit_cadence"] == "Extra"]["deposit_type"].value_counts()

df[df["deposit_cadence"] == "Extra"]["month_name"].value_counts()

'''
Some key points based on the previous cells:

Most extra deposits are observed in the West region as expected. This distribution closely matches the distribution of other deposit types as well
Clients who own their residence are approx. 2.33 times as likely to deposit extra amount than clients who rent their residence
Most extra deposits are observed in Month 3, when the campaign was running. Post-campaign numbers for extra deposits are 33% higher than pre-campaign.
Question 3
How do you think campaign performance would have changed if we did not run the campaign in Month 3, but instead postponed it until month 6? Provide an incremental number versus your result in Question #1.

One way we can simulate the postponement of the campaign is to "postpone" the deposits coming from new clients who were acquired during the third month. We (strongly) assume that the clients who made their first deposit in the third month in the data set are acquired due to the campaign; this is not necessarily correct, but for the sake of the exercise we can treat it as if it were.

Technically speaking, this means we should take the following steps.

Identify which clients made their first deposit in the third month, i.e., were acquired because of the campaign. (we have already done that in previous sections)
Postpone their deposits until after the fifth month, i.e., add exactly three months to the date of their deposit.
Re-run the same analyses from Question 1 and make summarise the difference in the results.
'''
df_copy = df.copy(deep=True)
#new_clients = set(clients_during_campaign).difference(set(clients_before_campaign))

import datetime
'''
def simulate_campaign_postponement(row):
    if row.client_id in new_clients:
        row.deposit_date = pd.to_datetime(row.deposit_date) + datetime.timedelta(days=90)
        if row.month_name == "Month 3":
            row.month_name = "Month 6"
        elif row.month_name == "Month 4":
            row.month_name = "Month 7"
        elif row.month_name == "Month 5":
            row.month_name = "Month 8"
    else:
        row.deposit_date = pd.to_datetime(row.deposit_date)
    return row

df_copy = df_copy.apply(func=simulate_campaign_postponement, axis=1)

df_copy["deposit_date"].max()

deposit_amount_by_month = df_copy.groupby(by=df_copy["month_name"])["deposit_amount"].sum()

print("Deposit amount per month", deposit_amount_by_month)

_ = plt.plot(deposit_amount_by_month)
_ = plt.title("Deposit amount by month")
_ = plt.ylabel("Deposit amount")
_ = plt.xlabel("Month")

avg_monthly_deposit = (df_copy.groupby(by=df_copy["month_name"])["deposit_amount"].sum()).mean()

avg_monthly_deposit

deposit_amount_by_month = df_copy.groupby(by=df_copy["month_name"])["deposit_amount"].sum()


deposit_amount_by_month.at["Month 6"] += avg_monthly_deposit
deposit_amount_by_month.at["Month 7"] += avg_monthly_deposit
deposit_amount_by_month.at["Month 8"] += avg_monthly_deposit

print(deposit_amount_by_month)


_ = plt.plot(deposit_amount_by_month)

_ = plt.title("Deposit amount by month")
_ = plt.ylabel("Deposit amount")
_ = plt.xlabel("Month")
'''
'''
The simulation shows quite an increase in deposits. Following are some key points to summarise the difference from the answer provided in Question 1.

During the month the campaign was running, Freedom Debt Relief received almost $2.5 million increase in deposit amounts than previous months, compared to $10 million in Question 1.

In the month following the campaign, the total deposit amount continues to increase to reach its maximum at $33 million. In the last month, it drops to $31 million but remains on a higher level than pre-campaign.

The cost of the campaign was $5 million, and the incurred deposit amount increased by a total of $8 million. In Question 1 this number was much higher: $26 million, and we determined that that was borderline profitable. So, $8 million is much lower, and we conclude that postponing the campaign would have not been the right choice.
'''