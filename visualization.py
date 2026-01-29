import plotly.express as px


class Visualizer:
    """
    A class to help you visualize your data with various plot types.
    
    Attributes
    ----------
    data : pandas.DataFrame
        The dataset to visualize

    Methods
    -------
    bar_plot(x_col)
        Creates a bar plot
    histogram(h_col, )
        Creates a histogram
    box_plot(b_col)
        Creates a box plot
    pie_plot(p_col)
        Creates a pie chart
    heatmap_plot(x_col=None, y_col=None)
        Creates a heatmap
    scatter_plot(first_col , second_col)
        Creates a scatter plot
    """
    def __init__(self , data):
        self.data = data

    def bar_plot(self , x_col):
        fig = px.bar(
            self.data ,
            x= x_col ,
            title= f"Bar plot of {x_col}" ,
            width=600 ,
            height= 400
        )
        # Customize layout
        fig.update_layout(
            title_x=0.5,  # Center the title
        )

        # Customize bars
        fig.update_traces(
            marker_color='lightblue',  # Single color like seaborn default
            marker_line_color='darkblue',
            marker_line_width=1.5,
            opacity=0.8
        )

        fig.show()

    def hist_plot(self , h_col , range =None):
        fig = px.histogram(
            self.data , 
            h_col ,
            nbins= 50 ,
            title= f"Distribution of {h_col}" ,
            width=600 ,
            height= 400
        )

        fig.show()

    def box_plot (self , b_col ):
        fig = px.box(
            self.data , 
            b_col ,
            title= f"Box plot of {b_col}"
        )

        fig.show()

    def pie_plot(self , p_col):
        fig = px.pie (
            self.data ,
            p_col ,
            color_discrete_sequence=px.colors.qualitative.Set2

        )

        fig.show()
    
    def heatmap_plot(self ):
        fig = px.density_heatmap(
            self.data ,
            title="The correclation between columns and other"
        )

        fig.show()

    def scatter_plot(self , col1 , col2):
        fig = px.scatter(
        self.data , 
        x= col1 ,
        y = col2 ,
        title= f"{col1} VS {col2}"
        )
        fig.show()

