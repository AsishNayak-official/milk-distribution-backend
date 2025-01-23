import docx
from docx.shared import Cm, Pt, Inches
from docx.enum.section import WD_ORIENT

def create_docx(data: dict, output_file: str):
    # Create a new Word document
    doc = docx.Document()

    # Access the first section of the document
    section = doc.sections[0]

    # Set the section orientation to landscape
    section.orientation = WD_ORIENT.LANDSCAPE

    # Set the page size and orientation (implicitly handled by section.orientation)
    new_width, new_height = section.page_height, section.page_width
    section.page_width = new_width
    section.page_height = new_height

    # Adjust margins using Cm (1 cm = 1 cm, intuitive unit)
    section.top_margin = Cm(0)      # Top margin of 1 cm
    section.bottom_margin = Cm(0)   # Bottom margin of 1 cm
    section.left_margin = Cm(1.2)     # Left margin of 1.2 cm
    section.right_margin = Cm(1.2)    # Right margin of 1.2 cm

    # Add Title
    title = doc.add_heading("CASH INCENTIVE TO OMFED DAIRY FARMERS", level=1)
    title.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.CENTER
    run = title.runs[0]
    run.font.size = Pt(12) 
    run.font.underline = True
    run.font.name = 'Arial'  # Set font to Arial

    # Add society details
    society_details = doc.add_paragraph()
    run = society_details.add_run(f"\n\tSociety Name: - {data['society_name']}")
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(10)  # Set font size to 10 points

    run = society_details.add_run(f"\t\t\tSociety Code: - {data['society_code']}")
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(10)  # Set font size to 10 points

    run = society_details.add_run(f"\t\t\t\t\t\t\tUnit: - {data['unit']}         ")
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(10)  # Set font size to 10 points

    # Add month and milk bill period
    period = doc.add_paragraph()
    run = period.add_run(f"  Month:-   {data['month']}")
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(10)  # Set font size to 10 points

    run = period.add_run(f"\t\t\t\tMilk Bill Period From:-   {data['start_date']}   To   {data['end_date']}")
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(10)  # Set font size to 10 points

    # Add Table Header
    paragraph = doc.add_paragraph("FILL ALL THE INFORMATION IN CAPITAL LETTER")
    paragraph.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.RIGHT
    run = paragraph.runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(9)  

    # Add table with merged cells for all columns except "Average", "Fat %", and "SNF %"
    table = doc.add_table(rows=2, cols=12)  # First row for headers, second row for content
    table.style = 'TableGrid'
    table.autofit = False
    table.allow_autofit = False

    # Add column headers
    headers = [
        "S.N",
        "Name of the Functional Members",
        "Membership No.",
        "Milk Supplied (No of)",
        "Total Qty of Milk Supplied",
        "Average",
          "",  # This header will span Fat % and SNF %
        "AADHAR NO.",
        "Name of the Bank in Full",
        "Branch Name",
        "Account No.",
        "IFSC Code",
    ]

    header_cells = table.rows[0].cells
    for idx, header in enumerate(headers):
        header_cells[idx].text = header
        paragraph = header_cells[idx].paragraphs[0]

    # Set horizontal alignment (center)
        paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.runs[0]
        run.font.name = 'Arial'  # Set font to Arial
        run.font.size = Pt(9)   # Set font size to 9 points

    # Merge cells for "Average" column (this will span two columns for Fat % and SNF %)
    for idx in [0, 1, 2, 3, 4, 7, 8, 9, 10,11]:  # Skipping Fat % and SNF %
        header_cells[idx].merge(table.rows[1].cells[idx])# Merge "Average" with the next column

    header_cells[5].merge(header_cells[6])

    table.columns[0].width=Inches(0.4)
    table.columns[1].width=Inches(1.5)
    table.columns[2].width=Inches(0.5)
    table.columns[3].width=Inches(0.5)
    table.columns[4].width=Inches(0.5)
    table.columns[5].width=Inches(0.6)
    table.columns[6].width=Inches(0.6)
    table.columns[7].width=Inches(1.0)
    table.columns[8].width=Inches(1.4)
    table.columns[9].width=Inches(0.8)
    table.columns[10].width=Inches(1.1)
    table.columns[11].width=Inches(1.0)

    # Add "Fat %" and "SNF %" headers in the second row under "Average"
    table.rows[1].cells[5].text = "Fat %"
    run = table.rows[1].cells[5].paragraphs[0].runs[0]
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(9)   # Set font size to 9 points
    table.rows[1].cells[6].text = "SNF %"
    run = table.rows[1].cells[6].paragraphs[0].runs[0]
    run.font.name = 'Arial'  # Set font to Arial
    run.font.size = Pt(9)   # Set font size to 9 points

    # Fill the table with data with custom font
    for idx, member in enumerate(data["members"], start=1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = str(member.get("name", ""))
        row_cells[2].text = str(member.get("membership_no", ""))
        row_cells[3].text = str(member.get("milk_supplied", ""))
        row_cells[4].text = str(member.get("total_qty_milk_supplied", ""))
        row_cells[5].text = str(member.get("fat_percentage", ""))  # Fat %
        row_cells[6].text = str(member.get("snf_percentage", ""))  # SNF %

        row_cells[7].text = str(member.get("aadhaar", ""))
        row_cells[8].text = str(member.get("bank_name", ""))
        row_cells[9].text = str(member.get("branch_name", ""))
        row_cells[10].text = str(member.get("account_number", ""))
        row_cells[11].text = str(member.get("ifsc_code", ""))

        # Apply font to each cell in the table
        for cell in row_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = 'Arial'  # Set font to Arial
                    run.font.size = Pt(10)   # Set font size to 10 points

    # Add signatures section with custom font
    doc.add_paragraph("\n\nPrepared by\t\t\t\t\t\t\t\tCertified by\t\t\t\t\t\t\t   Countersigned by")
    doc.add_paragraph("\nSecretary\t\t\t\t\t\t\tPresident\tMC Member-1\t\t\t\t  MC Member\tRoute Supervisor")

    # Save the document
    doc.save(output_file)
 