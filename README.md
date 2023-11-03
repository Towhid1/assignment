# Assignment
Task 1 and 2 done. Here I added how to run it and test it. Both endpoints take GET request.
Task 1 endpoint : `http://127.0.0.1:8000/coolest_ten`
Task 2 endpoint : `http://127.0.0.1:8000/predict/2023-12-10`
In case of prediction endpoint you need to provide date in this format `"YYYY-MM-DD"` example : `2023-12-10`.

## How to run:

1. install requirements
    ```bash
    pip install -r requirements.txt
    ```
2. Run fastAPI server:
    ```bash
    uvicorn api:app --reload
    ```

## Test API:
1. Create a new terminal.
2. Run test code.
   ```bash
   python test_api.py
   ```
    Output will be something like this :
    ```python
    api response : {'data': {"Cox's Bazar": 29.86021505376344, 'Barguna': 30.897849462365592, 'Chandpur': 30.91182795698925, 'Bhola': 30.933333333333334, 'Patuakhali': 31.08817204301075, 'Barishal': 31.12688172043011, 'Chattogram': 31.16021505376344, 'Noakhali': 31.162365591397847, 'Feni': 31.231182795698924, 'Thakurgaon': 31.24838709677419}}

    >> 1st task avg execution_time : 0.0028987884521484374 sec
    api response : {'date': '2023-11-03', 'predicted_temperature': 27.625208333333354, 'unit': '°C'}

    >> 2nd task execution_time : 0.005758976936340332 sec
```
