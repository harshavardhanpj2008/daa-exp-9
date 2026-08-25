import os
import math
from http.server import BaseHTTPRequestHandler, HTTPServer


# ============================================================
# FIRST FIT
# ============================================================

def first_fit(items, capacity=1.0):
    """
    First Fit Bin Packing Algorithm.

    Places each item into the first bin
    that has enough remaining space.
    """

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


# ============================================================
# FIRST FIT DECREASING
# ============================================================

def first_fit_decreasing(items, capacity=1.0):
    """
    First Fit Decreasing.

    Sorts items in decreasing order and
    then applies First Fit.
    """

    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)


# ============================================================
# BEST FIT DECREASING
# ============================================================

def best_fit_decreasing(items, capacity=1.0):
    """
    Best Fit Decreasing.

    Sorts items in decreasing order and places
    each item into the bin with the smallest
    remaining space where the item can fit.
    """

    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            remaining_space = space - item

            if space >= item and remaining_space < best_space:
                best_space = remaining_space
                best_idx = i

        if best_idx >= 0:

            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:

            bins.append(capacity - item)
            bin_contents.append([item])

    return bin_contents


# ============================================================
# BIN INFORMATION
# ============================================================

def get_bin_data(bins, capacity=1.0):

    data = []

    for i, items in enumerate(bins, 1):

        used = sum(items)
        remaining = capacity - used
        percentage = (used / capacity) * 100

        data.append({
            "number": i,
            "items": items,
            "used": used,
            "remaining": remaining,
            "percentage": percentage
        })

    return data


# ============================================================
# CREATE BIN HTML
# ============================================================

def create_bins_html(bin_data):

    html = ""

    for data in bin_data:

        items_html = ""

        for item in data["items"]:

            items_html += f"""
                <span class="bin-item">
                    {item:.1f}
                </span>
            """

        percentage = min(data["percentage"], 100)

        html += f"""
        <div class="bin">

            <div class="bin-title">
                Bin {data["number"]}
            </div>

            <div class="bin-items">
                {items_html}
            </div>

            <div class="bin-info">
                <strong>Used:</strong> {data["used"]:.1f}
                &nbsp;&nbsp;|&nbsp;&nbsp;
                <strong>Remaining:</strong> {data["remaining"]:.1f}
            </div>

            <div class="bar-container">
                <div class="bar"
                     style="width: {percentage}%;">
                </div>
            </div>

            <div class="percentage">
                {percentage:.0f}% Full
            </div>

        </div>
        """

    return html


# ============================================================
# GENERATE WEB PAGE
# ============================================================

def generate_page():

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    items = [
        0.5,
        0.7,
        0.3,
        0.9,
        0.2,
        0.6,
        0.8,
        0.4,
        0.1,
        0.5
    ]

    capacity = 1.0

    # --------------------------------------------------------
    # CALCULATIONS
    # --------------------------------------------------------

    total = sum(items)

    lower_bound = math.ceil(total / capacity)

    # First Fit
    ff_bins = first_fit(items, capacity)

    # First Fit Decreasing
    ffd_bins = first_fit_decreasing(items, capacity)

    # Best Fit Decreasing
    bfd_bins = best_fit_decreasing(items, capacity)

    # --------------------------------------------------------
    # BIN DATA
    # --------------------------------------------------------

    ff_data = get_bin_data(ff_bins, capacity)

    ffd_data = get_bin_data(
        ffd_bins,
        capacity
    )

    bfd_data = get_bin_data(
        bfd_bins,
        capacity
    )

    # --------------------------------------------------------
    # ITEMS HTML
    # --------------------------------------------------------

    items_html = ""

    for item in items:

        items_html += f"""
        <span class="item">
            {item:.1f}
        </span>
        """

    # --------------------------------------------------------
    # BIN HTML
    # --------------------------------------------------------

    ff_html = create_bins_html(ff_data)

    ffd_html = create_bins_html(ffd_data)

    bfd_html = create_bins_html(bfd_data)

    # --------------------------------------------------------
    # COMPLETE HTML
    # --------------------------------------------------------

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Bin Packing Problem
</title>


<style>

/* =========================================================
   GENERAL
   ========================================================= */

* {{
    box-sizing: border-box;
}}

body {{

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f4f6f8;

    color: #222;
}}


/* =========================================================
   HEADER
   ========================================================= */

.header {{

    background: #1f1f1f;

    color: white;

    text-align: center;

    padding: 35px 20px;
}}

.header h1 {{

    margin: 0;

    font-size: 32px;
}}

.header p {{

    margin: 10px 0 0;

    color: #cccccc;

    font-size: 16px;
}}


/* =========================================================
   CONTAINER
   ========================================================= */

.container {{

    width: 90%;

    max-width: 1100px;

    margin: 30px auto;
}}


/* =========================================================
   CARD
   ========================================================= */

.card {{

    background: white;

    padding: 25px;

    margin-bottom: 25px;

    border-radius: 12px;

    box-shadow:
        0 4px 15px
        rgba(0, 0, 0, 0.08);
}}

.card h2 {{

    margin-top: 0;

    margin-bottom: 15px;
}}


/* =========================================================
   ITEMS
   ========================================================= */

.items {{

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 15px;
}}

.item {{

    background: #eeeeee;

    padding: 10px 16px;

    border-radius: 8px;

    font-weight: bold;
}}


/* =========================================================
   STATS
   ========================================================= */

.stats {{

    display: flex;

    gap: 20px;

    margin-top: 25px;

    flex-wrap: wrap;
}}

.stat {{

    flex: 1;

    min-width: 200px;

    padding: 20px;

    text-align: center;

    background: #f5f5f5;

    border-radius: 10px;
}}

.stat-title {{

    color: #666;

    font-size: 14px;
}}

.stat-value {{

    font-size: 30px;

    font-weight: bold;

    margin-top: 8px;
}}


/* =========================================================
   TABLE
   ========================================================= */

table {{

    width: 100%;

    border-collapse: collapse;

    margin-top: 15px;
}}

th,
td {{

    border: 1px solid #ccc;

    padding: 14px;

    text-align: center;
}}

th {{

    background: #222;

    color: white;
}}


/* =========================================================
   BIN
   ========================================================= */

.bin {{

    border: 1px solid #ddd;

    border-radius: 10px;

    padding: 18px;

    margin-top: 15px;

    background: #fafafa;
}}

.bin-title {{

    font-size: 18px;

    font-weight: bold;

    margin-bottom: 12px;
}}

.bin-items {{

    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin-bottom: 12px;
}}

.bin-item {{

    background: #e5e5e5;

    padding: 7px 11px;

    border-radius: 6px;

    font-size: 14px;
}}

.bin-info {{

    color: #555;

    font-size: 14px;
}}


/* =========================================================
   PROGRESS BAR
   ========================================================= */

.bar-container {{

    width: 100%;

    height: 22px;

    background: #dddddd;

    border-radius: 12px;

    margin-top: 12px;

    overflow: hidden;
}}

.bar {{

    height: 100%;

    background: #333333;

    border-radius: 12px;

    transition: width 0.3s;
}}

.percentage {{

    margin-top: 6px;

    font-size: 13px;

    color: #666;

    text-align: right;
}}


/* =========================================================
   ALGORITHM
   ========================================================= */

.algorithm {{

    border-top: 1px solid #ddd;

    padding-top: 20px;

    margin-top: 20px;
}}

.algorithm h3 {{

    margin-bottom: 8px;
}}

.algorithm p {{

    line-height: 1.7;
}}


/* =========================================================
   FOOTER
   ========================================================= */

.footer {{

    text-align: center;

    padding: 25px;

    color: #666;

    font-size: 14px;
}}


/* =========================================================
   MOBILE
   ========================================================= */

@media (max-width: 600px) {{

    .container {{

        width: 95%;

        margin-top: 15px;
    }}

    .card {{

        padding: 18px;
    }}

    .header h1 {{

        font-size: 24px;
    }}

    th,
    td {{

        padding: 8px;

        font-size: 13px;
    }}

}}

</style>

</head>


<body>


<!-- =======================================================
     HEADER
     ======================================================= -->

<div class="header">

    <h1>
        Bin Packing Problem
    </h1>

    <p>
        Greedy Approximation Algorithms
    </p>

    <p>
        First Fit | First Fit Decreasing | Best Fit Decreasing
    </p>

</div>


<div class="container">


<!-- =======================================================
     INPUT
     ======================================================= -->

<div class="card">

    <h2>
        Input
    </h2>

    <p>
        <strong>Bin Capacity:</strong>
        {capacity}
    </p>

    <p>
        <strong>Items:</strong>
    </p>

    <div class="items">

        {items_html}

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


<!-- =======================================================
     COMPARISON
     ======================================================= -->

<div class="card">

    <h2>
        Algorithm Comparison
    </h2>


    <table>

        <tr>

            <th>
                Algorithm
            </th>

            <th>
                Number of Bins
            </th>

            <th>
                Difference from Lower Bound
            </th>

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

            <td>
                Best Fit Decreasing (BFD)
            </td>

            <td>
                {len(bfd_bins)}
            </td>

            <td>
                {len(bfd_bins) - lower_bound}
            </td>

        </tr>

    </table>

</div>


<!-- =======================================================
     FIRST FIT
     ======================================================= -->

<div class="card">

    <h2>
        First Fit (FF)
    </h2>

    <p>
        Each item is placed into the first bin
        that has enough remaining space.
    </p>

    {ff_html}

</div>


<!-- =======================================================
     FIRST FIT DECREASING
     ======================================================= -->

<div class="card">

    <h2>
        First Fit Decreasing (FFD)
    </h2>

    <p>
        Items are sorted in decreasing order
        before applying First Fit.
    </p>

    {ffd_html}

</div>


<!-- =======================================================
     BEST FIT DECREASING
     ======================================================= -->

<div class="card">

    <h2>
        Best Fit Decreasing (BFD)
    </h2>

    <p>
        Items are sorted in decreasing order and
        placed into the bin that leaves the smallest
        remaining space.
    </p>

    {bfd_html}

</div>


<!-- =======================================================
     CONCLUSION
     ======================================================= -->

<div class="card">

    <h2>
        Conclusion
    </h2>

    <p>

        The theoretical lower bound for the given
        input is

        <strong>
            {lower_bound} bins
        </strong>.

    </p>


    <p>

        First Fit uses

        <strong>
            {len(ff_bins)} bins
        </strong>.

    </p>


    <p>

        First Fit Decreasing uses

        <strong>
            {len(ffd_bins)} bins
        </strong>.

    </p>


    <p>

        Best Fit Decreasing uses

        <strong>
            {len(bfd_bins)} bins
        </strong>.

    </p>

</div>


<!-- =======================================================
     ALGORITHM EXPLANATION
     ======================================================= -->

<div class="card">

    <h2>
        Algorithm Explanation
    </h2>


    <div class="algorithm">

        <h3>
            1. First Fit
        </h3>

        <p>

            Process the items in their original order.
            For each item, search the bins from the beginning
            and place the item in the first bin where it fits.

            If no bin can accommodate the item,
            create a new bin.

        </p>

    </div>


    <div class="algorithm">

        <h3>
            2. First Fit Decreasing
        </h3>

        <p>

            First sort all items in decreasing order.
            Then apply the First Fit algorithm.

        </p>

    </div>


    <div class="algorithm">

        <h3>
            3. Best Fit Decreasing
        </h3>

        <p>

            First sort all items in decreasing order.
            For every item, find the bin that can hold
            the item while leaving the smallest possible
            remaining space.

        </p>

    </div>


    <div class="algorithm">

        <h3>
            Time Complexity
        </h3>

        <p>

            First Fit:
            <strong>O(n²)</strong>

        </p>

        <p>

            First Fit Decreasing:
            <strong>O(n log n + n²)</strong>

        </p>

        <p>

            Best Fit Decreasing:
            <strong>O(n log n + n²)</strong>

        </p>

    </div>

</div>


</div>


<!-- =======================================================
     FOOTER
     ======================================================= -->

<div class="footer">

    Bin Packing Problem | DAA Lab

</div>


</body>

</html>
"""

    return html


# ============================================================
# HTTP SERVER
# ============================================================

class BinPackingHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        # Only serve the home page
        if self.path != "/":

            try:

                self.send_response(404)

                self.send_header(
                    "Content-Type",
                    "text/plain; charset=utf-8"
                )

                self.end_headers()

                self.wfile.write(
                    b"Page Not Found"
                )

            except (
                BrokenPipeError,
                ConnectionResetError
            ):
                pass

            return

        try:

            # Generate HTML
            html = generate_page()

            data = html.encode("utf-8")

            # Send response
            self.send_response(200)

            self.send_header(
                "Content-Type",
                "text/html; charset=utf-8"
            )

            self.send_header(
                "Content-Length",
                str(len(data))
            )

            self.send_header(
                "Connection",
                "close"
            )

            self.end_headers()

            self.wfile.write(data)

        except (
            BrokenPipeError,
            ConnectionResetError
        ):

            # Render/client disconnected before
            # the response was completely sent.
            pass

        except Exception as error:

            print(
                f"Request error: {error}"
            )

    def log_message(self, format, *args):

        # Disable default HTTP request logs.
        # Keeps Render logs cleaner.
        return


# ============================================================
# START SERVER
# ============================================================

def main():

    # Render provides the PORT environment variable.
    # Local default = 10000.

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    server = HTTPServer(
        ("0.0.0.0", port),
        BinPackingHandler
    )

    print(
        f"Bin Packing server running on port {port}"
    )

    try:

        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "Server stopped."
        )

    finally:

        server.server_close()


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    main()
