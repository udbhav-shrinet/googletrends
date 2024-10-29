
</head>
<body>

<h1>Top 20 Trending Searches in India</h1>

<p>This project uses the <code>pytrends</code> library to fetch and analyze the top 20 trending searches in India. The script retrieves the interest by region for each trend across Indian states and saves the results to an Excel file.</p>

<p>The data can also be used for visualization on a map of India, allowing users to hover over different regions to see which trends are popular, making it a valuable tool for search engine optimization (SEO).</p>

<h2>Features</h2>
<ul>
    <li>Fetches the top 20 trending searches in India.</li>
    <li>Retrieves interest data by region for each trend.</li>
    <li>Excludes states with zero interest.</li>
    <li>Outputs the data to an Excel file for easy analysis.</li>
    <li>Can be visualized on a map of India, showing regional trend popularity.</li>
</ul>

<h2>Requirements</h2>
<p>To run this project, you need:</p>
<ul>
    <li>Python 3.x</li>
    <li>The following Python packages:</li>
    <ul>
        <li><code>pytrends</code></li>
        <li><code>pandas</code></li>
        <li><code>openpyxl</code> (for saving to Excel)</li>
    </ul>
</ul>

<p>You can install the required packages using pip:</p>
<pre><code>pip install pytrends pandas openpyxl</code></pre>

<h2>Usage</h2>
<p>Clone the repository to your local machine:</p>
<pre><code>git clone https://github.com/yourusername/repository-name.git</code></pre>

<p>Navigate to the project directory:</p>
<pre><code>cd repository-name</code></pre>

<p>Run the script:</p>
<pre><code>python your_script_name.py</code></pre>

<p>The results will be saved in an Excel file named <code>Top_20_Trends_Interest_by_Region.xlsx</code>.</p>

<h2>Output</h2>
<p>The output Excel file contains the following columns:</p>
<ul>
    <li><strong>Trend:</strong> The name of the trending topic.</li>
    <li><strong>Region:</strong> The Indian state/region where the interest is recorded.</li>
    <li><strong>Interest:</strong> The interest score representing search popularity.</li>
</ul>

<h2>Visualization</h2>
<p>The data obtained from this project can be visualized on a map of India. Users can hover over different regions to see which trends are popular, providing insights that can enhance search engine optimization (SEO) strategies.</p>

<h2>Contribution</h2>
<p>Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.</p>

</body>
</html>
