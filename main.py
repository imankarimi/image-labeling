from image_labeling.views import ImageLabelingView

# for build exe file run this command: pyinstaller --onefile --windowed --icon=static/img/icon.ico .\main.py
# then add database/image_labeling.db & static folder beside .exe file
if __name__ == '__main__':
    lb = ImageLabelingView()
    lb.mainloop()
