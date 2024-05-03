import tkinter as tk
from tkinter import messagebox, Toplevel, Label, Entry, Button, Listbox, Scrollbar, Frame
from datetime import datetime
import pickle

def save_data(entities, project3):
    with open(project, 'wb') as file:
        pickle.dump(entities, file)

def load_data(project3):
    try:
        with open(project3, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}


class Person:
    def __init__(self, id, name, address, contact_details):
        self.id = id
        self.name = name
        self.address = address
        self.contact_details = contact_details

    def get_details(self):
        return f"ID: {self.id}\nName: {self.name}\nAddress: {self.address}\nContact: {self.contact_details}"
class Employee(Person):
    def __init__(self, id, name, address, contact_details, employee_id, department, job_title, basic_salary, age, dob, passport):
        super().__init__(id, name, address, contact_details)
        self.employee_id = employee_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.dob = dob
        self.passport = passport

    def get_details(self):
        details = super().get_details()
        return f"{details}\nEmployee ID: {self.employee_id}\nDepartment: {self.department}\nJob Title: {self.job_title}\nSalary: ${self.basic_salary}\nAge: {self.age}\nDOB: {self.dob}\nPassport: {self.passport}"

class Client(Person):
    def __init__(self, id, name, address, contact_details, budget):
        super().__init__(id, name, address, contact_details)
        self.budget = budget

    def get_details(self):
        details = super().get_details()
        return f"{details}\nBudget: ${self.budget}"

class Guest(Person):
    def __init__(self, id, name, address, contact_details):
        super().__init__(id, name, address, contact_details)

class Invoice:
    def __init__(self, invoice_id, amount, date):
        self.invoice_id = invoice_id
        self.amount = amount
        self.date = date

class Event:
    def __init__(self, id, type, theme, date, time, duration, venue_address, client_id, guest_list, suppliers, invoice):
        self.id = id
        self.type = type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_address = venue_address
        self.client_id = client_id
        self.guest_list = guest_list
        self.suppliers = suppliers
        self.invoice = invoice  # Make sure this is an Invoice object

    def get_details(self):
        client_name = entities['clients'][self.client_id].name if self.client_id in entities['clients'] else "Unknown Client"
        event_name = self.type if self.type else "N/A"

        # Ensure guest_list is always a list
        guest_list = [self.guest_list] if isinstance(self.guest_list, int) else self.guest_list

        # Handling guest names
        guests = []
        for guest_id in guest_list:
            guest_name = entities['guests'].get(guest_id, None)
            if guest_name:
                guests.append(guest_name.name)
        guest_str = ', '.join(guests) if guests else "N/A"

        # Ensure supplier list is always a list
        supplier_list = [self.suppliers] if isinstance(self.suppliers, int) else self.suppliers

        # Handling supplier names
        suppliers = []
        for supplier_id in supplier_list:
            supplier_name = entities['suppliers'].get(supplier_id, None)
            if supplier_name:
                suppliers.append(supplier_name.name)
        supplier_str = ', '.join(suppliers) if suppliers else "N/A"

        return f"Event Name: {event_name}\nEvent ID: {self.id}\nType: {self.type}\nTheme: {self.theme}\nDate: {self.date}\nTime: {self.time}\nDuration: {self.duration} hours\nVenue: {self.venue_address}\nClient: {client_name}\nGuest List: {guest_str}\nSuppliers: {supplier_str}\nInvoice: {self.invoice}"
class Supplier(Person):
    def __init__(self, id, name, address, contact_details, service_details):
        super().__init__(id, name, address, contact_details)
        self.service_details = service_details

    def get_details(self):
        details = super().get_details()
        return f"{details}\nService Details: {self.service_details}"

class Venue:
    def __init__(self, id, name, address, contact, min_guests, max_guests):
        self.id = id
        self.name = name
        self.address = address
        self.contact = contact
        self.min_guests = min_guests
        self.max_guests = max_guests

    def get_details(self):
        return f"Venue ID: {self.id}\nName: {self.name}\nAddress: {self.address}\nContact: {self.contact}\nMin Guests: {self.min_guests}\nMax Guests: {self.max_guests}"
def save_all_data():
    save_data(entities['employees'], 'employees.pkl')
    save_data(entities['clients'], 'clients.pkl')
    save_data(entities['guests'], 'guests.pkl')
    save_data(entities['suppliers'], 'suppliers.pkl')
    save_data(entities['venues'], 'venues.pkl')
    save_data(entities['events'], 'events.pkl')

def load_all_data():
    entities['employees'] = load_data('employees.pkl')
    entities['clients'] = load_data('clients.pkl')
    entities['guests'] = load_data('guests.pkl')
    entities['suppliers'] = load_data('suppliers.pkl')
    entities['venues'] = load_data('venues.pkl')
    entities['events'] = load_data('events.pkl')
entities = {
    'employees': {},
    'clients': {},
    'guests': {},
    'events': {},
    'suppliers': {},
    'venues': {}
}

def add_initial_data():
    entities['employees'][1] = Employee(1, "Sara AlDhaheri", "113 Jumeirah St", "555-1234", "E001", "Sales", "Sales Manager", 50000, 30, "1988-05-01", "AB1234567")
    entities['clients'][1] = Client(1, "Falah Corp", "456 Yas Island Rd", "555-5678", 100000)
    entities['guests'][1] = Guest(1, "Mariam Al Hashimi", "789 Marina Walk", "555-8765")
    entities['suppliers'][1] = Supplier(1, "Royal Catering", "321 Corniche Rd", "555-4321", "Full menu catering")
    entities['venues'][1] = Venue(1, "Emirates Palace", "101 Khalifa St", "555-1010", 50, 200)
    entities['events'][1] = Event(1, "Wedding", "Vintage", "2023-09-15", "14:00", 4, "Emirates Palace", 1, [1], [1], "Invoice123")
class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Management System")
        self.create_main_menu()

    def create_main_menu(self):
        for entity_type in entities:
            btn = Button(self.root, text=f"Manage {entity_type.capitalize()}", command=lambda et=entity_type: self.manage_entity(et))
            btn.pack(fill=tk.X, padx=20, pady=5)

    def manage_entity(self, entity_type):
        top = Toplevel(self.root)
        top.title(f"Manage {entity_type.capitalize()}")
        self.list_entities(top, entity_type)

    def list_entities(self, top, entity_type):
        frame = Frame(top)
        frame.pack(fill=tk.BOTH, expand=True)

        listbox = Listbox(frame, width=50, height=10)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient="vertical")
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox.config(yscrollcommand=scrollbar.set)

        if entity_type == 'events':
            for id, event in entities[entity_type].items():
                client_name = entities['clients'][event.client_id].name if event.client_id in entities[
                    'clients'] else "Unknown Client"
                display_text = f"{id}: {event.type} - {client_name}"
                listbox.insert(tk.END, display_text)
        else:
            for id, entity in entities[entity_type].items():
                listbox.insert(tk.END, f"{id}: {entity.name if hasattr(entity, 'name') else 'N/A'}")

        Button(top, text="Add New", command=lambda: self.add_update_entity(top, entity_type, None, listbox)).pack(
            pady=10)
        Button(top, text="Edit Selected", command=lambda: self.execute_selected_action(
            lambda: self.add_update_entity(top, entity_type, listbox.get(listbox.curselection()), listbox),
            listbox)).pack(pady=5)
        Button(top, text="Delete Selected", command=lambda: self.execute_selected_action(
            lambda: self.delete_entity(entity_type, listbox.get(listbox.curselection()).split(':')[0], listbox),
            listbox)).pack(pady=5)
        Button(top, text="View Details", command=lambda: self.execute_selected_action(
            lambda: self.show_details(entity_type, listbox.get(listbox.curselection()).split(':')[0]), listbox)).pack(
            pady=5)

    def execute_selected_action(self, action, listbox):
        try:
            action()
        except tk.TclError:
            messagebox.showerror("Selection Error", "Please select an item to proceed.")
    def add_update_entity(self, parent, entity_type, selected, listbox):
        top = Toplevel(parent)
        top.title("Add / Update Entity")
        id = None
        entries = {}
        fields = {
            'employees': ['name', 'address', 'contact_details', 'employee_id', 'department', 'job_title', 'basic_salary', 'age', 'dob', 'passport'],
            'clients': ['name', 'address', 'contact_details', 'budget'],
            'guests': ['name', 'address', 'contact_details'],
            'events': ['type', 'theme', 'date', 'time', 'duration', 'venue_address', 'client_id', 'guest_list', 'suppliers', 'invoice'],
            'suppliers': ['name', 'address', 'contact_details', 'service_details'],
            'venues': ['name', 'address', 'contact', 'min_guests', 'max_guests']
        }[entity_type]

        for field in fields:
            Label(top, text=f"{field.replace('_', ' ').title()}:").pack()
            entry = Entry(top)
            entry.pack()
            entries[field] = entry

        if selected:
            id, _ = selected.split(': ')
            entity = entities[entity_type][int(id)]
            for field in fields:
                entries[field].insert(0, getattr(entity, field, ''))

        Button(top, text="Submit", command=lambda: self.submit_entity(top, entity_type, id, entries, listbox)).pack()

    def submit_entity(self, top, entity_type, id, entries, listbox):
        if id:
            entity = entities[entity_type][int(id)]
            for field, entry in entries.items():
                if field not in ['guest_list', 'suppliers']:
                    setattr(entity, field, entry.get())
                else:
                    setattr(entity, field, eval(entry.get()))
        else:
            new_id = max(entities[entity_type].keys(), default=0) + 1
            if entity_type == 'employees':
                entities[entity_type][new_id] = Employee(new_id, entries['name'].get(), entries['address'].get(), entries['contact_details'].get(), entries['employee_id'].get(), entries['department'].get(), entries['job_title'].get(), int(entries['basic_salary'].get()), int(entries['age'].get()), entries['dob'].get(), entries['passport'].get())
            elif entity_type == 'clients':
                entities[entity_type][new_id] = Client(new_id, entries['name'].get(), entries['address'].get(), entries['contact_details'].get(), float(entries['budget'].get()))
            elif entity_type == 'guests':
                entities[entity_type][new_id] = Guest(new_id, entries['name'].get(), entries['address'].get(), entries['contact_details'].get())
            elif entity_type == 'events':
                client_id = int(entries['client_id'].get())
                guest_list = eval(f"[{entries['guest_list'].get()}]") if entries['guest_list'].get() else []
                supplier_ids = eval(f"[{entries['suppliers'].get()}]") if entries['suppliers'].get() else []
                suppliers = [entities['suppliers'][supplier_id] for supplier_id in supplier_ids]
                entities[entity_type][new_id] = Event(new_id, entries['type'].get(), entries['theme'].get(), entries['date'].get(), entries['time'].get(), int(entries['duration'].get()), entries['venue_address'].get(), client_id, guest_list, suppliers, None)
            elif entity_type == 'suppliers':
                entities[entity_type][new_id] = Supplier(new_id, entries['name'].get(), entries['address'].get(), entries['contact_details'].get(), entries['service_details'].get())
            elif entity_type == 'venues':
                entities[entity_type][new_id] = Venue(new_id, entries['name'].get(), entries['address'].get(), entries['contact'].get(), int(entries['min_guests'].get()), int(entries['max_guests'].get()))
            listbox.insert(tk.END, f"{new_id}: {entries['name'].get()}")
        save_all_data()  # Save data after changes
        messagebox.showinfo("Success", "Entity saved successfully!")
        top.destroy()

    def delete_entity(self, entity_type, id, listbox):
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this entity?"):
            del entities[entity_type][int(id)]
            listbox.delete(listbox.curselection())
            save_all_data()  # Save data after deletion
            messagebox.showinfo("Success", "Entity deleted successfully!")

    def show_details(self, entity_type, id):
        entity = entities[entity_type][int(id)]
        details = entity.get_details()
        messagebox.showinfo(f"{entity_type.capitalize()} Details", details)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    add_initial_data()
    load_all_data()  # Load existing data from files
    root.mainloop()
