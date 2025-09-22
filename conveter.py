import mistune
from weasyprint import HTML, CSS
from pathlib import Path

class Converter:
    @staticmethod
    def md_to_pdf(input_md: str, output_pdf: str):
        """
        Convert a Markdown file into a styled PDF using Mistune + WeasyPrint.

    Args:
        input_md (str): Path to the Markdown file.
        output_pdf (str): Path to save the generated PDF.
    """
        # ====== STEP 1: READ MARKDOWN ======
        md_path = Path(input_md)
        if not md_path.exists():
            raise FileNotFoundError(f"Markdown file not found: {md_path}")

        with md_path.open("r", encoding="utf-8") as f:
            md_content = f.read()

        # ====== STEP 2: CONVERT MARKDOWN TO HTML ======
        markdown = mistune.create_markdown(
            renderer=mistune.HTMLRenderer(),
            plugins=['table', 'strikethrough'],
            escape=False
        )
        html = markdown(md_content)

        # Fix escaped <table> tags
        html = html.replace("<p>&lt;table&gt;", "&lt;table&gt;")
        html = html.replace("&lt;/table&gt;</p>", "&lt;/table&gt;")
        html = html.replace("&lt;", "<").replace("&gt;", ">")

        # ====== STEP 3: DEFINE CSS ======
        css = CSS(string="""
            @page {
                size: A4;
                margin: 2cm;
            }

            body {
                font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
                font-size: 13px;
                line-height: 1.6;
                color: #222;
                background: white;
            }

            h1, h2, h3, h4 {
                color: #2c3e50;
                font-weight: 600;
                margin-top: 1.5em;
                margin-bottom: 0.5em;
            }

            h1 { font-size: 24px; border-bottom: 2px solid #ccc; padding-bottom: 5px; }
            h2 { font-size: 20px; border-bottom: 1px solid #eee; padding-bottom: 3px; }
            h3 { font-size: 16px; }
            h4 { font-size: 14px; }

            p {
                margin: 0 0 10px;
            }

            table {
                width: 100%;
                border-collapse: collapse;
                margin: 1.5em 0;
                font-size: 13px;
            }

            th, td {
                border: 1px solid #ddd;
                padding: 8px 10px;
                text-align: left;
                vertical-align: top;
            }

            th {
                background-color: #f9f9f9;
                font-weight: 600;
            }

            tr:nth-child(even) td {
                background-color: #f5f5f5;
            }

            code {
                background-color: #f4f4f4;
                padding: 2px 4px;
                border-radius: 4px;
                font-family: monospace;
                font-size: 90%;
                color: #c7254e;
            }

            pre code {
                display: block;
                padding: 10px;
                background: #f4f4f4;
                border: 1px solid #ddd;
                overflow-x: auto;
            }

            ul, ol {
                padding-left: 1.5em;
                margin-bottom: 1em;
            }

            blockquote {
                border-left: 4px solid #ccc;
                padding-left: 1em;
                color: #666;
                margin: 1em 0;
                font-style: italic;
                background: #f9f9f9;
            }

            @page {
                size: A4;
                margin: 2cm;

                @bottom-center {
                    content: "Developed by AgenticVP – A tool by Vayavya Labs";
                    font-size: 10px;
                    color: #888;
                }
            }
        """)

        # ====== STEP 4: CONVERT TO PDF ======
        HTML(string=html).write_pdf(output_pdf, stylesheets=[css])

        print(f"✅ PDF successfully generated at: {output_pdf}")
