import flet as ft
import threading


def Alert(message: str, alert_type: str = "info", on_close=None, auto_dismiss_seconds: int = None):
    
    color_map = {
        "success": ft.Colors.GREEN_400,
        "error": ft.Colors.RED_400,
        "info": ft.Colors.BLUE_400,
    }
    icon_map = {
        "success": "check_circle",
        "error": "error",
        "info": "info",
    }
    bgcolor = color_map.get(alert_type, ft.Colors.BLUE_400)
    icon = icon_map.get(alert_type, "info")

   
    timer_holder = {"t": None}

    def _on_close(e):
        
        try:
            t = timer_holder.get("t")
            if t:
                t.cancel()
        except:
            pass
        if callable(on_close):
            try:
                on_close(e)
            except:
                pass

    # agendar auto-dismiss se pedido
    if auto_dismiss_seconds and callable(on_close):
        try:
            t = threading.Timer(auto_dismiss_seconds, lambda: on_close(None))
            t.daemon = True
            t.start()
            timer_holder["t"] = t
        except:
            timer_holder["t"] = None

    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, color=ft.Colors.WHITE),
            ft.Text(message, color=ft.Colors.WHITE, expand=True),
            ft.IconButton(icon="close", on_click=_on_close, tooltip="Fechar", icon_color=ft.Colors.WHITE),
        ], alignment=ft.MainAxisAlignment.CENTER),
        bgcolor=bgcolor,
        border_radius=10,
        padding=10,
        margin=ft.margin.only(bottom=10),
        width=420,
        alignment=ft.alignment.center,
    )
