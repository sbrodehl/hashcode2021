# \# Hash Code 2021 Practice Round

Solutions and code for the Practice Round of [Hash Code 2021](https://codingcompetitions.withgoogle.com/hashcode) **"Even More Pizza"**.  
The problem statement can be found [here](practice_problem.pdf).

#### Introduction

> Isn't it fun to share pizza with friends?
> But, sometimes you just don't have enough time to choose what pizza to order.
> Wouldn't it be nice if someone else chose for you?
>
> In an imaginary world...
>
> ![Practice Round Teaser](practice_round_teaser.png)
>
> _from [Problem statement for the Practice Round of Hash Code 2021](practice_round_2021_v3.pdf)_


#### Task
> Help the imaginary pizzeria choose the pizzas to deliver to Hash Code teams.
> And since we want everyone to enjoy their food, let's try to deliver to each team, as many different ingredients as we can.
> 
> _from [Problem statement for the Practice Round of Hash Code 2021](practice_round_2021_v3.pdf)_

#### Scoring

For each delivery, the score is the square of the total number of different ingredients of all the pizzas in the delivery.
The total score is the sum of the scores for all deliveries.

The final score of the round for the team will be the sum of the best scores for the individual data sets.

See the section on scoring in the [Problem statement for the Practice Round of Hash Code 2021](practice_round_2021_v3.pdf) for more details.

#### Input

The input files can be found in [`input/`](input)

| Data Set                                                             | Pizzas | Unique Ingredients | T2    | T3    | T4    |
| -------------------------------------------------------------------- | ------ | ------------------ | ----- | ----- | ----- |
| [a_example.in](input/a_example.in)                                   | 5      | 7                  | 1     | 2     | 1     |
| [b_little_bit_of_everything.in](input/b_little_bit_of_everything.in) | 500    | 10                 | 65    | 60    | 60    |
| [c_many_ingredients.in](input/c_many_ingredients.in)                 | 10000  | 10000              | 504   | 539   | 585   |
| [d_many_pizzas.in](input/d_many_pizzas.in)                           | 100000 | 100                | 1696  | 3661  | 2742  |
| [e_many_teams.in](input/e_many_teams.in)                             | 100000 | 100                | 39748 | 49195 | 29832 |

## Scores

Overall **725,282,679** points.

#### A – example

Our submission scored **74** points.

#### B - little bit of everything

Our submission scored **5,303** points.

#### C - many ingredients

Our submission scored **706,624,573** points.

#### D - many pizzas

Our submission scored **7,863,102** points.

#### E - many teams

Our submission scored **10,789,627** points.
