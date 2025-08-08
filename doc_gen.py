from docxtpl import DocxTemplate
import os

doc = DocxTemplate("invoice_template.docx")

invoice_list = [[2, "pen", 0.5, 1],
                [1, "paper pack", 5, 5],
                [2, "notebook", 2, 4]]


doc.render({"name":"john",
            "phone":"555-55555",
            "invoice_list": invoice_list,
            "subtotal":10,
            "salestax":"18%",
            "total":9})
doc.save("/Users/deepshikhasingh/Desktop/new_invoice.docx")
