import json
import asyncio
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QTextEdit, QPushButton, QComboBox, QGroupBox, QFormLayout,
    QMessageBox, QSplitter, QDialog, QProgressBar
)
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

from utils.async_utils import GenerationThread, ProgressIndicator
from ui.components import AIGenerateDialog


class OutlineEditTab(QWidget):
    """总大纲编辑标签页"""

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.outline = None

        # 初始化UI
        self._init_ui()

        # 加载大纲
        self._load_outline()

    def _init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)

        # 创建标题部分
        title_group = QGroupBox("小说标题")
        title_layout = QHBoxLayout()

        self.title_edit = QLineEdit()
        title_layout.addWidget(self.title_edit)

        self.title_ai_button = QPushButton("AI生成")
        self.title_ai_button.clicked.connect(lambda: self._generate_with_ai("标题", self.title_edit.text(), self.title_edit.setText))
        title_layout.addWidget(self.title_ai_button)

        title_group.setLayout(title_layout)
        main_layout.addWidget(title_group)

        # 创建中心思想部分
        theme_group = QGroupBox("中心思想")
        theme_layout = QVBoxLayout()

        self.theme_edit = QTextEdit()
        self.theme_edit.setMinimumHeight(80)
        theme_layout.addWidget(self.theme_edit)

        theme_button_layout = QHBoxLayout()
        theme_button_layout.addStretch()

        self.theme_ai_button = QPushButton("AI生成")
        self.theme_ai_button.clicked.connect(lambda: self._generate_with_ai("中心思想", self.theme_edit.toPlainText(), self.theme_edit.setPlainText))
        theme_button_layout.addWidget(self.theme_ai_button)

        theme_layout.addLayout(theme_button_layout)
        theme_group.setLayout(theme_layout)
        main_layout.addWidget(theme_group)

        # 创建故事梗概部分
        synopsis_group = QGroupBox("故事梗概")
        synopsis_layout = QVBoxLayout()

        self.synopsis_edit = QTextEdit()
        self.synopsis_edit.setMinimumHeight(150)
        synopsis_layout.addWidget(self.synopsis_edit)

        synopsis_button_layout = QHBoxLayout()
        synopsis_button_layout.addStretch()

        self.synopsis_ai_button = QPushButton("AI生成")
        self.synopsis_ai_button.clicked.connect(lambda: self._generate_with_ai("故事梗概", self.synopsis_edit.toPlainText(), self.synopsis_edit.setPlainText))
        synopsis_button_layout.addWidget(self.synopsis_ai_button)

        synopsis_layout.addLayout(synopsis_button_layout)
        synopsis_group.setLayout(synopsis_layout)
        main_layout.addWidget(synopsis_group)

        # 创建世界观设定部分
        world_group = QGroupBox("世界观设定")
        world_layout = QVBoxLayout()

        self.world_edit = QTextEdit()
        self.world_edit.setMinimumHeight(150)
        world_layout.addWidget(self.world_edit)

        world_button_layout = QHBoxLayout()
        world_button_layout.addStretch()

        self.world_ai_button = QPushButton("AI生成")
        self.world_ai_button.clicked.connect(lambda: self._generate_with_ai("世界观设定", self.world_edit.toPlainText(), self.world_edit.setPlainText))
        world_button_layout.addWidget(self.world_ai_button)

        world_layout.addLayout(world_button_layout)
        world_group.setLayout(world_layout)
        main_layout.addWidget(world_group)

        # 创建按钮部分
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.save_button = QPushButton("保存修改")
        self.save_button.clicked.connect(self._save_outline)
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

    def _load_outline(self):
        """加载大纲"""
        self.outline = self.main_window.get_outline()
        if not self.outline:
            return

        # 填充表单
        self.title_edit.setText(self.outline.get("title", ""))
        self.theme_edit.setPlainText(self.outline.get("theme", ""))
        self.synopsis_edit.setPlainText(self.outline.get("synopsis", ""))
        self.world_edit.setPlainText(self.outline.get("worldbuilding", ""))

    def _save_outline(self):
        """保存大纲"""
        if not self.outline:
            self.outline = {}

        # 更新大纲数据
        self.outline["title"] = self.title_edit.text()
        self.outline["theme"] = self.theme_edit.toPlainText()
        self.outline["synopsis"] = self.synopsis_edit.toPlainText()
        self.outline["worldbuilding"] = self.world_edit.toPlainText()

        # 保存大纲
        self.main_window.set_outline(self.outline)

        QMessageBox.information(self, "保存成功", "大纲修改已保存")

    def _generate_with_ai(self, field_name, current_text, set_func):
        """使用AI生成内容"""
        dialog = AIGenerateDialog(
            self,
            f"AI生成{field_name}",
            field_name,
            current_text
        )
        if dialog.exec() == QDialog.DialogCode.Accepted:
            result = dialog.get_result()
            if result:
                set_func(result)

    def update_outline(self):
        """更新大纲（供外部调用）"""
        self._load_outline()
