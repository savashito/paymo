# Table of Contents

1. [Challenge Summary] (README.md#challenge-summary)
2. [Research for implementation] (README.md#research-for-implementation)
3. [Running Implementation] (README.md#running-implementation)
4. [Description of Data] (README.md#description-of-data)

##Challenge Summary

PayMo allows users to easily request and make payments to other PayMo users. 
This repo is for preventing fraudulent payment requests from untrusted users. 

##Research for implementation

Because PayMo has hundreds of thousands of users and thousands of transactions, an efficient and smart implementation is necessary.
Each user is represented as a node in an undirected graph. Each edge that connects nodes in between represents a transaction between two users.
The graph is assumed to be sparse meaning that there are way more users (nodes) than transactions (edges).
Feature 1, 2 and 3 could be implemented with O(1) running time by implementing an all pairs shortest path. with a preprocessing time of:
O(mn) where n is the number of nodes (users) and m is the number of edges (transactions) [1]. 
The problem of this approach is the extra memory required to store the table which is impractical for millions of users of paymo.
Because we know that users usually only buy from friends (the graph is sparse) we can use this knowledge to our advantage.
Instead of preprocessing the data with the all pair shortest path, I work directly with the graph and perform a breath first search.
The search is stopped when all the nodes a distance t from the start node have been explored. This algorithm has a complexity of O(k^t) 
where k is the average number of edges a node has and t is the distance to explore (degrees of separation). 
Because the graph is assume to be sparse k is very small, and because we are at most checking for 3 degrees of separation, t is at most 3.
Because we are not using extra memory to store distances in a table it turns out to be in practice much faster that O(1) lookup from [1].

[1] Chan, Timothy M. "All-pairs shortest paths for unweighted undirected graphs in o (mn) time." ACM Transactions on Algorithms (TALG) 8.4 (2012): 34.

### Running implementation

This follows the convention provided by the instructions.
To run:
./run.sh
to test:
./insight_testsuite/run_test.sh
###Feature 1
When anyone makes a payment to another user, they'll be notified if they've never made a transaction with that user before.

* "unverified: You've never had a transaction with this user before. Are you sure you would like to proceed with this payment?"

###Feature 2
The PayMo team is concerned that these warnings could be annoying because there are many users who haven't had transactions, but are still in similar social networks. 

For example, User A has never had a transaction with User B, but both User A and User B have made transactions with User C, so User B is considered a "friend of a friend" for User A.

For this reason, User A and User B should be able to pay each other without triggering a warning notification since they're "2nd degree" friends. 

<img src="./images/friend-of-a-friend1.png" width="500">

To account for this, PayMo would like you to also implement this feature. When users make a payment, they'll be notified of when they're not "a friend of a friend".

* "unverified: This user is not a friend or a "friend of a friend". Are you sure you would like to proceed with this payment?"


###Feature 3
More generally, PayMo would like to extend this feature to larger social networks. Implement a feature to warn users only when they're outside the "4th degree friends network".

<img src="./images/fourth-degree-friends2.png" width="600">

In the above diagram, payments have transpired between User

* A and B 
* B and C 
* C and D 
* D and E 
* E and F

Under this feature, if User A were to pay User E, there would be no warning since they are "4th degree friends". 

However, if User A were to pay User F, a warning would be triggered as their transaction is outside of the "4th-degree friends network."

(Note that if User A were to pay User C instead, there would be no warning as they are "2nd-degree" friends and within the "4th degree network") 

###Other considerations and optional features

It's critical that these features don't take too long to run. For example, if it took 5 seconds when you make a payment to check whether a user is in your network, that would ruin your user experience and wouldn't be acceptable.


While PayMo is a fictional company, the dataset is quite interesting -- it's inspired by a real social network, includes the time of transaction, and the messages come from real Venmo transactions -- so feel free to implement additional features that might be useful to prevent fraudulent payments.

##Details of implementation

[Back to Table of Contents] (README.md#table-of-contents)

With this coding challenge, you should demonstrate strong understanding of computer science fundamentals. We won't be wowed by your knowledge of various available software libraries but will be impressed by your ability to pick and use the best data structures and algorithms for the job. 

We're looking for clean, well-thought-out code that correctly implements the desired features in an optimized way.

We also want to see how you use your programming skills to solve business problems. At a minimum, you should implement the three required features but feel free to expand upon this challenge or add other features you think would prevent fraud and further business goals. Be sure to document these add-ons so we know to look for them. 

###Input

Ideally, payment data would come from a real-time, streaming API, but we don't want this challenge to focus on the relatively uninteresting "DevOps" of connecting to an API.

As a result, you may assume that collecting the payments has been done for you and the data resides in two comma-delimited files in the `paymo_input` directory. 

The first file, `batch_payment.csv`, contains past data that can be used to track users who have previously paid one another. These transactions should be used to build the initial state of the entire user network.

Data in the second file, `stream_payment.csv` should be used to determine whether there's a possibility of fraud and a warning should be triggered.

You should assume that each new line of `stream_payment.csv` corresponds to a new, valid PayMo payment record -- regardless of being 'unverified' -- and design your program to handle a text file with a large number of payments. 

###Output

Your code should process each line in `stream_payment.csv` and for each payment, output a line containing one of two words, `trusted` or `unverified`. 

`trusted` means the two users involved in the transaction have previously paid one another (when implementing Feature 1) or are part of the "friends network" (when implementing Feature 2 and 3).

`unverified` means the two users have not previously been involved in a transaction (when implementing Feature 1) or are outside of the "friends network" (when implementing Features 2 and 3)

The output should be written to a text file in the `paymo_output` directory. Because we are asking you to implement a minimum of three features, your program should output to at least three text files in the `paymo_output` directory. 

Each output file should be named after the applicable feature you implemented (i.e., `output1.txt`, `output2.txt` and `output3.txt`)

For example, if there were 5 lines of transactions in the `stream_payment.csv`, then the following `output1.txt` file for Feature 1 could look like this: 

	trusted
	trusted
	unverified
	unverified
	trusted


##Description of Data

[Back to Table of Contents] (README.md#table-of-contents)

The `batch_payment.csv` and `stream_payment.csv` input files are formatted the same way.

As you would expect of comma-separated-value files, the first line is the header. It contains the names of all of the fields in the payment record. In this case, the fields are 

* `time`: Timestamp for the payment 
* `id1`: ID of the user making the payment 
* `id2`: ID of the user receiving the payment 
* `amount`: Amount of the payment 
* `message`: Any message the payer wants to associate with the transaction

Following the header, you can assume each new line contains a single new PayMo payment record with each field delimited by a comma. In some cases, the field can contain Unicode as PayMo users are fond of placing emojis in their messages. For simplicity's sake, you can choose to ignore those emojis.

For example, the first 10 lines (including the header) of `batch_payment.csv` or `stream_payment.csv` could look like: 

	time, id1, id2, amount, message
	2016-11-02 09:49:29, 52575, 1120, 25.32, Spam
	2016-11-02 09:49:29, 47424, 5995, 19.45, Food for 🌽 😎
	2016-11-02 09:49:29, 76352, 64866, 14.99, Clothing
	2016-11-02 09:49:29, 20449, 1552, 13.48, LoveWins
	2016-11-02 09:49:29, 28505, 45177, 19.01, 🌞🍻🌲🏔🍆
	2016-11-02 09:49:29, 56157, 16725, 4.85, 5
	2016-11-02 09:49:29, 25036, 24692, 20.42, Electric
	2016-11-02 09:49:29, 70230, 59830, 19.33, Kale Salad
	2016-11-02 09:49:29, 63967, 3197, 38.09, Diner
	
