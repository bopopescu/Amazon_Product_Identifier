# Amazon_Product_Identifier

ACM (Automated Content Management) is a HTTP REST service written in Flask (Python), which takes the text input from the user and finds all the products matching on Amazon.com for the matching query. It works in the following way:

1. Given the input query, the service first writes the query to the mongo database, and checks if any new thread is available to process the request. This is done to limit the no. of request processed at a particular time, since the requests are automatically bombarded externally by the SQS service.

2. If the thread is free, it picks up the query. It then executes the following functions:
    
    - get_candidates: This forms the candidate list of products by POS tagging the query and picking up Noun Compounds.
    - search: HTML parser for Amazon URL.
    - query_understanding: It searches each candidate on Amazon by calling search and assigns the most relevant category.
    - score_calculator: Calculates the score of for each candidate to be a product on Amazon.
