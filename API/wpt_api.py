import requests
import time

class WebPageTestAPI:
    def __init__(self, api_key, api_url, test_config):
        self.api_key = api_key
        self.api_url = api_url
        self.test_config = test_config

    def submit_api_and_get_response(self, url):
        try:
            params = {
                "url": url,
                "location": "Dulles:Chrome.FIOS",
                "f": "json",
                "runs": 2,
                "fvonly": 1,
                "lighthouse": 1,
            }
            headers = {"X-WPT-API-KEY": self.api_key}

            #response = requests.get(self.api_url, params=params, headers=headers, verify=False) #verify = False is equivalent to relaxedHTTPSValidation
            response = requests.get(self.api_url, params=params, headers=headers)  # verify = False is equivalent to relaxedHTTPSValidation

            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            response_json = response.json()
            self.test_config.log_comment(response_json)

            user_url = response_json["data"]["userUrl"]
            api_json_url = response_json["data"]["jsonUrl"]

            self.test_config.log_comment(f"WebPageTest API Run URL: {api_json_url}")
            self.test_config.log_comment(f"WebPageTest API User URL: {user_url}")

            #json_response = requests.get(api_json_url, params={"f": "json"}, verify=False)
            json_response = requests.get(api_json_url, params={"f": "json"})
            json_response.raise_for_status()
            json_response_data = json_response.json()

            while str(json_response_data["statusCode"]) != "200":
                self.test_config.wait_without_logging(30) #assume test_config has a wait_without_logging method
                #json_response = requests.get(api_json_url, params={"f": "json"}, verify=False)
                json_response = requests.get(api_json_url, params={"f": "json"})
                json_response.raise_for_status()
                json_response_data = json_response.json()

            self.test_config.log_comment(str(json_response_data["statusCode"]))

        except requests.exceptions.RequestException as e:
            print(f"Error during API request: {e}")
            # Handle the exception appropriately (e.g., log, raise, etc.)
        except KeyError as e:
            print(f"Error extracting data from JSON: {e}")
            # Handle the exception appropriately
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            # Handle other exceptions

class TestConfig: #example class, replace with your actual test config.
    def __init__(self):
        self.api_key = "99992029-356a-4717-b423-9750d5aa43f5"
        self.api_url = "https://webpagetest.org/runtest.php"

    def get_run_time_property(self, property_name):
        if property_name == "APIKey":
            return self.api_key
        elif property_name == "APIUrl":
            return self.api_url
        return None

    def log_comment(self, message):
        print(message)

    def wait_without_logging(self, seconds):
        time.sleep(seconds)



# Example usage:
if __name__ == "__main__":
    test_config = TestConfig() #replace with your implementation
    api_key = test_config.get_run_time_property("APIKey")
    api_url = test_config.get_run_time_property("APIUrl")

    wpt_api = WebPageTestAPI(api_key, api_url, test_config)
    wpt_api.submit_api_and_get_response("https://www.example.com")