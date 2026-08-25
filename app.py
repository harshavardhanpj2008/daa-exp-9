import os
import math
from http.server import BaseHTTPRequestHandler, HTTPServer


# -----------------------------------------
# First Fit
# -----------------------------------------
def first_fit(items, capacity=1.0):
    bins = []
    bin_contents = []

    for item in items:
        placed = False

        for i, space in enumerate(bins):

            if space >= item:
                bins[i] -= item
                bin_contents[i].append(item)
                placed = True
                break

        if not placed:
            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# -----------------------------------------
# First Fit Decreasing
# -----------------------------------------
def first_fit_decreasing(items, capacity=1.0):
    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)


# -----------------------------------------
# Best Fit Decreasing
# -----------------------------------------
def best_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item and space - item < best_space:
                best_space = space - item
                best_idx = i

        if best_idx >= 0:

            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# -----------------------------------------
# Generate bin information
# -----------------------------------------
def get_bin_data(bins):

    data = []

    for i, b in enumerate(bins, 1):

        used = sum(b)

        remaining = 1.0 - used

        percentage = used * 100

        data.append({
            "number": i,
            "items": b,
            "used": used,
            "remaining": remaining,
            "percentage": percentage
        })

    return data


# -----------------------------------------
# Generate HTML
# -----------------------------------------
def generate_page():

    items = [
        0.5, 0.7, 0.3, 0.9, 0.2,
        0.6, 0.8, 0.4, 0.1, 0.5
    ]

    capacity = 1.0

    total = sum(items)

    lower_bound = math.ceil(total / capacity)

    # Solve using three strategies
    ff_bins = first_fit(items, capacity)

    ffd_bins = first_fit_decreasing(
        items,
        capacity
    )

    bfd_bins = best_fit_decreasing(
        items,
        capacity
    )

    ff_data = get_bin_data(ff_bins)
    ffd_data = get_bin_data(ffd_bins)
    bfd_data = get_bin_data(bfd_bins)

    # -----------------------------------------
    # Create HTML
    # -----------------------------------------

    html = """
<!DOCTYPE html>

<html>

<head>

<title>Bin Packing Problem</title>

<meta name="viewport"
      content="width=device-width, initial-scale=1">

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family: Arial, sans-serif;

    background: #f4f6f8;

    color: #222;
}

.header {

    background: #222;

    color: white;

    text-align: center;

    padding: 30px;
}

.container {

    max-width: 1100px;

    margin: 30px auto;

    padding: 20px;
}

.card {

    background: white;

    padding: 25px;

    margin-bottom: 25px;

    border-radius: 12px;

    box-shadow:
        0 4px 15px
        rgba(0,0,0,0.08);
}

h1 {
    margin-bottom: 10px;
}

h2 {
    margin-top: 0;
}

.items {

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 15px;
}

.item {

    background: #eeeeee;

    padding: 10px 15px;

    border-radius: 8px;

    font-weight: bold;
}

.stats {

    display: flex;

    flex-wrap: wrap;

    gap: 15px;

    margin-top: 20px;
}

.stat {

    flex: 1;

    min-width: 180px;

    background: #f5f5f5;

    padding: 20px;

    border-radius: 10px;

    text-align: center;
}

.stat-title {

    font-size: 14px;

    color: #666;
}

.stat-value {

    font-size: 28px;

    font-weight: bold;

    margin-top: 8px;
}

.algorithm {

    margin-top: 25px;

    border-top: 1px solid #ddd;

    padding-top: 25px;
}

.bin {

    margin: 15px 0;

    padding: 18px;

    background: #fafafa;

    border: 1px solid #ddd;

    border-radius: 10px;
}

.bin-title {

    font-weight: bold;

    margin-bottom: 10px;
}

.bin-items {

    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin: 10px 0;
}

.bin-item {

    padding: 7px 10px;

    background: #e5e5e5;

    border-radius: 6px;

    font-size: 14px;
}

.bar-container {

    width: 100%;

    height: 22px;

    background: #ddd;

    border-radius: 12px;

    overflow: hidden;

    margin-top: 10px;
}

.bar {

    height: 100%;

    background: #444;

    border-radius: 12px;
}

.bin-info {

    margin-top: 8px;

    font-size: 14px;

    color: #555;
}

.summary-table {

    width: 100%;

    border-collapse: collapse;

    margin-top: 20px;
}

.summary-table th,
.summary-table td {

    border: 1px solid #ccc;

    padding: 14px;

    text-align: center;
}

.summary-table th {

    background: #222;

    color: white;
}

.best {

    font-weight: bold;
}

.footer {

    text-align: center;

    padding: 20px;

    color: #666;
}

@media(max-width:600px) {

    .container {
        padding: 10px;
    }

    .card {
        padding: 18px;
    }

}

</style>

</head>

<body>


<div class="header">

<h1>Bin Packing Problem</h1>

<p>
Greedy Approximation Algorithms
</p>

<p>
First Fit | First Fit Decreasing | Best Fit Decreasing
</p>

</div>


<div class="container">


<!-- Input -->

<div class="card">

<h2>Input</h2>

<p>
<strong>Bin Capacity:</strong> 1.0
</p>

<p>
<strong>Items:</strong>
</p>

<div class="items">
"""

    # Add items
    for item in items:

        html += f"""
<span class="item">
{item}
</span>
"""

    html += f"""
</div>

<div class="stats">

<div class="stat">

<div class="stat-title">
Total Item Size
</div>

<div class="stat-value">
{total:.1f}
</div>

</div>

<div class="stat">

<div class="stat-title">
Lower Bound
</div>

<div class="stat-value">
{lower_bound}
</div>

</div>

</div>

</div>


<!-- Algorithm Results -->

<div class="card">

<h2>Algorithm Comparison</h2>

<table class="summary-table">

<tr>

<th>Algorithm</th>

<th>Number of Bins</th>

<th>Difference from Lower Bound</th>

</tr>

<tr>

<td>
First Fit (FF)
</td>

<td>
{len(ff_bins)}
</td>

<td>
{len(ff_bins) - lower_bound}
</td>

</tr>

<tr>

<td>
First Fit Decreasing (FFD)
</td>

<td>
{len(ffd_bins)}
</td>

<td>
{len(ffd_bins) - lower_bound}
</td>

</tr>

<tr>

<td class="best">
Best Fit Decreasing (BFD)
</td>

<td class="best">
{len(bfd_bins)}
</td>

<td>
{len(bfd_bins) - lower_bound}
</td>

</tr>

</table>

</div>


<!-- First Fit -->

<div class="card">

<h2>
First Fit (FF)
</h2>

<p>
Items are placed into the first bin that has enough remaining space.
</p>

"""

    for data in ff_data:

        items_text = ""

        for item in data["items"]:

            items_text += f"""
<span class="bin-item">
{item}
</span>
"""

        html += f"""

<div class="bin">

<div class="bin-title">
Bin {data["number"]}
</div>

<div class="bin-items">

{items_text}

</div>

<div>
Used: {data["used"]:.1f}
&nbsp; | &nbsp;
Remaining: {data["remaining"]:.1f}
</div>

<div class="bar-container">

<div class="bar"
style="width:{data["percentage"]}%">
</div>

</div>

</div>

"""

    html += """

</div>


<!-- First Fit Decreasing -->

<div class="card">

<h2>
First Fit Decreasing (FFD)
</h2>

<p>
Items are sorted in decreasing order before applying First Fit.
</p>

"""

    for data in ffd_data:

        items_text = ""

        for item in data["items"]:

            items_text += f"""
<span class="bin-item">
{item}
</span>
"""

        html += f"""

<div class="bin">

<div class="bin-title">
Bin {data["number"]}
</div>

<div class="bin-items">

{items_text}

</div>

<div>
Used: {data["used"]:.1f}
&nbsp; | &nbsp;
Remaining: {data["remaining"]:.1f}
</div>

<div class="bar-container">

<div class="bar"
style="width:{data["percentage"]}%">
</div>

</div>

</div>

"""

    html += """

</div>


<!-- Best Fit Decreasing -->

<div class="card">

<h2>
Best Fit Decreasing (BFD)
</h2>

<p>
Items are sorted in decreasing order and placed into
the bin with the smallest remaining space that can hold the item.
</p>

"""

    for data in bfd_data:

        items_text = ""

        for item in data["items"]:

            items_text += f"""
<span class="bin-item">
{item}
</span>
"""

        html += f"""

<div class="bin">

<div class="bin-title">
Bin {data["number"]}
</div>

<div class="bin-items">

{items_text}

</div>

<div>
Used: {data["used"]:.1f}
&nbsp; | &nbsp;
Remaining: {data["remaining"]:.1f}
</div>

<div class="bar-container">

<div class="bar"
style="width:{data["percentage"]}%">
</div>

</div>

</div>

"""

    html += f"""

</div>


<!-- Conclusion -->

<div class="card">

<h2>Conclusion</h2>

<p>

The lower bound for the given input is
<strong>{lower_bound}</strong> bins.

</p>

<p>

First Fit uses
<strong>{len(ff_bins)}</strong> bins.

</p>

<p>

First Fit Decreasing uses
<strong>{len(ffd_bins)}</strong> bins.

</p>

<p>

Best Fit Decreasing uses
<strong>{len(bfd_bins)}</strong> bins.

</p>

</div>


<!-- Algorithm Information -->

<div class="card">

<h2>Algorithm Explanation</h2>

<div class="algorithm">

<h3>First Fit (FF)</h3>

<p>

Process items in their original order.
Place each item into the first bin where it fits.
If no bin can accommodate it, create a new bin.

</p>

</div>

<div class="algorithm">

<h3>First Fit Decreasing (FFD)</h3>

<p>

Sort all items in decreasing order and then apply
the First Fit algorithm.

</p>

</div>

<div class="algorithm">

<h3>Best Fit Decreasing (BFD)</h3>

<p>

Sort items in decreasing order and place each item into
the bin that leaves the smallest possible remaining space.

</p>

</div>

<h3>Time Complexity</h3>

<p>

First Fit:
<strong>O(n²)</strong> in this implementation.

</p>

<p>

First Fit Decreasing:
<strong>O(n log n + n²)</strong>.

</p>

<p>

Best Fit Decreasing:
<strong>O(n log n + n²)</strong>.

</p>

</div>


</div>


<div class="footer">

<p>
Bin Packing Problem | DAA Lab | Greedy Approximation
</p>

</div>


</body>

</html>
"""

    return html


# -----------------------------------------
# HTTP Server
# -----------------------------------------

class BinPackingHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        parsed_url = urlparse(self.path)

        if parsed_url.path != "/":

            self.send_error(
                404,
                "Page Not Found"
            )

            return

        html = generate_page()

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(html.encode("utf-8")))
        )

        self.end_headers()

        self.wfile.write(
            html.encode("utf-8")
        )


# -----------------------------------------
# Start Server
# -----------------------------------------

def main():

    port = int(
        os.environ.get(
            "PORT",
            10000
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        BinPackingHandler
    )

    print(
        f"Bin Packing server running on port {port}"
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
