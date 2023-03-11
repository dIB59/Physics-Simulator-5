import sys
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QVBoxLayout, QLineEdit, QPushButton

app = QApplication(sys.argv)

# Create a QWidget and set its layout to a vertical box layout
widget = QWidget()
layout = QVBoxLayout()
widget.setLayout(layout)

# Create a QListWidget and add it to the layout
list_widget = QListWidget()
layout.addWidget(list_widget)

# Create a line edit and a button to add items to the list
line_edit = QLineEdit()
add_button = QPushButton("Add Item")

# Connect the button's clicked signal to a slot that adds the
# text from the line edit to the list widget
add_button.clicked.connect(lambda: list_widget.addItem(line_edit.text()))

# Add the line edit and button to the layout
layout.addWidget(line_edit)
layout.addWidget(add_button)

# Show the widget to the user
widget.show() 

# Create a button to delete items from the list
delete_button = QPushButton("Delete Item")

# Connect the button's clicked signal to a slot that deletes the
# currently selected item from the list
delete_button.clicked.connect(lambda: list_widget.takeItem(list_widget.currentRow()))
layout.addWidget(delete_button)

# Show the widget to the user
widget.show()

# Run the application
sys.exit(app.exec_())
