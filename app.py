import os
import math
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


# ============================================================
# FIRST FIT
# ============================================================

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


# ============================================================
# FIRST FIT DECREASING
# ============================================================

def first_fit_decreasing(items, capacity=1.0):
    return first_fit(
        sorted(items, reverse=True),
        capacity
    )


# ============================================================
# BEST FIT DECREASING
# ============================================================

def best_fit_decreasing(items, capacity=1.0):

    sorted_items = sorted(
        items,
        reverse=True
    )

    bins = []
    bin_contents = []

    for item in sorted_items:

        best_idx = -1
        best_space = float("inf")

        for i, space in enumerate(bins):

            if space >= item:

                remaining = space - item

                if remaining < best_space:
                    best_space = remaining
                    best_idx = i

        if best_idx >= 0:

            bins[best_idx] -= item
            bin_contents[best_idx].append(item)

        else:

            bins.append(
                capacity - item
            )

            bin_contents.append(
                [item]
            )

    return bin_contents


# ============================================================
# FORMAT ITEMS
# ============================================================

def format_items(items):

    return "[" + ", ".join(
        f"{x:.1f}" for x in items
    ) + "]"


# ============================================================
# CREATE SAMPLE OUTPUT
# ============================================================

def generate_output():

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

    lines = []

    # --------------------------------------------------------
    # INPUT
    # --------------------------------------------------------

    lines.append(
        f"Items: {format_items(items)}"
    )

    lines.append(
        f"Capacity: {capacity:.1f}"
    )

    lines.append(
        f"Sum of items: {total:.1f}"
    )

    lines.append(
        f"Lower bound on bins: {lower_bound}"
    )

    lines.append("")

    # --------------------------------------------------------
    # DISPLAY FUNCTION
    # --------------------------------------------------------

    def add_algorithm(
        title,
        bins
    ):

        lines.append(
            f"{title}: {len(bins)} bins"
        )

        for i, bin_items in enumerate(
            bins,
            1
        ):

            used = sum(bin_items)

            # 20-character utilization bar
            bar_length = int(
                used * 20
            )

            bar = "#" * bar_length

            bar = bar.ljust(
                20
            )

            item_text = format_items(
                bin_items
            )

            # Match sample layout
            lines.append(
                f"    Bin {i}: "
                f"{item_text:<18} | "
                f"Used: {used:.1f} "
                f"[{bar}]"
            )

        lines.append("")

    # --------------------------------------------------------
    # FIRST FIT
    # --------------------------------------------------------

    add_algorithm(
        "First Fit (FF)",
        ff_bins
    )

    # --------------------------------------------------------
    # FIRST FIT DECREASING
    # --------------------------------------------------------

    add_algorithm(
        "First Fit Decreasing (FFD)",
        ffd_bins
    )

    # --------------------------------------------------------
    # BEST FIT DECREASING
    # --------------------------------------------------------

    add_algorithm(
        "Best Fit Decreasing (BFD)",
        bfd_bins
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    lines.append(
        f"Summary: "
        f"Lower Bound={lower_bound}, "
        f"FF={len(ff_bins)}, "
        f"FFD={len(ffd_bins)}, "
        f"BFD={len(bfd_bins)}"
    )

    return "\n".join(lines)


# ============================================================
# HTML PAGE
# ============================================================

def generate_page():

    output = generate_output()

    # Escape HTML special characters
    output = (
        output
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    return f"""
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>
Bin Packing Problem - Sample Output
</title>


<style>

/* ============================================================
   PAGE
   ============================================================ */

body {{

    margin: 0;

    background: white;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

}}


/* ============================================================
   TITLE
   ============================================================ */

.title {{

    width: 92%;

    margin: 0 auto;

    padding: 18px 0;

    background: #217346;

    color: white;

    text-align: center;

    font-size: 25px;

    font-weight: bold;

    letter-spacing: 1px;

}}


/* ============================================================
   OUTPUT BOX
   ============================================================ */

.output-container {{

    width: 88%;

    margin: 32px auto;

    background: #eaf5eb;

    padding: 25px 30px;

    border-radius: 0;

    overflow-x: auto;

}}


/* ============================================================
   CONSOLE OUTPUT
   ============================================================ */

pre {{

    margin: 0;

    font-family:
        "Courier New",
        Courier,
        monospace;

    font-size: 15px;

    line-height: 1.55;

    color: #222;

    white-space: pre;

}}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {{

    text-align: center;

    margin-top: 30px;

    margin-bottom: 30px;

    color: #666;

    font-size: 14px;

}}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 700px) {{

    .title {{

        width: 94%;

        font-size: 21px;

    }}

    .output-container {{

        width: 84%;

        padding: 20px;

    }}

    pre {{

        font-size: 12px;

    }}

}}

</style>

</head>


<body>


<div class="title">

    SAMPLE OUTPUT

</div>


<div class="output-container">

<pre>{output}</pre>

</div>


<div class="footer">

    DAA Lab | Bin Packing Problem

</div>


</body>

</html>
"""


# ============================================================
# HTTP SERVER
# ============================================================

class BinPackingHandler(
    BaseHTTPRequestHandler
):


    # --------------------------------------------------------
    # SEND PAGE
    # --------------------------------------------------------

    def send_page(
        self,
        send_body=True
    ):

        try:

            parsed_url = urlparse(
                self.path
            )

            # ------------------------------------------------
            # HOME PAGE
            # ------------------------------------------------

            if parsed_url.path in [
                "",
                "/"
            ]:

                html = generate_page()

                data = html.encode(
                    "utf-8"
                )

                self.send_response(
                    200
                )

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

                # HEAD request should not
                # send response body

                if send_body:

                    self.wfile.write(
                        data
                    )

                return


            # ------------------------------------------------
            # FAVICON
            # ------------------------------------------------

            if parsed_url.path == "/favicon.ico":

                self.send_response(
                    204
                )

                self.end_headers()

                return


            # ------------------------------------------------
            # 404
            # ------------------------------------------------

            self.send_response(
                404
            )

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

            # Client disconnected.
            pass


        except Exception as error:

            print(
                "Request error:",
                error
            )


    # --------------------------------------------------------
    # GET
    # --------------------------------------------------------

    def do_GET(self):

        self.send_page(
            send_body=True
        )


    # --------------------------------------------------------
    # HEAD
    # --------------------------------------------------------

    def do_HEAD(self):

        self.send_page(
            send_body=False
        )


    # --------------------------------------------------------
    # DISABLE DEFAULT LOGS
    # --------------------------------------------------------

    def log_message(
        self,
        format,
        *args
    ):

        return


# ============================================================
# START SERVER
# ============================================================

def main():

    # Render gives PORT automatically.
    # Local default = 10000

    port = int(
        os.environ.get(
            "PORT",
            "10000"
        )
    )

    print(
        f"Bin Packing Server running on port {port}"
    )

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
# RUN
# ============================================================

if __name__ == "__main__":

    main()
