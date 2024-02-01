import pandas as pd
import plotly.express as px


def do_plot():
    # Read the CSV file into a Pandas DataFrame
    file_path = '/Users/mbaker/Documents/PycharmProjects/python-training/aviemore_data.csv'
    df = pd.read_csv(file_path, delimiter=';', parse_dates=['Time'])

    # Create a basic line plot structure
    fig = px.line(title='Line Plot of Aviemore data over Time')

    # Add a scatter plotter to the line graph for the data you wish to see from above dataframes
    # selecting what you want on each axis
    fig.add_scatter(x=df["Time"], y=df["air-temp"], name="Air Temp")

    fig.update_xaxes(title_text='Date and Time')
    fig.update_yaxes(title_text='Degrees C')

    # Show the plot
    fig.show()


# Run the do_plot() function
if __name__ == "__main__":
    do_plot()
