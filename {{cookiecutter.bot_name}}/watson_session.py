import httpx


class AssistantSessionV2(object):
    def __init__(self, assistant_id, api_key,
                 base_url="https://api.eu-gb.assistant.watson.cloud.ibm.com" ,
                 version="2019-02-28"):
        self.session = httpx.Client(auth=("apikey", api_key))

        self.base_url = base_url
        self.version = version

        self.assistant_id = assistant_id
        self.session_id = self.create_session_id()

    def create_session_id(self):
        """
        Create a new session ID with the target assistant.

        Returns:
            Session ID (string).
        """
        request_url = f"{self.base_url}/v2/assistants/{self.assistant_id}/" \
                      f"sessions?version={self.version}"
        response = self.session.post(request_url)
        response.raise_for_status()
        return response.json()["session_id"]

    def send_message(self, text_input):
        """
        Send a message to the assistant and receive a full raw response.

        Arguments:
            text_input: (string) User input message.

        Returns:
            Assistant full response (dict).
        """
        request_url = f"{self.base_url}/v2/assistants/{self.assistant_id}/" \
                      f"sessions/{self.session_id}/message?version={self.version}"

        payload = {
            "input": {
                "text": text_input
            }
        }

        response = self.session.post(request_url, json=payload)

        response.raise_for_status()

        return response.json()

    def delete(self):
        """
        Delete current session.

        Returns:
            Returns True for success (bool).
        """
        request_url = f"{self.base_url}/v2/assistants/{self.assistant_id}/" \
                      f"sessions/{self.session_id}?version={self.version}"
        response = self.session.delete(request_url)
        response.raise_for_status()
        return True
