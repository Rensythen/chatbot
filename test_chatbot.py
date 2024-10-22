# -*- coding: utf-8 -*-
# Commented out IPython magic to ensure Python compatibility.
%pip install panel
import panel as pn
import param

class ChatBotInterface(param.Parameterized):
    user_input = param.String(default="")
    selected_option = param.ObjectSelector(default="test1", objects=["test1", "test2", "test3"])
    chat_history = param.List(default=[])

    def __init__(self, **params):
        super().__init__(**params)
        self.result = ""
        self.chat_panels = []

    def submit_query(self, event=None):
        if not self.user_input.strip():
            return

        response = self.mock_backend_response(self.user_input, self.selected_option)

        self.chat_panels.append(
            pn.Row(
                pn.Spacer(width=20),
                pn.Column(
                    pn.pane.Markdown("**User:**", width=600),
                    pn.pane.HTML(f"<div style='background-color: #E8F0FE; padding: 10px; border-radius: 5px;'>{self.user_input}</div>", width=600)
                ),
                pn.Spacer(width=20)
            )
        )
        self.chat_panels.append(
            pn.Row(
                pn.Spacer(width=20),
                pn.Column(
                    pn.pane.Markdown("**ChatBot:**", width=600),
                    pn.pane.HTML(f"<div style='background-color: #F6F6F6; padding: 10px; border-radius: 5px;'>{response}</div>", width=600)
                ),
                pn.Spacer(width=20)
            )
        )

        self.user_input = ""
        self.update_display()

    def update_display(self):
        chat_display.objects = list(self.chat_panels)

    def mock_backend_response(self, query, option):
        return f"Simulated response to '{query}' with option '{option}'."

    def view(self):
        input_box = pn.widgets.TextInput(name="", placeholder="Type your question...", sizing_mode="stretch_width")
        input_box.link(self, value='user_input')

        dropdown = pn.widgets.Select(name="", options=["test1", "test2", "test3"], width=150)
        dropdown.link(self, value='selected_option')

        submit_button = pn.widgets.Button(name="Submit", button_type="primary", width=100)
        submit_button.on_click(self.submit_query)

        global chat_display
        chat_display = pn.Column(*self.chat_panels, scroll=True, sizing_mode="stretch_both", height=400)

        input_row = pn.Row(input_box, dropdown, submit_button, align="center", sizing_mode="stretch_width", margin=(10, 0))

        outer_layout = pn.Column(
            chat_display,
            pn.Spacer(height=20),
            input_row,
            width=800,
            height=800,
            css_classes=["chat-container"]
        )

        centered_layout = pn.Column(
            pn.Spacer(height=20),
            outer_layout,
            pn.Spacer(height=20),
            width_policy="max",
        )

        return centered_layout

css = """
.chat-container {
    background-color: #ffffff;
    border: 1px solid #eaeaea;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    overflow-y: auto;
}

.bk.panel-sizer {
    width: 100%;
}

.bk-input {
    margin-right: 10px !important;
    flex-grow: 1;
}

.bk-button-primary {
    margin-left: 10px !important;
}

.bk-input, .bk-select {
    height: 40px;
    border-radius: 20px;
    padding-left: 15px;
}

.bk-button-primary {
    border-radius: 20px;
}

.bk.panel-widget-box {
    flex-grow: 1;
}

.bk .panel-widget-box {
    width: 100%;
}
"""

chatbot = ChatBotInterface()

pn.extension(raw_css=[css])

pn.serve(chatbot.view, port=5006)

