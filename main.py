from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.dialog import MDDialog
from kivymd.uix.progressbar import MDProgressBar
from kivymd.theming import ThemeManager
import os
import threading
from markitdown import MarkItDown

class MarkItDownApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.markitdown = MarkItDown()
        self.current_file = None
        self.conversion_result = ""

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"

        # 主布局
        main_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))

        # 顶部工具栏
        self.toolbar = MDTopAppBar(
            title="MarkItDown",
            elevation=4
        )
        main_layout.add_widget(self.toolbar)

        # 文件选择区域
        file_card = MDCard(
            size_hint=(1, None),
            height=dp(120),
            elevation=2,
            padding=dp(10)
        )

        file_layout = BoxLayout(orientation='vertical', spacing=dp(5))
        file_layout.add_widget(MDLabel(text="选择要转换的文件:", font_style="Body1", bold=True))

        file_select_layout = BoxLayout(orientation='horizontal', spacing=dp(5))
        self.file_path_input = MDTextField(
            hint_text="文件路径",
            readonly=True,
            size_hint_x=0.7
        )
        file_select_layout.add_widget(self.file_path_input)

        self.select_file_btn = MDRaisedButton(
            text="选择文件",
            size_hint_x=0.3
        )
        self.select_file_btn.bind(on_press=self.show_file_chooser)
        file_select_layout.add_widget(self.select_file_btn)

        file_layout.add_widget(file_select_layout)
        file_card.add_widget(file_layout)
        main_layout.add_widget(file_card)

        # 转换按钮
        self.convert_btn = MDRaisedButton(
            text="转换为Markdown",
            size_hint=(1, None),
            height=dp(50),
            disabled=True
        )
        self.convert_btn.bind(on_press=self.convert_file)
        main_layout.add_widget(self.convert_btn)

        # 进度条
        self.progress_bar = MDProgressBar(size_hint=(1, None), height=dp(4), value=0)
        self.progress_bar.opacity = 0  # 初始隐藏
        main_layout.add_widget(self.progress_bar)

        # 结果显示区域
        result_card = MDCard(
            size_hint=(1, 1),
            elevation=2,
            padding=dp(10)
        )

        result_layout = BoxLayout(orientation='vertical', spacing=dp(5))

        result_header = BoxLayout(orientation='horizontal', size_hint=(1, None), height=dp(40))
        result_header.add_widget(MDLabel(text="转换结果:", font_style="Body1", bold=True))

        self.copy_btn = MDFlatButton(
            text="复制",
            disabled=True
        )
        self.copy_btn.bind(on_press=self.copy_result)
        result_header.add_widget(self.copy_btn)

        result_layout.add_widget(result_header)

        # 结果文本区域
        scroll_view = ScrollView(size_hint=(1, 1))
        self.result_text = MDLabel(
            text="请先选择文件并点击转换...",
            font_style="Body2",
            size_hint_y=None,
            markup=True
        )
        self.result_text.bind(texture_size=self.result_text.setter('size'))
        scroll_view.add_widget(self.result_text)
        result_layout.add_widget(scroll_view)

        result_card.add_widget(result_layout)
        main_layout.add_widget(result_card)

        # 初始化文件管理器
        self.file_manager = MDFileManager(
            exit_manager=self.exit_file_manager,
            select_path=self.select_file
        )

        return main_layout

    def show_file_chooser(self, instance):
        self.file_manager.show(os.path.expanduser("~"))

    def exit_file_manager(self, *args):
        self.file_manager.close()

    def select_file(self, path):
        self.current_file = path
        self.file_path_input.text = path
        self.convert_btn.disabled = False
        self.file_manager.close()

    def convert_file(self, instance):
        if not self.current_file:
            return

        # 显示进度条
        self.progress_bar.opacity = 1
        self.progress_bar.value = 0
        self.convert_btn.disabled = True
        self.result_text.text = "正在转换中..."

        # 在后台线程中执行转换
        threading.Thread(target=self._convert_file_thread).start()

    def _convert_file_thread(self):
        try:
            # 更新进度
            self.progress_bar.value = 50

            # 执行转换
            result = self.markitdown.convert(self.current_file)

            # 更新进度
            self.progress_bar.value = 100

            # 更新UI
            self.conversion_result = result.text_content
            self.result_text.text = self.conversion_result
            self.copy_btn.disabled = False

        except Exception as e:
            self.result_text.text = f"转换失败: {str(e)}"
        finally:
            # 隐藏进度条
            self.progress_bar.opacity = 0
            self.convert_btn.disabled = False

    def copy_result(self, instance):
        if self.conversion_result:
            Clipboard.copy(self.conversion_result)

if __name__ == '__main__':
    MarkItDownApp().run()