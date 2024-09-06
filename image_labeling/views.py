import glob
import os
import re
import threading
import time
from functools import partial
from tkinter import filedialog, messagebox

from PIL import ImageTk, Image
from ttkbootstrap import Frame, Window, Label, Button, NE, LabelFrame, Entry, END, Spinbox, NW, Combobox

from image_labeling.models import FilePath, ImageLabel

FILE_FILTER_EXTENSIONS = ['.png', '.jpeg', '.jpg']
FILE_IGNORE_PARAM = ','
SHOW_OFFSET = 20

COLOR_LIST = ['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'primary-outline',
              'secondary-outline', 'success-outline', 'info-outline', 'warning-outline', 'danger-outline',
              'light-outline', 'dark-outline']


class ImageLabelingView(Window):
    current_frame = None

    def __init__(self, *args, **kwargs):
        kwargs['themename'] = "superhero"
        super().__init__(*args, **kwargs)

        self.container = Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.title("Image Labeling")
        self.iconbitmap("static/img/icon.ico")
        self.show_frame(MainView)

    def show_frame(self, view_class):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = view_class(self.container, controller=self)
        self.current_frame.run_win()
        self.current_frame.pack(fill="both", expand=True)


class MainView(Frame):
    controller = None
    setting_icon = None
    competed_img = None
    nodata_img = None

    images_path = []
    image_list = []
    current_image_path = None
    current_image = None
    image_name_label = None
    image_paginate_label = None
    counter = 0

    label_buttons = None
    data_dir = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        self.setting_icon = ImageTk.PhotoImage(Image.open("static/img/setting.png").resize((25, 25)))
        self.competed_img = ImageTk.PhotoImage(Image.open("static/img/completed.png").resize((700, 475)))
        self.nodata_img = ImageTk.PhotoImage(Image.open("static/img/nodata.png").resize((700, 475)))
        self.undo_img = ImageTk.PhotoImage(Image.open("static/img/undo.png").resize((25, 25)))

    def run_win(self):
        # Fetch settings (this can stay in the main thread)
        self.fetch_settings()

        # Display loading label
        self.loading_label = Label(self, text="Loading data, please wait...", font=("Verdana", 12), bootstyle="info")
        self.loading_label.pack(padx=20, pady=20)

        # Start a new thread to load data
        threading.Thread(target=self.load_data_with_loading, daemon=True).start()

    def load_data_with_loading(self):
        """Load data in a separate thread and update UI when done."""
        self.extract_data()  # Extract available image paths

        self.load_data()  # Actually load the images into the list

        # Simulate loading time (optional, for testing)
        time.sleep(2)  # Remove or adjust this in real-world use

        # Load data and update the UI in the main thread
        self.after(0, self.on_data_loaded)

    def on_data_loaded(self):
        """Update the UI after data is loaded."""
        # Remove the loading label
        self.loading_label.destroy()

        # Continue with your existing code to display images and controls
        if self.image_list:
            self.current_image_path, self.current_image = self.image_list[0]

        if self.current_image:
            undo_button = Button(self, bootstyle="warning-outline", image=self.undo_img, command=self.undo_image)
            undo_button.pack(anchor=NW)

        label = Label(self, text="Image Labeling", font=("Verdana", 15))
        label.pack(pady=(0, 0))

        setting_button = Button(self, bootstyle="light", image=self.setting_icon,
                                command=lambda: self.controller.show_frame(SettingView))
        setting_button.pack(anchor=NE)

        if self.current_image:
            file_name = self.current_image_path.split("\\")[-1]
            self.image_name_label = Label(self, text=f"File Name: {file_name}", bootstyle="inverse-dark",
                                          font=("Verdana", 10))
            self.image_name_label.pack(padx=(0, 0), pady=(10, 0))
            self.image_label = Label(self, image=self.current_image)
            self.image_label.pack(pady=(0, 5), padx=20)

            self.image_paginate_label = Label(self, text=f"Image 1 of {len(self.images_path)}",
                                              bootstyle="inverse-light", font=("Helvetica", 12))
            self.image_paginate_label.pack()

            btn_frame = Frame(self, name='btn_frame')
            btn_frame.pack()

            col = 0
            for pk, code, name, color_code in self.label_buttons:
                command_action = partial(self.change_image, code)
                btn = Button(btn_frame, text=name, bootstyle=color_code, command=command_action)
                btn.grid(row=0, column=col, sticky="news", padx=5, pady=30)
                col += 1
        else:
            self.image_label = Label(self, image=self.nodata_img)
            self.image_label.pack(pady=20, padx=20)

    def change_image(self, code=None, is_undo=False):
        if not is_undo:
            # set image label
            self.set_label(self.current_image_path, code)

        if self.counter < len(self.image_list) - 1:
            self.counter += 1

            self.current_image_path, self.current_image = self.image_list[self.counter]
            file_name = self.current_image_path.split("\\")[-1]
            if len(self.image_list) >= SHOW_OFFSET:
                action_idx = self.image_list.index(self.image_list[-5])
                if self.counter == action_idx:
                    self.load_data(self.counter + 5, SHOW_OFFSET)

            self.image_name_label.config(text=f"File Name: {file_name}")
            self.image_label.config(image=self.current_image)
            self.image_paginate_label.config(text=f"Image {self.counter + 1} of {len(self.images_path)}")
        else:
            # complete data labeling
            self.image_label.config(image=self.competed_img)
            self.image_name_label.destroy()
            self.image_paginate_label.destroy()

            # remove label buttons
            self.nametowidget('btn_frame').destroy()

            # remove label info
            self.image_paginate_label.destroy()

    def undo_image(self):
        if self.counter <= 0:
            messagebox.showerror("Error Occurred", "You can't undo more than this.")
        else:
            answer = messagebox.askyesno(title='Undo Confirmation', message='Are you sure that you want to undo?')
            if answer:
                self.counter -= 2 if self.counter > -1 else 0
                self.change_image(is_undo=True)

    def extract_number(self, filename):
        # Regular expression to match the leading number in the file name
        match = re.match(r'(\d+)', filename)  # Extract the leading number
        return int(match.group(1)) if match else 0  # Return 0 if no number found

    def extract_data(self):
        self.image_list = []
        self.images_path = []

        if self.data_dir:
            if not os.path.isdir(self.data_dir):
                messagebox.showerror("Error Occurred",
                                     f"Error Occurred While Extracting Data, the {self.data_dir} does not exist. please make sure this file is exist.")
                return

            files = os.listdir(self.data_dir)
            files = sorted(files, key=self.extract_number)
            for file_name in files:
                name, ext = os.path.splitext(file_name)
                file_path = os.path.join(self.data_dir, file_name)
                if ext in FILE_FILTER_EXTENSIONS and name.find(FILE_IGNORE_PARAM) < 0 and os.path.isfile(file_path):
                    self.images_path.append(file_path)

    def load_data(self, limit=0, offset=SHOW_OFFSET):
        for img_path in self.images_path[limit:limit + offset]:
            self.image_list.append((img_path, ImageTk.PhotoImage(Image.open(img_path).resize((1300, 825)))))

    def fetch_settings(self):
        paths = FilePath.fetch()
        __, self.data_dir = paths[0] if paths else (None, None)
        self.label_buttons = ImageLabel.fetch()

    def set_label(self, file_path, code):
        """
        set label for all file_path and like it
        :param file_path: this field specific the file path
        :param code: this field specific the label code
        :return:
        """

        base_dir, file_name = tuple(file_path.split('\\'))
        name, extension = os.path.splitext(file_name)
        file_likes = glob.glob(f"{base_dir}/{name}*")

        for file in file_likes:
            __, _sub_filename = tuple(file.split('\\'))
            sub_name, sub_ext = os.path.splitext(_sub_filename)
            sub_name = sub_name.split(',')[0]
            new_file = f"{base_dir}\\{sub_name},{code}{sub_ext}"

            try:
                os.rename(file, new_file)
            except Exception as e:
                messagebox.showerror("Error Occurred: Rename File", str(e))
                return


class SettingView(Frame):
    controller = None
    add_label_btn = None
    label_attr_entries = {}
    label_attr_row = 1

    labels = None
    file_path = None

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        self.controller = controller

        self.back_arrow = ImageTk.PhotoImage(Image.open("static/img/back_arrow.png").resize((20, 20)))
        self.trash_img = ImageTk.PhotoImage(Image.open("static/img/trash.png").resize((16, 16)))
        self.add_img = ImageTk.PhotoImage(Image.open("static/img/plus.png").resize((16, 16)))

    def run_win(self):
        self.label_attr_entries = {}
        self.load_data()

        label = Label(self, text="Settings", font=("Verdana", 15))
        label.pack(pady=(20, 0))

        back_btn = Button(self, bootstyle="secondary-outline", image=self.back_arrow,
                          command=lambda: self.controller.show_frame(MainView))
        back_btn.pack(anchor=NW, padx=20)

        setting_frame = Frame(self, name='setting_frame')
        setting_frame.pack()

        # Data Info
        data_conf_frame = LabelFrame(setting_frame, text="Data Configration", name='data_conf_frame')
        data_conf_frame.grid(row=0, column=0, sticky="news", padx=20, pady=20)

        data_path_label = Label(data_conf_frame, text="Data Folder: ")
        data_path_label.grid(row=0, column=0)
        dir_path_entry = Entry(data_conf_frame, text="dir_path", width=50)
        if self.file_path:
            pk, file_path = self.file_path
            dir_path_entry.delete(0, END)
            dir_path_entry.insert(0, file_path)
        dir_path_choose = Button(data_conf_frame, text='Choose',
                                 command=lambda: self.choose_data_folder(dir_path_entry))
        dir_path_choose.grid(row=0, column=1)
        dir_path_entry.grid(row=0, column=2)

        for widget in data_conf_frame.winfo_children():
            widget.grid_configure(padx=5, pady=10)

        # Data Labels
        label_frame = LabelFrame(setting_frame, text="Data Labels", name='label_frame')
        label_frame.grid(row=1, column=0, sticky="news", padx=20, pady=10)

        if not self.labels:
            self.set_label_setting_form(label_frame, row_id=0, code=1)
        else:
            self.label_attr_row = len(self.labels) + 1

            # Exist Label
            for row_label in self.labels:
                row_id = self.labels.index(row_label)
                pk, code, name, color_code = row_label

                self.set_label_setting_form(label_frame, row_id=row_id, has_remove_btn=bool(row_id), code=code,
                                            name=name, color_code=color_code)

            self.label_attr_row = 0
            if self.label_attr_entries:
                self.label_attr_row = int(self.label_attr_entries[max(self.label_attr_entries)][1].get())

        self.add_label_btn = Button(label_frame, bootstyle="success-outline", image=self.add_img,
                                    command=lambda: self.add_label_attrs(label_frame))
        self.add_label_btn.grid(row=self.label_attr_row + 1, column=7, sticky="news", padx=20, pady=10)

        for widget in label_frame.winfo_children():
            widget.grid_configure(padx=5, pady=10)

        # Save button
        button = Button(setting_frame, text="Save Setting", bootstyle="info",
                        command=lambda: self.save_settings(setting_frame))
        button.grid(row=3, column=0, sticky="news", padx=20, pady=(20, 10))

    def load_data(self):
        paths = FilePath.fetch()
        self.file_path = paths[0] if paths else None
        self.labels = ImageLabel.fetch()

    def choose_data_folder(self, dir_path_entry):
        folder_selected = filedialog.askdirectory()
        dir_path_entry.delete(0, END)
        dir_path_entry.insert(0, folder_selected)

    def rem_label_attrs(self, row_id):
        for item in self.label_attr_entries.pop(row_id):
            if hasattr(item, 'delete'):
                item.delete(0, END)
            item.destroy()

        self.label_attr_row = 1
        if self.label_attr_entries:
            self.label_attr_row = int(self.label_attr_entries[max(self.label_attr_entries)][1].get())

    def add_label_attrs(self, frame):
        self.label_attr_row += 1
        self.set_label_setting_form(frame, row_id=self.label_attr_row, has_remove_btn=bool(self.label_attr_row))
        self.add_label_btn.grid(row=self.label_attr_row + 1, column=7, sticky="news", padx=20, pady=10)

    def set_label_setting_form(self, frame, row_id, has_remove_btn=False, **kwargs):
        code, name, color_code = kwargs.get('code'), kwargs.get('name'), kwargs.get('color_code')
        code = code if code else row_id

        code_label = Label(frame, text="Code: ")
        code_label.grid(row=row_id, column=0)
        code_entry = Spinbox(frame, text=f"code__{row_id}", from_=row_id, to=20)
        if code:
            code_entry.delete(0, END)
            code_entry.insert(0, code)
        code_entry.grid(row=row_id, column=1)

        name_label = Label(frame, text="Name: ")
        name_label.grid(row=row_id, column=2)
        name_entry = Entry(frame, text=f"name__{row_id}")
        if name:
            name_entry.delete(0, END)
            name_entry.insert(0, name)
        name_entry.grid(row=row_id, column=3)

        color_label = Label(frame, text="Color: ")
        color_label.grid(row=row_id, column=4)
        color_entry = Combobox(frame, text=f"color_code__{row_id}", values=COLOR_LIST)
        color_entry.grid(row=row_id, column=6)
        if color_code:
            color_entry.delete(0, END)
            color_entry.insert(0, color_code)

        remove_btn = None
        if has_remove_btn:
            remove_btn_command_action = partial(self.rem_label_attrs, row_id)
            remove_btn = Button(frame, bootstyle="danger-outline", image=self.trash_img,
                                command=remove_btn_command_action)
            remove_btn.grid(row=row_id, column=7)

        for widget in frame.winfo_children():
            widget.grid_configure(pady=10)

        if row_id > 0:
            self.label_attr_entries[row_id] = (
                code_label, code_entry, name_label, name_entry, color_label, color_entry, remove_btn)

    def save_settings(self, frame):
        self.load_data()

        res = {'file': {'dir_path': None}, 'labels': {'code': [], 'name': [], 'color_code': []}}
        for label_frame in frame.winfo_children():
            for attr in label_frame.winfo_children():
                if hasattr(attr, 'get'):
                    if attr.cget('text') == "dir_path":
                        res['file']['dir_path'] = attr.get()
                        if not attr.get():
                            messagebox.showerror("Required Field",
                                                 "The `Data Folder` field can not be empty, please fill it")
                            return
                    else:
                        name, num = tuple(attr.cget('text').split('__'))
                        if name in ("code", "name", "color_code"):
                            if not attr.get():
                                messagebox.showerror("Required Field",
                                                     f"The `{name}` field can not be empty, please fill it.")
                                return

                            if attr.get() in res['labels'][name]:
                                messagebox.showerror("Duplicate Field",
                                                     f"The `{name}` field is duplicate, please check it again.")
                                return

                            res['labels'][name].append(attr.get())

        if res['file']['dir_path']:
            if self.file_path:
                FilePath.delete([self.file_path])
            FilePath.insert(file_path=res['file']['dir_path'])

        labels = []
        if res['labels']:
            for i in range(len(res['labels']['code'])):
                labels.append(ImageLabel(**{'code': res['labels']['code'][i], 'name': res['labels']['name'][i],
                                            'color_code': res['labels']['color_code'][i]}))

        if labels:
            ImageLabel.delete(self.labels)
            ImageLabel.bulk_insert(labels)

        self.load_data()
        messagebox.showinfo("Success", "Saved setting successfully.")
