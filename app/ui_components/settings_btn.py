import customtkinter as ctk

def settings_btn(card,fg_color,hover_color,text_color,show_editing_settings_modal):
    settings_button = ctk.CTkButton(
        card,
        text="↖",
        width=12,
        height=10,
        corner_radius=999,
        font=ctk.CTkFont(size=18, weight="bold"),
        fg_color=fg_color,
        hover_color=hover_color,
        text_color=text_color,
        command=show_editing_settings_modal,
    )
    
    settings_button.place(
    relx=0,
    rely=1,
    x=12,
    y=-10,
    anchor="sw",
    )