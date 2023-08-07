from flask import Flask, render_template
import pandas as pd
import folium
from folium import IFrame

app = Flask(__name__)


@app.route('/')
def map():
    def create_dash_html():
        dash_html = """
        <!DOCTYPE html>
<html>
<head>
    <title>Informações bike santos</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            color: #333;
            margin: 0;
        }

        h1 {
            text-align: center;
            margin-bottom: 20px;
        }

        ul {
            list-style: none;
            padding: 0;
            display: flex;
            justify-content: center;
            margin-bottom: 30px;
        }

        li {
            margin-right: 15px;
        }

        li a {
            text-decoration: none;
            color: #555;
            padding: 6px 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
            transition: background-color 0.3s ease;
        }

        li a:hover {
            background-color: #ddd;
        }

        #chart-container {
            display: flex;
            justify-content: center;
            margin-top: 30px;
        }

        .leaflet-popup-content-wrapper {
            max-width: 300px;
            max-height: 200px;
            overflow-y: auto;
            padding: 15px;
        }

        .leaflet-popup-content {
            margin: 0;
        }

        .leaflet-popup-content h2 {
            font-size: 18px;
            margin-bottom: 10px;
        }

        .leaflet-popup-content p {
            margin: 0;
        }

        .button-container {
            text-align: center;
            margin-top: 30px;
        }

        .button-container button {
            display: inline-block;
            background-color: #555;
            border: none;
            color: #fff;
            padding: 8px 16px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 14px;
            transition: background-color 0.3s ease;
        }

        .button-container button:hover {
            background-color: #333;
        }
    </style>
</head>
<body>
    <h1>Informações bike santos</h1>
    <ul>
        <li><a href="#" onclick="showGraph('data2')">Mais utilizadas</a></li>
        <li><a href="#" onclick="showGraph('data1')">Retiradas</a></li>
    </ul>

    <div id="chart-container"></div>

    <div class="button-container">
        <button onclick="openExternalDashboard()">Mais informações</button>
    </div>

    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <script>
        function showGraph(dataType) {
            const data1 = {
                x: [2018, 2019, 2020, 2021, 2022],
                y: [543906, 595938, 373419, 335322, 277419],
                type: 'bar'
            };

            const data2 = {
                labels: ['Gonzaga', 'Emissário', 'Fonte do sapo'],
                values: [21507, 16084, 15243],
                type: 'pie'
            };

            let data;
            let layout;
            

            if (dataType === 'data1') {
                data = [data1];
                layout = {
                    title: "Quantidade de retiradas",
                    xaxis: {
                        title: ''
                    },
                    yaxis: {
                        title: ''
                    }
                };
            } else if (dataType === 'data2') {
                data = [data2];
                layout = {
                    title: "Linhas mais utilizadas em 2022",
                };
            }

            Plotly.newPlot('chart-container', data, layout);
        }

        function openExternalDashboard() {
            window.open("http://127.0.0.1:8050/", "_blank");
        }
    </script>
</body>
</html>


        """
        return dash_html

    def open_dash_menu(lat, lon):
        iframe = IFrame(html=create_dash_html(), width=275, height=450)
        popup = folium.Popup(iframe, max_width=500)
        return folium.Marker(
            location=[lat, lon],
            icon=folium.Icon(icon="fa-bicycle", color="green", icon_color="white", prefix="fa"),
            popup=popup,
            tooltip=creche['Name'],


        )

    pontobike = pd.read_csv('bikes.csv')
    pontobike = pontobike.drop(columns=['Unnamed: 0', 'Type'])
    pontobike.rename(columns={'NAME': 'Name', 'GEOCODE_INPUT': 'Retiradas', 'LAT': 'Lat', 'LNG': 'Lng'}, inplace=True)
    pontobike.dropna(inplace=True)
    pontobike = pontobike.loc[(pontobike['Lat'] < -22) & (pontobike['Lat'] > -24) & (pontobike['Lng'] < -45) & (
            pontobike['Lng'] > -47), :]

    m = folium.Map(
        location=[-23.967658634272027, -46.310145462792015],
        tiles='cartodbpositron',
        zoom_start=13,
        zoom_control=False
    )

    for index, creche in pontobike.iterrows():
        m.add_child(open_dash_menu(creche['Lat'], creche['Lng']))

    m.get_root().html.add_child(folium.Element("<style>.leaflet-popup-content-wrapper {width: 300px;}</style>"))


    return m._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)