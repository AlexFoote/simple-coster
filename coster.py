import streamlit as st
import matplotlib.pyplot as plt
import copy

# ========= Parameters ==========

# ========= Model ==========


def run_period(months, current_cash, monthly_cost, monthly_income, current_month):
    cash_arr = [current_cash]
    income_arr = []
    cost_arr = []
    month_arr = [current_month]

    for month in range(months):
        current_cash -= monthly_cost
        current_cash += monthly_income

        cash_arr.append(current_cash)
        month_arr.append(current_month + month + 1)
        # income_arr.append(monthly_income)
        # cost_arr.append(monthly_cost)

    return cash_arr, month_arr


def run_simulation():
    # current_month = copy.deepcopy(starting_month)
    current_month = 0

    current_arr, current_month_arr = run_period(current_months, cash, current_monthly_cost, current_monthly_income, current_month)

    current_month += current_months

    transition_arr, transition_month_arr = run_period(transition_months, current_arr[-1], transition_monthly_cost, transition_monthly_income, current_month)

    new_arr, new_month_arr = run_period(new_months, transition_arr[-1], new_monthly_cost, new_monthly_income, current_month + transition_months)

    cash_arr = current_arr + transition_arr + new_arr

    return cash_arr, current_arr, transition_arr, new_arr, current_month_arr, transition_month_arr, new_month_arr


# ========= App ==========

cash = 50000

current_monthly_cost = 8000
transition_monthly_cost = 4000
new_monthly_cost = 6000

wind_up_cost = 14000

current_monthly_income = 3000
transition_monthly_income = 0
new_monthly_income = 0

current_months = 4
transition_months = 2
new_months = 6

starting_month = 3
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

step = 100

st.subheader("Cash")
misc_cols = st.columns(2)
with misc_cols[0]:
    cash = st.slider("Cash", 0, 100000, cash, step)
with misc_cols[1]:
    wind_up_cost = st.slider("Wind-up Cost", 0, 50000, wind_up_cost, step)

st.subheader("Costs")
cost_cols = st.columns(3)

with cost_cols[0]:
    current_monthly_cost = st.slider("Current Monthly Cost", 0, 10000, current_monthly_cost, step)
with cost_cols[1]:
    transition_monthly_cost = st.slider("Transition Monthly Cost", 0, 10000, transition_monthly_cost, step)
with cost_cols[2]:
    new_monthly_cost = st.slider("New Monthly Cost", 0, 10000, new_monthly_cost, step)

st.subheader("Income")
income_cols = st.columns(3)

with income_cols[0]:
    current_monthly_income = st.slider("Current Monthly Income", 0, 10000, current_monthly_income, step)
with income_cols[1]:
    transition_monthly_income = st.slider("Transition Monthly Income", 0, 10000, transition_monthly_income, step)
with income_cols[2]:
    new_monthly_income = st.slider("New Monthly Income", 0, 10000, new_monthly_income, step)

st.subheader("Months")
month_cols = st.columns(3)

with month_cols[0]:
    current_months = st.slider("Current Months", 0, 10, current_months)
with month_cols[1]:
    transition_months = st.slider("Transition Months", 0, 10, transition_months)
with month_cols[2]:
    new_months = st.slider("New Months", 0, 10, new_months)

cash_arr, current_arr, transition_arr, new_arr, current_month_arr, transition_month_arr, new_month_arr = run_simulation()

x_months = []
for i in range(len(cash_arr) + 1):
    x_months.append(months[starting_month])
    starting_month += 1
    if starting_month == 12:
        starting_month = 0

fig = plt.figure()

# plt.plot(cash_arr)
plt.plot(current_month_arr, current_arr)
plt.plot(transition_month_arr, transition_arr)
plt.plot(new_month_arr, new_arr)

plt.hlines(wind_up_cost, 0, len(cash_arr), colors="r", linestyles="dashed")
plt.hlines(0, 0, len(cash_arr), colors="r")

plt.xticks(range(len(x_months)), x_months)

plt.xlim([0, len(cash_arr) - 3])
plt.ylim([min(0, min(cash_arr)), max(cash_arr)])

plt.xlabel("Month")
plt.ylabel("Cash/£")

plt.grid()
plt.legend(["Current Model", "Transition", "New Model", "Wind-up Cost", "Zero Cash"])

st.pyplot(fig)
