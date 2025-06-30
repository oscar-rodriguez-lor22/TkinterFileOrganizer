import os
import tkinter as tk
from tkinter import filedialog, messagebox

class FileOrganizerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("600x600")
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.directory_path = ''
        self.organization_mode = ''
        self.bool_organized = False
        self.build_menu()

    def build_menu(self):
      # Menu Frame
      menu = tk.Frame(self.container)
      menu_label = tk.Label(menu, text="Menu", font=("none", 20))
      menu_label.pack(anchor="center", pady=20)

      # Set Directory Frame
      directory_frame = tk.Frame(menu)
      set_directory_button = tk.Button(directory_frame, text="Set Directory", width=20, command=self.set_directory_path)
      set_directory_button.pack(expand=True, side="left")
      directory_info = tk.Button(directory_frame, text="Info", command=lambda:messagebox.showinfo("Information", f"Current Directory: {self.directory_path}"))
      directory_info.pack(expand=True, side="right")
      directory_frame.pack(pady=3)

      # Set Organization Mode Frame
      set_organization_mode_frame = tk.Frame(menu)
      set_organization_mode_button = tk.Button(set_organization_mode_frame, text="Set Organization Mode", width=20, command=self.set_organization_mode)

      set_organization_mode_button.grid(column=0, row=0, sticky='w')
      organization_info_button = tk.Button(set_organization_mode_frame, text="Info", command=lambda:messagebox.showinfo("Information", f"Organization Mode: {self.organization_mode}"))
      organization_info_button.grid(column=1, row=0, sticky="e")
      set_organization_mode_frame.pack(pady=3)

      # Organize Files Frame
      organize_files_frame = tk.Frame(menu)
      organize_files_button = tk.Button(organize_files_frame, text="Organize Files", width=20, command=self.organize_files)
      organize_files_button.grid(column=0, row=0, sticky='w')
      is_organized_info = tk.Button(organize_files_frame, text="Info", command=lambda:messagebox.showinfo("Information", f"Is Organized: {self.bool_organized}"))
      is_organized_info.grid(column=1, row=0, sticky="e")
      organize_files_frame.pack(pady=3)

      menu.pack(fill="both", expand=True)

    def set_directory_path(self): 
      potential_directory_path = filedialog.askdirectory(title="Select a Directory")
      if (self.directory_check(potential_directory_path)):
        self.directory_path = potential_directory_path
        messagebox.showinfo("Information", f"Directory set to: {self.directory_path}")
      else:
        messagebox.showerror("Error", "Directory not set")

    def directory_check(self, directory_path):
      return directory_path != '' and os.path.exists(directory_path)

    def set_organization_mode(self):
      organization_mode_popup = tk.Toplevel(self, bg="white")
      organization_mode_popup.title("Set Organization Mode")
      organization_mode_popup.geometry("400x400")

      set_organization_mode_popup_frame = tk.Frame(organization_mode_popup, bg='white')
      set_organization_mode_label = tk.Label(
        set_organization_mode_popup_frame, 
        text="Set Organization Mode", 
        font=("none", 20), bg='white'
      )
      set_organization_mode_label.pack()
      alphabetically_button = tk.Button(
        set_organization_mode_popup_frame,
        text="Alphabetically", 
        width=20, 
        command=lambda:self.set_organization_mode_helper(
          organization_mode_popup, 
          "alphabetically"
        )
      ) 
      alphabetically_button.pack(pady=3)
      file_type_button = tk.Button(
        set_organization_mode_popup_frame,
        text="By File Type",
        width=20, 
        command=lambda:self.set_organization_mode_helper(
          organization_mode_popup, 
          "file_type"
        )
      ) 
      file_type_button.pack(pady=3)
      file_size_button = tk.Button(
        set_organization_mode_popup_frame,
        text="By File Size", 
        width=20, 
        command=lambda:self.set_organization_mode_helper(
          organization_mode_popup, 
          "file_size"
        )
      ) 
      file_size_button.pack(pady=3)
      set_organization_mode_popup_frame.pack()

    def set_organization_mode_helper(self, organization_mode_popup, organization_mode):
      try:
        self.organization_mode = organization_mode
      except Exception as e:
        messagebox.showinfo("Error", f"Error: {e}")
        return
      messagebox.showinfo("Information", f"Organization Mode set to: {self.organization_mode}")
      organization_mode_popup.destroy()

    def organize_files(self):
      if self.directory_path == '':
        messagebox.showwarning("Warning", "Please set a directory")
        return
      if self.organization_mode == '':
        messagebox.showwarning("Warning", "Please set an organization mode")
        return

      match self.organization_mode:
        case "alphabetically":
          self.organize_files_alphabetically()
        case "file_type":
          self.organize_files_file_type()
        case "file_size":
          self.organize_files_file_size()

    def organize_files_alphabetically(self):
      # creating folders for each letter, 0-9, and special characters
      try: 
        for letter in range(65, 91):
          folder_path = os.path.join(self.directory_path, chr(letter))
          if not os.path.exists(folder_path):
            os.mkdir(folder_path)

        folders_to_create = ["0-9", "special-characters"]
        for folder in folders_to_create:
          folder_path = os.path.join(self.directory_path, folder)
          if not os.path.exists(folder_path):
            os.mkdir(folder_path)
      except Exception as e:
        messagebox.showerror("Error", f"Error creating folders: {e}")
        return

      # move files to their respective folders
      try:
        files = os.listdir(self.directory_path)
        for file in files:
          file_path = os.path.join(self.directory_path, file)

          if os.path.isdir(file_path):
            continue

          first_char = file[0]

          if first_char.isalpha():
            destination = os.path.join(self.directory_path, first_char.upper(), file)
            os.rename(file_path, destination)
          elif first_char.isdigit():
            destination = os.path.join(self.directory_path, "0-9", file)
            os.rename(file_path, destination)
          else:
            destination = os.path.join(self.directory_path, "special-characters", file)
            os.rename(file_path, destination)

        self.bool_organized = True
        messagebox.showinfo("Success", "Files organized alphabetically!")
      except Exception as e:
        messagebox.showerror("Error", f"Could not sort files: {e}")
        self.bool_organized = False

    def organize_files_file_type(self):
      file_types = {}

      # get all file types in directory, populate file_types dictionary
      try:
        for file in os.listdir(self.directory_path):
          file_path = os.path.join(self.directory_path, file)
          if os.path.isfile(file_path):
            filename, extension = os.path.splitext(file)
            if extension:
              extension = extension[1:]
            else:
              extension = "no_extension"
            if extension not in file_types:
              file_types[extension] = []
            file_types[extension].append(file)
      except Exception as e:
        messagebox.showerror("Error", f"Could not collect all filetypes: {e}")

      # create folders for each file type
      try:
        for file_type in file_types:
          folder_path = os.path.join(self.directory_path, file_type)
          if not os.path.exists(folder_path):
            os.mkdir(folder_path)
      except Exception as e:
        messagebox.showerror("Error", f"Could not creat folders for each file type: {e}")

      # moving files to their respective folders
      try:
        for file_type, files in file_types.items():
          for file in files:
            file_path = os.path.join(self.directory_path, file)
            destination = os.path.join(self.directory_path, file_type, file)
            os.rename(file_path, destination)
        self.bool_organized = True
        messagebox.showinfo("Success", "Files organized by file type!")
      except Exception as e:
        messagebox.showerror("Error", f"An error occured: {e}")

    def organize_files_file_size(self):
      # create folders for each size range
      try:
        size_ranges = ["0KB-1MB", "1MB-10MB", "10MB-100MB", "100MB-1GB", "1GB+"]
        for size_range in size_ranges:
          folder_path = os.path.join(self.directory_path, size_range)
          if not os.path.exists(folder_path):
            os.mkdir(folder_path)
      except Exception as e:
        messagebox.showerror("Error", f"Could not create size folders : {e}")

      # move files to their respective folders
      try:
        for file in os.listdir(self.directory_path):
          file_path = os.path.join(self.directory_path, file)
          if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            if file_size <= 1024 * 1024:
              destination = os.path.join(self.directory_path, "0KB-1MB", file)
              os.rename(file_path, destination)
              continue
            if file_size <= 1024 * 1024 * 10:
              destination = os.path.join(self.directory_path, "1MB-10MB", file)
              os.rename(file_path, destination)
              continue
            if file_size <= 1024 * 1024 * 100:
              destination = os.path.join(self.directory_path, "10MB-100MB", file)
              os.rename(file_path, destination)
            if file_size <= 1024 * 1024 * 1024:
              destination = os.path.join(self.directory_path, "100MB-1GB", file)
              os.rename(file_path, destination)
            if file_size > 1024 * 1024 * 1024:
              destination = os.path.join(self.directory_path, "1GB+", file)
              os.rename(file_path, destination)
        self.bool_organized = True
        messagebox.showinfo("Success", "Files organized by file size!")
      except Exception as e:
        messagebox.showerror("Error", f"An error occured: {e}")

if __name__ == "__main__":
  app = FileOrganizerApp()
  app.mainloop()
