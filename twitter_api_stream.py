import requests
import os
import json
import pandas as pd


# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
with open('myconfig.json','r') as fh:
    config = json.load(fh)
os.environ["BEARER_TOKEN"] = config["BEARER_TOKEN"]

bearer_token = os.environ.get("BEARER_TOKEN")
print(bearer_token)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2FilteredStreamPython"
    return r


def get_rules():
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream/rules", auth=bearer_oauth
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot get rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('get_rules() response:')    
    print(json.dumps(response.json()))
    return response.json()


def delete_all_rules(rules):
    if rules is None or "data" not in rules:
        return None

    ids = list(map(lambda rule: rule["id"], rules["data"]))
    payload = {"delete": {"ids": ids}}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload
    )
    if response.status_code != 200:
        raise Exception(
            "Cannot delete rules (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    print('delete_all_rules(rules) response:')    
    
    (json.dumps(response.json()))


def set_rules(rules):
    # You can adjust the rules if needed 
    # if the passed in rules is null, then 
    if rules is None:
        sample_rules = [
            {"value": "dog has:images", "tag": "dog pictures"},
            {"value": "cat has:images -grumpy", "tag": "cat pictures"},
        ]
    else:
        print('assigning specified rules')
        sample_rules = rules
    payload = {"add": sample_rules}
    response = requests.post(
        "https://api.twitter.com/2/tweets/search/stream/rules",
        auth=bearer_oauth,
        json=payload,
    )
    if response.status_code != 201:
        raise Exception(
            "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
        )
    print('set_rules(delete) response:')      
    print(json.dumps(response.json()))


def get_stream(set):
    
    response = requests.get(
        "https://api.twitter.com/2/tweets/search/stream", auth=bearer_oauth, stream=True,
    )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Cannot get stream (HTTP {}): {}".format(
                response.status_code, response.text
            )
        )
    all_responses = []
    count = 0
    for response_line in response.iter_lines():
        if count >= 10:
            break;

        if response_line:
            # get the current tweet json
            json_response = json.loads(response_line)    
            
            # Keep count of the processed tweets
            count = count + 1 
            # initialize a dict to hold the current tweet
            tweet = {}

            # extract the data from the tweet and store it in our variable
            tweet['id'] = json_response["data"]["id"]
            tweet["text"] = json_response["data"]["text"]
            tweet["tag"] = json_response["matching_rules"][0]["tag"]
            # add the tweet to our response list
            all_responses.append(tweet)

            #print(json.dumps(json_response, indent=4, sort_keys=True))
            print(count)
    #take the streamed responses, put it into a dataframe and print the dataframe        
    #df = pd.DataFrame(all_responses)
    #print(df)

    #return the streamed responses         
    return(all_responses)


            

def main():
    rules = get_rules()
    delete = delete_all_rules(rules)
    set = set_rules(delete)
    get_stream(set) 
    


#if __name__ == "__main__":
    main()

