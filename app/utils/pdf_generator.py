import docx
from docx.shared import Cm, Pt, Inches
from docx.enum.section import WD_ORIENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def create_docx(data: dict, output_file: str):
    # Create a new Word document
    doc = docx.Document()

    # Access the first section of the document
    section = doc.sections[0]

    # Set the section orientation to landscape
    section.orientation = WD_ORIENT.LANDSCAPE

    # Set the page size and orientation (implicitly handled by section.orientation)
    section.page_width = Cm(29.7)  # A4 width in cm
    section.page_height = Cm(21.0)  # A4 height in cm

    # Adjust margins using Cm (1 cm = 1 cm, intuitive unit)
    section.top_margin = Cm(1)
    section.bottom_margin = Cm(0)
    section.left_margin = Cm(1.2)
    section.right_margin = Cm(1.2)

    members_per_page = 16
    total_members = len(data["members"])
    pages = [data["members"][i:i + members_per_page] for i in range(0, total_members, members_per_page)]

    # Add tables for each page
    for page_idx, page in enumerate(pages):
        if page_idx > 0:
            doc.add_page_break()  # Add page break before adding the table on subsequent pages
        
        # Add the table with headers and data
        add_table_page(doc, page,data)

        # Add signature footer at the bottom of each page
        doc.add_paragraph("\n\nPrepared by\t\t\t\t\t\t\t\t\tCertified by\t\t\t\t\t\t\t\tCountersigned by")
        doc.add_paragraph("\nSecretary\t\t\t\t\t\t\t\tPresident\tMC Member-1\t\t\t\tMC Member\t\tRoute Supervisor")

    # Save the document
    doc.save(output_file)


def add_table_page(doc, members,data):
    # Add Title (Heading)
    title = doc.add_heading("CASH INCENTIVE TO OMFED DAIRY FARMERS", level=1)
    title.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.CENTER
    run = title.runs[0]
    run.font.size = Pt(12)
    run.font.underline = True
    run.font.name = 'Arial'

    # Add society details (Same as the original)
    society_details = doc.add_paragraph()
    run = society_details.add_run(f"\n\t\tSociety Name: - {data['society_name']}")
    run.font.name = 'Arial'
    run.font.size = Pt(10)

    run = society_details.add_run(f"\t\t\t\tSociety Code: - {data['society_code']}")
    run.font.name = 'Arial'
    run.font.size = Pt(10)

    run = society_details.add_run(f"\t\t\t\t\t\t\tUnit: - {data['unit']}         ")
    run.font.name = 'Arial'
    run.font.size = Pt(10)

    # Add month and milk bill period
    period = doc.add_paragraph()
    run = period.add_run(f"\tMonth:-   {data['month']}")
    run.font.name = 'Arial'
    run.font.size = Pt(10)

    run = period.add_run(f"\t\t\t\t\tMilk Bill Period From:-   {data['start_date']}   To   {data['end_date']}")
    run.font.name = 'Arial'
    run.font.size = Pt(10)

    period.paragraph_format.space_after = Pt(0)

    paragraph = doc.add_paragraph("FILL ALL THE INFORMATION IN CAPITAL LETTER")
    paragraph.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.RIGHT
    run = paragraph.runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(9)

    paragraph.paragraph_format.space_after = Pt(0)

    # Add table layout
    table = doc.add_table(rows=2, cols=12)
    table.style = 'TableGrid'
    table.autofit = False
    table.allow_autofit = False

    # Add column headers and set their properties
    headers = [
        "S.N", "Name of the Functional Members", "Membership No.", "Milk Supplied (No of)", "Total Qty of Milk Supplied",
        "Average", "", "AADHAR NO.", "Name of the Bank in Full", "Branch Name", "Account No.", "IFSC Code"
    ]

    header_cells = table.rows[0].cells
    for idx, header in enumerate(headers):
        header_cells[idx].text = header
        paragraph = header_cells[idx].paragraphs[0]
        paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.runs[0]
        run.font.name = 'Arial'
        run.font.size = Pt(9)

        tc_pr = header_cells[idx]._element.get_or_add_tcPr()
        v_align = OxmlElement('w:vAlign')
        v_align.set(qn('w:val'), 'center')
        tc_pr.append(v_align)

    # Merge cells for the "Average" column and the span for Fat % and SNF %
    for idx in [0, 1, 2, 3, 4, 7, 8, 9, 10, 11]:
        header_cells[idx].merge(table.rows[1].cells[idx])

    header_cells[5].merge(header_cells[6])

    # Define column widths for the table
    table.columns[0].width = Inches(0.4)
    table.columns[1].width = Inches(1.45)
    table.columns[2].width = Inches(0.6)
    table.columns[3].width = Inches(0.6)
    table.columns[4].width = Inches(0.65)
    table.columns[5].width = Inches(0.55)
    table.columns[6].width = Inches(0.55)
    table.columns[7].width = Inches(1.0)
    table.columns[8].width = Inches(1.6)
    table.columns[9].width = Inches(1.2)
    table.columns[10].width = Inches(1.2)
    table.columns[11].width = Inches(1.1)

    # Add "Fat %" and "SNF %" headers
    table.rows[1].cells[5].text = "Fat %"
    paragraph = table.rows[1].cells[5].paragraphs[0]
    paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(9)
    tc_pr = table.rows[1].cells[5]._element.get_or_add_tcPr()
    v_align = OxmlElement('w:vAlign')
    v_align.set(qn('w:val'), 'center')
    tc_pr.append(v_align)

    table.rows[1].cells[6].text = "SNF %"
    paragraph = table.rows[1].cells[6]
    paragraph.alignment = docx.enum.text.WD_ALIGN_PARAGRAPH.CENTER
    run = table.rows[1].cells[6].paragraphs[0].runs[0]
    run.font.name = 'Arial'
    run.font.size = Pt(9)
    tc_pr = table.rows[1].cells[6]._element.get_or_add_tcPr()
    v_align = OxmlElement('w:vAlign')
    v_align.set(qn('w:val'), 'center')
    tc_pr.append(v_align)

    # Fill the table with data for this page
    row_count = 0
    for idx, member in enumerate(members, start=1):
        row_cells = table.add_row().cells
        row_cells[0].text = str(idx)
        row_cells[1].text = member.get("name", "") or ""
        row_cells[2].text = str(member.get("membership_no", "")) or ""
        row_cells[3].text = str(member.get("milk_supplied", "")) or ""
        row_cells[4].text = str(member.get("total_qty_milk_supplied", "")) or ""
        row_cells[5].text = str(member.get("fat_percentage", "")) or ""
        row_cells[6].text = str(member.get("snf_percentage", "")) or ""
        
        row_cells[7].text = member.get("aadhaar", "") or ""
        row_cells[8].text = member.get("bank_name", "") or ""
        row_cells[9].text = member.get("branch_name", "") or ""
        row_cells[10].text = member.get("account_number", "") or ""
        row_cells[11].text = member.get("ifsc_code", "") or ""

        # Apply font to each cell
        for cell in row_cells:
            for paragraph in cell.paragraphs:
                for run in paragraph.runs:
                    run.font.name = 'Arial'
                    run.font.size = Pt(9)

            tc_pr = cell._element.get_or_add_tcPr()
            v_align = OxmlElement('w:vAlign')  # Create <w:vAlign> element
            v_align.set(qn('w:val'), 'center')  # Use the correct namespace with qn()
            tc_pr.append(v_align)

        tr = table.rows[-1]._tr  # Access the last added row's <w:tr> element
        trPr = tr.get_or_add_trPr()  # Get or add the row properties
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), '300') 
        trHeight.set(qn('w:hRule'), 'exact')
        trPr.append(trHeight)

        row_count += 1

    # Add empty rows if necessary (Ensure there are exactly 16 rows)
    rows_needed = 18 - row_count
    for _ in range(rows_needed):
        row_cells = table.add_row().cells
        for cell in row_cells:
            cell.text = ""  # Empty content
            tc_pr = cell._element.get_or_add_tcPr()
            v_align = OxmlElement('w:vAlign')  # Create <w:vAlign> element
            v_align.set(qn('w:val'), 'center')  # Center align vertically
            tc_pr.append(v_align)

        tr = table.rows[-1]._tr
        trPr = tr.get_or_add_trPr()
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), '300')  # Set row height to 400 twips (~0.28 inches)
        trHeight.set(qn('w:hRule'), 'exact')
        trPr.append(trHeight)

    return row_count  # Return the row count for pagination handling
