# Car Number Plate Detection Project

This project is a car number plate detection system created using YOLOv10 and PaddleOCR. It allows you to detect and extract license plate information from images or video streams.

## Getting Started

To run this project, follow the steps below:

1. Clone this GitHub repository to your local machine and create a virtual environment with Python 3.10.11.

2. Change the directory to `yolov10`:
    ```
    cd yolov10
    ```

3. Install all the required dependencies from the `requirements.txt` file:
    ```
    pip install -r requirements.txt
    ```

4. Run the `sql_database.py` file to create a SQL database named `licensePlate.db`:
    ```
    python sql_database.py
    ```

5. Finally, run the `anpr.py` file to start the car number plate detection system:
    ```
    python anpr.py
    ```

Make sure you have the necessary weights and configuration files for YOLOv10 and PaddleOCR in the appropriate directories.

## License

