import os
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


# ============================================================
# BIN PACKING ALGORITHMS
# ============================================================

def first_fit(items, capacity=1.0):
    """
    First Fit (FF)

    Places each item into the first bin
    where the item fits.
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


def first_fit_decreasing(items, capacity=1.0):
    """
    First Fit Decreasing (FFD)

    Sorts items in decreasing order
    and then applies First Fit.
    """

    sorted_items = sorted(items, reverse=True)

    return first_fit(sorted_items, capacity)


def best_fit_decreasing(items, capacity=1.0):
    """
    Best Fit Decreasing (BFD)

    Sorts items in decreasing order and places
    each item into the bin that leaves the
    smallest remaining space.
    """

    sorted_items = sorted(items, reverse=True)

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item:

                remaining_space = space - item

                if remaining_space < best_space:

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

def get_bin_data(bins, capacity):

    result = []

    for number, items in enumerate(bins, 1):

        used = sum(items)

        remaining = capacity - used

        percentage = (used / capacity) * 100

        result.append({
            "number": number,
            "items": items,
            "used": used,
            "remaining": remaining,
            "percentage": percentage
        })

    return result


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

        percentage = min(
            max(data["percentage"], 0),
            100
        )

        html += f"""
        <div class="bin">

            <div class="bin-header">

                <h3>
                    Bin {data["number"]}
                </h3>

                <span>
                    {percentage:.0f}% Full
                </span>

            </div>

            <div class="bin-items">

                {items_html}

            </div>

            <div class="bin-info">

                <span>
                    Used:
                    <strong>
                        {data["used"]:.1f}
                    </strong>
                </span>

                <span>
                    Remaining:
                    <strong>
                        {data["remaining"]:.1f}
                    </strong>
                </span>

            </div>

            <div class="progress-container">

                <div
                    class="progress"
                    style="width:{percentage}%;">
                </div>

            </div>

        </div>
        """

    return html


# ============================================================
# GENERATE COMPLETE WEB PAGE
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

    lower_bound = math.ceil(
        total / capacity
    )

    # Algorithms

    ff_bins = first_fit(
        items,
        capacity
    )

    ffd_bins = first_fit_decreasing(
        items,
        capacity
    )

    bfd_bins = best_fit_decreasing(
        items,
        capacity
    )

    # --------------------------------------------------------
    # BIN DATA
    # --------------------------------------------------------

    ff_data = get_bin_data(
        ff_bins,
        capacity
    )

    ffd_data = get_bin_data(
        ffd_bins,
        capacity
    )

    bfd_data = get_bin_data(
        bfd_bins,
        capacity
    )

    # --------------------------------------------------------
    # INPUT ITEMS HTML
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

    ff_html = create_bins_html(
        ff_data
    )

    ffd_html = create_bins_html(
        ffd_data
    )

    bfd_html = create_bins_html(
        bfd_data
    )

    # --------------------------------------------------------
    # HTML PAGE
    # --------------------------------------------------------

    html = f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
DAA - Bin Packing Problem
</title>

<style>

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


/* ============================================================
   HEADER
   ============================================================ */

.header {{

    background: #171717;

    color: white;

    padding: 45px 20px;

    text-align: center;

}}

.header h1 {{

    margin: 0;

    font-size: 36px;

}}

.header p {{

    margin: 10px 0 0;

    color: #cfcfcf;

    font-size: 16px;

}}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.container {{

    width: 92%;

    max-width: 1100px;

    margin: 30px auto;

}}


/* ============================================================
   CARDS
   ============================================================ */

.card {{

    background: white;

    border-radius: 14px;

    padding: 28px;

    margin-bottom: 25px;

    box-shadow:
        0 4px 18px
        rgba(0,0,0,0.08);

}}

.card h2 {{

    margin-top: 0;

    margin-bottom: 15px;

}}


/* ============================================================
   ITEMS
   ============================================================ */

.items {{

    display: flex;

    flex-wrap: wrap;

    gap: 10px;

    margin-top: 15px;

}}

.item {{

    background: #222;

    color: white;

    padding: 9px 15px;

    border-radius: 8px;

    font-weight: bold;

}}


/* ============================================================
   STATS
   ============================================================ */

.stats {{

    display: flex;

    flex-wrap: wrap;

    gap: 18px;

    margin-top: 25px;

}}

.stat {{

    flex: 1;

    min-width: 200px;

    background: #f1f1f1;

    border-radius: 12px;

    padding: 20px;

    text-align: center;

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


/* ============================================================
   TABLE
   ============================================================ */

.table-wrapper {{

    overflow-x: auto;

}}

table {{

    width: 100%;

    border-collapse: collapse;

    margin-top: 20px;

}}

th,
td {{

    border: 1px solid #ddd;

    padding: 14px;

    text-align: center;

}}

th {{

    background: #222;

    color: white;

}}

td {{

    background: white;

}}


/* ============================================================
   ALGORITHM RESULT
   ============================================================ */

.algorithm-description {{

    color: #555;

    line-height: 1.7;

    margin-bottom: 20px;

}}


/* ============================================================
   BIN
   ============================================================ */

.bin {{

    border: 1px solid #ddd;

    background: #fafafa;

    border-radius: 12px;

    padding: 18px;

    margin-top: 15px;

}}

.bin-header {{

    display: flex;

    justify-content: space-between;

    align-items: center;

    margin-bottom: 15px;

}}

.bin-header h3 {{

    margin: 0;

}}

.bin-header span {{

    font-size: 13px;

    color: #666;

}}

.bin-items {{

    display: flex;

    flex-wrap: wrap;

    gap: 8px;

    margin-bottom: 15px;

}}

.bin-item {{

    background: #e1e1e1;

    padding: 7px 12px;

    border-radius: 6px;

    font-size: 14px;

    font-weight: bold;

}}

.bin-info {{

    display: flex;

    gap: 25px;

    flex-wrap: wrap;

    color: #555;

    font-size: 14px;

}}


/* ============================================================
   PROGRESS
   ============================================================ */

.progress-container {{

    height: 18px;

    background: #ddd;

    border-radius: 20px;

    margin-top: 15px;

    overflow: hidden;

}}

.progress {{

    height: 100%;

    background: #222;

    border-radius: 20px;

}}


/* ============================================================
   CONCLUSION
   ============================================================ */

.conclusion {{

    line-height: 1.8;

}}

.result-box {{

    background: #f1f1f1;

    padding: 18px;

    border-radius: 10px;

    margin-top: 15px;

}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{

    text-align: center;

    padding: 30px 20px;

    color: #666;

    font-size: 14px;

}}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {{

    .header h1 {{

        font-size: 26px;

    }}

    .container {{

        width: 95%;

    }}

    .card {{

        padding: 20px;

    }}

    .bin-info {{

        flex-direction: column;

        gap: 5px;

    }}

}}

</style>

</head>


<body>


<!-- ==========================================================
     HEADER
     ========================================================== -->

<div class="header">

    <h1>
        Bin Packing Problem
    </h1>

    <p>
        DAA Lab - Greedy Approximation Algorithms
    </p>

    <p>
        First Fit | First Fit Decreasing | Best Fit Decreasing
    </p>

</div>


<!-- ==========================================================
     MAIN
     ========================================================== -->

<div class="container">


<!-- ==========================================================
     INPUT
     ========================================================== -->

<div class="card">

    <h2>
        Input
    </h2>

    <p>
        <strong>
            Bin Capacity:
        </strong>

        {capacity}
    </p>

    <p>
        <strong>
            Items:
        </strong>
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
                Theoretical Lower Bound
            </div>

            <div class="stat-value">
                {lower_bound}
            </div>

        </div>

    </div>

</div>


<!-- ==========================================================
     COMPARISON
     ========================================================== -->

<div class="card">

    <h2>
        Algorithm Comparison
    </h2>

    <div class="table-wrapper">

        <table>

            <tr>

                <th>
                    Algorithm
                </th>

                <th>
                    Bins Used
                </th>

                <th>
                    Lower Bound
                </th>

                <th>
                    Extra Bins
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
                    {lower_bound}
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
                    {lower_bound}
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
                    {lower_bound}
                </td>

                <td>
                    {len(bfd_bins) - lower_bound}
                </td>

            </tr>

        </table>

    </div>

</div>


<!-- ==========================================================
     FIRST FIT
     ========================================================== -->

<div class="card">

    <h2>
        First Fit (FF)
    </h2>

    <p class="algorithm-description">

        Each item is processed in its original order.
        The item is placed into the first bin that has
        enough remaining capacity. If no bin can hold
        the item, a new bin is created.

    </p>

    <p>
        <strong>
            Bins Used:
        </strong>

        {len(ff_bins)}
    </p>

    {ff_html}

</div>


<!-- ==========================================================
     FIRST FIT DECREASING
     ========================================================== -->

<div class="card">

    <h2>
        First Fit Decreasing (FFD)
    </h2>

    <p class="algorithm-description">

        Items are first sorted in decreasing order.
        First Fit is then applied to the sorted items.

    </p>

    <p>
        <strong>
            Bins Used:
        </strong>

        {len(ffd_bins)}
    </p>

    {ffd_html}

</div>


<!-- ==========================================================
     BEST FIT DECREASING
     ========================================================== -->

<div class="card">

    <h2>
        Best Fit Decreasing (BFD)
    </h2>

    <p class="algorithm-description">

        Items are first sorted in decreasing order.
        Each item is placed into the bin that leaves
        the smallest possible remaining space.

    </p>

    <p>
        <strong>
            Bins Used:
        </strong>

        {len(bfd_bins)}
    </p>

    {bfd_html}

</div>


<!-- ==========================================================
     CONCLUSION
     ========================================================== -->

<div class="card">

    <h2>
        Conclusion
    </h2>

    <div class="conclusion">

        <p>
            Total size of all items:
            <strong>
                {total:.1f}
            </strong>
        </p>

        <p>
            Theoretical minimum number of bins:
            <strong>
                {lower_bound}
            </strong>
        </p>


        <div class="result-box">

            <p>
                <strong>
                    First Fit:
                </strong>

                {len(ff_bins)} bins
            </p>

            <p>
                <strong>
                    First Fit Decreasing:
                </strong>

                {len(ffd_bins)} bins
            </p>

            <p>
                <strong>
                    Best Fit Decreasing:
                </strong>

                {len(bfd_bins)} bins
            </p>

        </div>

    </div>

</div>


<!-- ==========================================================
     ALGORITHM EXPLANATION
     ========================================================== -->

<div class="card">

    <h2>
        Algorithm Explanation
    </h2>


    <h3>
        1. First Fit
    </h3>

    <p class="algorithm-description">

        Process each item in the original order.
        Search the existing bins from the beginning.
        Place the item in the first bin where it fits.
        If no suitable bin exists, create a new bin.

    </p>


    <h3>
        2. First Fit Decreasing
    </h3>

    <p class="algorithm-description">

        Sort all items from largest to smallest.
        Then apply the First Fit algorithm.

    </p>


    <h3>
        3. Best Fit Decreasing
    </h3>

    <p class="algorithm-description">

        Sort all items from largest to smallest.
        For each item, check all available bins and
        select the bin that leaves the smallest
        remaining space after placement.

    </p>


    <h3>
        Time Complexity
    </h3>

    <p>
        First Fit:
        <strong>
            O(n²)
        </strong>
    </p>

    <p>
        First Fit Decreasing:
        <strong>
            O(n log n + n²)
        </strong>
    </p>

    <p>
        Best Fit Decreasing:
        <strong>
            O(n log n + n²)
        </strong>
    </p>

</div>


</div>


<!-- ==========================================================
     FOOTER
     ========================================================== -->

<div class="footer">

    DAA Lab | Bin Packing Problem

</div>


</body>

</html>
"""

    return html


# ============================================================
# HTTP SERVER
# ============================================================

class BinPackingHandler(BaseHTTPRequestHandler):

    def send_page(self, send_body=True):

        try:

            # Parse URL
            parsed_url = urlparse(self.path)

            # ------------------------------------------------
            # HOME PAGE
            # ------------------------------------------------

            if parsed_url.path in ["", "/"]:

                html = generate_page()

                data = html.encode("utf-8")

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
                    "Cache-Control",
                    "no-cache"
                )

                self.end_headers()

                # HEAD requests should not send content
                if send_body:

                    self.wfile.write(data)

                return

            # ------------------------------------------------
            # FAVICON
            # ------------------------------------------------

            if parsed_url.path == "/favicon.ico":

                self.send_response(204)

                self.end_headers()

                return

            # ------------------------------------------------
            # 404
            # ------------------------------------------------

            self.send_response(404)

            self.send_header(
                "Content-Type",
                "text/plain; charset=utf-8"
            )

            self.end_headers()

            if send_body:

                self.wfile.write(
                    b"404 - Page Not Found"
                )

        except (
            BrokenPipeError,
            ConnectionResetError
        ):

            # Browser/Render disconnected.
            # This is not a server failure.
            pass

        except Exception as error:

            print(
                "Request error:",
                error
            )


    # ========================================================
    # GET
    # ========================================================

    def do_GET(self):

        self.send_page(
            send_body=True
        )


    # ========================================================
    # HEAD
    # ========================================================

    def do_HEAD(self):

        self.send_page(
            send_body=False
        )


    # ========================================================
    # LOGGING
    # ========================================================

    def log_message(self, format, *args):

        # Disable default HTTP logs.
        pass


# ============================================================
# MAIN SERVER
# ============================================================

def main():

    # Render provides PORT automatically.
    #
    # When running locally:
    # http://localhost:10000

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    print(
        "=================================================="
    )

    print(
        "Bin Packing Problem Server"
    )

    print(
        f"Server running on port: {port}"
    )

    print(
        "=================================================="
    )


    # Listen on all network interfaces.
    # Required for Render.

    server = HTTPServer(
        ("0.0.0.0", port),
        BinPackingHandler
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
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    main()
